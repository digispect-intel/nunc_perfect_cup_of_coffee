from modules.agent_config import setup_agents

def get_recommendation(preferences, coffee_info=None):
    """Get coffee recommendations based on user preferences and coffee information
    
    Args:
        preferences (dict): User taste preferences (intensity, flavor, acidity, drink_type)
        coffee_info (dict, optional): Coffee information extracted from package image
        
    Returns:
        dict: Detailed brewing recommendations
    """
    # Get recommendation agent
    agents = setup_agents()
    recommendation_agent = agents["recommendation_agent"]
    
    # Format preferences for the agent
    preferences_str = "\n".join([f"- {key}: {value}" for key, value in preferences.items()])
    
    # Add coffee information if available
    coffee_info_str = ""
    if coffee_info:
        coffee_info_str = "\nCoffee Information:\n" + "\n".join([f"- {key}: {value}" for key, value in coffee_info.items()])
    
    # Use ControlFlow to generate recommendations
    recommendation = recommendation_agent.run(f"""
    Based on these coffee preferences:
    {preferences_str}
    {coffee_info_str}
    
    Provide a coffee recommendation with the following details in JSON format:
    - coffee_name: Name of recommended coffee
    - description: Brief description of flavor profile
    - origin: Country/region of origin
    - roast_level: Roast level
    
    And include these specific brewing parameters:
    - flow_rate: Recommended flow rate or pressure profile for the espresso shot
    - brewing_temp: Recommended brewing temperature in Celsius
    - grind_setting: Recommended grind setting using 120 μm of "BAR ITALIA" as the reference point
    - brew_ratio: The ratio of ground coffee to total water used (e.g., "1:2" for 18g coffee to 36g water)
    - brewing_time: Recommended brewing time in seconds
    - notes: Any additional brewing notes or tips
    
    Take into account the coffee origin, roast level, and user's taste preferences to provide accurate recommendations.
    """)
    
    return recommendation
