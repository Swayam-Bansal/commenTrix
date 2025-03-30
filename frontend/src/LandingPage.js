// src/LandingPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css'; // Your landing page CSS

function LandingPage({ setDataRetrieved }) {
  const [youtubeUrl1, setYoutubeUrl1] = useState('');
  const [youtubeUrl2, setYoutubeUrl2] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you can add any data retrieval logic with the URLs.
    console.log("Retrieving data for:", youtubeUrl1, youtubeUrl2);
    
    // Mark that data has been retrieved
    setDataRetrieved(true);
    // Navigate to the Comparison page
    navigate('/comparison');
  };

  return (
    <div className="landing-page">
      <h1 className="landing-title">Welcome to My Dashboard App</h1>
      <form className="youtube-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="youtubeUrl1">YouTube Video URL 1:</label>
          <input
            type="text"
            id="youtubeUrl1"
            value={youtubeUrl1}
            onChange={(e) => setYoutubeUrl1(e.target.value)}
            placeholder="Enter first YouTube video URL"
          />
        </div>
        <div className="form-group">
          <label htmlFor="youtubeUrl2">YouTube Video URL 2:</label>
          <input
            type="text"
            id="youtubeUrl2"
            value={youtubeUrl2}
            onChange={(e) => setYoutubeUrl2(e.target.value)}
            placeholder="Enter second YouTube video URL"
          />
        </div>
        <button type="submit">Retrieve Data</button>
      </form>
    </div>
  );
}

export default LandingPage;
