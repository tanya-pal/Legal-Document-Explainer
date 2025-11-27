import re
from typing import List, Dict, Any
from .models import Clause, ClauseType, RiskLevel, AnalysisResult

class LLMAnalyzer:
    """AI-powered text analysis using transformers (mock implementation)"""
    
    def __init__(self):
        # Define keywords and patterns for clause detection
        self.clause_patterns = {
            ClauseType.DATA_SHARING: [
                r'data.*shar', r'personal.*information', r'privacy.*policy',
                r'third.*party.*access', r'data.*transfer', r'information.*disclosure'
            ],
            ClauseType.AUTO_RENEWAL: [
                r'auto.*renew', r'automatic.*renewal', r'evergreen.*clause',
                r'continuous.*renewal', r'perpetual.*renewal'
            ],
            ClauseType.ARBITRATION: [
                r'arbitration', r'arbitrator', r'dispute.*resolution',
                r'mediation', r'alternative.*dispute.*resolution'
            ],
            ClauseType.LIABILITY: [
                r'liability', r'limitation.*of.*liability', r'disclaimer',
                r'hold.*harmless', r'indemnification', r'waiver.*of.*damages'
            ],
            ClauseType.CANCELLATION: [
                r'cancellation', r'termination', r'early.*termination',
                r'breach.*of.*contract', r'default.*provisions'
            ],
            ClauseType.CONFIDENTIALITY: [
                r'confidentiality', r'non.*disclosure', r'proprietary.*information',
                r'trade.*secret', r'confidential.*information'
            ],
            ClauseType.TERMINATION: [
                r'termination', r'end.*of.*agreement', r'contract.*expiration',
                r'notice.*of.*termination', r'breach.*termination'
            ]
        }
        
        # Risk indicators for each clause type
        self.risk_indicators = {
            ClauseType.DATA_SHARING: {
                'high_risk': [r'unlimited.*access', r'permanent.*retention', r'no.*consent'],
                'medium_risk': [r'reasonable.*use', r'business.*purpose', r'with.*consent'],
                'low_risk': [r'limited.*access', r'secure.*storage', r'user.*control']
            },
            ClauseType.AUTO_RENEWAL: {
                'high_risk': [r'no.*notice', r'perpetual', r'irrevocable'],
                'medium_risk': [r'30.*day.*notice', r'annual.*renewal'],
                'low_risk': [r'written.*notice', r'opt.*out', r'cancellation.*right']
            },
            ClauseType.ARBITRATION: {
                'high_risk': [r'mandatory.*arbitration', r'no.*jury.*trial', r'class.*action.*waiver'],
                'medium_risk': [r'voluntary.*arbitration', r'mediation.*first'],
                'low_risk': [r'optional.*arbitration', r'right.*to.*sue']
            }
        }
    
    def analyze_text(self, text: str) -> AnalysisResult:
        """
        Analyze legal text and extract key information
        
        Args:
            text: The legal text to analyze
            
        Returns:
            AnalysisResult with summary, clauses, and risk assessment
        """
        # Clean and normalize text
        text = self._clean_text(text)
        
        # Generate summary
        summary = self._generate_summary(text)
        
        # Extract clauses
        clauses = self._extract_clauses(text)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(clauses)
        
        # Calculate confidence (mock implementation)
        analysis_confidence = 0.85
        
        return AnalysisResult(
            summary=summary,
            clauses=clauses,
            risk_score=risk_score,
            total_words=len(text.split()),
            analysis_confidence=analysis_confidence
        )
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def _generate_summary(self, text: str) -> str:
        """
        Generate a plain English summary of the legal document
        
        This is a mock implementation that can be replaced with a real LLM
        """
        # Simple rule-based summary generation
        sentences = text.split('.')
        key_sentences = []
        
        # Look for key terms and extract relevant sentences
        key_terms = ['agreement', 'contract', 'terms', 'conditions', 'obligations', 'rights']
        
        for sentence in sentences[:20]:  # Limit to first 20 sentences
            if any(term in sentence.lower() for term in key_terms):
                key_sentences.append(sentence.strip())
        
        if key_sentences:
            summary = '. '.join(key_sentences[:3]) + '.'
        else:
            # Fallback summary
            summary = f"This legal document contains {len(text.split())} words and appears to be a contract or agreement. Key terms and conditions should be reviewed carefully."
        
        return summary
    
    def _extract_clauses(self, text: str) -> List[Clause]:
        """Extract legal clauses from text using pattern matching"""
        clauses = []
        
        for clause_type, patterns in self.clause_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    # Get surrounding context
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    clause_text = text[start:end]
                    
                    # Determine risk level
                    risk_level = self._assess_clause_risk(clause_type, clause_text)
                    
                    # Generate explanation
                    explanation = self._generate_clause_explanation(clause_type, risk_level)
                    
                    clause = Clause(
                        type=clause_type,
                        text=clause_text,
                        start_index=start,
                        end_index=end,
                        risk_level=risk_level,
                        explanation=explanation
                    )
                    
                    clauses.append(clause)
        
        return clauses
    
    def _assess_clause_risk(self, clause_type: ClauseType, clause_text: str) -> RiskLevel:
        """Assess the risk level of a specific clause"""
        if clause_type in self.risk_indicators:
            indicators = self.risk_indicators[clause_type]
            
            # Check for high risk indicators
            for pattern in indicators.get('high_risk', []):
                if re.search(pattern, clause_text, re.IGNORECASE):
                    return RiskLevel.HIGH
            
            # Check for medium risk indicators
            for pattern in indicators.get('medium_risk', []):
                if re.search(pattern, clause_text, re.IGNORECASE):
                    return RiskLevel.MEDIUM
        
        return RiskLevel.LOW
    
    def _generate_clause_explanation(self, clause_type: ClauseType, risk_level: RiskLevel) -> str:
        """Generate explanation for a clause based on type and risk level"""
        explanations = {
            ClauseType.DATA_SHARING: {
                RiskLevel.HIGH: "This clause allows extensive data sharing with third parties. Review carefully as it may compromise your privacy.",
                RiskLevel.MEDIUM: "This clause permits data sharing under certain conditions. Ensure you understand the scope and limitations.",
                RiskLevel.LOW: "This clause has reasonable data sharing provisions with appropriate safeguards."
            },
            ClauseType.AUTO_RENEWAL: {
                RiskLevel.HIGH: "This auto-renewal clause may lock you into long-term commitments. Check cancellation terms carefully.",
                RiskLevel.MEDIUM: "This auto-renewal clause has some notice requirements. Understand your cancellation rights.",
                RiskLevel.LOW: "This auto-renewal clause provides reasonable notice and cancellation options."
            },
            ClauseType.ARBITRATION: {
                RiskLevel.HIGH: "This arbitration clause may limit your legal rights. Consider consulting a lawyer.",
                RiskLevel.MEDIUM: "This arbitration clause provides alternative dispute resolution. Understand the process.",
                RiskLevel.LOW: "This arbitration clause offers a reasonable dispute resolution mechanism."
            },
            ClauseType.LIABILITY: {
                RiskLevel.HIGH: "This liability clause significantly limits your rights to damages. Review carefully.",
                RiskLevel.MEDIUM: "This liability clause has some limitations but provides reasonable protection.",
                RiskLevel.LOW: "This liability clause provides fair and reasonable terms."
            }
        }
        
        return explanations.get(clause_type, {}).get(risk_level, "This clause should be reviewed for potential risks and implications.")
    
    def _calculate_risk_score(self, clauses: List[Clause]) -> int:
        """Calculate overall risk score based on identified clauses"""
        if not clauses:
            return 0
        
        # Weight different risk levels
        risk_weights = {
            RiskLevel.LOW: 10,
            RiskLevel.MEDIUM: 30,
            RiskLevel.HIGH: 60,
            RiskLevel.CRITICAL: 90
        }
        
        total_score = 0
        for clause in clauses:
            total_score += risk_weights.get(clause.risk_level, 0)
        
        # Normalize to 0-100 scale
        max_possible_score = len(clauses) * 90  # Assuming all clauses could be critical
        if max_possible_score > 0:
            normalized_score = min(100, int((total_score / max_possible_score) * 100))
        else:
            normalized_score = 0
        
        return normalized_score 