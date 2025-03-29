import React from "react";
import "./index.css";

function App() {
  return (
    <div className="container">
      {/* YouTube Link Input */}
      <div className="section">
        <input
          type="text"
          placeholder="Enter a YouTube Link"
          className="input-box"
        />
      </div>

      {/* Video and AI Summary Section */}
      <div className="section row">
        <div className="video-box">Video Box</div>
        <div className="summary-box">
          <h2>AI Summary</h2>
          <p>Summary content goes here...</p>
        </div>
      </div>

      {/* Sentiment Chart Placeholder */}
      <div className="section sentiment-chart">
        <h2>Sentiment Analysis</h2>
        <div className="bars">
          <div className="bar-group">
            <div className="bar positive"></div>
            <span>Positive</span>
          </div>
          <div className="bar-group">
            <div className="bar negative"></div>
            <span>Negative</span>
          </div>
          <div className="bar-group">
            <div className="bar neutral"></div>
            <span>Neutral</span>
          </div>
        </div>
      </div>

      {/* Depth and Editability Section */}
      <div className="section footer-box">
        <div className="footer-header">
          <span>Depth</span>
          <span>Editability</span>
        </div>
        <div className="footer-content">Content/Indicators go here</div>
      </div>
    </div>
  );
}

export default App;
