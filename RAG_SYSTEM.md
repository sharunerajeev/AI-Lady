# RAG System Documentation

## Overview

This AI Insurance Assistant uses a **lightweight RAG (Retrieval Augmented Generation)** system to provide accurate, contextual responses based on a comprehensive insurance knowledge base.

## What is RAG?

**RAG** stands for **Retrieval Augmented Generation**. It's a technique that combines:

1. **Retrieval**: Finding relevant information from a knowledge base
2. **Augmentation**: Adding that information as context to the AI prompt
3. **Generation**: AI generates response based on retrieved context

## Our RAG Implementation

### Architecture

```
User Query
    ↓
[1] Keyword-Based Search
    ↓
[2] Retrieve Top 5 FAQs
    ↓
[3] Inject as Context
    ↓
[4] Azure OpenAI/Ollama
    ↓
AI Response with Sources
```

### Components

#### 1. **Knowledge Base** (`knowledge_base/` directory)

- **Format**: JSON files (easy to edit, no ML required)
- **Structure**:
  ```
  knowledge_base/
  ├── company_info.json          # Company details
  ├── products/
  │   ├── life_insurance.json
  │   ├── health_insurance.json
  │   ├── auto_insurance.json
  │   └── home_insurance.json
  └── policies/
      └── claims_process.json
  ```
- **Total Items**: 57 (23 default + 34 custom)
- **Categories**: 10 (life, health, auto, home, claims, etc.)

#### 2. **Vector Service** (`app/services/vector_service.py`)

- **Search Method**: Keyword similarity (TF-IDF-like)
- **NO External Dependencies**: No ChromaDB, Pinecone, FAISS needed
- **In-Memory**: Fast retrieval (< 10ms)
- **Scoring**: Weighted keyword matching
  - Question match: 50%
  - Keyword match: 40%
  - Answer match: 10%
  - Priority boost: +0-15%

#### 3. **AI Service** (`app/services/ai_service.py`)

- **Context Building**: Structured prompt with FAQs
- **Context Size**: Top 5 relevant FAQs
- **Prompt Engineering**:
  - System instructions
  - Retrieved FAQs with scores
  - Conversation history (last 3)
  - Current query
  - Response guidelines

## How It Works

### Step-by-Step Example

**User asks**: "How much is auto insurance?"

**Step 1: Query Preprocessing**

- Extract keywords: "much", "auto", "insurance"
- Validate query (security check)

**Step 2: Knowledge Retrieval**

```python
similar_faqs = vector_store_service.search_similar(query, n_results=5)
```

**Results**:

1. "How much does auto insurance cost..." (score: 0.670)
2. "What auto insurance coverage options..." (score: 0.580)
3. "What factors affect my insurance premium..." (score: 0.540)
4. "Do you offer usage-based insurance..." (score: 0.480)
5. "What is collision vs comprehensive..." (score: 0.450)

**Step 3: Context Injection**
Build prompt with:

```
SYSTEM: You are AI Lady, insurance assistant...
CRITICAL RULES: [guardrails]
EXAMPLE INTERACTIONS: [few-shot examples]

KNOWLEDGE BASE (FAQs):
[FAQ 1]
Category: auto_insurance
Question: How much does auto insurance cost and what affects my rate?
Answer: Our auto insurance rates start as low as $85/month...
Relevance Score: 0.67

[FAQ 2-5...]

CURRENT USER QUESTION: How much is auto insurance?

TASK: Provide accurate response using FAQ knowledge base...
```

**Step 4: AI Generation**

- Send to Azure OpenAI GPT-4
- Temperature: 0.3 (consistent responses)
- Max tokens: 800

**Step 5: Response**

```json
{
  "response": "Our auto insurance rates start as low as $85/month for basic coverage. However, your specific rate depends on several factors:\n\n[Detailed response based on FAQs]...",
  "sources": [
    {
      "question": "How much does auto insurance cost...",
      "category": "auto_insurance",
      "similarity_score": 0.67
    },
    ...
  ],
  "model": "gpt-4",
  "provider": "azure"
}
```

## Why This Approach?

### ✅ **Advantages**

1. **No Heavy Dependencies**

   - No need for Pinecone, ChromaDB, or Weaviate
   - No embedding models to maintain
   - Simple JSON files anyone can edit

2. **Fast & Efficient**

   - In-memory search (< 10ms)
   - No network calls to vector DB
   - Perfect for POC and small-medium knowledge bases

3. **Easy to Update**

   - Edit JSON files
   - Reload via API endpoint
   - No reindexing or re-embedding needed

4. **Transparent**

   - See exactly which FAQs matched
   - Similarity scores visible
   - Easy to debug

5. **Cost-Effective**
   - No vector database hosting fees
   - No embedding API costs
   - Lower infrastructure requirements

### ⚠️ **Limitations**

1. **Semantic Understanding**

   - Keyword-based (not semantic embeddings)
   - May miss synonyms or context
   - "automobile" vs "car" requires both in keywords

2. **Scale**

   - Optimal for < 10,000 items
   - Linear search (O(n))
   - For 100K+ items, consider vector DB

3. **Multilingual**
   - Works best in English
   - Other languages need separate knowledge bases

## Knowledge Base Statistics

```
Total Items: 57
Categories: 10
Priorities: High (20), Medium (37), Low (0)

By Category:
├── auto_insurance:     10 items
├── health_insurance:   11 items
├── home_insurance:      9 items
├── life_insurance:      6 items
├── claims:              8 items
├── company_info:        5 items
└── general/policy:      8 items
```

## Upgrading to Vector Database (Future)

If you need semantic search and scale, consider:

### Option 1: Chroma DB (Local, Open Source)

```python
# Install
pip install chromadb

# Initialize
import chromadb
client = chromadb.Client()
collection = client.create_collection("insurance_kb")

# Add documents with embeddings
collection.add(
    documents=[faq['answer'] for faq in faqs],
    metadatas=[{'question': faq['question']} for faq in faqs],
    ids=[str(i) for i in range(len(faqs))]
)

# Query
results = collection.query(
    query_texts=["How much is auto insurance?"],
    n_results=5
)
```

### Option 2: Pinecone (Cloud, Managed)

```python
# Best for production scale
# Handles millions of vectors
# Managed service ($)
```

### Option 3: Azure AI Search

```python
# Integrated with Azure OpenAI
# Semantic ranking built-in
# Enterprise features
```

## Testing the RAG System

### Manual Test

```bash
python test_improvements.py
```

### Query Knowledge Stats

```bash
curl http://localhost:8000/api/v1/admin/knowledge/stats
```

### Test Specific Query

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"How much is auto insurance?"}'
```

## Monitoring RAG Quality

### Key Metrics

1. **Retrieval Quality**

   - Are top 5 FAQs relevant?
   - Similarity scores > 0.3?
   - Check `sources` in response

2. **Response Accuracy**

   - Does AI cite the FAQs?
   - Hallucinations minimized?
   - Track user ratings

3. **Coverage**
   - Questions with no good matches?
   - Add more FAQs to fill gaps

### Improvement Tips

1. **Add Keywords**

   - If searches miss, add synonyms to keywords
   - "auto" = ["car", "vehicle", "automobile"]

2. **Set Priorities**

   - High priority = +15% boost
   - Critical FAQs ranked higher

3. **Monitor Logs**
   - Track common queries
   - Identify knowledge gaps

## Conclusion

Our RAG system provides:

- ✅ **57 comprehensive insurance FAQs**
- ✅ **Fast keyword-based retrieval**
- ✅ **Structured context injection**
- ✅ **Accurate AI responses with sources**
- ✅ **Easy knowledge base management**

Perfect for POC and production use up to ~10,000 knowledge items!

For questions or to expand further, see: `knowledge_base/README.md`
