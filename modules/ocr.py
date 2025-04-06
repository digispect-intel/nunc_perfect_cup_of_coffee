import json
import os
import base64
from mistralai import Mistral
from modules.agent_config import setup_agents
from pydantic import BaseModel, Field
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from pydantic import BaseModel, Field
from typing import Optional, List

class CoffeeInfo(BaseModel):
    origin: str = Field(default="Unknown", description="Country or region of origin of the coffee")
    roast_level: str = Field(default="Medium", description="Roast level (Light, Medium, Medium-Dark, Dark)")
    variety: str = Field(default="Arabica", description="Coffee variety (e.g., Arabica, Robusta)")
    process: str = Field(default="Washed", description="Processing method (e.g., Washed, Natural, Honey)")
    tasting_notes: List[str] = Field(default_factory=list, description="Flavor notes mentioned on package")


def extract_coffee_info(ocr_result):
    """Extract coffee information using ControlFlow"""
    try:
        # Get our agents
        agents = setup_agents()
        ocr_agent = agents["ocr_agent"]
        
        # Create a prompt for the OCR agent
        prompt = f"""
        Extract coffee information from the following text:
        
        {ocr_result}
        
        Analyze the text and identify the following details about the coffee:
        - The country or region of origin
        - The roast level (Light, Medium, Dark)
        - The coffee bean variety (Arabica, Robusta)
        - The processing method (Washed, Natural, Honey)
        - Any flavor notes or tasting notes mentioned
        
        If any information is not found in the text, make a reasonable guess based on other available information.
        """
        
        # Use ControlFlow to extract structured information
        coffee_info = ocr_agent.run(prompt, result_type=CoffeeInfo)
        
        # Return as JSON string for compatibility with existing code
        return coffee_info.model_dump_json()
        
    except Exception as e:
        print(f"Error extracting coffee info: {e}")
        # Return default values if extraction fails
        return CoffeeInfo().model_dump_json()


def extract_text_with_mistral_ocr(image_path):
    """Extract text from an image using Mistral OCR"""
    # Initialize Mistral client
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    
    client = Mistral(api_key=api_key)
    
    # Check if image_path is a URL or a local file
    if image_path.startswith(('http://', 'https://')):
        # Process image from URL
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": image_path
            }
        )
    else:
        # Encode local image to base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Process image from base64
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            }
        )
    
    # Return the extracted text
    return ocr_response.text


def process_image(image_path):
    """Process an image using Mistral OCR and extract coffee information"""
    try:
        # First, try to extract text from the image using Mistral OCR
        import os
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is required")
        
        client = Mistral(api_key=api_key)
        
        # Encode local image to base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Process image from base64
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            }
        )
        
        print(f"OCR Response: {ocr_response}")
        
        # Extract text from OCR response
        raw_text = ""
        if hasattr(ocr_response, 'text'):
            raw_text = ocr_response.text
        elif hasattr(ocr_response, 'pages') and ocr_response.pages:
            for page in ocr_response.pages:
                if hasattr(page, 'content') and page.content:
                    raw_text += page.content + "\n"
                elif hasattr(page, 'text') and page.text:
                    raw_text += page.text + "\n"
                elif hasattr(page, 'markdown') and page.markdown:
                    raw_text += page.markdown + "\n"
        
        # If we couldn't extract enough text, add some context
        if not raw_text or len(raw_text.strip()) < 10:
            raw_text = "This is a coffee package image. Please extract information about the coffee based on the image filename and your knowledge of coffee."
            
        # Add the filename which might contain useful information
        import os
        filename = os.path.basename(image_path)
        raw_text += f"\n\nFilename: {filename}"
        
        # Now use extract_coffee_info to process the text
        return extract_coffee_info(raw_text)
        
    except Exception as e:
        print(f"Error processing image: {e}")
        # Return default values if processing fails
        return CoffeeInfo().model_dump_json()
