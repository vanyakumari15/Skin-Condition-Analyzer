import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Analyze from './pages/Analyze';
import Report from './pages/Report';
import History from './pages/History';
import FAQ from './pages/FAQ';
import Profile from './pages/Profile';
import './App.css';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get('/api/check-auth');
      if (response.data.authenticated) {
        setUser({ username: response.data.username });
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (username) => {
    setUser({ username });
  };

  const handleLogout = async () => {
    try {
      await axios.post('/api/logout');
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Navbar user={user} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<Home user={user} />} />
          <Route 
            path="/login" 
            element={user ? <Navigate to="/analyze" /> : <Login onLogin={handleLogin} />} 
          />
          <Route 
            path="/register" 
            element={user ? <Navigate to="/analyze" /> : <Register />} 
          />
          <Route 
            path="/analyze" 
            element={user ? <Analyze /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/report" 
            element={user ? <Report /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/history" 
            element={user ? <History /> : <Navigate to="/login" />} 
          />
          <Route path="/faq" element={<FAQ />} />
          <Route 
            path="/profile" 
            element={user ? <Profile /> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
