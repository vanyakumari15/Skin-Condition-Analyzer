import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './History.css';

function History() {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/history');
      if (response.data.success) {
        setAnalyses(response.data.analyses);
      }
    } catch (error) {
      setError('Failed to load history');
      console.error('Error fetching history:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="history-page">
        <div className="loading">Loading history...</div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="history-container">
        <div className="history-header">
          <h1>📊 Analysis History</h1>
          <p>View all your past skin condition analyses</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        {analyses.length > 0 ? (
          <div className="analysis-grid">
            {analyses.map((analysis) => (
              <div key={analysis._id} className="analysis-card">
                {analysis.image_data ? (
                  <img 
                    src={analysis.image_data} 
                    alt="Analysis" 
                    className="analysis-image"
                  />
                ) : (
                  <div className="analysis-image-placeholder">
                    📸
                  </div>
                )}
                
                <div className="analysis-content">
                  <div className="analysis-date">
                    📅 {formatDate(analysis.created_at)}
                  </div>
                  
                  <div className="diagnosis-badge">
                    {analysis.primary_diagnosis || 'Unknown'}
                  </div>
                  
                  <div className="confidence-score">
                    {analysis.confidence ? (analysis.confidence * 100).toFixed(1) : 0}% Confidence
                  </div>
                  
                  {analysis.predictions && analysis.predictions.length > 0 && (
                    <div className="predictions-list">
                      {analysis.predictions.slice(0, 3).map((pred, index) => (
                        <div key={index} className="prediction-item">
                          <span className="prediction-name">{pred.class}</span>
                          <span className="prediction-confidence">
                            {(pred.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-history">
            <div className="no-history-icon">🔬</div>
            <h2>No Analysis History Yet</h2>
            <p>Start analyzing skin conditions to see your history here</p>
            <Link to="/analyze" className="btn-analyze">
              Start First Analysis
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}

export default History;
