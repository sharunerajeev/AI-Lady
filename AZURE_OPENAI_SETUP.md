# Azure OpenAI Integration Guide

This guide explains how to configure the AI Insurance Assistant to use Azure OpenAI with either GPT-4 or DeepSeek R1 models.

## Overview

The application uses a **single Azure OpenAI API key** that provides access to multiple model deployments:

- **GPT-4** (or GPT-4 Turbo): Advanced language model for high-quality responses
- **DeepSeek R1**: Reasoning-enhanced model with advanced problem-solving capabilities

## Prerequisites

1. **Azure Subscription**: You need an active Azure account
2. **Azure OpenAI Resource**: Create an Azure OpenAI resource in the Azure Portal
3. **Model Deployments**: Deploy your desired models (GPT-4 and/or DeepSeek R1) in your Azure OpenAI resource

## Configuration Steps

### 1. Get Your Azure OpenAI Credentials

From the Azure Portal:

1. Navigate to your Azure OpenAI resource
2. Go to **Keys and Endpoint** section
3. Copy:
   - **KEY 1** (your API key)
   - **Endpoint** (e.g., `https://your-resource.openai.azure.com/`)

### 2. Create Model Deployments

In your Azure OpenAI Studio:

1. Go to **Deployments** section
2. Create a deployment for GPT-4:
   - Model: `gpt-4` or `gpt-4-turbo`
   - Deployment name: e.g., `gpt-4-deployment`
3. (Optional) Create a deployment for DeepSeek R1:
   - Model: `deepseek-r1`
   - Deployment name: e.g., `deepseek-deployment`

### 3. Configure Environment Variables

Update your `.env` file with the following settings:

```bash
# ==================== AI MODEL PROVIDER ====================
# Set to "azure" to use Azure OpenAI
MODEL_PROVIDER=azure

# ==================== AZURE OPENAI ====================
# Single Azure key provides access to both GPT-4 and DeepSeek R1
AZURE_OPENAI_API_KEY=your_azure_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Model Deployments (use your deployment names from Azure Portal)
AZURE_OPENAI_DEPLOYMENT=gpt-4-deployment
AZURE_DEEPSEEK_DEPLOYMENT=deepseek-deployment

# Choose which model to use
AZURE_MODEL_TYPE=gpt-4
# Options: "gpt-4", "gpt-4-turbo", "deepseek-r1"

# ==================== AI SETTINGS ====================
MAX_TOKENS=2000
TEMPERATURE=0.7
ENABLE_MARKDOWN=true
STRIP_REASONING_TAGS=true
```

### 4. Switch Between Models

To switch between GPT-4 and DeepSeek R1, simply update `AZURE_MODEL_TYPE`:

**For GPT-4:**

```bash
AZURE_MODEL_TYPE=gpt-4
```

**For DeepSeek R1:**

```bash
AZURE_MODEL_TYPE=deepseek-r1
```

## Model Comparison

### GPT-4

- **Best for**: General-purpose conversations, creative responses, nuanced understanding
- **Strengths**: Broad knowledge, excellent at following instructions, great at markdown formatting
- **Use cases**: Customer inquiries, policy explanations, general insurance questions

### DeepSeek R1

- **Best for**: Complex reasoning, analytical queries, multi-step problem solving
- **Strengths**: Advanced reasoning with `<think>` tags (automatically stripped), detailed analysis
- **Use cases**: Policy comparisons, claim analysis, complex eligibility calculations
- **Note**: Responses include reasoning process in `<think>` tags that are automatically removed

## Features

### 1. Automatic Reasoning Tag Removal

When using DeepSeek R1, the system automatically removes `<think>...</think>` tags that contain the model's internal reasoning process:

```
STRIP_REASONING_TAGS=true  # Enabled by default
```

**Example:**

- **Raw DeepSeek Response:**

  ```
  <think>
  The user is asking about life insurance for a 35-year-old...
  Need to consider term vs whole life options...
  </think>

  Based on your age and needs, I recommend...
  ```

- **What User Sees:**
  ```
  Based on your age and needs, I recommend...
  ```

### 2. Enhanced Markdown Support

Both models are configured to use full markdown formatting:

- **Bold** for important terms
- Lists with bullet points and numbers
- Code blocks for policy details
- Tables for comparisons
- Blockquotes for important notes

The frontend automatically renders markdown using:

- `marked.js` for parsing
- `DOMPurify` for XSS protection

### 3. Smart Recommendation Integration

The AI models integrate seamlessly with the recommendation engine:

- Multi-turn conversations for gathering user requirements
- Context-aware product suggestions
- Personalized insurance matching

## Testing Your Configuration

### 1. Check System Health

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{
  "status": "healthy",
  "model_provider": "azure",
  "azure_configured": true,
  "available_providers": {
    "ollama": false,
    "azure": true,
    "azure_model": "gpt-4"
  }
}
```

### 2. Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What types of life insurance do you offer?",
    "session_id": "test-session"
  }'
```

### 3. Web Interface

1. Open `http://localhost:8000/static/index.html`
2. Send a test message
3. Check the response formatting and quality

## Troubleshooting

### Issue: "Azure OpenAI client not configured"

**Solution:** Verify these environment variables are set:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`

### Issue: 401 Unauthorized

**Solution:**

- Check your API key is correct
- Verify key hasn't expired in Azure Portal
- Ensure your Azure OpenAI resource is active

### Issue: 404 Model Not Found

**Solution:**

- Verify deployment names match your Azure configuration
- Check `AZURE_OPENAI_DEPLOYMENT` or `AZURE_DEEPSEEK_DEPLOYMENT`
- Ensure model is deployed and active in Azure OpenAI Studio

### Issue: Slow Responses

**Solution:**

- Check your Azure OpenAI resource tier and quotas
- Consider reducing `MAX_TOKENS` (default: 2000)
- Verify network connectivity to Azure endpoint

### Issue: DeepSeek `<think>` Tags Showing

**Solution:**

- Ensure `STRIP_REASONING_TAGS=true` in `.env`
- Verify `AZURE_MODEL_TYPE=deepseek-r1`
- Check server logs for tag stripping execution

## Cost Optimization

### Token Usage

- GPT-4: Higher quality, higher cost per token
- DeepSeek R1: Reasoning overhead, but often more thorough
- Configure `MAX_TOKENS` based on your needs:
  - Short answers: `MAX_TOKENS=500`
  - Detailed responses: `MAX_TOKENS=2000`
  - Complex analysis: `MAX_TOKENS=4000`

### Rate Limiting

Azure OpenAI has different quota tiers. Monitor usage in Azure Portal:

- **Requests per minute**: Varies by tier
- **Tokens per minute**: Check your resource limits
- Consider implementing caching for frequent questions

## Advanced Configuration

### Custom System Prompts

The application uses comprehensive insurance domain knowledge from:

```python
from data.insurance_domain_knowledge import get_full_system_prompt
```

To customize prompts:

1. Edit `data/insurance_domain_knowledge.py`
2. Modify `get_full_system_prompt()` function
3. Restart the server

### Markdown Customization

Markdown rendering is controlled by:

- **Backend**: `ENABLE_MARKDOWN=true` in `.env`
- **Frontend**: `static/script.js` (marked.js configuration)
- **Styling**: `static/styles.css` (markdown element styles)

### Multiple Deployments

You can maintain multiple deployment configurations:

```bash
# Production
AZURE_OPENAI_DEPLOYMENT=gpt-4-prod
AZURE_DEEPSEEK_DEPLOYMENT=deepseek-prod

# Development/Testing
# AZURE_OPENAI_DEPLOYMENT=gpt-4-dev
# AZURE_DEEPSEEK_DEPLOYMENT=deepseek-dev
```

## Security Best Practices

1. **Never commit `.env` file**: Always use `.env.example` as template
2. **Rotate API keys regularly**: Update in both `.env` and Azure Portal
3. **Use Azure RBAC**: Implement role-based access control
4. **Monitor usage**: Set up alerts for unusual activity
5. **Enable logging**: Track API calls and errors for audit

## Support

For issues specific to:

- **Azure OpenAI Service**: Check [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- **This Application**: See `README.md` and `.github/copilot-instructions.md`
- **API Errors**: Check server logs: `tail -f insurance_assistant.log`

## Migration Notes

### From Separate OpenAI/DeepSeek Keys

If you previously had:

```bash
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
```

Now use:

```bash
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_DEEPSEEK_DEPLOYMENT=deepseek-r1
AZURE_MODEL_TYPE=gpt-4  # or deepseek-r1
```

All provider logic now routes through Azure with the model selection happening via `AZURE_MODEL_TYPE`.
