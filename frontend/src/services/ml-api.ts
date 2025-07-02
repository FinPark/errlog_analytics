/**
 * Machine Learning API service for advanced error analysis
 */

import axios from 'axios'

// Use same API configuration as main api service
const API_BASE_URL = 'http://localhost:8080'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export interface UserRiskScore {
  user: string
  risk_score: number
  category: string
  color: string
  total_errors: number
  critical_errors: number
  most_common_error: string
  insights: string[]
  risk_factors: {
    frequency: number
    severity: number
    diversity: number
    trend: number
    critical_ratio: number
  }
}

export interface SimilarError {
  id: number
  type: string
  user: string
  timestamp: string
  severity: string
  similarity_score: number
  similarity_percentage: number
}

export interface CategoryResult {
  name: string
  count: number
  errors: number[]
  common_patterns: Record<string, any>
}

export interface AutoCategorizationResult {
  categories: Record<string, CategoryResult>
  suggestions: Array<{
    category: string
    suggestion: string
    priority: string
  }>
  total_clusters: number
  outliers: number
}

export interface RootCauseSuggestion {
  type: string
  title: string
  description: string
  confidence: number
  suggestion: string
  error_count: number
}

export interface UserRiskHeatmapData {
  heatmap_data: Array<{
    user: string
    risk_score: number
    category: string
    color: string
    total_errors: number
    critical_errors: number
    insights: string[]
  }>
  risk_distribution: {
    high_risk: number
    medium_risk: number
    low_risk: number
    minimal_risk: number
  }
  total_users: number
}

export interface MLInsightsSummary {
  total_users_analyzed: number
  high_risk_users: number
  risk_percentage: number
  total_categories_found: number
  outlier_errors: number
  top_correlations: RootCauseSuggestion[]
  categorization_suggestions: Array<{
    category: string
    suggestion: string
    priority: string
  }>
  insights_generated: number
}

export class MLApiService {
  /**
   * Get user risk scores
   */
  static async getUserRiskScores(): Promise<UserRiskScore[]> {
    try {
      const response = await api.get('/api/ml/user-risk-scores')
      return response.data
    } catch (error) {
      console.error('Error fetching user risk scores:', error)
      throw error
    }
  }

  /**
   * Get similar errors for a specific error
   */
  static async getSimilarErrors(errorId: number, limit: number = 5): Promise<SimilarError[]> {
    try {
      const response = await api.get(`/api/ml/similar-errors/${errorId}?limit=${limit}`)
      return response.data
    } catch (error) {
      console.error('Error fetching similar errors:', error)
      throw error
    }
  }

  /**
   * Get auto-categorization results
   */
  static async getAutoCategorizationResults(): Promise<AutoCategorizationResult> {
    try {
      const response = await api.get('/api/ml/auto-categorize')
      return response.data
    } catch (error) {
      console.error('Error fetching auto-categorization results:', error)
      throw error
    }
  }

  /**
   * Get root cause suggestions
   */
  static async getRootCauseSuggestions(): Promise<RootCauseSuggestion[]> {
    try {
      const response = await api.get('/api/ml/root-cause-suggestions')
      return response.data
    } catch (error) {
      console.error('Error fetching root cause suggestions:', error)
      throw error
    }
  }

  /**
   * Get user risk heatmap data
   */
  static async getUserRiskHeatmap(): Promise<UserRiskHeatmapData> {
    try {
      const response = await api.get('/api/ml/user-risk-heatmap')
      return response.data
    } catch (error) {
      console.error('Error fetching user risk heatmap:', error)
      throw error
    }
  }

  /**
   * Get ML insights summary
   */
  static async getMLInsightsSummary(): Promise<MLInsightsSummary> {
    try {
      const response = await api.get('/api/ml/insights-summary')
      return response.data
    } catch (error) {
      console.error('Error fetching ML insights summary:', error)
      throw error
    }
  }
}