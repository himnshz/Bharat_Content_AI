"""Cohere Content Generation Service"""

import os
import time
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class CohereContentGenerator:
    """Content generation using Cohere API"""
    
    def __init__(self):
        self.api_key = os.getenv('COHERE_API_KEY')
        self.model = os.getenv('COHERE_MODEL', 'command-r-plus')
        
        try:
            import cohere
            self.client = cohere.Client(api_key=self.api_key)
        except ImportError:
            raise ImportError("Cohere package not installed. Run: pip install cohere")
    
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
        """Generate content using Cohere"""
        start_time = time.time()
        
        model_to_use = model or self.model
        enhanced_prompt = self._build_prompt(prompt, language, tone, content_type)
        
        try:
            response = self.client.generate(
                model=model_to_use,
                prompt=enhanced_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                k=0,
                p=0.9,
            )
            
            content = response.generations[0].text
            generation_time = int((time.time() - start_time) * 1000)
            
            return {
                "content": content,
                "model_used": model_to_use,
                "model_name": f"Cohere {model_to_use}",
                "generation_time_ms": generation_time,
                "input_tokens": 0,  # Cohere doesn't return token counts in basic API
                "output_tokens": 0,
                "stop_reason": response.generations[0].finish_reason,
            }
            
        except Exception as e:
            raise Exception(f"Cohere API Error: {str(e)}")
    
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
        
        return f"""Create {content_type} content in {target_lang} with a {tone} tone.

User Request: {prompt}

Requirements:
- Write ENTIRELY in {target_lang} (use native script)
- Maintain {tone} tone
- Make it culturally relevant for Indian audiences
- Include emojis if appropriate
- For social posts, add 3-5 relevant hashtags

Generate the content:"""
