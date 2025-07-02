"""
Machine Learning Analyzer for Error Log Analytics
Provides advanced analytics including user risk scoring, error clustering,
and auto-categorization of error patterns.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import re


class MLAnalyzer:
    """Advanced ML-based analyzer for error log insights"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
        self.error_clusters = {}
        self.user_profiles = {}
    
    def calculate_user_risk_scores(self, errors: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Calculate comprehensive risk scores for users based on their error patterns
        
        Returns:
            Dict with user risk scores, categories, and insights
        """
        if not errors:
            return {}
        
        df = pd.DataFrame(errors)
        user_scores = {}
        
        for user in df['user'].unique():
            if not user or user == 'Unknown':
                continue
                
            user_errors = df[df['user'] == user]
            
            # Calculate various risk factors
            risk_factors = self._calculate_risk_factors(user_errors, df)
            
            # Weighted risk score (0-10 scale)
            weights = {
                'frequency': 0.25,      # How often they get errors
                'severity': 0.30,       # How severe their errors are  
                'diversity': 0.20,      # How many different error types
                'trend': 0.15,          # Are errors increasing?
                'critical_ratio': 0.10  # Ratio of critical errors
            }
            
            risk_score = sum(risk_factors[factor] * weight 
                           for factor, weight in weights.items())
            
            # Determine risk category
            if risk_score >= 7.5:
                category = "High Risk"
                color = "#f44336"  # Red
            elif risk_score >= 5.0:
                category = "Medium Risk" 
                color = "#ff9800"  # Orange
            elif risk_score >= 2.5:
                category = "Low Risk"
                color = "#ffc107"  # Yellow
            else:
                category = "Minimal Risk"
                color = "#4caf50"  # Green
            
            # Generate insights
            insights = self._generate_user_insights(user_errors, risk_factors, df)
            
            user_scores[user] = {
                'risk_score': round(risk_score, 1),
                'category': category,
                'color': color,
                'total_errors': len(user_errors),
                'critical_errors': len(user_errors[user_errors['severity'] == 'Critical']),
                'most_common_error': user_errors['type'].mode().iloc[0] if not user_errors['type'].mode().empty else 'N/A',
                'insights': insights,
                'risk_factors': risk_factors
            }
        
        return user_scores
    
    def _calculate_risk_factors(self, user_errors: pd.DataFrame, all_errors: pd.DataFrame) -> Dict[str, float]:
        """Calculate individual risk factors for a user"""
        
        # 1. Frequency Factor (0-10): How often compared to average
        user_error_count = len(user_errors)
        avg_error_count = len(all_errors) / all_errors['user'].nunique()
        frequency_score = min(10, (user_error_count / max(avg_error_count, 1)) * 3)
        
        # 2. Severity Factor (0-10): Weighted by error severity
        severity_weights = {'Critical': 10, 'High': 7, 'Medium': 4, 'Low': 1}
        if len(user_errors) > 0:
            severity_score = user_errors['severity'].map(severity_weights).mean()
        else:
            severity_score = 0
        
        # 3. Diversity Factor (0-10): How many different error types
        unique_errors = user_errors['type'].nunique()
        max_diversity = all_errors['type'].nunique()
        diversity_score = min(10, (unique_errors / max(max_diversity, 1)) * 10)
        
        # 4. Trend Factor (0-10): Are errors increasing over time?
        trend_score = self._calculate_trend_score(user_errors)
        
        # 5. Critical Ratio (0-10): Percentage of critical errors
        critical_count = len(user_errors[user_errors['severity'] == 'Critical'])
        if len(user_errors) > 0:
            critical_ratio = (critical_count / len(user_errors)) * 10
        else:
            critical_ratio = 0
        
        return {
            'frequency': frequency_score,
            'severity': severity_score,
            'diversity': diversity_score,
            'trend': trend_score,
            'critical_ratio': critical_ratio
        }
    
    def _calculate_trend_score(self, user_errors: pd.DataFrame) -> float:
        """Calculate if user's errors are trending up or down"""
        if len(user_errors) < 2:
            return 5.0  # Neutral
        
        try:
            # Convert timestamps and sort
            user_errors = user_errors.copy()
            user_errors['date'] = pd.to_datetime(user_errors['timestamp'], format='%d.%m.%Y %H:%M:%S', errors='coerce')
            user_errors = user_errors.dropna(subset=['date']).sort_values('date')
            
            if len(user_errors) < 2:
                return 5.0
            
            # Group by day and count errors
            daily_counts = user_errors.groupby(user_errors['date'].dt.date).size()
            
            if len(daily_counts) < 2:
                return 5.0
            
            # Calculate linear trend
            x = np.arange(len(daily_counts))
            y = daily_counts.values
            
            if len(x) > 1:
                slope = np.polyfit(x, y, 1)[0]
                # Convert slope to 0-10 score (positive slope = higher risk)
                trend_score = 5 + (slope * 2)  # Adjust sensitivity
                return max(0, min(10, trend_score))
            
        except Exception:
            pass
        
        return 5.0  # Neutral if calculation fails
    
    def _generate_user_insights(self, user_errors: pd.DataFrame, risk_factors: Dict[str, float], all_errors: pd.DataFrame) -> List[str]:
        """Generate actionable insights for a user"""
        insights = []
        
        # High frequency insight
        if risk_factors['frequency'] > 7:
            avg_errors = len(all_errors) / all_errors['user'].nunique()
            insights.append(f"Generates {len(user_errors)} errors vs {avg_errors:.1f} average - needs attention")
        
        # Severity insight
        if risk_factors['severity'] > 7:
            critical_count = len(user_errors[user_errors['severity'] == 'Critical'])
            insights.append(f"High severity pattern: {critical_count} critical errors detected")
        
        # Diversity insight  
        if risk_factors['diversity'] > 7:
            unique_types = user_errors['type'].nunique()
            insights.append(f"Wide error variety: {unique_types} different error types - broad system usage issues")
        
        # Trend insight
        if risk_factors['trend'] > 7:
            insights.append("Error frequency increasing over time - system degradation or learning curve")
        elif risk_factors['trend'] < 3:
            insights.append("Error frequency decreasing - showing improvement")
        
        # Common error insight
        most_common = user_errors['type'].mode()
        if not most_common.empty:
            common_error = most_common.iloc[0]
            count = len(user_errors[user_errors['type'] == common_error])
            if count > len(user_errors) * 0.5:
                insights.append(f"Dominant issue: {count} '{common_error}' errors - focused training needed")
        
        if not insights:
            insights.append("Normal error pattern - no specific concerns identified")
        
        return insights[:3]  # Limit to top 3 insights
    
    def find_similar_errors(self, target_error: Dict[str, Any], all_errors: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find errors similar to the target error using ML clustering
        
        Returns:
            List of similar errors with similarity scores
        """
        if not all_errors:
            return []
        
        df = pd.DataFrame(all_errors)
        target_id = target_error.get('id')
        
        # Remove target error from candidates
        candidates = df[df['id'] != target_id] if target_id else df
        
        if len(candidates) == 0:
            return []
        
        # Prepare text for similarity analysis
        target_text = self._prepare_error_text(target_error)
        candidate_texts = [self._prepare_error_text(row.to_dict()) for _, row in candidates.iterrows()]
        
        if not target_text.strip():
            return []
        
        # Calculate similarity using TF-IDF and cosine similarity
        all_texts = [target_text] + candidate_texts
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            # Add similarity scores to candidates
            candidates = candidates.copy()
            candidates['similarity_score'] = similarities
            
            # Sort by similarity and get top matches
            similar_errors = candidates.nlargest(limit, 'similarity_score')
            
            # Convert to list of dicts with similarity scores
            result = []
            for _, row in similar_errors.iterrows():
                error_dict = row.to_dict()
                similarity = error_dict.pop('similarity_score')
                error_dict['similarity_score'] = round(similarity, 3)
                error_dict['similarity_percentage'] = round(similarity * 100, 1)
                result.append(error_dict)
            
            return result
            
        except Exception as e:
            print(f"Error in similarity calculation: {e}")
            # Fallback: return errors with same type
            same_type = candidates[candidates['type'] == target_error.get('type', '')]
            return same_type.head(limit).to_dict('records')
    
    def _prepare_error_text(self, error: Dict[str, Any]) -> str:
        """Prepare error text for similarity analysis"""
        parts = []
        
        # Add error type (most important)
        if error.get('type'):
            parts.append(error['type'])
        
        # Add error content/description
        if error.get('content'):
            # Clean and normalize content
            content = error['content']
            content = re.sub(r'[^\w\s]', ' ', content)  # Remove special chars
            content = re.sub(r'\s+', ' ', content)      # Normalize whitespace
            parts.append(content)
        
        # Add severity
        if error.get('severity'):
            parts.append(error['severity'])
        
        # Add code if available
        if error.get('code'):
            parts.append(f"code_{error['code']}")
        
        return ' '.join(parts).lower().strip()
    
    def auto_categorize_errors(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Automatically categorize unknown error types using clustering
        
        Returns:
            Dict with categorization results and suggestions
        """
        if not errors:
            return {'categories': {}, 'suggestions': []}
        
        df = pd.DataFrame(errors)
        
        # Prepare texts for clustering
        error_texts = [self._prepare_error_text(error) for error in errors]
        
        try:
            # Use TF-IDF for feature extraction
            tfidf_matrix = self.vectorizer.fit_transform(error_texts)
            
            # Use DBSCAN for clustering (automatically determines number of clusters)
            clustering = DBSCAN(eps=0.3, min_samples=2, metric='cosine')
            cluster_labels = clustering.fit_predict(tfidf_matrix.toarray())
            
            # Analyze clusters
            categories = {}
            suggestions = []
            
            for cluster_id in set(cluster_labels):
                if cluster_id == -1:  # Noise/outliers
                    continue
                
                cluster_errors = df[cluster_labels == cluster_id]
                
                # Generate category name based on most common terms
                cluster_texts = [error_texts[i] for i in range(len(error_texts)) if cluster_labels[i] == cluster_id]
                category_name = self._generate_category_name(cluster_texts, cluster_errors)
                
                categories[f"Category_{cluster_id}"] = {
                    'name': category_name,
                    'count': len(cluster_errors),
                    'errors': cluster_errors['id'].tolist() if 'id' in cluster_errors.columns else [],
                    'common_patterns': self._extract_common_patterns(cluster_errors)
                }
                
                # Generate suggestions for this category
                if len(cluster_errors) >= 3:  # Only suggest for significant clusters
                    suggestions.append({
                        'category': category_name,
                        'suggestion': f"Consider creating a specific handler for '{category_name}' - {len(cluster_errors)} similar errors detected",
                        'priority': 'High' if len(cluster_errors) > 10 else 'Medium'
                    })
            
            # Handle outliers
            outlier_count = sum(1 for label in cluster_labels if label == -1)
            if outlier_count > 0:
                suggestions.append({
                    'category': 'Unique Errors',
                    'suggestion': f"{outlier_count} unique error patterns identified - may need individual investigation",
                    'priority': 'Low'
                })
            
            return {
                'categories': categories,
                'suggestions': suggestions,
                'total_clusters': len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
                'outliers': outlier_count
            }
            
        except Exception as e:
            print(f"Error in auto-categorization: {e}")
            return {'categories': {}, 'suggestions': [], 'error': str(e)}
    
    def _generate_category_name(self, cluster_texts: List[str], cluster_errors: pd.DataFrame) -> str:
        """Generate a meaningful name for an error cluster"""
        
        # Try to use most common error type
        if 'type' in cluster_errors.columns:
            most_common_type = cluster_errors['type'].mode()
            if not most_common_type.empty:
                return most_common_type.iloc[0]
        
        # Fallback: extract key terms from texts
        all_text = ' '.join(cluster_texts)
        words = re.findall(r'\w+', all_text.lower())
        word_counts = Counter(words)
        
        # Remove common words
        stopwords = {'error', 'exception', 'failed', 'cannot', 'unable', 'code', 'type'}
        meaningful_words = [(word, count) for word, count in word_counts.most_common(5) 
                          if word not in stopwords and len(word) > 3]
        
        if meaningful_words:
            return ' '.join([word.capitalize() for word, _ in meaningful_words[:2]]) + ' Related'
        
        return 'Unknown Pattern'
    
    def _extract_common_patterns(self, cluster_errors: pd.DataFrame) -> Dict[str, Any]:
        """Extract common patterns from a cluster of errors"""
        patterns = {}
        
        # Most common severity
        if 'severity' in cluster_errors.columns:
            patterns['common_severity'] = cluster_errors['severity'].mode().iloc[0] if not cluster_errors['severity'].mode().empty else 'Unknown'
        
        # Most common user (if relevant)
        if 'user' in cluster_errors.columns:
            user_counts = cluster_errors['user'].value_counts()
            if len(user_counts) > 0:
                patterns['primary_user'] = user_counts.index[0]
                patterns['user_concentration'] = f"{user_counts.iloc[0]}/{len(cluster_errors)}"
        
        # Time pattern
        if 'timestamp' in cluster_errors.columns:
            try:
                cluster_errors['hour'] = pd.to_datetime(cluster_errors['timestamp'], format='%d.%m.%Y %H:%M:%S', errors='coerce').dt.hour
                common_hour = cluster_errors['hour'].mode()
                if not common_hour.empty:
                    patterns['common_time'] = f"{common_hour.iloc[0]:02d}:00"
            except:
                pass
        
        return patterns
    
    def find_root_cause_correlations(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find potential root causes by analyzing error correlations
        
        Returns:
            List of root cause suggestions with supporting evidence
        """
        if not errors:
            return []
        
        df = pd.DataFrame(errors)
        correlations = []
        
        # 1. Time-based correlations
        time_correlations = self._find_time_correlations(df)
        correlations.extend(time_correlations)
        
        # 2. User-based correlations
        user_correlations = self._find_user_correlations(df)
        correlations.extend(user_correlations)
        
        # 3. Error-type correlations
        type_correlations = self._find_type_correlations(df)
        correlations.extend(type_correlations)
        
        # Sort by confidence and return top suggestions
        correlations.sort(key=lambda x: x['confidence'], reverse=True)
        return correlations[:10]  # Top 10 suggestions
    
    def _find_time_correlations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Find errors that occur close together in time"""
        correlations = []
        
        try:
            df['datetime'] = pd.to_datetime(df['timestamp'], format='%d.%m.%Y %H:%M:%S', errors='coerce')
            df = df.dropna(subset=['datetime']).sort_values('datetime')
            
            # Look for error bursts (multiple errors within short time windows)
            time_threshold = timedelta(minutes=30)  # 30-minute window
            
            for i in range(len(df) - 1):
                current_error = df.iloc[i]
                following_errors = []
                
                for j in range(i + 1, min(i + 10, len(df))):  # Check next 10 errors
                    next_error = df.iloc[j]
                    time_diff = next_error['datetime'] - current_error['datetime']
                    
                    if time_diff <= time_threshold:
                        following_errors.append(next_error)
                    else:
                        break
                
                if len(following_errors) >= 2:  # Found a burst
                    involved_errors = [current_error] + following_errors
                    error_types = [e['type'] for e in involved_errors]
                    users = [e['user'] for e in involved_errors]
                    
                    correlations.append({
                        'type': 'time_burst',
                        'title': f"Error burst detected: {len(involved_errors)} errors in {time_threshold}",
                        'description': f"Multiple errors occurred within {time_threshold.total_seconds()/60:.0f} minutes",
                        'error_types': list(set(error_types)),
                        'affected_users': list(set(users)),
                        'start_time': current_error['datetime'].strftime('%d.%m.%Y %H:%M:%S'),
                        'confidence': min(0.9, 0.5 + (len(following_errors) * 0.1)),
                        'suggestion': "Investigate system state during this time period - possible cascading failure or external trigger",
                        'error_count': len(involved_errors)
                    })
        
        except Exception as e:
            print(f"Error in time correlation analysis: {e}")
        
        return correlations
    
    def _find_user_correlations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Find users who consistently experience similar errors"""
        correlations = []
        
        try:
            user_error_patterns = df.groupby('user')['type'].apply(list).to_dict()
            
            for user, error_types in user_error_patterns.items():
                if len(error_types) < 3:  # Skip users with few errors
                    continue
                
                error_counter = Counter(error_types)
                most_common = error_counter.most_common(3)
                
                # Check if user has repetitive error pattern
                if most_common[0][1] >= 3:  # At least 3 of the same error
                    dominant_error = most_common[0][0]
                    count = most_common[0][1]
                    total_errors = len(error_types)
                    
                    correlations.append({
                        'type': 'user_pattern',
                        'title': f"User {user} has repetitive error pattern",
                        'description': f"{count}/{total_errors} errors are '{dominant_error}'",
                        'user': user,
                        'dominant_error': dominant_error,
                        'frequency': f"{count}/{total_errors}",
                        'confidence': min(0.9, count / total_errors),
                        'suggestion': f"User {user} may need specific training on '{dominant_error}' or there's a systemic issue affecting this user",
                        'error_count': count
                    })
        
        except Exception as e:
            print(f"Error in user correlation analysis: {e}")
        
        return correlations
    
    def _find_type_correlations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Find error types that frequently occur together"""
        correlations = []
        
        try:
            # Group errors by user and day to find co-occurring errors
            df['date'] = pd.to_datetime(df['timestamp'], format='%d.%m.%Y %H:%M:%S', errors='coerce').dt.date
            
            grouped = df.groupby(['user', 'date'])['type'].apply(list).reset_index()
            
            # Find error type pairs that co-occur
            type_pairs = defaultdict(int)
            
            for _, row in grouped.iterrows():
                error_types = list(set(row['type']))  # Unique types per user per day
                
                if len(error_types) >= 2:
                    for i in range(len(error_types)):
                        for j in range(i + 1, len(error_types)):
                            pair = tuple(sorted([error_types[i], error_types[j]]))
                            type_pairs[pair] += 1
            
            # Find significant correlations
            for (type1, type2), count in type_pairs.items():
                if count >= 3:  # Occurred together at least 3 times
                    total_type1 = len(df[df['type'] == type1])
                    total_type2 = len(df[df['type'] == type2])
                    
                    # Calculate correlation strength
                    correlation_strength = count / min(total_type1, total_type2)
                    
                    if correlation_strength >= 0.3:  # At least 30% correlation
                        correlations.append({
                            'type': 'type_correlation',
                            'title': f"'{type1}' and '{type2}' frequently occur together",
                            'description': f"These error types co-occurred {count} times",
                            'error_type_1': type1,
                            'error_type_2': type2,
                            'co_occurrence_count': count,
                            'correlation_strength': round(correlation_strength, 2),
                            'confidence': min(0.9, correlation_strength),
                            'suggestion': f"Investigate common root cause between '{type1}' and '{type2}' - possible shared dependency or workflow issue",
                            'error_count': count
                        })
        
        except Exception as e:
            print(f"Error in type correlation analysis: {e}")
        
        return correlations