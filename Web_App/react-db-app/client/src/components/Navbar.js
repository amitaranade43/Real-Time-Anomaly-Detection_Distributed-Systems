import React from 'react';
import './navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      
       <button onClick={() => { window.location.href = '/' }} className="view-abnormal-servers">View Abnormal Servers</button>
       <button onClick={() => { window.location.href = '/data/history' }} className="view-history">View History</button>

    </nav>
  );
}

export default Navbar;
