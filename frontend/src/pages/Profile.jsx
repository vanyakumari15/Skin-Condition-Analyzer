import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Profile.css';

function Profile() {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await axios.get('/api/check-auth');
      if (response.data.authenticated) {
        setUser({ username: response.data.username });
        // You can add an API endpoint to get user stats
        setStats({
          total_analyses: 0,
          days_active: 0
        });
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  if (!user) {
    return <div className="loading">User not found</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <div className="profile-avatar">
            {user.username[0].toUpperCase()}
          </div>
          <div className="profile-info">
            <h1>{user.username}</h1>
            <span className="profile-badge">✓ Verified Account</span>
          </div>
        </div>

        <div className="profile-content">
          <div className="profile-card">
            <h2>📋 Account Information</h2>
            <div className="info-row">
              <span className="info-label">Username</span>
              <span className="info-value">{user.username}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Account Status</span>
              <span className="info-value" style={{color: '#28a745'}}>Active</span>
            </div>
          </div>

          <div className="profile-card">
            <h2>📊 Activity Statistics</h2>
            <div className="stats-grid">
              <div className="stat-box">
                <div className="stat-number">{stats?.total_analyses || 0}</div>
                <div className="stat-label">Analyses</div>
              </div>
              <div className="stat-box">
                <div className="stat-number">{stats?.days_active || 0}</div>
                <div className="stat-label">Days Active</div>
              </div>
            </div>
            <Link to="/analyze" className="action-btn btn-analyze">
              Start New Analysis
            </Link>
          </div>

          <div className="profile-card full-width">
            <h2>⚡ Quick Actions</h2>
            <div className="quick-actions">
              <Link to="/analyze" className="quick-action-btn">
                <span className="quick-action-icon">🔬</span>
                <span>New Analysis</span>
              </Link>
              <Link to="/history" className="quick-action-btn">
                <span className="quick-action-icon">📊</span>
                <span>View History</span>
              </Link>
              <Link to="/faq" className="quick-action-btn">
                <span className="quick-action-icon">❓</span>
                <span>View FAQ</span>
              </Link>
              <Link to="/" className="quick-action-btn">
                <span className="quick-action-icon">🏠</span>
                <span>Home</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
