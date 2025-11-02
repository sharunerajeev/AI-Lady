"""
AI service for handling chat interactions with multiple AI providers.
Supports: Fallback (FAQ-based), Ollama (local), and Azure OpenAI.
"""

from typing import List, Dict, Any, Optional
import httpx
from openai import AzureOpenAI
from app.config import get_settings
from app.services.vector_service import vector_store_service


class AIService:
    """Service for AI-powered chat interactions with multiple providers."""

    def __init__(self):
        """Initialize AI service."""
        settings = get_settings()
        self.settings = settings
        self.azure_client = None

        # Initialize Azure OpenAI client if configured
        if settings.azure_openai_api_key and settings.azure_openai_endpoint:
            if settings.azure_openai_api_key != "your_azure_api_key_here":
                self.azure_client = AzureOpenAI(
                    api_key=settings.azure_openai_api_key,
                    api_version=settings.azure_openai_api_version,
                    azure_endpoint=settings.azure_openai_endpoint,
                )

    async def _call_ollama(
        self,
        prompt: str,
        system_message: str = "You are AI Lady, a helpful insurance assistant.",
    ) -> str:
        """Call Ollama local model."""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.settings.ollama_base_url}/api/generate",
                    json={
                        "model": self.settings.ollama_model,
                        "prompt": f"{system_message}\n\n{prompt}",
                        "stream": False,
                        "options": {
                            "temperature": self.settings.temperature,
                            "num_predict": self.settings.max_tokens,
                        },
                    },
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
        except httpx.TimeoutException as e:
            raise Exception(f"Ollama request timed out after 60 seconds: {str(e)}")
        except httpx.HTTPError as e:
            raise Exception(f"Ollama HTTP error: {str(e)}")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")

    async def _call_azure_openai(
        self,
        prompt: str,
        system_message: str = "You are AI Lady, a helpful insurance assistant.",
    ) -> str:
        """Call Azure OpenAI API."""
        if not self.azure_client:
            raise Exception("Azure OpenAI client not configured")

        response = self.azure_client.chat.completions.create(
            model=self.settings.azure_openai_deployment,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.settings.max_tokens,
            temperature=self.settings.temperature,
        )
        return response.choices[0].message.content

    def _build_context_prompt(
        self,
        query: str,
        similar_faqs: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Build context-aware prompt for OpenAI."""

        # System prompt
        system_context = """You are AI Lady, a helpful and friendly AI assistant for an insurance company. 
Your role is to help customers with questions about insurance policies, claims, renewals, and general insurance topics.

Key guidelines:
- Be professional, empathetic, and clear in your responses
- Use the provided FAQ context to answer questions accurately
- If you're not sure about something, be honest and suggest contacting a human agent
- Keep responses concise but informative
- Use simple language, avoiding excessive jargon
- For complex situations, recommend speaking with a licensed insurance agent
"""

        # Add relevant FAQ context
        context_section = "\n\nRelevant FAQ Information:\n"
        for i, faq in enumerate(similar_faqs, 1):
            context_section += f"\n{i}. Q: {faq['question']}\n   A: {faq['answer']}\n"

        # Add conversation history if available
        history_section = ""
        if conversation_history:
            history_section = "\n\nRecent Conversation History:\n"
            for msg in conversation_history[-3:]:  # Last 3 exchanges
                history_section += (
                    f"User: {msg['user']}\nAssistant: {msg['assistant']}\n\n"
                )

        # Current query
        query_section = f"\n\nCurrent User Question: {query}\n"

        full_prompt = (
            system_context
            + context_section
            + history_section
            + query_section
            + "\nProvide a helpful, accurate response based on the FAQ information and conversation context:"
        )

        return full_prompt

    async def get_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get AI response for user message.

        Args:
            user_message: The user's question
            conversation_history: Previous conversation context
            provider: Override AI provider ("fallback", "ollama", "azure")
                     If None, uses settings.model_provider
        """

        # Search for similar FAQs
        similar_faqs = vector_store_service.search_similar(user_message, n_results=3)

        # Determine which provider to use
        active_provider = provider or self.settings.model_provider

        # Fallback mode - rule-based responses
        if active_provider == "fallback":
            return {
                "response": self._get_fallback_response(similar_faqs),
                "sources": similar_faqs,
                "model": "fallback",
                "provider": "fallback",
            }

        # Build context-aware prompt
        prompt = self._build_context_prompt(
            user_message, similar_faqs, conversation_history
        )

        try:
            # Call appropriate AI provider
            if active_provider == "ollama":
                assistant_message = await self._call_ollama(prompt)
                model_name = self.settings.ollama_model

            elif active_provider == "azure":
                assistant_message = await self._call_azure_openai(prompt)
                model_name = self.settings.azure_openai_deployment

            else:
                # Unknown provider, fall back
                return {
                    "response": self._get_fallback_response(similar_faqs),
                    "sources": similar_faqs,
                    "model": "fallback",
                    "provider": "fallback",
                    "warning": f"Unknown provider '{active_provider}', using fallback",
                }

            return {
                "response": assistant_message,
                "sources": similar_faqs,
                "model": model_name,
                "provider": active_provider,
            }

        except Exception as e:
            print(f"Error calling {active_provider} API: {e}")
            # Fall back to rule-based response on error
            return {
                "response": self._get_fallback_response(similar_faqs),
                "sources": similar_faqs,
                "model": "fallback",
                "provider": "fallback",
                "error": str(e),
                "warning": f"Failed to use {active_provider}, using fallback",
            }

    def _get_fallback_response(self, similar_faqs: List[Dict[str, Any]]) -> str:
        """Generate fallback response when OpenAI is not available."""
        if not similar_faqs:
            return (
                "I'm here to help with your insurance questions! "
                "I can assist with information about policies, claims, renewals, and more. "
                "Could you please rephrase your question or provide more details?"
            )

        # Return the most similar FAQ answer
        best_match = similar_faqs[0]
        response = f"Based on your question, here's what I can tell you:\n\n{best_match['answer']}\n\n"

        # Add related questions if available
        if len(similar_faqs) > 1:
            response += "\nYou might also be interested in:\n"
            for faq in similar_faqs[1:]:
                response += f"• {faq['question']}\n"

        response += "\nIs there anything specific you'd like to know more about?"

        return response


# Global AI service instance
ai_service = AIService()
