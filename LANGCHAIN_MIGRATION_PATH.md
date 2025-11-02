# LangChain Migration Path (If You Decide to Proceed)

> ⚠️ **Warning:** This document is provided for completeness, but the recommendation is **NOT to migrate** at this time. See LANGCHAIN_DECISION_SUMMARY.md for reasons.

If, despite the analysis showing negative ROI, you still want to migrate to LangChain (perhaps for learning, experimentation, or future requirements), here's the safest approach.

---

## Phase-Based Migration Strategy

### Strategy: Incremental Replacement (Minimize Risk)

Instead of a big-bang rewrite, replace components one at a time while maintaining backward compatibility.

---

## Phase 0: Preparation (1 day)

### 0.1 Create Feature Branch

```bash
git checkout -b experiment/langchain-migration
```

### 0.2 Set Up Parallel Implementation

Keep current system working while adding LangChain alongside:

```python
# app/config.py - Add new settings
class Settings(BaseSettings):
    # ... existing settings ...

    # LangChain experiment
    use_langchain: bool = False  # Feature flag
    langchain_vectorstore: str = "faiss"  # or "chroma"
```

### 0.3 Install LangChain Dependencies

```bash
# Create backup of current requirements
cp requirements.txt requirements.txt.backup

# Add LangChain (minimal install)
pip install langchain==0.1.0 \
            langchain-openai==0.0.2 \
            langchain-community==0.0.10 \
            faiss-cpu==1.7.4

# Update requirements.txt
pip freeze > requirements_langchain.txt
```

**Checkpoint:** Ensure existing system still works with new packages installed.

---

## Phase 1: Vector Store Migration (2-3 days)

### 1.1 Create Parallel Vector Service

Create `app/services/langchain_vector_service.py`:

```python
"""
LangChain-based vector store service (experimental).
Runs in parallel with keyword-based search.
"""

from typing import List, Dict, Any
from pathlib import Path
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from app.config import get_settings
from data.insurance_faq import get_all_faqs


class LangChainVectorService:
    """Vector store using LangChain + FAISS."""

    def __init__(self):
        settings = get_settings()
        self.settings = settings
        self.vectorstore = None
        self.embeddings = None

    def initialize_knowledge_base(self):
        """Initialize FAISS vector store with embeddings."""
        # Get all FAQs
        faqs = get_all_faqs()

        # Convert to LangChain Documents
        documents = []
        for faq in faqs:
            doc = Document(
                page_content=f"Question: {faq['question']}\nAnswer: {faq['answer']}",
                metadata={
                    "question": faq["question"],
                    "category": faq["category"],
                    "priority": faq.get("priority", "medium"),
                }
            )
            documents.append(doc)

        # Create embeddings (use Azure or local)
        self.embeddings = OpenAIEmbeddings(
            deployment=self.settings.azure_openai_deployment,
            openai_api_key=self.settings.azure_openai_api_key,
        )

        # Create FAISS vector store
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)

        print(f"✓ LangChain vector store initialized with {len(documents)} documents")

    def search_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search using vector similarity."""
        if not self.vectorstore:
            self.initialize_knowledge_base()

        # Vector search
        docs = self.vectorstore.similarity_search_with_score(query, k=n_results)

        # Convert to common format
        results = []
        for doc, score in docs:
            results.append({
                "question": doc.metadata["question"],
                "answer": doc.page_content.split("Answer: ", 1)[1],
                "category": doc.metadata["category"],
                "similarity_score": 1.0 - score,  # Convert distance to similarity
            })

        return results


# Global instance
langchain_vector_service = LangChainVectorService()
```

### 1.2 A/B Test Vector Stores

Modify `app/services/ai_service.py`:

```python
from app.services.vector_service import vector_store_service
from app.services.langchain_vector_service import langchain_vector_service  # NEW


class AIService:
    async def get_response(self, user_message, conversation_history, provider):
        # ... validation ...

        # Choose vector store based on feature flag
        if self.settings.use_langchain:
            similar_faqs = langchain_vector_service.search_similar(user_message, n_results=5)
        else:
            similar_faqs = vector_store_service.search_similar(user_message, n_results=5)

        # Rest of the code stays the same
        # ...
```

### 1.3 Compare Quality

Add comparison endpoint in `app/api/routes.py`:

```python
@router.post("/debug/compare-search")
async def compare_search(request: dict):
    """Compare keyword vs vector search quality (debug only)."""
    query = request.get("query", "")

    # Keyword search (current)
    keyword_results = vector_store_service.search_similar(query, n_results=5)

    # Vector search (LangChain)
    vector_results = langchain_vector_service.search_similar(query, n_results=5)

    return {
        "query": query,
        "keyword_search": keyword_results,
        "vector_search": vector_results,
        "recommendation": "Use this to evaluate which is better for your use case"
    }
```

**Test queries:**

- "What health insurance plans do you offer?"
- "How much is auto insurance?"
- "Do I need flood insurance?"

**Checkpoint:** Compare search quality. If vector search isn't significantly better, **stop here** and keep keyword search.

---

## Phase 2: LLM Provider Abstraction (1-2 days)

### 2.1 Create LangChain LLM Wrappers

Create `app/services/langchain_llm_service.py`:

```python
"""
LangChain LLM providers (experimental).
"""

from typing import Optional
from langchain_openai import AzureChatOpenAI
from langchain_community.llms import Ollama
from langchain.schema import HumanMessage, SystemMessage
from app.config import get_settings


class LangChainLLMService:
    """LLM service using LangChain abstractions."""

    def __init__(self):
        settings = get_settings()
        self.settings = settings
        self.azure_llm = None
        self.ollama_llm = None

        # Initialize Azure if configured
        if settings.azure_openai_api_key:
            self.azure_llm = AzureChatOpenAI(
                deployment_name=settings.azure_openai_deployment,
                openai_api_key=settings.azure_openai_api_key,
                azure_endpoint=settings.azure_openai_endpoint,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
            )

        # Initialize Ollama
        self.ollama_llm = Ollama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.temperature,
        )

    async def get_response(
        self,
        prompt: str,
        system_message: str,
        provider: str = "azure"
    ) -> str:
        """Get response from LLM via LangChain."""
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=prompt),
        ]

        if provider == "azure" and self.azure_llm:
            response = await self.azure_llm.ainvoke(messages)
            return response.content

        elif provider == "ollama":
            response = await self.ollama_llm.ainvoke(messages)
            return response

        else:
            raise Exception(f"Provider {provider} not available")


langchain_llm_service = LangChainLLMService()
```

### 2.2 Add Feature Flag to Switch

In `app/services/ai_service.py`:

```python
async def _call_azure_openai(self, prompt, system_message):
    """Call Azure OpenAI (with optional LangChain)."""
    if self.settings.use_langchain:
        # Use LangChain wrapper
        from app.services.langchain_llm_service import langchain_llm_service
        return await langchain_llm_service.get_response(prompt, system_message, "azure")
    else:
        # Use direct API call (current implementation)
        # ... existing code ...
```

**Checkpoint:** Test with `USE_LANGCHAIN=True` in .env. Ensure responses are identical.

---

## Phase 3: Chains & Prompts (1-2 days)

### 3.1 Create Prompt Templates

```python
"""
LangChain prompt templates.
"""

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


# Main chat template
INSURANCE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """You are AI Lady, a professional insurance assistant.

CRITICAL RULES:
1. ONLY answer insurance-related questions
2. Base answers on provided FAQ context
3. Never make up policy details
4. For complex cases, recommend contacting an agent
5. Stay professional and empathetic

CONTEXT FROM KNOWLEDGE BASE:
{context}

CONVERSATION HISTORY:
{history}
"""),
    ("human", "{question}"),
])


def build_context_from_faqs(faqs):
    """Build context string from FAQ list."""
    context = ""
    for i, faq in enumerate(faqs, 1):
        context += f"\n[FAQ {i}]\n"
        context += f"Q: {faq['question']}\n"
        context += f"A: {faq['answer']}\n"
        context += f"Category: {faq['category']}\n"
    return context
```

### 3.2 Create Conversational Chain

```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


class LangChainAIService:
    """Full LangChain implementation with chains."""

    def __init__(self):
        settings = get_settings()
        self.settings = settings
        self.llm = None
        self.retriever = None
        self.chain = None

    def initialize_chain(self):
        """Initialize conversational retrieval chain."""
        # Get LLM
        from app.services.langchain_llm_service import langchain_llm_service
        self.llm = langchain_llm_service.azure_llm

        # Get retriever from vector store
        from app.services.langchain_vector_service import langchain_vector_service
        if not langchain_vector_service.vectorstore:
            langchain_vector_service.initialize_knowledge_base()
        self.retriever = langchain_vector_service.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )

        # Create conversational chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True,
            verbose=True,
        )

    async def get_response(self, query: str, chat_history: list):
        """Get response using chain."""
        if not self.chain:
            self.initialize_chain()

        result = await self.chain.ainvoke({
            "question": query,
            "chat_history": chat_history,
        })

        return {
            "response": result["answer"],
            "sources": [doc.metadata for doc in result["source_documents"]],
            "model": "langchain-chain",
            "provider": "azure",
        }
```

**Checkpoint:** Test chain-based responses. Compare quality with current implementation.

---

## Phase 4: Memory Integration (1 day)

### 4.1 LangChain Memory with SQLAlchemy Backend

```python
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from app.config import get_settings


def get_langchain_memory(session_id: str):
    """Get LangChain memory with SQL persistence."""
    settings = get_settings()

    # Use SQL for persistence (reuse existing DB)
    message_history = SQLChatMessageHistory(
        session_id=session_id,
        connection_string=settings.database_url.replace("+aiosqlite", ""),  # Sync for LangChain
    )

    memory = ConversationBufferMemory(
        chat_memory=message_history,
        return_messages=True,
        memory_key="chat_history",
    )

    return memory
```

**Issue:** LangChain memory is not async-compatible with your current async SQLAlchemy setup. You'd need:

1. Separate sync connection for LangChain memory, OR
2. Custom async memory implementation

**This is a complexity that your current system doesn't have.**

**Checkpoint:** Evaluate if LangChain memory is worth the hassle vs. your current clean async implementation.

---

## Phase 5: Full Integration & Testing (2-3 days)

### 5.1 Switch Routes to LangChain

Update `app/api/routes.py`:

```python
@router.post("/chat")
async def chat(request: ChatRequest):
    settings = get_settings()

    if settings.use_langchain:
        # Use LangChain implementation
        from app.services.langchain_ai_service import langchain_ai_service
        ai_response = await langchain_ai_service.get_response(
            request.message,
            conversation_history
        )
    else:
        # Use current implementation
        ai_response = await ai_service.get_response(
            request.message,
            conversation_history,
            provider=request.provider,
        )

    # ... rest stays the same ...
```

### 5.2 Comprehensive Testing

```bash
# Run tests with both implementations
USE_LANGCHAIN=False pytest tests/
USE_LANGCHAIN=True pytest tests/

# Load testing
locust -f tests/load_test.py

# Quality comparison
python scripts/compare_responses.py
```

### 5.3 Performance Benchmarking

```python
# scripts/benchmark.py
import time
import asyncio
from app.services.ai_service import ai_service
from app.services.langchain_ai_service import langchain_ai_service


async def benchmark():
    queries = [
        "What health insurance plans do you offer?",
        "How much is auto insurance?",
        "How do I file a claim?",
    ]

    # Benchmark current system
    print("Testing current system...")
    start = time.time()
    for query in queries:
        await ai_service.get_response(query, [], "azure")
    current_time = time.time() - start

    # Benchmark LangChain
    print("Testing LangChain system...")
    start = time.time()
    for query in queries:
        await langchain_ai_service.get_response(query, [])
    langchain_time = time.time() - start

    print(f"\nResults:")
    print(f"Current system: {current_time:.2f}s")
    print(f"LangChain system: {langchain_time:.2f}s")
    print(f"Difference: {((langchain_time / current_time) - 1) * 100:.1f}% slower")


asyncio.run(benchmark())
```

---

## Rollback Plan

At ANY phase, if things go wrong:

```bash
# 1. Switch feature flag
export USE_LANGCHAIN=False

# 2. Or rollback code
git checkout main
pip install -r requirements.txt

# 3. Restart server
python main.py
```

**Your current system keeps working throughout.**

---

## Success Criteria

Only proceed to next phase if ALL criteria are met:

### After Phase 1 (Vector Store):

- [ ] Vector search is **at least as good** as keyword search
- [ ] Search time is **acceptable** (< 100ms)
- [ ] No degradation in answer quality
- [ ] Memory usage is **acceptable** (< 1GB)

### After Phase 2 (LLM):

- [ ] LangChain LLM calls work reliably
- [ ] Response quality is identical to direct API calls
- [ ] Latency increase is **< 10%**
- [ ] Error handling works correctly

### After Phase 3 (Chains):

- [ ] Chains produce **better** responses (subjective evaluation)
- [ ] Context is properly passed through chain
- [ ] Debugging is manageable (not too many layers)

### After Phase 4 (Memory):

- [ ] Conversation history works correctly
- [ ] No async/sync conflicts
- [ ] Database persistence is reliable

### Before Final Deployment:

- [ ] All tests pass with USE_LANGCHAIN=True
- [ ] Performance is acceptable (< 20% slower)
- [ ] Code is well-documented
- [ ] Team is trained on debugging LangChain
- [ ] **Users report improved experience** (most important!)

---

## Estimated Total Timeline

```
Phase 0: Preparation           │ ▓░░░░░░░░░░ │ 1 day
Phase 1: Vector Store          │ ▓▓▓░░░░░░░░ │ 2-3 days
Phase 2: LLM Abstraction       │ ▓▓░░░░░░░░░ │ 1-2 days
Phase 3: Chains & Prompts      │ ▓▓░░░░░░░░░ │ 1-2 days
Phase 4: Memory Integration    │ ▓░░░░░░░░░░ │ 1 day
Phase 5: Testing & Integration │ ▓▓▓░░░░░░░░ │ 2-3 days
─────────────────────────────────────────────────────────────
Total:                         │ ▓▓▓▓▓▓▓▓▓▓▓ │ 8-12 days
```

---

## Recommendation

Even with this careful, phased approach:

1. **Phase 1 (Vector Store)** will likely show that keyword search is faster and equally accurate for 57 FAQs
2. **Phase 2 (LLM)** will show minimal benefit vs. direct API calls
3. **Phase 3 (Chains)** adds complexity without clear value for simple Q&A
4. **Phase 4 (Memory)** is actually **worse** than your current async implementation

**Most likely outcome:** You'll stop after Phase 1 when data shows keyword search is superior for your scale.

---

## Better Alternative: Targeted Improvements

Instead of full LangChain migration, cherry-pick useful concepts:

### Option 1: Add Semantic Search as Fallback

```python
# Only use when keyword search fails (score < 0.3)
if best_keyword_score < 0.3:
    # Fall back to semantic search
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    semantic_results = semantic_search(query, model)
```

**Effort:** 1 day  
**Benefit:** Better handling of edge cases  
**Risk:** Low

### Option 2: Improve Prompt Engineering

```python
# Use LangChain's PromptTemplate for better organization
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([...])
# But still use your direct API calls
```

**Effort:** 2-3 hours  
**Benefit:** More maintainable prompts  
**Risk:** Very low

### Option 3: Add Response Streaming

```python
# Stream responses from Azure OpenAI for better UX
# (No need for LangChain - OpenAI SDK supports this)
async for chunk in await azure_client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    stream=True
):
    yield chunk.choices[0].delta.content
```

**Effort:** 1 day  
**Benefit:** Better perceived performance  
**Risk:** Low

---

## Final Advice

1. **Don't migrate just to migrate.** Your system is excellent.
2. **If you do migrate, use this phased approach** and stop at Phase 1 when data shows it's not worth it.
3. **Better ROI:** Spend time on features users ask for, not internal refactoring.

---

\*This migration path is provided for completeness, but the recommendation remains: **Keep your current excellent implementation.\***
