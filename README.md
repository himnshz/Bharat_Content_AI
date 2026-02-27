# Bharat Content AI - Multilingual Smart Content Assistant

A powerful AI-driven content creation and management platform designed specifically for Indian creators, supporting multiple Indian languages.

## 🎯 Features

### 1. Content Generator
Generate high-quality content in multiple Indian languages including Hindi, Tamil, Telugu, Bengali, and more.

### 2. Smart Translation & Tone Change
Translate content between Indian languages while maintaining cultural context and adjusting tone as needed.

### 3. Social Media Scheduler
Schedule and automate posts across multiple social media platforms.

### 4. Creative Assistant
Get AI-powered creative suggestions, ideation support, and content variations.

### 5. Content Summarizer
Summarize long-form content and extract key points in multiple Indian languages.

### 6. Engagement Analytics
Track content performance with comprehensive analytics and insights.

## 🚀 Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy with SQLite (dev) / PostgreSQL (production)
- **AI Models**: 
  - Google Gemini 2.5 Flash (currently active)
  - AWS Bedrock (Claude 3.5, Llama 3.1) - configured for future use
- **Translation**: AWS Translate
- **Voice**: AWS Transcribe
- **Storage**: AWS S3

### Frontend
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **State Management**: React Hooks

## 📦 Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

Frontend will run on: http://localhost:3000

## 🔑 API Keys Required

### Currently Active: Google Gemini
- Get your free API key: https://makersuite.google.com/app/apikey
- Add to `backend/.env`: `GEMINI_API_KEY=your_key_here`
- Free tier: 1,500 requests/day

### Future: AWS Services
- AWS Bedrock (Claude, Llama models)
- AWS Translate (Indian languages)
- AWS Transcribe (Voice-to-text)
- AWS S3 (Media storage)

## 📊 Database Models

The application includes comprehensive database models:

- **User**: Role-based access, subscription tiers
- **Content**: AI-generated content with quality metrics
- **Post**: Multi-platform social media posts
- **Translation**: Translation history and quality tracking
- **SocialAccount**: OAuth and token management
- **Analytics**: Comprehensive engagement metrics
- **VoiceInput**: Voice-to-text processing
- **AIModelConfig**: Model management and cost tracking

## 🎨 Supported Languages

- Hindi (हिंदी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Bengali (বাংলা)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Punjabi (ਪੰਜਾਬੀ)
- Urdu (اردو)
- English

## 🔧 Configuration

### Environment Variables

Create `backend/.env` with:

```env
# API Configuration
PORT=8000
DEBUG=True

# Google Gemini API (Currently Active)
GEMINI_API_KEY=your_gemini_api_key_here

# AWS Credentials (For Future Use)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Database
DATABASE_URL=sqlite:///./bharat_content_ai.db
```

## 📱 API Endpoints

### Content Generation
```
POST /api/content/generate
Body: {
  "prompt": "Write about AI in India",
  "language": "hindi",
  "tone": "professional",
  "content_type": "blog"
}
```

### Translation
```
POST /api/translation/translate
Body: {
  "text": "Hello, how are you?",
  "source_language": "english",
  "target_language": "hindi",
  "tone": "casual"
}
```

## 🎯 Project Structure

```
AI-Content_Creator/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   │   ├── content_generation/
│   │   │   │   ├── gemini_service.py    # Google Gemini
│   │   │   │   └── bedrock_service.py   # AWS Bedrock
│   │   │   ├── translation/
│   │   │   ├── social_media/
│   │   │   ├── analytics/
│   │   │   └── voice/
│   │   ├── config/          # Configuration
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   └── package.json
├── design.md
├── requirements.md
└── README.md
```

## 👥 Target Users

- Students
- YouTubers
- Small Businesses
- Teachers
- Startups

## 🚀 Innovation Highlights

- **Regional Language Focus**: Native support for Indian languages
- **Voice Input**: Speak to create content (AWS Transcribe)
- **Low Bandwidth Mode**: Optimized for areas with poor connectivity
- **Mobile-Friendly**: Responsive design for on-the-go content creation

## 🔮 Future Enhancements

- AI Video Generation
- Voice Cloning
- Meme Maker
- News Bot
- Advanced Analytics Dashboard

## 📄 License

This project is part of the AI for Bharat Hackathon.

## 👨‍💻 Author

Vaibhav R

## 🙏 Acknowledgments

Built for the AI for Bharat Hackathon to empower Indian content creators with multilingual AI tools.

---

## 🎉 Current Status

✅ **Working Features:**
- Content generation in 10+ Indian languages (Google Gemini 2.5 Flash)
- Translation API endpoints
- Database models complete
- FastAPI backend running
- Next.js frontend structure

⏳ **In Progress:**
- AWS Bedrock integration (configured, pending account access)
- Social media scheduler
- Analytics dashboard
- Voice input processing

**Note**: The application is currently using Google Gemini API for content generation. AWS Bedrock integration is fully configured and will be activated once AWS account access is enabled.
