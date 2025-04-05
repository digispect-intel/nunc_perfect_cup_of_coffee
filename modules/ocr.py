import json
import controlflow as cf
import os
import base64
from mistralai import Mistral
from modules.agent_config import setup_agents

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
    """Process an image using Mistral OCR and enhance with ControlFlow"""
    try:
        # Initialize Mistral client
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
        
        # Let's print the entire response structure
        print(f"OCR Response: {ocr_response}")
        
        # Try to extract text from pages
        raw_text = ""
        if hasattr(ocr_response, 'pages') and ocr_response.pages:
            # Combine text from all pages
            for page in ocr_response.pages:
                if hasattr(page, 'content'):
                    raw_text += page.content + "\n"
                elif hasattr(page, 'text'):
                    raw_text += page.text + "\n"
        
        # If we couldn't extract text, use the string representation
        if not raw_text:
            raw_text = str(ocr_response)
        
        return raw_text
    except Exception as e:
        print(f"Error processing image: {e}")
        return json.dumps({"error": f"OCR processing failed: {str(e)}"})

def extract_coffee_info(ocr_result):
    """Parse the structured information from OCR result"""
    try:
        # Simple text-based extraction without ControlFlow
        info = {
            "origin": "Unknown",
            "roast_level": "Medium",
            "variety": "Arabica",
            "process": "Washed"
        }
        
        # Check if ocr_result is valid
        if isinstance(ocr_result, str) and len(ocr_result) > 10:
            # Simple text-based extraction
            text = ocr_result.lower()
            
            # Extract origin
            origins = ["colombia", "ethiopia", "brazil", "kenya", "guatemala", "costa rica"]
            for origin in origins:
                if origin in text:
                    info["origin"] = origin.title()
                    break
            
            # Extract roast level
            if "light roast" in text or "light-roast" in text:
                info["roast_level"] = "Light"
            elif "dark roast" in text or "dark-roast" in text:
                info["roast_level"] = "Dark"
            
            # Extract variety
            if "robusta" in text:
                info["variety"] = "Robusta"
            
            # Extract process
            if "natural" in text or "dry process" in text:
                info["process"] = "Natural"
            elif "honey" in text or "honey process" in text:
                info["process"] = "Honey"
        
        return json.dumps(info)
    except Exception as e:
        print(f"Error extracting coffee info: {e}")
        return json.dumps({"error": f"Information extraction failed: {str(e)}"})
