import os
import base64
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import modules from our project
from estimator import analyze_face
from recommendations import get_recommendations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="I Model (Face Detection & Age/Glow Estimator)",
    description="Analyze skin metrics and age to provide tailored skincare advice.",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Payloads for API
class WebcamPayload(BaseModel):
    image: str  # Base64 data URL

# Routes
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join("templates", "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_path)

@app.post("/analyze")
async def analyze_webcam_frame(payload: WebcamPayload):
    """
    Accepts base64 encoded images from the webcam, runs face metrics estimation
    and fetches dynamic dietary and skincare suggestions.
    """
    try:
        # Decode base64 image data
        data_str = payload.image
        if "," in data_str:
            header, encoded_data = data_str.split(",", 1)
        else:
            encoded_data = data_str
            
        img_bytes = base64.b64decode(encoded_data)
        
        # Perform face estimation
        analysis = analyze_face(img_bytes)
        
        # Generate recommendations based on Age and Glow Score
        recs = {}
        if analysis["face_detected"]:
            recs = get_recommendations(analysis["age"], analysis["glow_score"])
            
        return {
            "status": "success",
            "face_detected": analysis["face_detected"],
            "data": analysis,
            "recommendations": recs
        }
    except Exception as e:
        logger.error(f"Failed to analyze webcam frame: {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/analyze-file")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """
    Accepts image file uploads, runs face metrics estimation
    and fetches dynamic dietary and skincare suggestions.
    """
    try:
        img_bytes = await file.read()
        
        # Perform face estimation
        analysis = analyze_face(img_bytes)
        
        # Generate recommendations based on Age and Glow Score
        recs = {}
        if analysis["face_detected"]:
            recs = get_recommendations(analysis["age"], analysis["glow_score"])
            
        return {
            "status": "success",
            "face_detected": analysis["face_detected"],
            "data": analysis,
            "recommendations": recs
        }
    except Exception as e:
        logger.error(f"Failed to analyze uploaded file: {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    # Start the server locally
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
