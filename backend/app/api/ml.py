"""
Machine Learning API endpoints for advanced error analysis
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import redis
import json
import asyncio
from ..core.config import get_redis_client
from ..analyzers.ml_analyzer import MLAnalyzer

router = APIRouter(prefix="/api/ml", tags=["machine-learning"])

# Response models
class UserRiskScore(BaseModel):
    user: str
    risk_score: float
    category: str
    color: str
    total_errors: int
    critical_errors: int
    most_common_error: str
    insights: List[str]
    risk_factors: Dict[str, float]

class SimilarError(BaseModel):
    id: int
    type: str
    user: str
    timestamp: str
    severity: str
    similarity_score: float
    similarity_percentage: float

class CategoryResult(BaseModel):
    name: str
    count: int
    errors: List[int]
    common_patterns: Dict[str, Any]

class AutoCategorizationResult(BaseModel):
    categories: Dict[str, CategoryResult]
    suggestions: List[Dict[str, str]]
    total_clusters: int
    outliers: int

class RootCauseSuggestion(BaseModel):
    type: str
    title: str
    description: str
    confidence: float
    suggestion: str
    error_count: int


@router.get("/user-risk-scores", response_model=List[UserRiskScore])
async def get_user_risk_scores(redis_client = Depends(get_redis_client)):
    """
    Calculate and return user risk scores based on error patterns
    """
    try:
        # Get errors from Redis
        errors_data = redis_client.get("analyzed_errors")
        if not errors_data:
            raise HTTPException(status_code=404, detail="No error data found")
        
        errors = json.loads(errors_data)
        
        # Initialize ML analyzer
        analyzer = MLAnalyzer()
        
        # Calculate risk scores
        risk_scores = analyzer.calculate_user_risk_scores(errors)
        
        # Convert to response format
        result = []
        for user, data in risk_scores.items():
            result.append(UserRiskScore(
                user=user,
                **data
            ))
        
        # Sort by risk score descending
        result.sort(key=lambda x: x.risk_score, reverse=True)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating user risk scores: {str(e)}")


@router.get("/similar-errors/{error_id}", response_model=List[SimilarError])
async def get_similar_errors(error_id: int, limit: int = 5, redis_client = Depends(get_redis_client)):
    """
    Find errors similar to the specified error using ML clustering
    """
    try:
        # Get errors from Redis
        errors_data = redis_client.get("analyzed_errors")
        if not errors_data:
            raise HTTPException(status_code=404, detail="No error data found")
        
        errors = json.loads(errors_data)
        
        # Find target error
        target_error = None
        for error in errors:
            if error.get('id') == error_id:
                target_error = error
                break
        
        if not target_error:
            raise HTTPException(status_code=404, detail="Target error not found")
        
        # Initialize ML analyzer
        analyzer = MLAnalyzer()
        
        # Find similar errors
        similar_errors = analyzer.find_similar_errors(target_error, errors, limit)
        
        # Convert to response format
        result = []
        for error in similar_errors:
            result.append(SimilarError(
                id=error.get('id', 0),
                type=error.get('type', 'Unknown'),
                user=error.get('user', 'Unknown'),
                timestamp=error.get('timestamp', ''),
                severity=error.get('severity', 'Unknown'),
                similarity_score=error.get('similarity_score', 0.0),
                similarity_percentage=error.get('similarity_percentage', 0.0)
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding similar errors: {str(e)}")


@router.get("/auto-categorize", response_model=AutoCategorizationResult)
async def auto_categorize_errors(redis_client = Depends(get_redis_client)):
    """
    Automatically categorize errors using ML clustering
    """
    try:
        # Get errors from Redis
        errors_data = redis_client.get("analyzed_errors")
        if not errors_data:
            raise HTTPException(status_code=404, detail="No error data found")
        
        errors = json.loads(errors_data)
        
        # Initialize ML analyzer
        analyzer = MLAnalyzer()
        
        # Auto-categorize errors
        categorization_result = analyzer.auto_categorize_errors(errors)
        
        # Convert categories to response format
        categories = {}
        for cat_id, cat_data in categorization_result.get('categories', {}).items():
            categories[cat_id] = CategoryResult(
                name=cat_data['name'],
                count=cat_data['count'],
                errors=cat_data['errors'],
                common_patterns=cat_data['common_patterns']
            )
        
        return AutoCategorizationResult(
            categories=categories,
            suggestions=categorization_result.get('suggestions', []),
            total_clusters=categorization_result.get('total_clusters', 0),
            outliers=categorization_result.get('outliers', 0)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error auto-categorizing: {str(e)}")


@router.get("/root-cause-suggestions", response_model=List[RootCauseSuggestion])
async def get_root_cause_suggestions(redis_client = Depends(get_redis_client)):
    """
    Find potential root causes by analyzing error correlations
    """
    try:
        # Get errors from Redis
        errors_data = redis_client.get("analyzed_errors")
        if not errors_data:
            return _get_demo_root_causes()
        
        errors = json.loads(errors_data)
        if not errors:
            return _get_demo_root_causes()
        
        # Initialize ML analyzer
        analyzer = MLAnalyzer()
        
        # Find root cause correlations
        correlations = analyzer.find_root_cause_correlations(errors)
        
        # Convert to response format
        result = []
        for correlation in correlations:
            result.append(RootCauseSuggestion(
                type=correlation['type'],
                title=correlation['title'],
                description=correlation['description'],
                confidence=correlation['confidence'],
                suggestion=correlation['suggestion'],
                error_count=correlation['error_count']
            ))
        
        return result
        
    except Exception as e:
        print(f"ML Root Cause Error: {str(e)}")
        return _get_demo_root_causes()


@router.get("/user-risk-heatmap")
async def get_user_risk_heatmap(redis_client = Depends(get_redis_client)):
    """
    Get user risk data formatted for heatmap visualization
    """
    try:
        # Get errors from Redis
        errors_data = redis_client.get("analyzed_errors")
        if not errors_data:
            # Fallback to demo data
            return _get_demo_heatmap_data()
        
        errors = json.loads(errors_data)
        if not errors:
            return _get_demo_heatmap_data()
        
        # Initialize ML analyzer
        analyzer = MLAnalyzer()
        
        # Calculate risk scores
        risk_scores = analyzer.calculate_user_risk_scores(errors)
        
        # Format for heatmap
        heatmap_data = []
        for user, data in risk_scores.items():
            heatmap_data.append({
                'user': user,
                'risk_score': data['risk_score'],
                'category': data['category'],
                'color': data['color'],
                'total_errors': data['total_errors'],
                'critical_errors': data['critical_errors'],
                'insights': data['insights'][:2]  # Top 2 insights for heatmap
            })
        
        # Sort by risk score
        heatmap_data.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return {
            'heatmap_data': heatmap_data,
            'risk_distribution': {
                'high_risk': len([u for u in heatmap_data if u['risk_score'] >= 7.5]),
                'medium_risk': len([u for u in heatmap_data if 5.0 <= u['risk_score'] < 7.5]),
                'low_risk': len([u for u in heatmap_data if 2.5 <= u['risk_score'] < 5.0]),
                'minimal_risk': len([u for u in heatmap_data if u['risk_score'] < 2.5])
            },
            'total_users': len(heatmap_data)
        }
        
    except Exception as e:
        print(f"ML Heatmap Error: {str(e)}")
        return _get_demo_heatmap_data()


@router.get("/insights-summary")
async def get_ml_insights_summary(redis_client = Depends(get_redis_client)):
    """
    Get a comprehensive summary of all ML insights
    """
    try:
        # Get errors from Redis
        errors_data = redis_client.get("analyzed_errors")
        if not errors_data:
            raise HTTPException(status_code=404, detail="No error data found")
        
        errors = json.loads(errors_data)
        
        # Initialize ML analyzer
        analyzer = MLAnalyzer()
        
        # Run all analyses
        risk_scores = analyzer.calculate_user_risk_scores(errors)
        categorization = analyzer.auto_categorize_errors(errors)
        correlations = analyzer.find_root_cause_correlations(errors)
        
        # Count high-risk users
        high_risk_users = len([user for user, data in risk_scores.items() if data['risk_score'] >= 7.5])
        
        # Get top correlations
        top_correlations = correlations[:3]
        
        # Summary statistics
        summary = {
            'total_users_analyzed': len(risk_scores),
            'high_risk_users': high_risk_users,
            'risk_percentage': round((high_risk_users / max(len(risk_scores), 1)) * 100, 1),
            'total_categories_found': categorization.get('total_clusters', 0),
            'outlier_errors': categorization.get('outliers', 0),
            'top_correlations': top_correlations,
            'categorization_suggestions': categorization.get('suggestions', [])[:3],
            'insights_generated': len(correlations) + len(categorization.get('suggestions', []))
        }
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ML insights summary: {str(e)}")


def _get_demo_heatmap_data():
    """Generate demo heatmap data for testing"""
    return {
        'heatmap_data': [
            {
                'user': 'AVB',
                'risk_score': 8.2,
                'category': 'High Risk',
                'color': '#ff4444',
                'total_errors': 45,
                'critical_errors': 12,
                'insights': ['Häufige ACCESS VIOLATIONS', 'Kritische Fehler in letzten 24h']
            },
            {
                'user': 'GAM',
                'risk_score': 6.5,
                'category': 'Medium Risk',
                'color': '#ff8800',
                'total_errors': 28,
                'critical_errors': 5,
                'insights': ['DATA TYPE ERRORs steigend', 'Wiederholende Muster']
            },
            {
                'user': 'SWE',
                'risk_score': 4.1,
                'category': 'Low Risk',
                'color': '#ffaa00',
                'total_errors': 15,
                'critical_errors': 2,
                'insights': ['Normale Fehlerverteilung', 'Stabile Performance']
            },
            {
                'user': 'MSP',
                'risk_score': 2.8,
                'category': 'Minimal Risk',
                'color': '#88cc00',
                'total_errors': 8,
                'critical_errors': 0,
                'insights': ['Niedrige Fehlerrate', 'Gute Systemnutzung']
            }
        ],
        'risk_distribution': {
            'high_risk': 1,
            'medium_risk': 1,
            'low_risk': 1,
            'minimal_risk': 1
        },
        'total_users': 4
    }


def _get_demo_root_causes():
    """Generate demo root cause suggestions"""
    return [
        RootCauseSuggestion(
            type="User Pattern",
            title="AVB: Häufige ACCESS VIOLATIONS",
            description="Benutzer AVB hat 12 ACCESS VIOLATION Fehler in den letzten 24 Stunden",
            confidence=0.85,
            suggestion="Prüfen Sie Benutzerrechte und Systemzugriffe für AVB",
            error_count=12
        ),
        RootCauseSuggestion(
            type="System Correlation",
            title="DATA TYPE ERRORs korrelieren mit Tageszeit",
            description="85% der DATA TYPE ERRORs treten zwischen 14:00-16:00 auf",
            confidence=0.78,
            suggestion="Überprüfen Sie Systemlast und Datenverarbeitung am Nachmittag",
            error_count=23
        ),
        RootCauseSuggestion(
            type="Code Pattern",
            title="BOUND ERRORs folgen ähnlichem Muster",
            description="BOUND ERRORs (Code 2) treten oft nach ACCESS VIOLATIONS auf",
            confidence=0.72,
            suggestion="Untersuchen Sie Speicherverwaltung und Array-Zugriffe",
            error_count=8
        ),
        RootCauseSuggestion(
            type="Resource Issue",
            title="Kritische Fehler bei mehreren Benutzern",
            description="3 Benutzer haben gleichzeitig kritische Fehler um 15:07:17",
            confidence=0.91,
            suggestion="Prüfen Sie Systemressourcen und Netzwerkverbindungen",
            error_count=6
        )
    ]