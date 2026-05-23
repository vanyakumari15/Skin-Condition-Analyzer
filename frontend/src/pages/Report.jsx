import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Report.css';

function Report() {
  const [predictions, setPredictions] = useState(null);
  const [imageData, setImageData] = useState(null);
  const [downloading, setDownloading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const resultsData = sessionStorage.getItem('analysisResults');
    const imgData = sessionStorage.getItem('analysisImage');

    if (resultsData && imgData) {
      setPredictions(JSON.parse(resultsData));
      setImageData(imgData);
    } else {
      navigate('/analyze');
    }
  }, [navigate]);

  const downloadReport = async () => {
    setDownloading(true);
    try {
      const response = await axios.post('/download-report', {
        predictions,
        image: imageData
      }, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `skin_analysis_report_${Date.now()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Failed to download report. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  if (!predictions) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="report-page">
      <div className="report-container">
        <div className="report-header">
          <h1>📊 Analysis Report</h1>
          <p className="report-date">Generated on {new Date().toLocaleString()}</p>
        </div>

        <div className="image-section">
          <img src={imageData} alt="Analyzed" className="analyzed-image" />
        </div>

        <div className="results-section">
          <h2 className="section-title">🔬 Diagnosis Results</h2>
          {predictions.map((pred, index) => {
            const percentage = (pred.confidence * 100).toFixed(1);
            const isPrimary = index === 0;

            return (
              <div key={index} className={`result-card ${isPrimary ? 'primary' : ''}`}>
                <div className="result-header">
                  <div className="result-title">{pred.class}</div>
                  <div className={`result-badge ${isPrimary ? 'badge-primary' : 'badge-secondary'}`}>
                    {isPrimary ? 'Primary Diagnosis' : 'Possible Condition'}
                  </div>
                </div>
                <div className="confidence-section">
                  <div className="confidence-text">{percentage}%</div>
                  <div className="confidence-bar">
                    <div
                      className={`confidence-fill ${isPrimary ? 'primary' : ''}`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
                <div className="result-description">
                  <strong>Description:</strong> {pred.description}
                </div>
              </div>
            );
          })}
        </div>

        <div className="action-buttons">
          <button className="btn btn-success" onClick={downloadReport} disabled={downloading}>
            {downloading ? '⏳ Generating...' : '📄 Download PDF Report'}
          </button>
          <Link to="/analyze" className="btn btn-primary">
            🔄 New Analysis
          </Link>
        </div>

        <div className="disclaimer">
          <div className="disclaimer-title">⚠️ Important Medical Disclaimer</div>
          <div className="disclaimer-text">
            This AI-generated analysis is for informational and educational purposes only.
            It is NOT a substitute for professional medical advice, diagnosis, or treatment.
            Always consult a qualified dermatologist or healthcare provider.
          </div>
        </div>
      </div>
    </div>
  );
}

export default Report;
