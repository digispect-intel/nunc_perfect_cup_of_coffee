from modules.agent_config import setup_agents
from pydantic import Field, BaseModel
from typing import Optional

import json

def get_recommendation(preferences, coffee_info=None):
    """Get coffee recommendations based on user preferences and coffee information
    
    Args:
        preferences (dict): User taste preferences (intensity, flavor, acidity, drink_type)
        coffee_info (dict, optional): Coffee information extracted from package image
        
    Returns:
        dict: Detailed brewing recommendations
    """
    try:
        # Get recommendation agent
        agents = setup_agents()
        recommendation_agent = agents["recommendation_agent"]
        
        # Format preferences for the agent
        preferences_str = "\n".join([f"- {key}: {value}" for key, value in preferences.items()])
        
        # Add coffee information if available
        coffee_info_str = ""
        if coffee_info:
            coffee_info_str = "\nCoffee Information:\n" + "\n".join([f"- {key}: {value}" for key, value in coffee_info.items()])
        
        # Create a structured output model
        class BrewingRecommendation(BaseModel):
            coffee_name: str = Field(description="Name of recommended coffee")
            description: str = Field(description="Brief description of flavor profile")
            origin: str = Field(description="Country/region of origin")
            roast_level: str = Field(description="Roast level")
            flow_rate: str = Field(description="Recommended flow rate or pressure profile")
            brewing_temp: int = Field(description="Recommended brewing temperature in Celsius")
            grind_setting: str = Field(description="Recommended grind setting")
            brew_ratio: str = Field(description="Ratio of ground coffee to total water used")
            brewing_time: int = Field(description="Recommended brewing time in seconds")
            notes: Optional[str] = Field(None, description="Additional brewing notes or tips")
        
        # Use ControlFlow to generate recommendations with a user message
        prompt = f"""
        Based on these coffee preferences:
        {preferences_str}
        {coffee_info_str}
        
        Provide a coffee recommendation with brewing parameters tailored to these preferences.
        Take into account the coffee origin, roast level, and user's taste preferences to provide accurate recommendations.
        """
        
        recommendation = recommendation_agent.run(prompt, result_type=BrewingRecommendation)
        
        # Convert to dictionary for JSON serialization
        result = recommendation.model_dump()
        return json.dumps(result)
        
    except Exception as e:
        print(f"Error generating recommendation: {e}")
        # Return a default recommendation if there's an error
        default_recommendation = {
            "coffee_name": "House Blend",
            "description": "A balanced, medium roast coffee with notes of chocolate and nuts",
            "origin": "Brazil",
            "roast_level": "Medium",
            "flow_rate": "Steady 2ml/s",
            "brewing_temp": 93,
            "grind_setting": "Medium (120 μm)",
            "brew_ratio": "1:2",
            "brewing_time": 28,
            "notes": "For a stronger flavor, try a slightly finer grind."
        }
        return json.dumps(default_recommendation)
