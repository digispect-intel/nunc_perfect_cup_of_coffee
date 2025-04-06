from modules.agent_config import setup_agents
from pydantic import Field, BaseModel
from typing import Optional, Dict, Any, List, Tuple
import json

class CoffeePreferences(BaseModel):
    intensity: str = Field(description="Preferred coffee intensity (strong, medium, light)")
    flavor_profile: str = Field(description="Preferred flavor profile (fruity, bold, balanced)")
    acidity: str = Field(description="Preferred acidity level (sour, bitter, balanced)")
    drink_type: str = Field(description="Type of coffee drink (espresso, americano, etc.)")
    notes: Optional[str] = Field(None, description="Any additional preference notes")

class CoffeeKnowledgeBase:
    """Knowledge base for coffee brewing parameters based on coffee characteristics"""
    
    # Origin-based temperature recommendations
    origin_temp_map = {
        "ethiopia": {"min_temp": 91, "max_temp": 94, "notes": "Ethiopian coffees often benefit from higher temperatures to highlight floral and fruity notes"},
        "colombia": {"min_temp": 90, "max_temp": 93, "notes": "Colombian coffees extract well at standard temperatures"},
        "brazil": {"min_temp": 88, "max_temp": 92, "notes": "Brazilian coffees often have chocolate notes that develop at slightly lower temperatures"},
        "kenya": {"min_temp": 92, "max_temp": 95, "notes": "Kenyan coffees are often bright and acidic, benefiting from higher temperatures"},
        "guatemala": {"min_temp": 89, "max_temp": 93, "notes": "Guatemalan coffees have balanced acidity and body that develops well at medium temperatures"},
        "costa rica": {"min_temp": 90, "max_temp": 93, "notes": "Costa Rican coffees are often clean with bright acidity, extracting well at medium-high temperatures"}
    }
    
    # Roast level brewing parameters
    roast_params = {
        "light": {
            "temp_range": (92, 96),
            "grind_offset": -5,  # Finer than reference point
            "brew_ratio": "1:2.5",
            "flow_rate": "slow start, gradual increase",
            "notes": "Light roasts need higher temperatures and finer grinds to properly extract"
        },
        "medium": {
            "temp_range": (90, 94),
            "grind_offset": 0,  # At reference point
            "brew_ratio": "1:2",
            "flow_rate": "standard profile",
            "notes": "Medium roasts work well with standard parameters"
        },
        "dark": {
            "temp_range": (88, 92),
            "grind_offset": 5,  # Coarser than reference point
            "brew_ratio": "1:1.5",
            "flow_rate": "fast start, declining pressure",
            "notes": "Dark roasts extract more easily and benefit from lower temperatures"
        }
    }
    
    # Flavor profile adjustments
    flavor_adjustments = {
        "fruity": {"temp_offset": 1, "grind_offset": -2, "flow_rate": "slower start, gradual increase"},
        "bold": {"temp_offset": -1, "grind_offset": 2, "flow_rate": "high pressure throughout"},
        "balanced": {"temp_offset": 0, "grind_offset": 0, "flow_rate": "standard pressure profile"},
        "sweet": {"temp_offset": -1, "grind_offset": -1, "flow_rate": "medium pressure, extended pre-infusion"},
        "chocolatey": {"temp_offset": -2, "grind_offset": 1, "flow_rate": "high pressure start, gradual decline"}
    }
    
    # Processing method influences
    process_influences = {
        "washed": {"clarity": "high", "body": "medium", "acidity_boost": 1},
        "natural": {"clarity": "medium", "body": "full", "acidity_boost": -1},
        "honey": {"clarity": "medium-high", "body": "medium-full", "acidity_boost": 0}
    }
    
    # Reference points
    reference = {
        "grind_setting": 120,  # μm, BAR ITALIA reference point
        "base_temp": 93,       # Celsius
        "base_ratio": "1:2",   # Coffee to water ratio
        "base_time": 28        # Seconds for standard shot
    }
    
    def calculate_parameters(self, coffee_info: Dict[str, Any], preferences: Dict[str, str]) -> Dict[str, Any]:
        """Calculate brewing parameters based on coffee info and user preferences"""
        
        # Start with default values
        brewing_temp = self.reference["base_temp"]
        grind_setting = self.reference["grind_setting"]
        brew_ratio = self.reference["base_ratio"]
        flow_rate = "standard profile"
        brewing_time = self.reference["base_time"]
        
        # Adjust based on roast level
        if coffee_info and 'roast_level' in coffee_info:
            roast = coffee_info['roast_level'].lower()
            for key in self.roast_params:
                if key in roast:
                    roast_data = self.roast_params[key]
                    brewing_temp = (roast_data["temp_range"][0] + roast_data["temp_range"][1]) / 2
                    grind_setting += roast_data["grind_offset"]
                    brew_ratio = roast_data["brew_ratio"]
                    flow_rate = roast_data["flow_rate"]
                    break
        
        # Adjust based on origin
        if coffee_info and 'origin' in coffee_info:
            origin = coffee_info['origin'].lower()
            for key in self.origin_temp_map:
                if key in origin:
                    origin_data = self.origin_temp_map[key]
                    origin_temp = (origin_data["min_temp"] + origin_data["max_temp"]) / 2
                    # Blend with existing temp recommendation
                    brewing_temp = (brewing_temp + origin_temp) / 2
                    break
        
        # Adjust based on processing method
        if coffee_info and 'process' in coffee_info:
            process = coffee_info['process'].lower()
            for key in self.process_influences:
                if key in process:
                    process_data = self.process_influences[key]
                    # Adjust acidity based on process
                    if process_data["acidity_boost"] > 0:
                        brewing_temp += 1  # Higher temp for more acidity
                    elif process_data["acidity_boost"] < 0:
                        brewing_temp -= 1  # Lower temp for less acidity
                    break
        
        # Fine-tune based on user preferences
        if 'flavor_profile' in preferences:
            flavor = preferences['flavor_profile'].lower()
            for key in self.flavor_adjustments:
                if key in flavor:
                    flavor_data = self.flavor_adjustments[key]
                    brewing_temp += flavor_data["temp_offset"]
                    grind_setting += flavor_data["grind_offset"]
                    flow_rate = flavor_data["flow_rate"]
                    break
        
        # Adjust for intensity preference
        if 'intensity' in preferences:
            intensity = preferences['intensity'].lower()
            if 'strong' in intensity:
                grind_setting -= 3  # Finer grind for stronger coffee
                brew_ratio = "1:1.5"  # Less water for stronger coffee
            elif 'light' in intensity:
                grind_setting += 3  # Coarser grind for lighter coffee
                brew_ratio = "1:2.5"  # More water for lighter coffee
        
        # Adjust for acidity preference
        if 'acidity' in preferences:
            acidity = preferences['acidity'].lower()
            if 'sour' in acidity:
                brewing_temp += 2  # Higher temp to enhance acidity
            elif 'bitter' in acidity:
                brewing_temp -= 2  # Lower temp to reduce bitterness
        
        # Ensure parameters are within reasonable bounds
        brewing_temp = max(88, min(96, brewing_temp))
        grind_setting = max(100, min(140, grind_setting))
        
        # Return calculated parameters
        return {
            "brewing_temp": int(brewing_temp),
            "grind_setting": int(grind_setting),
            "brew_ratio": brew_ratio,
            "flow_rate": flow_rate,
            "brewing_time": brewing_time
        }

class BrewingRecommendation(BaseModel):
    coffee_name: str = Field(description="Name of recommended coffee")
    description: str = Field(description="Brief description of flavor profile")
    origin: str = Field(description="Country/region of origin")
    roast_level: str = Field(description="Roast level")
    flow_rate: str = Field(description="Recommended flow rate or pressure profile")
    brewing_temp: int = Field(description="Recommended brewing temperature in Celsius")
    grind_setting: int = Field(description="Recommended grind setting in μm")
    brew_ratio: str = Field(description="Ratio of ground coffee to total water used")
    brewing_time: int = Field(description="Recommended brewing time in seconds")
    notes: Optional[str] = Field(None, description="Additional brewing notes or tips")

def get_recommendation(preferences, coffee_info=None, history=None):
    """Get coffee recommendations based on user preferences and coffee information
    
    Args:
        preferences (dict): User taste preferences (intensity, flavor_profile, acidity, drink_type)
        coffee_info (dict, optional): Coffee information extracted from package image
        history (list, optional): Previous user preferences and recommendations
        
    Returns:
        dict: Detailed brewing recommendations
    """
    try:
        # Print debug information
        print(f"Generating recommendation with preferences: {preferences}")
        if coffee_info:
            print(f"Coffee info provided: {coffee_info}")
        if history:
            print(f"User has {len(history)} previous recommendations")
        
        # Get recommendation agent
        agents = setup_agents()
        recommendation_agent = agents["recommendation_agent"]
        
        # Initialize knowledge base
        kb = CoffeeKnowledgeBase()
        
        # Calculate initial parameters from knowledge base
        calculated_params = kb.calculate_parameters(coffee_info, preferences)
        
        # Format preferences for the agent
        preferences_str = "\n".join([f"- {key}: {value}" for key, value in preferences.items()])
        
        # Add coffee information if available
        coffee_info_str = ""
        if coffee_info:
            coffee_info_str = "\nCoffee Information:\n" + "\n".join([f"- {key}: {value}" for key, value in coffee_info.items()])
        
        # Add calculated parameters to context
        params_str = "\nCalculated Parameters:\n" + "\n".join([f"- {key}: {value}" for key, value in calculated_params.items()])
        
        # Add history context if available
        history_context = ""
        if history and len(history) > 0:
            history_context = "\nUser History:\n"
            for i, entry in enumerate(history[-3:]):  # Use last 3 entries
                rec = entry.get('recommendation', {})
                pref = entry.get('preferences', {})
                feedback = entry.get('feedback', 'unknown')
                comments = entry.get('feedback_comments', '')
                
                history_context += f"- Previous recommendation {i+1}: {rec.get('coffee_name', 'Unknown')} "
                history_context += f"(Origin: {rec.get('origin', 'Unknown')}, "
                history_context += f"Roast: {rec.get('roast_level', 'Unknown')})\n"
                history_context += f"  User preferences: {pref.get('intensity', '')}, {pref.get('flavor_profile', '')}, {pref.get('acidity', '')}\n"
                history_context += f"  User feedback: {feedback}\n"
                if comments:
                    history_context += f"  User comments: \"{comments}\"\n"
        
        # Adjust for origin preference if specified
        origin_context = ""
        if preferences.get('origin_preference') and preferences.get('origin_preference') != 'any':
            origin_pref = preferences.get('origin_preference')
            origin_mapping = {
                'african': "African coffees like Ethiopian, Kenyan, or Rwandan that are known for bright acidity and fruity notes",
                'latin_american': "Latin American coffees like Colombian, Costa Rican, or Guatemalan that are known for balance and chocolate notes",
                'asian_pacific': "Asian/Pacific coffees like Sumatran, Indonesian, or Vietnamese that are known for earthy, spicy notes and full body"
            }
            if origin_pref in origin_mapping:
                origin_context = f"\nUser has expressed preference for {origin_mapping[origin_pref]}."
        
        # Use ControlFlow to generate recommendations with a user message
        prompt = f"""
        Based on these coffee preferences:
        {preferences_str}
        {coffee_info_str}
        {params_str}
        {history_context}
        {origin_context}
        
        Provide a coffee recommendation with brewing parameters tailored to these preferences.
        Take into account the coffee origin, roast level, and user's taste preferences to provide accurate recommendations.
        Use the calculated parameters as a starting point but feel free to adjust them based on your expertise.
        
        If the user has provided feedback on previous recommendations, use this to refine your recommendation.
        Pay special attention to any detailed comments the user has provided about previous recommendations.
        Positive feedback suggests similar coffees, while negative feedback suggests trying different characteristics.
        """
        
        # Create a structured output model
        recommendation = recommendation_agent.run(prompt, result_type=BrewingRecommendation)
        
        # Convert to dictionary for JSON serialization
        result = recommendation.model_dump()
        
        # Print the final recommendation for debugging
        print(f"Generated recommendation: {result}")
        
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
            "grind_setting": 120,
            "brew_ratio": "1:2",
            "brewing_time": 28,
            "notes": "For a stronger flavor, try a slightly finer grind."
        }
        return json.dumps(default_recommendation)
