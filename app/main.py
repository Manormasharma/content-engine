import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.tasks import run_content_pipeline
from google import genai

app = FastAPI(title="Autonomous Content Engine API", version="1.0.0")

# Mount static folder so images can be served to the frontend
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class ContentRequest(BaseModel):
    topic: str
    output_format: str = "Blog Post"

@app.post("/generate")
def generate_content(payload: ContentRequest):
    try:
        output = run_content_pipeline(topic=payload.topic, output_format=payload.output_format)
        
        image_url = None
        post_text = output
        
        # If LinkedIn post generated an image prompt, create the image using Gemini
        if "IMAGE_PROMPT:" in output:
            parts = output.split("IMAGE_PROMPT:")
            post_text = parts[0].strip()
            image_prompt = parts[1].strip()
            
            try:
                api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-3.1-flash-image',
                    contents=[image_prompt],
                )
                for part in response.parts:
                    if part.inline_data:
                        image = part.as_image()
                        file_path = "app/static/linkedin_visual.png"
                        image.save(file_path)
                        image_url = "http://localhost:8000/static/linkedin_visual.png"
            except Exception as img_err:
                print(f"Image generation fallback triggered: {img_err}")

        return {
            "status": "success",
            "topic": payload.topic,
            "format": payload.output_format,
            "content": post_text,
            "image_url": image_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
        
@app.get("/health")
def health_check():
    return {"status": "healthy", "system": "active"}