"""
AI service for handling chat interactions with multiple AI providers.
Supports: Fallback (FAQ-based), Ollama (local), and Azure OpenAI.
Includes security guardrails, input validation, and smart recommendation flow.
"""

import json
from typing import List, Dict, Any, Optional
import re
import httpx
from openai import AzureOpenAI
from app.config import get_settings
from app.services.vector_service import vector_store_service
from app.services.recommendation_service import get_recommendation_engine
from app.services.database_service import db_service
from data.insurance_domain_knowledge import get_full_system_prompt


class AIService:
    """Service for AI-powered chat interactions with multiple providers."""

    def __init__(self):
        """Initialize AI service."""
        settings = get_settings()
        self.settings = settings
        self.azure_client = None
        self.recommendation_engine = get_recommendation_engine()

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
        system_message: str = "You are AI Avustaa, a helpful insurance assistant.",
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
        system_message: str = "You are AI Avustaa, a helpful insurance assistant.",
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

    def _validate_insurance_query(self, query: str) -> Dict[str, Any]:
        """Validate if query is insurance-related and check for attacks."""
        query_lower = query.lower()

        # Check for prompt injection attempts
        injection_patterns = [
            r"ignore\s+(previous|above|all)\s+instructions?",
            r"forget\s+(everything|previous|all)",
            r"you\s+are\s+now",
            r"new\s+instructions?:",
            r"system\s*[:=]",
            r"<\s*script",
            r"javascript:",
            r"disregard\s+(previous|all)",
            r"instead\s+of\s+insurance",
        ]

        for pattern in injection_patterns:
            if re.search(pattern, query_lower):
                return {
                    "valid": False,
                    "reason": "security",
                    "message": "I can only help with insurance-related questions. Please ask about policies, claims, coverage, or renewals.",
                }

        # Check if query is insurance-related
        insurance_keywords = [
            "insurance",
            "policy",
            "claim",
            "coverage",
            "premium",
            "deductible",
            "beneficiary",
            "liability",
            "collision",
            "comprehensive",
            "health",
            "life",
            "auto",
            "home",
            "renew",
            "cancel",
            "quote",
            "agent",
            "accident",
            "damage",
            "medical",
            "death benefit",
            "copay",
            "coinsurance",
            "hmo",
            "ppo",
            "term",
            "whole life",
            "flood",
            "fire",
            "theft",
            "vandalism",
        ]

        # Query must have at least one insurance keyword or be a general greeting
        greetings = ["hello", "hi", "hey", "help", "thanks", "thank you", "bye"]

        has_insurance_keyword = any(kw in query_lower for kw in insurance_keywords)
        is_greeting = (
            any(g in query_lower for g in greetings) and len(query.split()) <= 5
        )

        if not has_insurance_keyword and not is_greeting and len(query.split()) > 3:
            return {
                "valid": False,
                "reason": "off_topic",
                "message": "I specialize in insurance-related questions. I can help you with:\n"
                "• Life, Health, Auto, and Home Insurance\n"
                "• Policy information and renewals\n"
                "• Claims process and filing\n"
                "• Coverage options and quotes\n\n"
                "What insurance question can I help you with?",
            }

        return {"valid": True}

    def _build_context_prompt(
        self,
        query: str,
        similar_faqs: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Build context-aware prompt for Azure OpenAI with enhanced accuracy."""

        # Load comprehensive insurance domain knowledge from dedicated module
        system_context = get_full_system_prompt()

        # Add relevant FAQ context
        context_section = "\n\n=== KNOWLEDGE BASE (FAQs to reference) ===\n"
        for i, faq in enumerate(similar_faqs, 1):
            context_section += f"\n[FAQ {i}]\n"
            context_section += f"Category: {faq.get('category', 'general')}\n"
            context_section += f"Question: {faq['question']}\n"
            context_section += f"Answer: {faq['answer']}\n"
            context_section += (
                f"Relevance Score: {faq.get('similarity_score', 0):.2f}\n"
            )

        # Add conversation history if available
        history_section = ""
        if conversation_history:
            history_section = "\n\n=== RECENT CONVERSATION ===\n"
            for msg in conversation_history[-3:]:  # Last 3 exchanges
                history_section += f"User: {msg['user']}\n"
                history_section += f"AI Avustaa: {msg['assistant']}\n\n"

        # Current query with clear instruction
        query_section = f"\n\n=== CURRENT USER QUESTION ===\n{query}\n"

        instruction = """
=== YOUR TASK ===
Provide a helpful, accurate response to the user's question by:
1. Using information from the FAQ knowledge base above
2. Maintaining conversation continuity if there's prior context
3. Following all critical rules and quality standards
4. Staying strictly within insurance topics
5. Being honest if you don't have enough information

Your response:"""

        full_prompt = (
            system_context
            + context_section
            + history_section
            + query_section
            + instruction
        )

        return full_prompt

    async def get_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        provider: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get AI response for user message with validation and guardrails.

        Args:
            user_message: The user's question
            conversation_history: Previous conversation context
            provider: Override AI provider ("fallback", "ollama", "azure")
                     If None, uses settings.model_provider
            session_id: Session ID for recommendation flow tracking
        """

        # Step 1: Check if we're in a recommendation flow
        if session_id:
            db_context = await db_service.get_conversation_context(session_id)
            if db_context and db_context.current_flow == "recommendation":
                # Continue existing recommendation flow
                rec_response = await self._handle_recommendation_flow(
                    user_message, session_id
                )
                if rec_response:
                    return rec_response
            else:
                # Check if user is starting a new recommendation flow
                intent = self._detect_recommendation_intent(user_message)
                if intent:
                    # Start new recommendation flow
                    rec_response = await self._handle_recommendation_flow(
                        user_message, session_id
                    )
                    if rec_response:
                        return rec_response

        # Step 2: Validate input and check for security issues
        validation = self._validate_insurance_query(user_message)
        if not validation["valid"]:
            return {
                "response": validation["message"],
                "sources": [],
                "model": "guardrails",
                "provider": "security",
                "warning": f"Query rejected: {validation['reason']}",
            }

        # Step 3: Search for similar FAQs
        similar_faqs = vector_store_service.search_similar(user_message, n_results=5)

        # Determine which provider to use
        active_provider = provider or self.settings.model_provider

        # Fallback mode - rule-based responses
        if active_provider == "fallback":
            return {
                "response": self._get_fallback_response(similar_faqs),
                "sources": similar_faqs[:3],
                "model": "fallback",
                "provider": "fallback",
            }

        # Build context-aware prompt with enhanced quality
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
                    "sources": similar_faqs[:3],
                    "model": "fallback",
                    "provider": "fallback",
                    "warning": f"Unknown provider '{active_provider}', using fallback",
                }

            return {
                "response": assistant_message,
                "sources": similar_faqs[:3],
                "model": model_name,
                "provider": active_provider,
            }

        except Exception as e:
            print(f"Error calling {active_provider} API: {e}")
            # Fall back to rule-based response on error
            return {
                "response": self._get_fallback_response(similar_faqs),
                "sources": similar_faqs[:3],
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

    # ========== RECOMMENDATION FLOW METHODS ==========

    def _detect_recommendation_intent(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Detect if user is asking for product recommendations

        Returns:
            Dict with insurance_type if detected, None otherwise
        """
        message_lower = message.lower()

        # Explicit recommendation triggers
        recommendation_triggers = [
            "recommend",
            "suggest",
            "which plan",
            "which policy",
            "best for me",
            "help me choose",
            "what should i get",
            "which one",
            "compare",
            "looking for",
            "need insurance",
            "want insurance",
            "shopping for",
        ]

        # Insurance type detection
        insurance_types = {
            "health_insurance": [
                "health insurance",
                "health plan",
                "medical insurance",
                "health coverage",
            ],
            "life_insurance": [
                "life insurance",
                "life policy",
                "life coverage",
                "term life",
                "whole life",
            ],
            "auto_insurance": [
                "auto insurance",
                "car insurance",
                "vehicle insurance",
                "auto coverage",
            ],
            "home_insurance": [
                "home insurance",
                "homeowner",
                "property insurance",
                "house insurance",
            ],
        }

        # Check for explicit triggers
        has_trigger = any(
            trigger in message_lower for trigger in recommendation_triggers
        )

        # Detect insurance type
        detected_type = None
        for ins_type, keywords in insurance_types.items():
            if any(kw in message_lower for kw in keywords):
                detected_type = ins_type
                break

        # If asking about a type with a trigger, or asking "which" about a type
        if detected_type and (has_trigger or "which" in message_lower):
            return {"insurance_type": detected_type, "intent": "recommendation"}

        return None

    async def _handle_recommendation_flow(
        self,
        user_message: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Handle multi-turn recommendation flow

        Args:
            user_message: User's current message
            session_id: Session identifier
            context: Current conversation context from database

        Returns:
            Response dict with next question or recommendations
        """
        # Get or create context
        if not context:
            db_context = await db_service.get_conversation_context(session_id)
            if db_context and db_context.collected_answers:
                context = {
                    "current_flow": db_context.current_flow,
                    "insurance_type": db_context.insurance_type,
                    "current_question_index": db_context.current_question_index,
                    "collected_answers": (
                        json.loads(db_context.collected_answers)
                        if db_context.collected_answers
                        else {}
                    ),
                    "awaiting_response_for": db_context.awaiting_response_for,
                }
            else:
                # New recommendation flow - detect intent
                intent = self._detect_recommendation_intent(user_message)
                if not intent:
                    return None

                context = {
                    "current_flow": "recommendation",
                    "insurance_type": intent["insurance_type"],
                    "current_question_index": 0,
                    "collected_answers": {},
                    "awaiting_response_for": None,
                }

        insurance_type = context.get("insurance_type")
        questionnaire = self.recommendation_engine.get_questionnaire(insurance_type)

        if not questionnaire:
            return None

        questions = questionnaire["questions"]
        current_index = context.get("current_question_index", 0)
        collected_answers = context.get("collected_answers", {})

        # If we're awaiting a response, validate and store it
        if context.get("awaiting_response_for"):
            question_id = context["awaiting_response_for"]

            # Validate the answer
            is_valid, error_msg = self.recommendation_engine.validate_answer(
                insurance_type, question_id, user_message
            )

            if not is_valid:
                # Ask again with error message
                response = f"❌ {error_msg}\n\nPlease try again."
                return {
                    "response": response,
                    "sources": [],
                    "model": "recommendation_flow",
                    "provider": "recommendation",
                    "context": context,
                    "is_recommendation_flow": True,
                }

            # Store the answer
            collected_answers[question_id] = user_message
            current_index += 1
            context["awaiting_response_for"] = None

        # Check if we have more questions
        if current_index < len(questions):
            question = questions[current_index]

            # Build the question message
            question_text = (
                f"\n📋 **Question {current_index + 1} of {len(questions)}**\n\n"
            )
            question_text += f"{question['question']}\n\n"

            if question["type"] == "choice":
                question_text += "Please choose from:\n"
                for option in question["options"]:
                    question_text += f"• {option}\n"
            elif question["type"] == "number":
                if "validation" in question:
                    val = question["validation"]
                    if "min" in val and "max" in val:
                        question_text += (
                            f"(Enter a number between {val['min']} and {val['max']})\n"
                        )

            # Update context
            context["current_question_index"] = current_index
            context["collected_answers"] = collected_answers
            context["awaiting_response_for"] = question["id"]

            # Save context to database
            await db_service.save_conversation_context(
                session_id=session_id,
                current_flow="recommendation",
                insurance_type=insurance_type,
                current_question_index=current_index,
                collected_answers=collected_answers,
                awaiting_response_for=question["id"],
            )

            return {
                "response": question_text,
                "sources": [],
                "model": "recommendation_flow",
                "provider": "recommendation",
                "context": context,
                "is_recommendation_flow": True,
            }

        # All questions answered - generate recommendations
        recommendations = self.recommendation_engine.recommend_products(
            insurance_type, collected_answers, self
        )

        # Save recommendations to database
        for rec in recommendations[:3]:  # Top 3
            await db_service.save_recommendation(
                session_id=session_id,
                insurance_type=insurance_type,
                product_id=rec["product"]["id"],
                product_name=rec["product"]["name"],
                match_score=rec["score"],
                match_reasons=rec["reasons"],
                user_requirements=collected_answers,
            )

        # Save preferences
        await db_service.save_user_preference(
            session_id=session_id,
            insurance_type=insurance_type,
            requirements=collected_answers,
        )

        # Format recommendations response
        response = self._format_recommendations_response(
            recommendations, insurance_type
        )

        # Clear context
        await db_service.clear_conversation_context(session_id)

        return {
            "response": response,
            "sources": [],
            "model": "recommendation_engine",
            "provider": "recommendation",
            "recommendations": recommendations,
            "is_recommendation_flow": False,
        }

    def _format_recommendations_response(
        self, recommendations: List[Dict[str, Any]], insurance_type: str
    ) -> str:
        """Format recommendations into a user-friendly response"""
        if not recommendations:
            return (
                "I couldn't find any suitable products based on your requirements. "
                "Please try adjusting your criteria or contact our support team."
            )

        insurance_name = insurance_type.replace("_", " ").title()
        response = f"\n🎯 **Your Personalized {insurance_name} Recommendations**\n\n"
        response += "Based on your requirements, here are the best matches:\n\n"

        # Show top 3 recommendations
        for i, rec in enumerate(recommendations[:3], 1):
            product = rec["product"]
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"

            response += f"{medal} **{i}. {product['name']}** ({rec['match_percentage']}% match)\n"
            response += f"   📊 Type: {product['type']}\n"
            response += f"   💰 Premium: {product['monthly_premium_range']}\n"

            if "coverage_amount" in product:
                response += f"   🛡️ Coverage: {product['coverage_amount']}\n"

            response += "\n   ✅ **Why this is a good fit:**\n"
            for reason in rec["reasons"][:3]:  # Top 3 reasons
                response += f"      • {reason}\n"

            response += "\n   📌 **Key Features:**\n"
            for feature in product["features"][:3]:  # Top 3 features
                response += f"      • {feature}\n"

            response += "\n"

        response += "\n💡 **Next Steps:**\n"
        response += "• Review the detailed features of each plan\n"
        response += "• Ask me questions about any specific plan\n"
        response += "• Request a detailed comparison\n"
        response += "• When ready, I can help you with the application process\n"

        return response


# Global AI service instance
ai_service = AIService()
