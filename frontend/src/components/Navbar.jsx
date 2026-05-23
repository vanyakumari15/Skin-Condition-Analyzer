import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar({ user, onLogout }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="logo">🔬 SkinAnalyzer</Link>
        <button className="mobile-menu-btn" onClick={() => setMenuOpen(!menuOpen)}>
          ☰
        </button>
        <div className={`nav-links ${menuOpen ? 'active' : ''}`}>
          <Link to="/" onClick={() => setMenuOpen(false)}>Home</Link>
          <Link to="/faq" onClick={() => setMenuOpen(false)}>FAQ</Link>
          {user ? (
            <>
              <Link to="/analyze" onClick={() => setMenuOpen(false)}>Analyze</Link>
              <Link to="/history" onClick={() => setMenuOpen(false)}>📊 History</Link>
              <Link to="/profile" onClick={() => setMenuOpen(false)}>👤 Profile</Link>
              <button onClick={() => { onLogout(); setMenuOpen(false); }} className="btn btn-secondary">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" onClick={() => setMenuOpen(false)}>
                <button className="btn btn-secondary">Login</button>
              </Link>
              <Link to="/register" onClick={() => setMenuOpen(false)}>
                <button className="btn btn-primary">Sign Up</button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
