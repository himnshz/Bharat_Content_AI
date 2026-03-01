"""Anthropic Claude Content Generation Service"""

import os
import time
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class AnthropicContentGenerator:
    """Content generation using Anthropic Claude API"""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    
    def generate_content(
        self,
        prompt: str,
        language: str = "hindi",
        tone: str = "casual",
        content_type: str = "social_post",
        model: str = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Generate content using Anthropic Claude"""
        start_time = time.time()
        
        model_to_use = model or self.model
        enhanced_prompt = self._build_prompt(prompt, language, tone, content_type)
        
        try:
            response = self.client.messages.create(
                model=model_to_use,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": enhanced_prompt}
                ]
            )
            
            content = response.content[0].text
            generation_time = int((time.time() - start_time) * 1000)
            
            return {
                "content": content,
                "model_used": model_to_use,
                "model_name": f"Anthropic {model_to_use}",
                "generation_time_ms": generation_time,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "stop_reason": response.stop_reason,
            }
            
        except Exception as e:
            raise Exception(f"Anthropic API Error: {str(e)}")
    
    def _build_prompt(self, prompt: str, language: str, tone: str, content_type: str) -> str:
        """Build enhanced prompt"""
        language_map = {
            "hindi": "Hindi (हिंदी) using Devanagari script",
            "tamil": "Tamil (தமிழ்) using Tamil script",
            "telugu": "Telugu (తెలుగు) using Telugu script",
            "bengali": "Bengali (বাংলা) using Bengali script",
            "marathi": "Marathi (मराठी) using Devanagari script",
            "gujarati": "Gujarati (ગુજરાતી) using Gujarati script",
            "kannada": "Kannada (ಕನ್ನಡ) using Kannada script",
            "malayalam": "Malayalam (മലയാളം) using Malayalam script",
            "punjabi": "Punjabi (ਪੰਜਾਬੀ) using Gurmukhi script",
            "english": "English",
        }
        
        target_lang = language_map.get(language, language)
        
        return f"""You are an expert content creator for Indian audiences.

Create {content_type} content in {target_lang} with a {tone} tone.

User Request: {prompt}

Requirements:
- Write ENTIRELY in {target_lang} (use native script)
- Maintain {tone} tone throughout
- Make it culturally relevant for Indian audiences
- Include appropriate emojis if suitable
- For social posts, suggest 3-5 relevant hashtags

Generate the content now:"""
