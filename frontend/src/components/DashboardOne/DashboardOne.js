// src/components/DDashboardOne.js
import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import './DashboardOne.css';

const COLORS = ['#f06292', '#ffc658', '#82ca9d']; // Negative, Neutral, Positive

function DashboardOne({ results }) {
  if (!results || !results.video_id) {
    return (
      <div className="dashboard">
        <p className="dashboard-title">No analysis results available yet.</p>
      </div>
    );
  }

  const youtubeUrl = `https://www.youtube.com/watch?v=${results.video_id}`;
  const thumbnailUrl = `https://i.ytimg.com/vi/${results.video_id}/mqdefault.jpg`;

  const sentimentData = Object.entries(results.sentiment_distribution).map(
    ([name, value]) => ({ name, value })
  );

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">Analysis for Video: {results.video_id}</h1>
  
      {/* Flex container for video + chart */}
      <div className="dashboard-center-wrapper">
        <div className="video-info-container">
          {/* Left: Video thumbnail + title */}
          <div className="video-panel">
            <a
              href={youtubeUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="video-link"
            >
              <img
                src={thumbnailUrl}
                alt="Video Thumbnail"
                className="video-thumbnail"
              />
              <div className="video-details">
                <h3>Video Title (Replace with actual title if available)</h3>
              </div>
            </a>
          </div>
  
          {/* Right: Chart */}
          <div className="sentiment-chart">
            <h3>Sentiment Analysis of the Comments Towards the Video</h3>
            {sentimentData.length > 0 ? (
              <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={sentimentData}
                      cx="50%"
                      cy="45%"
                      labelLine={false}
                      outerRadius={120}
                      dataKey="value"
                    >
                      {sentimentData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#ffffff",
                        border: "1px solid #ccc",
                        borderRadius: "8px",
                        color: "#0f172a",
                        fontSize: "0.9rem",
                        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.15)",
                      }}
                      itemStyle={{
                        color: "#0f172a",
                      }}
                      formatter={(value, name) => [`${value}`, `${name}`]}
                    />
                    <Legend
                      verticalAlign="bottom"
                      iconType="circle"
                      layout="horizontal"
                      align="center"
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p>No sentiment data available.</p>
            )}
          </div>
        </div>
      </div>
  
      {/* Summary section at the bottom, centered */}
      <div className="summary-bottom">
        <div className="summary-container-top">
          <h4>Summary</h4>
          {results.summary ? <p>{results.summary}</p> : <p>No summary available.</p>}
        </div>
      </div>
    </div>
  );
  
}

export default DashboardOne;
