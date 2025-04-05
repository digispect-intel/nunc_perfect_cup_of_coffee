# Perfect Cup of Coffee

An AI-powered application that helps coffee lovers find their perfect brew. Developed for the AI Hackathon #3 - Next Level Coffee Track.

## Repository

https://github.com/digispect-intel/nunc_perfect_cup_of_coffee

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
   git clone https://github.com/digispect-intel/nunc_perfect_cup_of_coffee.git
   cd nunc_perfect_cup_of_coffee
   ```

2. Create and activate a virtual environment with Python 3.11:
   ```
   # Linux/macOS
   python3.11 -m venv env
   source env/bin/activate
   
   # Windows
   py -3.11 -m venv env
   env\Scripts\activate
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
   
   If port 5001 is already in use, modify the port in app.py:
   ```python
   serve(port=5002)
   ```

## Project Structure

- `app.py`: Main application file with routes
- `modules/`: Functional components (OCR, recommender, etc.)
- `static/`: Static assets (CSS, JS, images)
- `data/`: Data files and sample images

## Hackathon Information

This project was developed for the AI Hackathon #3 - Next Level Coffee Track, focusing on creating AI-powered solutions to enhance the coffee brewing experience.

## Team

Team: Perfect Cup of Coffee

## License

MIT