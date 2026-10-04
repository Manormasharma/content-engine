import os
from google import genai
from crewai.tools import tool

@tool("Generate Gemini Image")
def generate_gemini_image(prompt: str) -> str:
    """
    Generates a matching visual graphic based on a descriptive prompt using Gemini image capabilities.
    Returns the local file path of the generated image.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-image',
            contents=[prompt],
        )
        
        for part in response.parts:
            if part.inline_data:
                image = part.as_image()
                os.makedirs("app/static", exist_ok=True)
                file_path = "app/static/linkedin_visual.png"
                image.save(file_path)
                return file_path
        return "Visual generated successfully."
    except Exception as e:
        return f"Image generation error: {str(e)}"