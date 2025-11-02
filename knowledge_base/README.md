# Knowledge Base Management

This directory contains the insurance company's knowledge base that powers AI Lady's responses.

## 📁 Structure

```
knowledge_base/
├── README.md                    # This file
├── company_info.json           # Company-specific information
├── products/                    # Product information files
│   ├── life_insurance.json
│   ├── health_insurance.json
│   ├── auto_insurance.json
│   └── home_insurance.json
└── policies/                    # Company policies and procedures
    ├── claims_process.json
    └── renewal_process.json
```

## 📝 How to Add/Update Knowledge

### Option 1: Edit JSON Files (Recommended)

Each JSON file contains structured information that AI Lady uses to answer questions.

**Format:**

```json
{
  "category": "life_insurance",
  "company_name": "Your Insurance Company",
  "items": [
    {
      "question": "What life insurance products do we offer?",
      "answer": "We offer Term Life, Whole Life, and Universal Life insurance...",
      "keywords": ["life insurance", "products", "offerings"],
      "priority": "high"
    }
  ]
}
```

**Fields:**

- `question`: The question this information answers (used for matching)
- `answer`: The detailed answer (be specific and accurate)
- `keywords`: Words that help match user queries to this answer
- `priority`: "high", "medium", or "low" (affects ranking in results)

### Option 2: Use the Admin API (Coming Soon)

Upload knowledge files via the `/api/v1/admin/knowledge/upload` endpoint.

## 🎯 Best Practices

1. **Be Specific**: Include your company's actual policy details, prices, and procedures
2. **Use Keywords**: Add relevant keywords to improve search accuracy
3. **Keep Updated**: Review and update knowledge base quarterly
4. **Test Queries**: After adding content, test with common customer questions
5. **Avoid Duplication**: Check existing entries before adding new ones

## 📊 Priority Levels

- **High**: Critical information, frequently asked questions, core products
- **Medium**: Important but less common questions, secondary products
- **Low**: Edge cases, rare scenarios, supplementary information

## 🔄 Loading Changes

After editing files:

1. **Development**: Restart the application

   ```bash
   ./start.sh
   ```

2. **Production**: The system reloads knowledge base automatically (if enabled)
   Or trigger reload via API:
   ```bash
   curl -X POST http://localhost:8000/api/v1/admin/knowledge/reload
   ```

## 💡 Examples

### Good Example

```json
{
  "question": "What is our maximum coverage for term life insurance?",
  "answer": "Acme Insurance offers term life insurance coverage up to $5 million for qualified applicants. Coverage terms available: 10, 20, and 30 years. Rates start at $25/month for $250,000 in coverage for healthy non-smokers aged 30-40.",
  "keywords": ["term life", "maximum coverage", "coverage limit", "how much"],
  "priority": "high"
}
```

### Bad Example (Too Vague)

```json
{
  "question": "Tell me about insurance",
  "answer": "We offer insurance products.",
  "keywords": ["insurance"],
  "priority": "medium"
}
```

## 🔐 Security Notes

- Never include customer personal information (PII)
- Don't store sensitive policy pricing algorithms
- Keep this directory secure (not in public repositories)
- Review content for compliance with regulations
