import controlflow as cf
from langchain_mistralai import ChatMistralAI
import os

def setup_agents():
    # Make sure you have your API key set in environment variables
    if "MISTRAL_API_KEY" not in os.environ:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    
    # Create the Mistral model instances with specific configurations
    mistral_large = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.3,
        max_tokens=1024
    )
    
    mistral_small = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.3,
        max_tokens=1024
    )
    
    # Configure default model to use MistralAI
    cf.defaults.model = mistral_large
    
    # Create agents with specific configurations
    recommendation_agent = cf.Agent(
        name="CoffeeRecommender",
        description="Recommends coffee based on user preferences",
        model=mistral_large
    )
    
    # We'll keep the OCR agent for text processing if needed
    ocr_agent = cf.Agent(
        name="OCRProcessor",
        description="Processes text to extract coffee information",
        model=mistral_small
    )
    
    return {
        "recommendation_agent": recommendation_agent,
        "ocr_agent": ocr_agent
    }
