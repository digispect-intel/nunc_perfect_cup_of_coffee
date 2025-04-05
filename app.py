from fasthtml.common import *
from modules.ocr import process_image, extract_coffee_info


app, rt = fast_app(hdrs=(
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),
))

@rt("/")
def get():
    return Titled("Coffee Recommender", 
        Main(cls="max-w-3xl mx-auto px-4 py-8")(
            H1("AI Coffee Recommender", cls="text-3xl font-bold text-center mb-6"),
            P("Find your perfect coffee match based on your taste preferences", cls="text-center mb-8"),
            
            # Preference Form
            Div(cls="bg-amber-50 rounded-lg p-6 mb-6 shadow-md")(
                H2("Your Taste Preferences", cls="text-xl font-semibold mb-4"),
                Form(id="preference-form", action="/recommend", method="post")(
                    # Taste Profile 1: Strong-Light
                    Div(cls="mb-4")(
                        Label("Intensity:", fr="intensity", cls="block mb-2 font-medium"),
                        Select(id="intensity", name="intensity", cls="w-full p-2 border rounded")(
                            Option("Strong", value="strong"),
                            Option("Medium", value="medium", selected="selected"),
                            Option("Light", value="light")
                        )
                    ),
                    
                    # Taste Profile 2: Fruity-Bold
                    Div(cls="mb-4")(
                        Label("Flavor Profile:", fr="flavor", cls="block mb-2 font-medium"),
                        Select(id="flavor", name="flavor", cls="w-full p-2 border rounded")(
                            Option("Fruity", value="fruity"),
                            Option("Bold", value="bold", selected="selected")
                        )
                    ),
                    
                    # Taste Profile 3: Sour-Bitter
                    Div(cls="mb-4")(
                        Label("Acidity:", fr="acidity", cls="block mb-2 font-medium"),
                        Select(id="acidity", name="acidity", cls="w-full p-2 border rounded")(
                            Option("Sour", value="sour"),
                            Option("Bitter", value="bitter", selected="selected")
                        )
                    ),
                    
                    # Drink Type Selector
                    Div(cls="mb-6")(
                        Label("What kind of drink?", fr="drink_type", cls="block mb-2 font-medium"),
                        Select(id="drink_type", name="drink_type", cls="w-full p-2 border rounded")(
                            Option("Espresso", value="espresso", selected="selected"),
                            Option("Americano", value="americano")
                        )
                    ),
                    
                    Button("Get Recommendations", type="submit", cls="w-full bg-amber-700 text-white py-2 px-4 rounded hover:bg-amber-800")
                )
            ),
            
            # Image Upload Section
            Div(cls="bg-amber-50 rounded-lg p-6 mb-6 shadow-md")(
                H2("Or Upload a Coffee Package", cls="text-xl font-semibold mb-4"),
                P("We'll analyze the package to recommend brewing parameters", cls="mb-4 text-sm"),
                Form(id="upload-form", action="/analyze", method="post", enctype="multipart/form-data")(
                    Div(cls="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center")(
                        Input(type="file", id="coffee-image", name="coffee-image", cls="hidden", accept="image/*"),
                        Label(fr="coffee-image", cls="cursor-pointer bg-amber-100 px-4 py-2 rounded hover:bg-amber-200")("Select Image"),
                        P("or drag and drop", cls="mt-2 text-sm text-gray-500")
                    ),
                    Div(id="image-preview", cls="mt-4 hidden"),
                    Div(cls="mt-4")(
                        Button("Analyze Package", type="submit", cls="w-full bg-amber-700 text-white py-2 px-4 rounded hover:bg-amber-800")
                    )
                )
            ),
            
            # Results Section (hidden initially)
            Div(id="results", cls="bg-amber-50 rounded-lg p-6 shadow-md hidden")(
                H2("Your Coffee Match", cls="text-xl font-semibold mb-4"),
                Div(id="recommendation-results")
            )
        )
    )


@rt("/recommend", methods=["POST"])
async def post(request):
    form = await request.form()
    strong_light = form.get("strong_light")
    fruity_bold = form.get("fruity_bold")
    sour_bitter = form.get("sour_bitter")
    drink_type = form.get("drink_type")
    
    # This would be where you'd implement your recommendation logic
    # For demo purposes, just return the values
    
    return Titled("Coffee Recommendation Results",
        Container(cls="max-w-3xl mx-auto px-4 py-8")(
            H1("Your Coffee Match", cls="text-3xl font-bold text-center mb-6"),
            Div(cls="bg-amber-50 rounded-lg p-6 shadow-md")(
                H2("Based on Your Preferences", cls="text-xl font-semibold mb-4"),
                P(f"Strong-Light: {strong_light}/10"),
                P(f"Fruity-Bold: {fruity_bold}/10"),
                P(f"Sour-Bitter: {sour_bitter}/10"),
                P(f"Drink Type: {drink_type}"),
                
                Div(cls="mt-6 p-4 bg-amber-100 rounded-lg")(
                    H3("Recommended Coffee", cls="font-semibold mb-2"),
                    P("Ethiopian Yirgacheffe", cls="text-lg"),
                    P("Light roast, fruity with citrus notes", cls="text-sm text-gray-600"),
                    
                    H3("Brewing Parameters", cls="font-semibold mt-4 mb-2"),
                    P("Grind Size: Medium-fine"),
                    P("Water Temperature: 92°C"),
                    P("Brewing Time: 2:30 minutes")
                ),
                
                Div(cls="mt-6")(
                    A("← Back to Home", href="/", cls="text-amber-700 hover:underline")
                )
            )
        )
    )

@rt("/analyze", methods=["POST"])
async def post(request):
    # This would handle the image upload and analysis
    # For demo purposes, just return a placeholder result
    
    return Titled("Coffee Package Analysis",
        Container(cls="max-w-3xl mx-auto px-4 py-8")(
            H1("Coffee Package Analysis", cls="text-3xl font-bold text-center mb-6"),
            Div(cls="bg-amber-50 rounded-lg p-6 shadow-md")(
                H2("Detected Coffee Information", cls="text-xl font-semibold mb-4"),
                
                Div(cls="mt-6 p-4 bg-amber-100 rounded-lg")(
                    H3("Package Details", cls="font-semibold mb-2"),
                    P("Origin: Colombia"),
                    P("Roast Level: Medium"),
                    P("Variety: Arabica"),
                    P("Process: Washed"),
                    
                    H3("Recommended Brewing Parameters", cls="font-semibold mt-4 mb-2"),
                    P("Grind Size: Medium"),
                    P("Water Temperature: 94°C"),
                    P("Brewing Time: 3:00 minutes")
                ),
                
                Div(cls="mt-6")(
                    A("← Back to Home", href="/", cls="text-amber-700 hover:underline")
                )
            )
        )
    )

serve()
