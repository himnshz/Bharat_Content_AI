# AI Services - Quick Reference Card

## 🚀 Setup (Choose ONE or MORE)

```bash
# Gemini (Free - Recommended for Dev)
export GEMINI_API_KEY="your_key"

# OpenAI (High Quality)
export OPENAI_API_KEY="sk-your_key"

# AWS Bedrock (Enterprise)
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"

# Anthropic (Claude Direct)
export ANTHROPIC_API_KEY="your_key"

# Cohere
export COHERE_API_KEY="your_key"
```

## 📋 Quick Commands

```bash
# Check available services
curl http://localhost:8000/api/content/ai-services/status

# Generate content (auto-selects best service)
curl -X POST "http://localhost:8000/api/content/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write about AI","language":"hindi","tone":"casual","content_type":"social_post","user_id":1}'

# Install optional packages
pip install openai anthropic cohere
```

## 🎯 Service Priority

```
1. Gemini    → Free, multilingual
2. Bedrock   → Enterprise, AWS
3. OpenAI    → High quality
4. Anthropic → Content creation
5. Groq      → Fast inference
6. Cohere    → Generation
7. Together  → Open source
8. HuggingFace → Fallback
```

## 💰 Cost Comparison

| Service | Free Tier | Cost/1M tokens |
|---------|-----------|----------------|
| Gemini | ✅ Yes | Free / $0.50 |
| Groq | ✅ Yes | Free / Low |
| OpenAI | ❌ No | $0.15-60 |
| Bedrock | ❌ No | $3-15 |
| Anthropic | ❌ No | $3-15 |
| Cohere | ✅ Limited | $0.40-15 |

## 🔧 Configuration Files

```
backend/
├── .env                    # Your API keys here
├── .env.example            # Template with all options
├── AI_SERVICES_GUIDE.md    # Full documentation
└── AI_QUICK_REFERENCE.md   # This file
```

## ✅ Verification

```bash
# 1. Check service status
curl http://localhost:8000/api/content/ai-services/status

# 2. Should return:
{
  "status": "operational",
  "primary_service": "gemini",
  "available_services": ["gemini"],
  "total_available": 1
}

# 3. If total_available = 0, configure an API key!
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| No services available | Set at least one API key in .env |
| Service not detected | Install package: `pip install openai` |
| API key invalid | Check key format and validity |
| All services failing | Check internet, API status pages |

## 📚 Documentation

- **Full Guide:** `AI_SERVICES_GUIDE.md`
- **Summary:** `AI_INTEGRATION_SUMMARY.md`
- **API Docs:** `API_DOCUMENTATION.md`
- **Setup:** `SETUP_GUIDE.md`

## 🎓 Recommended Setups

**Development:**
```env
GEMINI_API_KEY=your_key
```

**Production (Budget):**
```env
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
```

**Production (Quality):**
```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
```

**Enterprise:**
```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
```

---

**Need help?** Check `AI_SERVICES_GUIDE.md` for detailed instructions!
