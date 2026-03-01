# AI Services Integration Guide

## Overview

The Bharat Content AI backend now features a **unified AI service manager** that automatically detects and uses whatever API keys you have configured. No need to manually switch between services - the system intelligently selects the best available option!

## Supported AI Services

### ✅ Currently Integrated

1. **Google Gemini** (Recommended for free tier)
   - Model: `gemini-2.5-flash`, `gemini-pro`
   - Best for: Multilingual content, free tier available
   - Cost: Free tier available

2. **AWS Bedrock** (Enterprise-grade)
   - Models: Claude 3.5 Sonnet, Llama 3.1, Mistral, and more
   - Best for: AWS integration, multiple model options
   - Cost: Pay per use

3. **OpenAI** (High quality)
   - Models: GPT-4o, GPT-4o-mini, GPT-4, GPT-3.5-turbo
   - Best for: High-quality content generation
   - Cost: Pay per token

4. **Anthropic Claude** (Excellent for content)
   - Models: Claude 3.5 Sonnet, Claude 3 Opus/Sonnet/Haiku
   - Best for: Long-form content, analysis
   - Cost: Pay per token

5. **Cohere** (Good for generation)
   - Models: Command R+, Command R
   - Best for: Text generation, embeddings
   - Cost: Pay per use

6. **HuggingFace** (Open source models)
   - Various open-source models
   - Best for: Custom models, experimentation
   - Cost: Free tier available

7. **Groq** (Fast inference)
   - Fast inference for various models
   - Best for: Speed-critical applications
   - Cost: Free tier available

8. **Together AI** (Open source)
   - Various open-source models
   - Best for: Cost-effective solutions
   - Cost: Competitive pricing

---

## Quick Setup

### Option 1: Google Gemini (Easiest - Free Tier)

```bash
# Get API key from: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### Option 2: AWS Bedrock

```bash
# Method 1: IAM Credentials
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_REGION="us-east-1"

# Method 2: Bearer Token
export AWS_BEARER_TOKEN_BEDROCK="your_bearer_token"
export BEDROCK_REGION="us-east-1"
```

### Option 3: OpenAI

```bash
# Get API key from: https://platform.openai.com/api-keys
export OPENAI_API_KEY="your_openai_api_key_here"
export OPENAI_MODEL="gpt-4o-mini"  # Optional, defaults to gpt-4o-mini
```

### Option 4: Anthropic Claude

```bash
# Get API key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"  # Optional
```

### Option 5: Cohere

```bash
# Get API key from: https://dashboard.cohere.com/api-keys
export COHERE_API_KEY="your_cohere_api_key_here"
export COHERE_MODEL="command-r-plus"  # Optional
```

---

## Environment Configuration

Create or update `backend/.env`:

```env
# Choose ONE or MORE services (system will auto-select best available)

# Google Gemini (Free tier)
GEMINI_API_KEY=your_gemini_api_key_here

# AWS Bedrock
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Cohere
COHERE_API_KEY=your_cohere_api_key_here
COHERE_MODEL=command-r-plus

# HuggingFace
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Groq
GROQ_API_KEY=your_groq_api_key_here

# Together AI
TOGETHER_API_KEY=your_together_api_key_here
```

---

## How It Works

### Automatic Service Selection

The AI Service Manager automatically:

1. **Detects** which API keys are configured
2. **Selects** the best available service based on priority
3. **Falls back** to alternative services if primary fails
4. **Provides** unified interface for all services

### Priority Order

```
1. Google Gemini    (Free tier, good multilingual)
2. AWS Bedrock      (Enterprise, multiple models)
3. OpenAI           (High quality)
4. Anthropic        (Excellent for content)
5. Groq             (Fast inference)
6. Cohere           (Good generation)
7. Together AI      (Open source)
8. HuggingFace      (Fallback)
```

### Fallback Mechanism

If the primary service fails, the system automatically tries the next available service:

```
Request → Gemini (fails) → Bedrock (fails) → OpenAI (success) ✓
```

---

## Installation

### Install Base Requirements

```bash
pip install -r requirements.txt
```

### Install Optional AI Service Packages

Install only the packages for services you want to use:

```bash
# Google Gemini (already included in requirements.txt)
pip install google-generativeai

# OpenAI
pip install openai

# Anthropic
pip install anthropic

# Cohere
pip install cohere

# HuggingFace
pip install huggingface-hub

# Groq
pip install groq

# Install all at once
pip install google-generativeai openai anthropic cohere huggingface-hub groq
```

---

## API Usage

### Check Available Services

```bash
curl http://localhost:8000/api/content/ai-services/status
```

Response:
```json
{
  "status": "operational",
  "primary_service": "gemini",
  "available_services": ["gemini", "openai", "bedrock"],
  "total_available": 3,
  "service_status": {
    "gemini": true,
    "bedrock": true,
    "openai": true,
    "anthropic": false,
    "cohere": false
  }
}
```

### Generate Content (Auto-selects best service)

```bash
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write about Indian festivals",
    "language": "hindi",
    "tone": "casual",
    "content_type": "social_post",
    "user_id": 1
  }'
```

Response includes which service was used:
```json
{
  "id": 1,
  "generated_content": "भारतीय त्योहार...",
  "model_used": "gemini-pro",
  "service_used": "gemini",
  ...
}
```

---

## Service Comparison

| Service | Free Tier | Multilingual | Speed | Quality | Cost (per 1M tokens) |
|---------|-----------|--------------|-------|---------|---------------------|
| **Gemini** | ✅ Yes | ⭐⭐⭐⭐⭐ | Fast | High | Free / $0.50 |
| **Bedrock** | ❌ No | ⭐⭐⭐⭐ | Fast | Very High | $3-15 |
| **OpenAI** | ❌ No | ⭐⭐⭐⭐ | Medium | Very High | $0.15-60 |
| **Anthropic** | ❌ No | ⭐⭐⭐⭐ | Medium | Very High | $3-15 |
| **Cohere** | ✅ Limited | ⭐⭐⭐ | Fast | Good | $0.40-15 |
| **Groq** | ✅ Yes | ⭐⭐⭐ | Very Fast | Good | Free / Low |
| **Together** | ✅ Limited | ⭐⭐⭐ | Fast | Good | $0.20-1 |

---

## Advanced Usage

### Specify Preferred Service

```python
from app.services.content_generation.ai_service_manager import get_ai_service_manager

ai_manager = get_ai_service_manager()

# Use specific service
result = ai_manager.generate_content(
    prompt="Write about AI",
    language="hindi",
    preferred_service="openai"  # Force OpenAI
)
```

### Summarize Content

```python
result = ai_manager.summarize_content(
    text="Long text to summarize...",
    target_length=100,
    language="english"
)
```

### Translate Content

```python
result = ai_manager.translate_content(
    text="Hello, how are you?",
    source_language="english",
    target_language="hindi",
    maintain_tone=True
)
```

### Enhance Content

```python
result = ai_manager.enhance_content(
    text="Original content...",
    enhancement_type="improve",  # or "expand", "simplify", "formalize"
    language="english"
)
```

---

## Troubleshooting

### No Services Available

**Error:** `No AI services available`

**Solution:**
1. Check if at least one API key is configured in `.env`
2. Verify API key is valid (not placeholder)
3. Check service status endpoint

```bash
curl http://localhost:8000/api/content/ai-services/status
```

### Service-Specific Errors

**Gemini Error:** `GEMINI_API_KEY not found`
```bash
# Get key from: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="your_actual_key"
```

**OpenAI Error:** `Incorrect API key provided`
```bash
# Verify key at: https://platform.openai.com/api-keys
export OPENAI_API_KEY="sk-..."
```

**Bedrock Error:** `Unable to locate credentials`
```bash
# Configure AWS credentials
aws configure
# Or set environment variables
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### Package Not Installed

**Error:** `openai package not installed`

**Solution:**
```bash
pip install openai
# Or for the specific service you need
pip install anthropic  # for Anthropic
pip install cohere     # for Cohere
```

---

## Cost Optimization

### Recommended Setup by Use Case

**Development/Testing:**
```env
GEMINI_API_KEY=your_key  # Free tier
```

**Production (Budget):**
```env
GEMINI_API_KEY=your_key      # Primary
GROQ_API_KEY=your_key        # Fallback (fast & cheap)
```

**Production (Quality):**
```env
OPENAI_API_KEY=your_key      # Primary (GPT-4o-mini)
GEMINI_API_KEY=your_key      # Fallback
```

**Enterprise:**
```env
AWS_ACCESS_KEY_ID=your_key   # Bedrock (Claude 3.5)
OPENAI_API_KEY=your_key      # Fallback
GEMINI_API_KEY=your_key      # Emergency fallback
```

---

## Monitoring

### Check Service Health

```bash
# Get service status
curl http://localhost:8000/api/content/ai-services/status

# Generate test content
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test",
    "language": "english",
    "tone": "casual",
    "content_type": "social_post",
    "user_id": 1
  }'
```

### Monitor Usage

Check the `model_used` field in responses to see which service was used:

```json
{
  "model_used": "gemini-pro",
  "service_used": "gemini",
  "generation_time_ms": 1250,
  "input_tokens": 45,
  "output_tokens": 120
}
```

---

## Best Practices

1. **Configure Multiple Services** for redundancy
2. **Start with Gemini** (free tier) for development
3. **Monitor costs** in production
4. **Use appropriate models** for your use case
5. **Implement rate limiting** to control costs
6. **Cache responses** when possible
7. **Log service usage** for analytics

---

## Migration Guide

### From Old System (Manual Selection)

**Before:**
```python
use_gemini = os.getenv('GEMINI_API_KEY') and ...
if use_gemini:
    generator = GeminiContentGenerator()
else:
    generator = BedrockContentGenerator()
```

**After:**
```python
from app.services.content_generation.ai_service_manager import get_ai_service_manager

ai_manager = get_ai_service_manager()
result = ai_manager.generate_content(...)
```

### Benefits

- ✅ Automatic service detection
- ✅ Built-in fallback mechanism
- ✅ Support for 8+ AI services
- ✅ Unified interface
- ✅ Easy to add new services
- ✅ Better error handling

---

## Support

For issues or questions:
- Check service status endpoint
- Review error messages
- Verify API keys are valid
- Check service-specific documentation
- Review logs for detailed errors

---

## Future Enhancements

- [ ] Automatic cost tracking
- [ ] Service performance metrics
- [ ] Smart model selection based on task
- [ ] Response caching
- [ ] Rate limiting per service
- [ ] A/B testing between services
- [ ] Custom model fine-tuning support
