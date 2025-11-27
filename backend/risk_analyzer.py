from typing import List, Dict, Any
from .models import Clause, RiskLevel, RiskScoreResponse

class RiskAnalyzer:
    """Advanced risk analysis and scoring for legal documents"""
    
    def __init__(self):
        # Define risk weights for different clause types
        self.clause_risk_weights = {
            'data_sharing': 25,
            'auto_renewal': 20,
            'arbitration': 15,
            'liability': 20,
            'cancellation': 10,
            'confidentiality': 5,
            'termination': 5
        }
        
        # Risk level multipliers
        self.risk_level_multipliers = {
            RiskLevel.LOW: 0.3,
            RiskLevel.MEDIUM: 0.6,
            RiskLevel.HIGH: 1.0,
            RiskLevel.CRITICAL: 1.5
        }
    
    def calculate_detailed_risk_score(self, clauses: List[Clause]) -> RiskScoreResponse:
        """
        Calculate detailed risk score with breakdown and recommendations
        
        Args:
            clauses: List of identified clauses
            
        Returns:
            RiskScoreResponse with score, breakdown, and recommendations
        """
        if not clauses:
            return RiskScoreResponse(
                score=0,
                breakdown={},
                recommendations=["No significant risks identified in this document."]
            )
        
        # Calculate breakdown by clause type
        breakdown = self._calculate_breakdown(clauses)
        
        # Calculate overall score
        total_score = self._calculate_total_score(clauses)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(clauses, breakdown)
        
        return RiskScoreResponse(
            score=total_score,
            breakdown=breakdown,
            recommendations=recommendations
        )
    
    def _calculate_breakdown(self, clauses: List[Clause]) -> Dict[str, int]:
        """Calculate risk breakdown by clause type"""
        breakdown = {}
        
        for clause in clauses:
            clause_type = clause.type.value
            if clause_type not in breakdown:
                breakdown[clause_type] = 0
            
            # Calculate score for this clause
            base_weight = self.clause_risk_weights.get(clause_type, 10)
            risk_multiplier = self.risk_level_multipliers.get(clause.risk_level, 0.5)
            clause_score = int(base_weight * risk_multiplier)
            
            breakdown[clause_type] += clause_score
        
        return breakdown
    
    def _calculate_total_score(self, clauses: List[Clause]) -> int:
        """Calculate overall risk score"""
        total_score = 0
        
        for clause in clauses:
            base_weight = self.clause_risk_weights.get(clause.type.value, 10)
            risk_multiplier = self.risk_level_multipliers.get(clause.risk_level, 0.5)
            clause_score = base_weight * risk_multiplier
            total_score += clause_score
        
        # Normalize to 0-100 scale
        max_possible_score = sum(self.clause_risk_weights.values()) * 1.5  # Max multiplier
        if max_possible_score > 0:
            normalized_score = min(100, int((total_score / max_possible_score) * 100))
        else:
            normalized_score = 0
        
        return normalized_score
    
    def _generate_recommendations(self, clauses: List[Clause], breakdown: Dict[str, int]) -> List[str]:
        """Generate actionable recommendations based on identified risks"""
        recommendations = []
        
        # Check for high-risk clauses
        high_risk_clauses = [c for c in clauses if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        
        if high_risk_clauses:
            recommendations.append("⚠️ High-risk clauses detected. Consider consulting a legal professional.")
        
        # Specific recommendations by clause type
        clause_recommendations = {
            'data_sharing': "Review data sharing provisions carefully. Ensure you understand what information is being shared and with whom.",
            'auto_renewal': "Check auto-renewal terms. Understand your cancellation rights and notice requirements.",
            'arbitration': "Arbitration clauses may limit your legal rights. Consider the implications before agreeing.",
            'liability': "Liability limitations may affect your ability to recover damages. Review carefully.",
            'cancellation': "Understand cancellation terms and any penalties for early termination."
        }
        
        for clause_type, score in breakdown.items():
            if score > 0 and clause_type in clause_recommendations:
                recommendations.append(clause_recommendations[clause_type])
        
        # General recommendations
        if len(clauses) > 5:
            recommendations.append("This document contains many legal clauses. Consider having it reviewed by a lawyer.")
        
        if not recommendations:
            recommendations.append("No significant risks identified. Standard legal document review recommended.")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def get_risk_summary(self, clauses: List[Clause]) -> Dict[str, Any]:
        """Get a summary of risk analysis"""
        if not clauses:
            return {
                "risk_level": "low",
                "total_clauses": 0,
                "high_risk_count": 0,
                "summary": "No significant risks identified"
            }
        
        high_risk_count = len([c for c in clauses if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
        medium_risk_count = len([c for c in clauses if c.risk_level == RiskLevel.MEDIUM])
        
        # Determine overall risk level
        if high_risk_count > 0:
            risk_level = "high"
            summary = f"High-risk document with {high_risk_count} concerning clauses"
        elif medium_risk_count > 2:
            risk_level = "medium"
            summary = f"Medium-risk document with {medium_risk_count} clauses requiring attention"
        else:
            risk_level = "low"
            summary = f"Low-risk document with {len(clauses)} standard clauses"
        
        return {
            "risk_level": risk_level,
            "total_clauses": len(clauses),
            "high_risk_count": high_risk_count,
            "medium_risk_count": medium_risk_count,
            "summary": summary
        } 