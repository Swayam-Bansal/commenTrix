// src/components/DashboardOne/DashboardOne.js
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import './DashboardOne.css'; // Or whichever CSS file you are using (e.g., Dashboard.css)

ChartJS.register(ArcElement, Tooltip, Legend);

function DashboardOne({ results }) {
    if (!results || !results.video_id) {
        return <div className="dashboard"><p className="dashboard-title">No analysis results available yet.</p></div>;
    }

    const chartData = {
        labels: Object.keys(results.sentiment_distribution),
        datasets: [
            {
                label: 'Sentiment Distribution',
                data: Object.values(results.sentiment_distribution),
                backgroundColor: ['#f06292', '#ffc658', '#82ca9d'], // Positive, Neutral, Negative
            },
        ],
    };

    return (
      <div className="dashboard">
          <h1 className="dashboard-title">Analysis for Video: {results.video_id}</h1>
  
          <div className="video-info-container">
              <div className="video-thumbnail">
                  {/* Placeholder for video thumbnail */}
                  <img src={`https://i.ytimg.com/vi/${results.video_id}/mqdefault.jpg`} alt="Video Thumbnail" style={{ maxWidth: '200px', height: 'auto' }} />
              </div>
              <div className="video-details">
                  {/* Placeholder for video title */}
                  <h3>Video Title (Replace with actual title if available)</h3>
              </div>
              <div className="sentiment-chart">
                  <h3>Sentiment Distribution</h3>
                  {results.sentiment_distribution && Object.keys(results.sentiment_distribution).length > 0 ? (
                      <Pie data={chartData} options={{ plugins: { legend: { position: 'bottom' } } }} />
                  ) : (
                      <p>No sentiment data available.</p>
                  )}
              </div>
          </div>
  
          <div className="summary-container">
              <h2>Summary</h2>
              <div className="card">
                  {results.summary && <p>{results.summary}</p>}
                  {!results.summary && <p>No summary available.</p>}
              </div>
            </div>
        </div>
    );
  }

  export default DashboardOne;
  