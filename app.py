import json
from fasthtml.common import *
from modules.ocr import process_image, extract_coffee_info
from modules.recommender import get_recommendation
import json
import os

if "MISTRAL_API_KEY" not in os.environ:
    print("Warning: MISTRAL_API_KEY not set. ControlFlow agents will not work properly.")

app, rt = fast_app(hdrs=(
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
    Link(rel="stylesheet", href="/static/styles.css"),
    Script("""
    document.addEventListener('DOMContentLoaded', function() {
        const fileInput = document.getElementById('coffee-image');
        const previewDiv = document.getElementById('image-preview');
        const previewImg = document.getElementById('preview-img');
        const filenameDisplay = document.getElementById('filename-display');
        const form = document.getElementById('coffee-form');
        const loadingOverlay = document.getElementById('loading-overlay');
        
        if (fileInput && previewDiv && previewImg && filenameDisplay) {
            fileInput.addEventListener('change', function(e) {
                if (this.files && this.files[0]) {
                    const file = this.files[0];
                    
                    // Show the preview
                    previewDiv.classList.remove('hidden');
                    
                    // Display the image
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewImg.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                    
                    // Display the filename
                    filenameDisplay.textContent = file.name;
                } else {
                    // Hide the preview if no file selected
                    previewDiv.classList.add('hidden');
                }
            });
        }
        
        if (form && loadingOverlay) {
            form.addEventListener('submit', function() {
                loadingOverlay.classList.remove('hidden');
            });
        }
    });
    """)
))

@rt("/")
def get():
    return Titled("Next Level Coffee | nunc.", 
        Main(cls="max-w-4xl mx-auto px-4 py-8")(
            H1("Perfect Cup of Coffee", cls="title-main text-center mb-2"),
            H2("For Everyone", cls="subtitle text-center mb-6"),
            P("Find your perfect coffee match based on your taste preferences", cls="text-center mb-8 text-muted"),            
                       
            Div(id="message-container", cls="hidden bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4")(
                P(id="message-text", cls="text-center")
            ),
            
            Form(id="coffee-form", action="/process", method="post", enctype="multipart/form-data")(
                Div(cls="card rounded-lg p-6 mb-6 shadow-md")(
                    H2("Your Taste Preferences", cls="text-2xl mb-4"),
                    
                    Div(cls="mb-4")(
                        Label("Intensity:", fr="intensity", cls="block mb-2 font-bold"),
                        Select(id="intensity", name="intensity", cls="w-full p-2 border rounded bg-white")(
                            Option("Strong", value="strong"),
                            Option("Medium", value="medium", selected="selected"),
                            Option("Light", value="light")
                        )
                    ),
                    
                    Div(cls="mb-4")(
                        Label("Flavor Profile:", fr="flavor", cls="block mb-2 font-bold"),
                        Select(id="flavor", name="flavor", cls="w-full p-2 border rounded bg-white")(
                            Option("Fruity", value="fruity"),
                            Option("Bold", value="bold", selected="selected")
                        )
                    ),
                    
                    Div(cls="mb-4")(
                        Label("Acidity:", fr="acidity", cls="block mb-2 font-bold"),
                        Select(id="acidity", name="acidity", cls="w-full p-2 border rounded bg-white")(
                            Option("Sour", value="sour"),
                            Option("Bitter", value="bitter", selected="selected")
                        )
                    ),
                    
                    Div(cls="mb-6")(
                        Label("What kind of drink?", fr="drink_type", cls="block mb-2 font-bold"),
                        Select(id="drink_type", name="drink_type", cls="w-full p-2 border rounded bg-white")(
                            Option("Espresso", value="espresso", selected="selected"),
                            Option("Americano", value="americano")
                        )
                    ),
                ),
                
                Div(cls="card rounded-lg p-6 mb-6 shadow-md")(
                    H2("Or Upload a Coffee Package", cls="text-2xl mb-4"),
                    P("We'll analyze the package to recommend brewing parameters", cls="mb-4 text-sm text-muted"),
                    
                    Div(cls="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center")(
                        Input(type="file", id="coffee-image", name="coffee-image", cls="hidden", accept="image/*"),
                        Label(fr="coffee-image", cls="cursor-pointer bg-white px-4 py-2 rounded hover:bg-gray-100 font-bold")("Select Image"),
                        P("or drag and drop", cls="mt-2 text-sm text-muted")
                    ),
                    # Add this div for image preview
                    Div(id="image-preview", cls="mt-4 hidden flex flex-col items-center")(
                        Img(id="preview-img", cls="max-h-48 rounded-lg shadow-sm"),
                        P(id="filename-display", cls="mt-2 text-sm text-muted")
                    ),
                ),
                Div(id="loading-overlay", cls="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50")(
                    Div(cls="bg-white p-6 rounded-lg shadow-lg text-center")(
                        Div(cls="animate-spin rounded-full h-12 w-12 border-b-2 border-accent mx-auto"),
                        P("Analyzing your coffee image...", cls="mt-4 text-lg")
                    )
                ),

                Div(cls="mt-4")(
                    Button("Find Your Perfect Coffee", type="submit", cls="w-full btn-primary py-3 px-4 rounded font-bold text-xl")
                )
            ),
            
            Div(id="results", cls="card rounded-lg p-6 shadow-md hidden")(
                H2("Your Coffee Match", cls="text-2xl mb-4"),
                Div(id="recommendation-results")
            )
        )
    )

async def process_preferences(request):
    form = await request.form()
    intensity = form.get("intensity")
    flavor = form.get("flavor")
    acidity = form.get("acidity")
    drink_type = form.get("drink_type")
    
    return Titled("Next Level Coffee | nunc.",
        Div(cls="max-w-5xl mx-auto px-4 py-8")(
            Div(cls="flex justify-between items-center text-center mb-8")(
                # A("← Back to Home", href="/", cls="text-accent hover:underline font-bold mb-4 block"),
                H1("Perfect Cup of Coffee", cls="title-main text-center mb-2")

            ),
            H1("Your Coffee Match", cls="text-4xl text-center mb-6"),
            Div(cls="card rounded-lg p-6 shadow-md")(
                H2("Based on Your Preferences", cls="text-2xl mb-4"),
                P(f"Intensity: {intensity}", cls="text-muted"),
                P(f"Flavor Profile: {flavor}", cls="text-muted"),
                P(f"Acidity: {acidity}", cls="text-muted"),
                P(f"Drink Type: {drink_type}", cls="text-muted"),
                
                Div(cls="mt-6 p-4 bg-white rounded-lg border border-gray-200")(
                    H3("Recommended Coffee", cls="font-bold mb-2"),
                    P("Ethiopian Yirgacheffe", cls="text-lg"),
                    P("Light roast, fruity with citrus notes", cls="text-sm text-muted"),
                    
                    H3("Brewing Parameters", cls="font-bold mt-4 mb-2"),
                    P("Grind Size: Medium-fine", cls="text-muted"),
                    P("Water Temperature: 92°C", cls="text-muted"),
                    P("Brewing Time: 2:30 minutes", cls="text-muted")
                ),
                
                Div(cls="mt-6")(
                    A("← Back to Home", href="/", cls="text-accent hover:underline font-bold")
                )
            )
        )
    )


def parse_agent_response(response_text):
    """Parse JSON from agent response text, with basic error handling
    
    Args:
        response_text (str): The text response from the agent
        
    Returns:
        dict: Parsed JSON as a dictionary, or empty dict if parsing fails
    """
    # Handle None response
    if response_text is None:
        print("Warning: Received None response from agent")
        return {}
        
    try:
        # Try to find JSON in the response
        # Look for content between curly braces
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        
        # If no JSON found, try the whole text
        return json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from: {response_text}")
        return {}

async def analyze_image(request):
    form = await request.form()
    
    # Get user preferences from the form
    intensity = form.get("intensity", "medium")
    flavor = form.get("flavor", "balanced")
    acidity = form.get("acidity", "balanced")
    drink_type = form.get("drink_type", "espresso")
    
    # Collect user preferences
    preferences = {
        "intensity": intensity,
        "flavor": flavor,
        "acidity": acidity,
        "drink_type": drink_type
    }
    
    image_file = form.get("coffee-image")
    image_url = None
    
    # Save the image temporarily
    if image_file and hasattr(image_file, "filename") and image_file.filename:
        import os
        import uuid
        from modules.vision import analyze_coffee_image
        
        # Create a unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())[:8]
        original_filename = image_file.filename
        image_filename = f"{unique_id}_{original_filename}"
        
        # Ensure directory exists
        os.makedirs("static/uploads", exist_ok=True)
        
        # Full path to save the image
        save_path = f"static/uploads/{image_filename}"
        
        # Read and save the image
        with open(save_path, "wb") as f:
            content = await image_file.read()
            f.write(content)
        
        # Process image using vision model
        coffee_info = analyze_coffee_image(save_path)
        parsed_coffee_info = parse_agent_response(coffee_info)

        recommendation = get_recommendation(preferences, parsed_coffee_info)
        parsed_recommendation = parse_agent_response(recommendation)
        
        # Set the image URL for display
        image_url = f"/static/uploads/{image_filename}"
        
        return create_results_page(parsed_coffee_info, parsed_recommendation, image_url)
    else:
        # Handle case when no image is provided
        return Titled("Error",
            Div(cls="max-w-4xl mx-auto px-4 py-8")(
                H1("Error", cls="text-4xl text-center mb-6"),
                P("No image was provided. Please upload a coffee package image.", cls="text-center")
            )
        )

def create_results_page(coffee_info, recommendation, image_url=None):
    """Create a results page from coffee info and recommendations"""
    return Titled("Next Level Coffee | nunc.",
        Div(cls="max-w-4xl mx-auto px-4 py-8")(
            Div(cls="flex justify-between items-center mb-8")(
                H1("Perfect Cup of Coffee", cls="title-main text-center")
            ),
            H1("Coffee Package Analysis", cls="text-4xl text-center mb-6"),
            Div(cls="card rounded-lg p-6 shadow-md")(
                H2("Detected Coffee Information", cls="text-2xl mb-4"),
                # Add image display if available
                Div(cls="mb-6 text-center" if image_url else "hidden")(
                    Img(src=image_url, cls="max-h-64 mx-auto rounded-lg shadow-md")
                ) if image_url else "",
                Div(cls="mt-6 p-4 bg-white rounded-lg border border-gray-200")(
                    H3("Package Details", cls="font-bold mb-2"),
                    P(f"Origin: {coffee_info.get('origin', 'Unknown')}", cls="text-muted"),
                    P(f"Roast Level: {coffee_info.get('roast_level', 'Unknown')}", cls="text-muted"),
                    P(f"Variety: {coffee_info.get('variety', 'Unknown')}", cls="text-muted"),
                    P(f"Process: {coffee_info.get('process', 'Unknown')}", cls="text-muted"),
                    
                    H3("Recommended Brewing Parameters", cls="font-bold mt-4 mb-2"),
                    P(f"Flow Rate: {recommendation.get('flow_rate', 'Unknown')}", cls="text-muted"),
                    P(f"Brewing Temperature: {recommendation.get('brewing_temp', 'Unknown')}°C", cls="text-muted"),
                    P(f"Grind Setting: {recommendation.get('grind_setting', 'Unknown')}", cls="text-muted"),
                    P(f"Brew Ratio: {recommendation.get('brew_ratio', 'Unknown')}", cls="text-muted"),
                    P(f"Brewing Time: {recommendation.get('brewing_time', 'Unknown')} seconds", cls="text-muted"),
                    
                    H3("Tasting Notes", cls="font-bold mt-4 mb-2"),
                    P(recommendation.get('description', 'No description available'), cls="text-muted"),
                    P(recommendation.get('notes', ''), cls="text-muted mt-2 italic")
                ),
                
                Div(cls="mt-6")(
                    A("← Back to Home", href="/", cls="text-accent hover:underline font-bold")
                )
            )
        )
    )


@rt("/process", methods=["POST"])
async def post(request):
    form = await request.form()
    
    # Check if image was uploaded
    has_image = False
    if "coffee-image" in form and hasattr(form["coffee-image"], "filename") and form["coffee-image"].filename:
        has_image = True
    
    # Check if all taste preferences are empty (shouldn't happen with select boxes)
    intensity = form.get("intensity")
    flavor = form.get("flavor")
    acidity = form.get("acidity")
    drink_type = form.get("drink_type")
    has_preferences = intensity or flavor or acidity or drink_type
    
    # If nothing provided, use default
    if not has_image and not has_preferences:
        return Titled("Coffee Recommendation Results",
            Div(cls="container max-w-3xl mx-auto px-4 py-8")(
                Div(cls="flex justify-between items-center mb-8")(
                    H1("nunc.", cls="title-main text-left"),
                    H2("Perfect Cup of Coffee", cls="title-main text-center text-lg font-bold")
                ),
                H1("Your Coffee Match", cls="text-4xl text-center mb-6"),
                Div(cls="card rounded-lg p-6 shadow-md")(
                    H2("Default Standard", cls="text-2xl mb-4"),
                    P("Using our default recommendations since no preferences were provided.", cls="text-muted mb-4"),
                    
                    Div(cls="mt-6 p-4 bg-white rounded-lg border border-gray-200")(
                        H3("Recommended Coffee", cls="font-bold mb-2"),
                        P("House Blend", cls="text-lg"),
                        P("Medium roast, balanced flavor profile", cls="text-sm text-muted"),
                        
                        H3("Brewing Parameters", cls="font-bold mt-4 mb-2"),
                        P("Grind Size: Medium", cls="text-muted"),
                        P("Water Temperature: 93°C", cls="text-muted"),
                        P("Brewing Time: 3:00 minutes", cls="text-muted")
                    ),
                    
                    Div(cls="mt-6")(
                        A("← Back to Home", href="/", cls="text-accent hover:underline font-bold")
                    )
                )
            )
        )
    
    # Process based on image if available
    if has_image:
        return await analyze_image(request)
    
    # Otherwise process based on preferences
    return await process_preferences(request)

serve()
