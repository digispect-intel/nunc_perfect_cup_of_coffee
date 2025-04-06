import os
import base64
from mistralai import Mistral
from pydantic import BaseModel, Field
from typing import List, Optional

# Define a Pydantic model for coffee information
class CoffeeInfo(BaseModel):
    origin: str = Field(default="Unknown", description="Country or region of origin of the coffee")
    roast_level: str = Field(default="Medium", description="Roast level (Light, Medium, Dark)")
    variety: str = Field(default="Arabica", description="Coffee variety (e.g., Arabica, Robusta)")
    process: str = Field(default="Washed", description="Processing method (e.g., Washed, Natural, Honey)")
    tasting_notes: List[str] = Field(default_factory=list, description="Flavor notes mentioned on package")

def analyze_coffee_image(image_path):
    """Analyze a coffee package image using Mistral Vision model"""
    try:
        # Initialize Mistral client
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is required")
        
        client = Mistral(api_key=api_key)
        
        # Encode image to base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Create the messages for the vision model
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analyze this coffee package image and extract the following information:
                        1. Origin: The country or region where the coffee was grown
                        2. Roast Level: How dark the coffee is roasted (Light, Medium, Dark)
                        3. Variety: The type of coffee bean (e.g., Arabica, Robusta)
                        4. Process: How the coffee was processed (e.g., Washed, Natural, Honey)
                        5. Tasting Notes: Any flavor descriptors mentioned
                        
                        Format your response as JSON with the following fields:
                        {
                            "origin": "country name",
                            "roast_level": "Light/Medium/Dark",
                            "variety": "bean type",
                            "process": "processing method",
                            "tasting_notes": ["note1", "note2", ...]
                        }
                        
                        If you can't determine any field with certainty, use a reasonable default value.
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ]
        
        # Get the response from the vision model
        response = client.chat.complete(
            model="mistral-small-latest",  # Using Small model with vision capabilities
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        # Extract the JSON response
        json_response = response.choices[0].message.content
        
        # Parse into CoffeeInfo model and return as JSON
        import json
        coffee_data = json.loads(json_response)
        coffee_info = CoffeeInfo(**coffee_data)
        
        return coffee_info.model_dump_json()
        
    except Exception as e:
        print(f"Error analyzing coffee image: {e}")
        # Return default values if analysis fails
        return CoffeeInfo().model_dump_json()
