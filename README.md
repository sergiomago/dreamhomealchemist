# AI Dream Home Alchemist

Transform your living space into your perfect sanctuary with AI-powered recommendations for décor, color schemes, and lifestyle habits.

## Features

- Generate personalized home transformation suggestions based on your desired atmosphere
- Receive recommendations for:
  - Color schemes
  - Furniture and décor
  - Lighting
  - Sensory elements (music, scents)
  - Daily habits and rituals

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a description of your desired home atmosphere in the text area
2. Click "Transform My Space"
3. Review your personalized transformation plan

## Technologies Used

- Backend: Python, Flask
- Frontend: HTML, CSS (Tailwind CSS), JavaScript
- AI: OpenAI GPT-4
- Additional: dotenv for environment variables
