import os
import base64
from dotenv import load_dotenv
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Support for Bearer Token (your method)
AWS_BEARER_TOKEN_BEDROCK = os.getenv("AWS_BEARER_TOKEN_BEDROCK")

# Support for standard IAM credentials (alternative)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# AWS Bedrock Configuration
BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")

# Advanced Bedrock Models for Bharat Content AI
BEDROCK_MODELS = {
    "content_generation": {
        # Claude 3.5 Family (Most Advanced - Recommended)
        "claude_3_5_sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",  # Latest, best performance
        "claude_3_5_sonnet_v1": "anthropic.claude-3-5-sonnet-20240620-v1:0",  # Previous version
        
        # Claude 3 Family (High Performance)
        "claude_3_opus": "anthropic.claude-3-opus-20240229-v1:0",  # Most capable, best quality
        "claude_3_sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",  # Balanced performance
        "claude_3_haiku": "anthropic.claude-3-haiku-20240307-v1:0",  # Fast and cost-effective
        
        # Claude 2 Family (Legacy but reliable)
        "claude_v2_1": "anthropic.claude-v2:1",
        "claude_v2": "anthropic.claude-v2",
        "claude_instant": "anthropic.claude-instant-v1",
        
        # Meta Llama Family (Open Source)
        "llama3_1_405b": "meta.llama3-1-405b-instruct-v1:0",  # Largest, most capable
        "llama3_1_70b": "meta.llama3-1-70b-instruct-v1:0",  # High performance
        "llama3_1_8b": "meta.llama3-1-8b-instruct-v1:0",  # Fast and efficient
        "llama3_70b": "meta.llama3-70b-instruct-v1:0",
        "llama3_8b": "meta.llama3-8b-instruct-v1:0",
        "llama2_70b": "meta.llama2-70b-chat-v1",
        "llama2_13b": "meta.llama2-13b-chat-v1",
        
        # Amazon Titan Family
        "titan_premier": "amazon.titan-text-premier-v1:0",  # Advanced reasoning
        "titan_express": "amazon.titan-text-express-v1",
        "titan_lite": "amazon.titan-text-lite-v1",
        
        # Mistral AI Family (European alternative)
        "mistral_large_2": "mistral.mistral-large-2407-v1:0",  # Most advanced
        "mistral_large": "mistral.mistral-large-2402-v1:0",
        "mistral_7b": "mistral.mistral-7b-instruct-v0:2",
        "mixtral_8x7b": "mistral.mixtral-8x7b-instruct-v0:1",
        
        # Cohere Command Family
        "cohere_command_r_plus": "cohere.command-r-plus-v1:0",  # Best for RAG
        "cohere_command_r": "cohere.command-r-v1:0",
        "cohere_command_light": "cohere.command-light-text-v14",
        
        # AI21 Labs Jamba Family
        "jamba_1_5_large": "ai21.jamba-1-5-large-v1:0",  # Hybrid architecture
        "jamba_1_5_mini": "ai21.jamba-1-5-mini-v1:0",
        "jamba_instruct": "ai21.jamba-instruct-v1:0",
    },
    
    "multilingual_content": {
        # Best for Indian languages
        "claude_3_5_sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",  # Excellent multilingual
        "claude_3_opus": "anthropic.claude-3-opus-20240229-v1:0",
        "llama3_1_405b": "meta.llama3-1-405b-instruct-v1:0",
        "mistral_large_2": "mistral.mistral-large-2407-v1:0",
    },
    
    "summarization": {
        "claude_3_haiku": "anthropic.claude-3-haiku-20240307-v1:0",  # Fast summarization
        "claude_3_sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
        "llama3_1_8b": "meta.llama3-1-8b-instruct-v1:0",
        "titan_lite": "amazon.titan-text-lite-v1",
    },
    
    "creative_writing": {
        "claude_3_opus": "anthropic.claude-3-opus-20240229-v1:0",  # Most creative
        "claude_3_5_sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "llama3_1_405b": "meta.llama3-1-405b-instruct-v1:0",
    },
    
    "embeddings": {
        "titan_embeddings_v2": "amazon.titan-embed-text-v2:0",  # Latest
        "titan_embeddings": "amazon.titan-embed-text-v1",
        "cohere_embed_multilingual": "cohere.embed-multilingual-v3",
        "cohere_embed_english": "cohere.embed-english-v3",
    },
    
    "image_generation": {
        "titan_image_g1": "amazon.titan-image-generator-v1",
        "titan_image_g2": "amazon.titan-image-generator-v2:0",  # Latest
        "stable_diffusion_xl": "stability.stable-diffusion-xl-v1",
    }
}

# Model Capabilities and Pricing (as of 2024)
MODEL_SPECS = {
    "anthropic.claude-3-5-sonnet-20241022-v2:0": {
        "name": "Claude 3.5 Sonnet v2",
        "context_window": 200000,
        "max_output": 8192,
        "cost_per_1k_input": 0.003,
        "cost_per_1k_output": 0.015,
        "strengths": ["reasoning", "coding", "multilingual", "analysis"],
        "best_for": "complex content generation, multilingual tasks",
    },
    "anthropic.claude-3-opus-20240229-v1:0": {
        "name": "Claude 3 Opus",
        "context_window": 200000,
        "max_output": 4096,
        "cost_per_1k_input": 0.015,
        "cost_per_1k_output": 0.075,
        "strengths": ["highest_quality", "creative", "complex_reasoning"],
        "best_for": "premium content, creative writing, complex analysis",
    },
    "anthropic.claude-3-sonnet-20240229-v1:0": {
        "name": "Claude 3 Sonnet",
        "context_window": 200000,
        "max_output": 4096,
        "cost_per_1k_input": 0.003,
        "cost_per_1k_output": 0.015,
        "strengths": ["balanced", "fast", "reliable"],
        "best_for": "general content generation, balanced performance",
    },
    "anthropic.claude-3-haiku-20240307-v1:0": {
        "name": "Claude 3 Haiku",
        "context_window": 200000,
        "max_output": 4096,
        "cost_per_1k_input": 0.00025,
        "cost_per_1k_output": 0.00125,
        "strengths": ["speed", "cost_effective", "simple_tasks"],
        "best_for": "high-volume, simple content, quick responses",
    },
    "meta.llama3-1-405b-instruct-v1:0": {
        "name": "Llama 3.1 405B",
        "context_window": 128000,
        "max_output": 4096,
        "cost_per_1k_input": 0.00532,
        "cost_per_1k_output": 0.016,
        "strengths": ["open_source", "large_context", "multilingual"],
        "best_for": "complex reasoning, long documents, multilingual",
    },
    "meta.llama3-1-70b-instruct-v1:0": {
        "name": "Llama 3.1 70B",
        "context_window": 128000,
        "max_output": 4096,
        "cost_per_1k_input": 0.00099,
        "cost_per_1k_output": 0.00099,
        "strengths": ["cost_effective", "good_quality", "fast"],
        "best_for": "balanced performance and cost",
    },
    "mistral.mistral-large-2407-v1:0": {
        "name": "Mistral Large 2",
        "context_window": 128000,
        "max_output": 8192,
        "cost_per_1k_input": 0.003,
        "cost_per_1k_output": 0.009,
        "strengths": ["multilingual", "reasoning", "european"],
        "best_for": "multilingual content, European languages",
    },
}

# Recommended model selection based on use case
def get_recommended_model(use_case: str, priority: str = "quality") -> str:
    """
    Get recommended model based on use case and priority
    
    Args:
        use_case: content_generation, translation, summarization, creative_writing
        priority: quality, speed, cost, balanced
    
    Returns:
        Model ID string
    """
    recommendations = {
        "content_generation": {
            "quality": "anthropic.claude-3-opus-20240229-v1:0",
            "speed": "anthropic.claude-3-haiku-20240307-v1:0",
            "cost": "meta.llama3-1-8b-instruct-v1:0",
            "balanced": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        },
        "multilingual": {
            "quality": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "speed": "anthropic.claude-3-haiku-20240307-v1:0",
            "cost": "meta.llama3-1-70b-instruct-v1:0",
            "balanced": "anthropic.claude-3-sonnet-20240229-v1:0",
        },
        "creative_writing": {
            "quality": "anthropic.claude-3-opus-20240229-v1:0",
            "speed": "anthropic.claude-3-sonnet-20240229-v1:0",
            "cost": "meta.llama3-1-70b-instruct-v1:0",
            "balanced": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        },
        "summarization": {
            "quality": "anthropic.claude-3-sonnet-20240229-v1:0",
            "speed": "anthropic.claude-3-haiku-20240307-v1:0",
            "cost": "meta.llama3-1-8b-instruct-v1:0",
            "balanced": "anthropic.claude-3-haiku-20240307-v1:0",
        },
    }
    
    return recommendations.get(use_case, {}).get(priority, 
        "anthropic.claude-3-5-sonnet-20241022-v2:0")

# AWS Translate Configuration
TRANSLATE_REGION = os.getenv("TRANSLATE_REGION", "us-east-1")

# Supported Indian languages in AWS Translate
SUPPORTED_LANGUAGES = {
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "bengali": "bn",
    "marathi": "mr",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "punjabi": "pa",
    "urdu": "ur",
    "english": "en",
}

# AWS Transcribe Configuration
TRANSCRIBE_REGION = os.getenv("TRANSCRIBE_REGION", "us-east-1")

# AWS S3 Configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "bharat-content-ai-media")
S3_REGION = os.getenv("S3_REGION", "us-east-1")

# AWS Secrets Manager
SECRETS_MANAGER_REGION = os.getenv("SECRETS_MANAGER_REGION", "us-east-1")

# AWS EventBridge (for scheduling)
EVENTBRIDGE_REGION = os.getenv("EVENTBRIDGE_REGION", "us-east-1")

# AWS CloudWatch (for logging and monitoring)
CLOUDWATCH_REGION = os.getenv("CLOUDWATCH_REGION", "us-east-1")
CLOUDWATCH_LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/bharat-content-ai")

# Initialize AWS clients
def get_bedrock_client():
    """Get AWS Bedrock Runtime client with Bearer Token support"""
    
    # If Bearer Token is provided, use it
    if AWS_BEARER_TOKEN_BEDROCK:
        import requests
        from botocore.session import Session
        
        # Create a custom client that uses Bearer Token
        session = Session()
        client = session.create_client(
            service_name="bedrock-runtime",
            region_name=BEDROCK_REGION,
        )
        
        # Add bearer token to client
        client._request_signer._credentials = None
        
        # Monkey patch the client to add Authorization header
        original_make_request = client._make_request
        
        def make_request_with_bearer(operation_model, request_dict, request_context):
            # Add Authorization header with Bearer token
            if 'headers' not in request_dict:
                request_dict['headers'] = {}
            request_dict['headers']['Authorization'] = f'Bearer {AWS_BEARER_TOKEN_BEDROCK}'
            return original_make_request(operation_model, request_dict, request_context)
        
        client._make_request = make_request_with_bearer
        return client
    
    # Otherwise use standard IAM credentials
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=BEDROCK_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

def get_translate_client():
    """Get AWS Translate client"""
    return boto3.client(
        service_name="translate",
        region_name=TRANSLATE_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

def get_transcribe_client():
    """Get AWS Transcribe client"""
    return boto3.client(
        service_name="transcribe",
        region_name=TRANSCRIBE_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

def get_s3_client():
    """Get AWS S3 client"""
    return boto3.client(
        service_name="s3",
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

def get_secrets_manager_client():
    """Get AWS Secrets Manager client"""
    return boto3.client(
        service_name="secretsmanager",
        region_name=SECRETS_MANAGER_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

def get_eventbridge_client():
    """Get AWS EventBridge client"""
    return boto3.client(
        service_name="events",
        region_name=EVENTBRIDGE_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

def get_cloudwatch_client():
    """Get AWS CloudWatch Logs client"""
    return boto3.client(
        service_name="logs",
        region_name=CLOUDWATCH_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
