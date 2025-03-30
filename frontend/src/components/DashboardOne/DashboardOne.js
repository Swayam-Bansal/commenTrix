// src/components/DashboardOne/DashboardOne.js
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import './DashboardOne.css'; // Or whichever CSS file you are using

const COLORS = ['#f06292', '#ffc658','#82ca9d']; // Negative, Neutral, Positive

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index, payload }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
        <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
            {`${payload.name} ${(percent * 100).toFixed(0)}%`}
        </text>
    );
};

function DashboardOne({ results }) {
    if (!results || !results.video_id) {
        return <div className="dashboard"><p className="dashboard-title">No analysis results available yet.</p></div>;
    }

    const youtubeUrl = `https://www.youtube.com/watch?v=${results.video_id}`;
    const thumbnailUrl = `https://i.ytimg.com/vi/${results.video_id}/mqdefault.jpg`;

    const sentimentData = Object.entries(results.sentiment_distribution)
        .map(([name, value]) => ({ name, value }));

    return (
        <div className="dashboard">
            <h1 className="dashboard-title">Analysis for Video: {results.video_id}</h1>

            <div className="video-info-container">
                <div className="video-details-summary">
                    <a href={youtubeUrl} target="_blank" rel="noopener noreferrer" className="video-link">
                        <img src={thumbnailUrl} alt="Video Thumbnail" className="video-thumbnail" />
                        <div className="video-details">
                            <h3>Video Title (Replace with actual title if available)</h3>
                        </div>
                    </a>
                    <div className="summary-container-top">
                        <h4>Summary</h4>
                        {results.summary && <p>{results.summary}</p>}
                        {!results.summary && <p>No summary available.</p>}
                    </div>
                </div>
                <div className="sentiment-chart">
                    <h3>Sentiment Analysis of the Comments Towards the Video</h3>
                    {results.sentiment_distribution && Object.keys(results.sentiment_distribution).length > 0 ? (
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={sentimentData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={renderCustomizedLabel}
                                    outerRadius={100}
                                    dataKey="value"
                                >
                                    {sentimentData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                            </PieChart>
                        </ResponsiveContainer>
                    ) : (
                        <p>No sentiment data available.</p>
                    )}
                </div>
            </div>

            {/* The original summary container is now hidden */}
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