import controlflow as cf
from langchain_mistralai import ChatMistralAI
import os

# Set MistralAI as the default model provider
def setup_agents():
    # Make sure you have your API key set in environment variables
    if "MISTRAL_API_KEY" not in os.environ:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    
    # Configure default model to use MistralAI
    cf.defaults.model = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.3
    )
    
    # Create a recommendation agent
    recommendation_agent = cf.Agent(
        name="CoffeeRecommender",
        description="Recommends coffee based on user preferences"
    )
    
    # Create an OCR agent with specific model
    ocr_agent = cf.Agent(
        name="OCRProcessor",
        description="Processes coffee package images and extracts information",
        model="mistral/mistral-small" # Using a smaller model for OCR tasks
    )
    
    return {
        "recommendation_agent": recommendation_agent,
        "ocr_agent": ocr_agent
    }
