import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home({ user }) {
  return (
    <div className="home">
      <div className="hero">
        <h1>AI-Powered Skin Condition Analysis</h1>
        <p>Get instant insights into skin conditions using advanced deep learning technology</p>
        <div className="hero-buttons">
          {user ? (
            <Link to="/analyze" className="hero-btn hero-btn-primary">Start Analysis</Link>
          ) : (
            <>
              <Link to="/register" className="hero-btn hero-btn-primary">Get Started Free</Link>
              <Link to="/login" className="hero-btn hero-btn-secondary">Login</Link>
            </>
          )}
        </div>
      </div>

      <div className="features">
        <h2>Why Choose SkinAnalyzer?</h2>
        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI-Powered</h3>
            <p>Advanced deep learning model trained on thousands of dermatological images</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Instant Results</h3>
            <p>Get comprehensive analysis in seconds with confidence scores</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Detailed Reports</h3>
            <p>Download professional PDF reports with analysis results</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Secure & Private</h3>
            <p>Your medical data is encrypted and never shared</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📸</div>
            <h3>Easy Upload</h3>
            <p>Upload images or capture photos directly from your device</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>23 Conditions</h3>
            <p>Identifies a wide range of skin conditions</p>
          </div>
        </div>
      </div>

      <div className="about">
        <h2>About This Project</h2>
        <div className="about-content">
          <div className="about-text">
            <p><strong>SkinAnalyzer</strong> is an advanced AI-powered platform designed to help identify various skin conditions using state-of-the-art deep learning technology.</p>
            <p>Our system uses a sophisticated neural network trained on extensive dermatological datasets to provide accurate preliminary assessments.</p>
            <p><strong>Important:</strong> This tool is for educational purposes. Always consult with a qualified dermatologist for proper medical advice.</p>
          </div>
          <div className="about-stats">
            <div className="stat-card">
              <div className="stat-number">23</div>
              <div className="stat-label">Skin Conditions</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">95%</div>
              <div className="stat-label">Accuracy Rate</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">&lt;3s</div>
              <div className="stat-label">Analysis Time</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">100%</div>
              <div className="stat-label">Private & Secure</div>
            </div>
          </div>
        </div>
      </div>

      <footer className="footer">
        <p>&copy; 2024 Skin Condition Analyzer. For educational purposes only.</p>
        <p>Not a substitute for professional medical advice.</p>
      </footer>
    </div>
  );
}

export default Home;
