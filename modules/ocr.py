import controlflow as cf
from PIL import Image
import pytesseract
import os
from modules.agent_config import setup_agents

def process_image(image_path):
    """Process an image using pytesseract OCR and enhance with MistralAI"""
    # Basic OCR with pytesseract
    try:
        img = Image.open(image_path)
        raw_text = pytesseract.image_to_string(img)
        
        # Get OCR agent
        agents = setup_agents()
        ocr_agent = agents["ocr_agent"]
        
        # Use ControlFlow agent to enhance OCR results
        enhanced_result = ocr_agent.run(f"""
        I have extracted text from a coffee package using OCR. 
        The raw extracted text is:
        {raw_text}
        
        Please identify and extract the following information in JSON format:
        - Country/Origin
        - Roast Level (Light, Medium, Dark)
        - Variety (Arabica, Robusta, etc.)
        - Process (Washed, Natural, Honey, etc.)
        
        If any information is missing, indicate with "Unknown".
        """)
        
        return enhanced_result
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def extract_coffee_info(ocr_result):
    """Parse the structured information from OCR result"""
    # Get recommendation agent
    agents = setup_agents()
    recommendation_agent = agents["recommendation_agent"]
    
    # Use ControlFlow to extract structured information
    coffee_info = recommendation_agent.run(f"""
    Based on this OCR result from a coffee package: 
    {ocr_result}
    
    Extract and return a JSON object with these fields:
    - origin: The country or region of origin
    - roast_level: Light, Medium, or Dark
    - variety: Type of coffee bean
    - process: Processing method
    - recommended_grind: Recommended grind size
    - recommended_temp: Recommended water temperature in Celsius
    - recommended_time: Recommended brewing time in minutes:seconds format
    
    Use your knowledge of coffee to fill in reasonable recommendations for brewing parameters.
    """)
    
    return coffee_info
