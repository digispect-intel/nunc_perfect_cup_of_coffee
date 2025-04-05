from modules.agent_config import setup_agents

def get_recommendation(preferences):
    """Get coffee recommendations based on user preferences"""
    # Get recommendation agent
    agents = setup_agents()
    recommendation_agent = agents["recommendation_agent"]
    
    # Format preferences for the agent
    preferences_str = "\n".join([f"- {key}: {value}" for key, value in preferences.items()])
    
    # Use ControlFlow to generate recommendations
    recommendation = recommendation_agent.run(f"""
    Based on these coffee preferences:
    {preferences_str}
    
    Provide a coffee recommendation with the following details in JSON format:
    - coffee_name: Name of recommended coffee
    - description: Brief description of flavor profile
    - origin: Country/region of origin
    - roast_level: Roast level
    - grind_size: Recommended grind size
    - water_temp: Recommended water temperature in Celsius
    - brewing_time: Recommended brewing time in minutes:seconds format
    - notes: Any additional brewing notes
    """)
    
    return recommendation
