// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './NavBar';
import LandingPage from './LandingPage'; // Home and Landing Page are the same
import DashboardOne from './DashboardOne'; // Video1 page
import DashboardTwo from './DashboardTwo'; // Video2 page
import Comparison from './Comparison';

function App() {
  // Global state to indicate whether data has been retrieved.
  const [dataRetrieved, setDataRetrieved] = useState(false);

  return (
    <Router>
      {/* Pass the state to NavBar so it can conditionally render links */}
      <NavBar dataRetrieved={dataRetrieved} />
      <Routes>
        {/* Home route (landing page with retrieve data form) */}
        <Route path="/" element={<LandingPage setDataRetrieved={setDataRetrieved} />} />
        <Route path="/video1" element={<DashboardOne />} />
        <Route path="/video2" element={<DashboardTwo />} />
        <Route path="/comparison" element={<Comparison />} />
      </Routes>
    </Router>
  );
}

export default App;
