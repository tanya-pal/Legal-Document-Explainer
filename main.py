import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional

from backend.pdf_parser import PDFParser
from backend.llm_analyzer import LLMAnalyzer
from backend.risk_analyzer import RiskAnalyzer
from backend.models import AnalysisResult, RiskScoreResponse, ErrorResponse

# Initialize FastAPI app
app = FastAPI(
    title="Legal Document Explainer",
    description="AI-powered legal document analysis and risk assessment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Initialize components
pdf_parser = PDFParser()
llm_analyzer = LLMAnalyzer()
risk_analyzer = RiskAnalyzer()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/styles.css")
async def get_styles():
    """Serve the CSS file"""
    return FileResponse("frontend/styles.css", media_type="text/css")

@app.get("/script.js")
async def get_script():
    """Serve the JavaScript file"""
    return FileResponse("frontend/script.js", media_type="application/javascript")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and parse a legal document (PDF or text)
    
    Args:
        file: The uploaded file (PDF or text)
        
    Returns:
        UploadResponse with extracted text and metadata
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check file extension
        _, ext = os.path.splitext(file.filename.lower())
        if ext not in ['.pdf', '.txt']:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {ext}. Only PDF and TXT files are supported."
            )
        
        # Save uploaded file
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse the file
        result = pdf_parser.parse_file(file_path, file.filename)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return result
        
    except Exception as e:
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_text(text: str = Form(...)):
    """
    Analyze legal text and extract key information
    
    Args:
        text: The legal text to analyze
        
    Returns:
        AnalysisResult with summary, clauses, and risk assessment
    """
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text provided for analysis")
        
        # Analyze the text
        result = llm_analyzer.analyze_text(text)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/risk_score")
async def get_risk_score():
    """
    Get detailed risk score for the last analyzed document
    
    Note: This endpoint would typically work with session data or stored analysis results.
    For this implementation, it returns a mock response.
    """
    try:
        # Mock response - in a real implementation, this would use stored analysis data
        mock_clauses = []
        result = risk_analyzer.calculate_detailed_risk_score(mock_clauses)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze_document")
async def analyze_document(file: UploadFile = File(...)):
    """
    Complete document analysis pipeline: upload, parse, and analyze
    
    Args:
        file: The uploaded document
        
    Returns:
        Complete analysis including summary, clauses, and risk score
    """
    try:
        # Step 1: Upload and parse
        upload_result = await upload_file(file)
        
        # Step 2: Analyze the extracted text
        analysis_result = llm_analyzer.analyze_text(upload_result.text_content)
        
        # Step 3: Calculate detailed risk score
        risk_result = risk_analyzer.calculate_detailed_risk_score(analysis_result.clauses)
        
        # Combine results
        return {
            "upload_info": upload_result,
            "analysis": analysis_result,
            "risk_assessment": risk_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Legal Document Explainer"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 