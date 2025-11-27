# Legal Document Explainer

A full-stack web application that analyzes legal documents using AI to extract key clauses, identify risks, and provide plain English summaries.

## Features

- 📄 **PDF Document Upload**: Support for PDF and text file uploads
- 🤖 **AI-Powered Analysis**: Uses transformers to analyze legal text
- 📋 **Key Clause Extraction**: Identifies data sharing, auto-renewals, arbitration, and liability terms
- ⚠️ **Risk Assessment**: Flags risky/ambiguous sections with explanations
- 📊 **Risk Scoring**: Provides a 0-100 risk score based on identified clauses
- 🎨 **Interactive UI**: Clean, modern interface with highlighted clauses and explanations

## Tech Stack

- **Backend**: FastAPI (Python)
- **LLM**: Hugging Face Transformers
- **PDF Parser**: PyMuPDF
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with utility-first approach

## Setup Instructions

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Backend Server**:
   ```bash
   python main.py
   ```

3. **Open the Application**:
   Navigate to `http://localhost:8000` in your browser

## API Endpoints

- `POST /upload`: Upload and parse documents
- `POST /analyze`: Analyze text and extract clauses
- `GET /risk_score`: Calculate risk score for analyzed document

## Project Structure

```
Legal_Document_Explainer/
├── main.py                 # FastAPI application entry point
├── backend/
│   ├── __init__.py
│   ├── pdf_parser.py      # PDF text extraction
│   ├── llm_analyzer.py    # AI-powered text analysis
│   ├── risk_analyzer.py   # Risk assessment logic
│   └── models.py          # Pydantic data models
├── frontend/
│   ├── index.html         # Main application page
│   ├── styles.css         # Custom styling
│   └── script.js          # Frontend JavaScript logic
├── uploads/               # Temporary file storage
└── requirements.txt       # Python dependencies
```

## Usage

1. Upload a legal document (PDF or text)
2. View the extracted text and AI-generated summary
3. Review highlighted risky clauses with explanations
4. Check the overall risk score
5. Click on highlighted clauses for detailed explanations

## Development Notes
- The LLM component uses a mock implementation that can be easily replaced with a real model
- All components are modular for easy maintenance and updates
- The frontend uses vanilla JavaScript for simplicity and performance



