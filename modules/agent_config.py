import controlflow as cf
from langchain_mistralai import ChatMistralAI
import os

# Set MistralAI as the default model provider
def setup_agents():
    # Make sure you have your API key set in environment variables
    if "MISTRAL_API_KEY" not in os.environ:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    
    # Create the Mistral model instances directly
    mistral_large = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.3
    )
    
    mistral_small = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.3
    )
    
    # Configure default model to use MistralAI
    cf.defaults.model = mistral_large
    
    # Create a recommendation agent
    recommendation_agent = cf.Agent(
        name="CoffeeRecommender",
        description="Recommends coffee based on user preferences",
        model=mistral_large
    )
    
    # Create an OCR agent with specific model
    ocr_agent = cf.Agent(
        name="OCRProcessor",
        description="Processes coffee package images and extracts information",
        model=mistral_small
    )
    
    return {
        "recommendation_agent": recommendation_agent,
        "ocr_agent": ocr_agent
    }
