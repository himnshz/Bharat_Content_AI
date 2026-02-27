import json
import time
import requests
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError
import os

from app.config.aws_config import (
    AWS_BEARER_TOKEN_BEDROCK,
    BEDROCK_REGION,
    BEDROCK_MODELS,
    MODEL_SPECS,
    get_recommended_model
)


class BedrockContentGenerator:
    """Advanced content generation using AWS Bedrock models with Bearer Token"""
    
    def __init__(self):
        self.bearer_token = AWS_BEARER_TOKEN_BEDROCK
        self.region = BEDROCK_REGION
        self.use_bearer_token = bool(self.bearer_token)
    
    def generate_content(
        self,
        prompt: str,
        language: str = "hindi",
        tone: str = "casual",
        content_type: str = "social_post",
        model_preference: str = "balanced",
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate content using the most advanced Bedrock models
        
        Args:
            prompt: User's content request
            language: Target language (hindi, tamil, etc.)
            tone: Content tone (casual, formal, etc.)
            content_type: Type of content to generate
            model_preference: quality, speed, cost, or balanced
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0-1)
        
        Returns:
            Dict with generated content and metadata
        """
        start_time = time.time()
        
        # Select best model for the task
        model_id = get_recommended_model("content_generation", model_preference)
        
        # Build enhanced prompt
        enhanced_prompt = self._build_prompt(
            prompt, language, tone, content_type
        )
        
        try:
            # Use Bearer Token method (HTTP requests)
            if self.use_bearer_token:
                response = self._invoke_with_bearer_token(
                    model_id, enhanced_prompt, max_tokens, temperature
                )
            else:
                # Fallback to boto3 (if IAM credentials available)
                response = self._invoke_with_boto3(
                    model_id, enhanced_prompt, max_tokens, temperature
                )
            
            generation_time = int((time.time() - start_time) * 1000)
            
            return {
                "content": response["content"],
                "model_used": model_id,
                "model_name": MODEL_SPECS.get(model_id, {}).get("name", model_id),
                "generation_time_ms": generation_time,
                "input_tokens": response.get("input_tokens", 0),
                "output_tokens": response.get("output_tokens", 0),
                "stop_reason": response.get("stop_reason", "complete"),
            }
            
        except Exception as e:
            raise Exception(f"Bedrock Error: {str(e)}")
    
    def _invoke_with_bearer_token(
        self,
        model_id: str,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Invoke Bedrock model using Bearer Token (HTTP request)"""
        
        url = f"https://bedrock-runtime.{self.region}.amazonaws.com/model/{model_id}/invoke"
        
        # Build request body based on model type
        if "claude-3" in model_id or "claude-3-5" in model_id:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}]
            }
        elif "llama" in model_id:
            body = {
                "prompt": prompt,
                "max_gen_len": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
            }
        elif "mistral" in model_id:
            body = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
            }
        else:  # Claude 2
            body = {
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
            }
        
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=body, timeout=60)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        result = response.json()
        
        # Parse response based on model type
        if "claude-3" in model_id or "claude-3-5" in model_id:
            return {
                "content": result['content'][0]['text'],
                "input_tokens": result['usage']['input_tokens'],
                "output_tokens": result['usage']['output_tokens'],
                "stop_reason": result.get('stop_reason', 'end_turn'),
            }
        elif "llama" in model_id:
            return {
                "content": result['generation'],
                "input_tokens": result.get('prompt_token_count', 0),
                "output_tokens": result.get('generation_token_count', 0),
                "stop_reason": result.get('stop_reason', 'complete'),
            }
        elif "mistral" in model_id:
            return {
                "content": result['outputs'][0]['text'],
                "input_tokens": 0,
                "output_tokens": 0,
                "stop_reason": result['outputs'][0].get('stop_reason', 'complete'),
            }
        else:  # Claude 2
            return {
                "content": result['completion'],
                "input_tokens": 0,
                "output_tokens": 0,
                "stop_reason": result.get('stop_reason', 'complete'),
            }
    
    def _invoke_with_boto3(
        self,
        model_id: str,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> Dict[str, Any]:
        """Invoke Bedrock model using boto3 (fallback method)"""
        from app.config.aws_config import get_bedrock_client
        
        client = get_bedrock_client()
        
        # Use Claude 3.5 Sonnet (most advanced)
        if "claude-3" in model_id or "claude-3-5" in model_id:
            return self._invoke_claude_3(model_id, prompt, max_tokens, temperature, client)
        # Use Llama 3.1
        elif "llama3-1" in model_id:
            return self._invoke_llama_3(model_id, prompt, max_tokens, temperature, client)
        # Use Mistral
        elif "mistral" in model_id:
            return self._invoke_mistral(model_id, prompt, max_tokens, temperature, client)
        # Fallback to Claude 2
        else:
            return self._invoke_claude_2(model_id, prompt, max_tokens, temperature, client)
    
    def _build_prompt(
        self, 
        prompt: str, 
        language: str, 
        tone: str, 
        content_type: str
    ) -> str:
        """Build enhanced prompt with context"""
        
        language_map = {
            "hindi": "Hindi (हिंदी)",
            "tamil": "Tamil (தமிழ்)",
            "telugu": "Telugu (తెలుగు)",
            "bengali": "Bengali (বাংলা)",
            "marathi": "Marathi (मराठी)",
            "gujarati": "Gujarati (ગુજરાતી)",
            "kannada": "Kannada (ಕನ್ನಡ)",
            "malayalam": "Malayalam (മലയാളം)",
            "punjabi": "Punjabi (ਪੰਜਾਬੀ)",
            "english": "English",
        }
        
        tone_descriptions = {
            "casual": "friendly, conversational, and relatable",
            "formal": "professional, polished, and respectful",
            "professional": "business-appropriate and authoritative",
            "friendly": "warm, approachable, and engaging",
            "humorous": "witty, entertaining, and light-hearted",
            "inspirational": "motivating, uplifting, and empowering",
            "educational": "informative, clear, and instructive",
        }
        
        content_instructions = {
            "social_post": "Create an engaging social media post with appropriate hashtags",
            "blog": "Write a comprehensive blog article with introduction, body, and conclusion",
            "article": "Compose a well-structured article with clear sections",
            "caption": "Write a concise, catchy caption",
            "script": "Create a video or audio script with natural flow",
            "email": "Draft a professional email with proper greeting and closing",
            "ad_copy": "Write persuasive advertising copy that drives action",
        }
        
        target_lang = language_map.get(language, language)
        tone_desc = tone_descriptions.get(tone, tone)
        content_inst = content_instructions.get(content_type, "Create engaging content")
        
        enhanced_prompt = f"""You are an expert content creator for Indian audiences, specializing in multilingual content.

Task: {content_inst}
Language: {target_lang}
Tone: {tone_desc}

User Request: {prompt}

Instructions:
1. Write ENTIRELY in {target_lang} (use native script)
2. Maintain a {tone_desc} tone throughout
3. Make it culturally relevant for Indian audiences
4. Include appropriate emojis if suitable for the platform
5. For social posts, suggest 3-5 relevant hashtags at the end
6. Keep it engaging and authentic

Generate the content now:"""
        
        return enhanced_prompt
    
    def _invoke_claude_3(
        self, 
        model_id: str, 
        prompt: str, 
        max_tokens: int, 
        temperature: float,
        client=None
    ) -> Dict[str, Any]:
        """Invoke Claude 3/3.5 models with Messages API"""
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            "content": response_body['content'][0]['text'],
            "input_tokens": response_body['usage']['input_tokens'],
            "output_tokens": response_body['usage']['output_tokens'],
            "stop_reason": response_body.get('stop_reason', 'end_turn'),
        }
    
    def _invoke_llama_3(
        self, 
        model_id: str, 
        prompt: str, 
        max_tokens: int, 
        temperature: float,
        client=None
    ) -> Dict[str, Any]:
        """Invoke Llama 3.1 models"""
        
        body = {
            "prompt": prompt,
            "max_gen_len": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
        }
        
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            "content": response_body['generation'],
            "input_tokens": response_body.get('prompt_token_count', 0),
            "output_tokens": response_body.get('generation_token_count', 0),
            "stop_reason": response_body.get('stop_reason', 'complete'),
        }
    
    def _invoke_mistral(
        self, 
        model_id: str, 
        prompt: str, 
        max_tokens: int, 
        temperature: float,
        client=None
    ) -> Dict[str, Any]:
        """Invoke Mistral models"""
        
        body = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
        }
        
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            "content": response_body['outputs'][0]['text'],
            "input_tokens": 0,  # Mistral doesn't return token counts
            "output_tokens": 0,
            "stop_reason": response_body['outputs'][0].get('stop_reason', 'complete'),
        }
    
    def _invoke_claude_2(
        self, 
        model_id: str, 
        prompt: str, 
        max_tokens: int, 
        temperature: float,
        client=None
    ) -> Dict[str, Any]:
        """Invoke Claude 2 models (legacy)"""
        
        body = {
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
        }
        
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            "content": response_body['completion'],
            "input_tokens": 0,
            "output_tokens": 0,
            "stop_reason": response_body.get('stop_reason', 'complete'),
        }
    
    def generate_multilingual_variations(
        self,
        content: str,
        source_language: str,
        target_languages: list,
        tone: str = "casual"
    ) -> Dict[str, str]:
        """
        Generate content variations in multiple Indian languages
        Uses Claude 3.5 Sonnet for best multilingual performance
        """
        model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
        
        variations = {}
        
        for target_lang in target_languages:
            prompt = f"""Translate and adapt this content from {source_language} to {target_lang}.
Maintain the {tone} tone and make it culturally appropriate.

Original content:
{content}

Provide ONLY the translated content in {target_lang} (use native script):"""
            
            try:
                result = self._invoke_claude_3(model_id, prompt, 2000, 0.7)
                variations[target_lang] = result["content"]
            except Exception as e:
                variations[target_lang] = f"Error: {str(e)}"
        
        return variations
