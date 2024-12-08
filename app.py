from flask import Flask, render_template, request, jsonify
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_interior_images(prompt, num_images=3):
    """Generate interior design images using DALL-E."""
    try:
        # Create a more detailed prompt for better interior design images
        enhanced_prompt = f"Professional interior design visualization of {prompt}. Architectural Digest style, showing a beautiful and detailed {prompt} interior with perfect lighting and composition. Photorealistic, 8k quality."
        logger.debug(f"Generating image with prompt: {enhanced_prompt}")
        
        images = []
        for _ in range(num_images):
            response = client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            images.append({
                "url": response.data[0].url,
                "credit": "Generated with DALL-E 3"
            })
        return images
    except Exception as e:
        logger.error(f"Error generating images: {str(e)}")
        return []

def generate_home_transformation(theme_description):
    """Generate structured home transformation suggestions using GPT-3.5-turbo."""
    try:
        logger.info(f"Generating transformation for theme: {theme_description}")
        
        prompt = f"""Create a detailed home transformation plan based on the following desired atmosphere:
        {theme_description}
        
        Provide your response in the following JSON format:
        {{
            "summary": "A brief 2-3 sentence overview of the theme",
            "color_scheme": {{
                "primary": "hex_color",
                "secondary": "hex_color",
                "accent1": "hex_color",
                "accent2": "hex_color",
                "description": "Description of how to use these colors"
            }},
            "furniture": [
                {{"item": "item name", "description": "brief description"}},
                // 3-4 key furniture pieces
            ],
            "lighting": [
                {{"type": "lighting type", "purpose": "its purpose"}},
                // 2-3 lighting recommendations
            ],
            "sensory": {{
                "scents": ["2-3 recommended scents"],
                "sounds": ["2-3 music or sound recommendations"]
            }},
            "daily_rituals": [
                "3-4 suggested daily habits or rituals"
            ]
        }}
        
        Make sure all color codes are valid hex codes (e.g., #FF5733) and descriptions are concise but evocative.
        Ensure the response is valid JSON format.
        """
        
        # Get the design suggestions from GPT-3.5
        logger.debug("Calling OpenAI API for design suggestions")
        completion_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # Using the latest model version
            messages=[
                {"role": "system", "content": "You are an expert interior designer and lifestyle consultant. You always provide responses in valid JSON format with proper hex color codes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={ "type": "json_object" }  # Ensure JSON response
        )
        
        # Get the response content
        content = completion_response.choices[0].message.content
        logger.debug(f"Raw GPT response: {content}")
        
        # Parse the response to ensure it's valid JSON
        transformation = json.loads(content)
        logger.info("Successfully parsed GPT response as JSON")
        
        # Generate interior design images based on the theme
        logger.debug("Generating interior design images")
        images = generate_interior_images(theme_description)
        transformation["inspiration_images"] = images
        
        return transformation
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        return {"error": f"Invalid JSON response from AI: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    try:
        data = request.get_json()
        theme_description = data.get('theme')
        
        if not theme_description:
            logger.warning("No theme description provided")
            return jsonify({'error': 'No theme description provided'}), 400
        
        logger.info(f"Processing transformation request for theme: {theme_description}")
        transformation = generate_home_transformation(theme_description)
        
        if "error" in transformation:
            logger.error(f"Error in transformation: {transformation['error']}")
            return jsonify(transformation), 400
            
        return jsonify(transformation)
    except Exception as e:
        logger.error(f"Error in transform endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
