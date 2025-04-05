# AI Coffee Recommender

A smart application that recommends coffee based on taste preferences and package analysis, developed for the AI Hackathon #3 - Next Level Coffee Track.

## Features

- **Taste Preference Analysis**: Select your preferred coffee characteristics to get personalized recommendations
- **Coffee Package OCR**: Upload images of coffee packages to automatically extract information and get brewing parameters
- **Smart Recommendations**: Get coffee recommendations based on your taste profile and extracted package data

## Tech Stack

- **Backend**: Python with FastHTML
- **Frontend**: HTML, CSS (Tailwind)
- **AI Components**: 
  - OCR for coffee package text extraction
  - Recommendation algorithm based on taste preferences
  - Data analysis of brewing parameters

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/coffee-recommender.git
   cd coffee-recommender
   ```

2. Create and activate a virtual environment:
   ```
   python3.11 -m venv env source env/bin/activate
   source env/bin/activate  # On Windows: py -3.11 -m venv env env\Scripts\activate



   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5001
   ```

## Project Structure

- `app.py`: Main application file with routes
- `modules/`: Functional components (OCR, recommender, etc.)
- `static/`: Static assets (CSS, JS, images)
- `data/`: Data files and sample images

## Contributing

This project was created during the AI Hackathon #3. Feel free to fork, modify, and use it as a starting point for your own projects.

## License

MIT