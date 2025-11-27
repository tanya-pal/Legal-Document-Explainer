import pdfplumber
import os
from typing import Tuple, Optional
from .models import UploadResponse

class PDFParser:
    """Handles PDF text extraction and parsing using pdfplumber"""
    
    def __init__(self):
        self.supported_extensions = ['.pdf', '.txt']
    
    def extract_text_from_pdf(self, file_path: str) -> Tuple[str, int]:
        """
        Extract text from PDF file using pdfplumber
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, number_of_pages)
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                text_content = ""
                page_count = len(pdf.pages)
                
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
                
                return text_content.strip(), page_count
                
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_txt(self, file_path: str) -> Tuple[str, int]:
        """
        Extract text from plain text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Tuple of (extracted_text, number_of_pages)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            return text_content.strip(), 1
            
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    def parse_file(self, file_path: str, filename: str) -> UploadResponse:
        """
        Parse uploaded file and extract text content
        
        Args:
            file_path: Path to the uploaded file
            filename: Original filename
            
        Returns:
            UploadResponse with extracted text and metadata
        """
        # Get file extension
        _, ext = os.path.splitext(filename.lower())
        
        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {ext}")
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Extract text based on file type
        if ext == '.pdf':
            text_content, pages = self.extract_text_from_pdf(file_path)
        elif ext == '.txt':
            text_content, pages = self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return UploadResponse(
            filename=filename,
            text_content=text_content,
            file_size=file_size,
            pages=pages
        )
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove common PDF artifacts
        text = text.replace('\x00', '')  # Null characters
        text = text.replace('\uf0b7', '•')  # Bullet points
        
        return text.strip() 