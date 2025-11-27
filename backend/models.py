from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ClauseType(str, Enum):
    DATA_SHARING = "data_sharing"
    AUTO_RENEWAL = "auto_renewal"
    ARBITRATION = "arbitration"
    LIABILITY = "liability"
    CANCELLATION = "cancellation"
    CONFIDENTIALITY = "confidentiality"
    TERMINATION = "termination"

class Clause(BaseModel):
    """Represents an identified legal clause"""
    type: ClauseType
    text: str
    start_index: int
    end_index: int
    risk_level: RiskLevel
    explanation: str
    page_number: Optional[int] = None

class AnalysisResult(BaseModel):
    """Result of document analysis"""
    summary: str
    clauses: List[Clause]
    risk_score: int
    total_words: int
    analysis_confidence: float

class UploadResponse(BaseModel):
    """Response for file upload"""
    filename: str
    text_content: str
    file_size: int
    pages: int

class RiskScoreResponse(BaseModel):
    """Response for risk score calculation"""
    score: int
    breakdown: Dict[str, int]
    recommendations: List[str]

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    details: Optional[str] = None 