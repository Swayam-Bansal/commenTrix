// src/components/Comparision/Comparision.js
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import './Comparision.css'; // Or whichever CSS file you are using (e.g., Dashboard.css)

const COLORS = ['#4CAF50', '#FFC107', '#F44336'];

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

function Comparison({ results }) {
    console.log("Results prop in Comparison component:", results);
    if (!results || !results.video1 || !results.video2) {
        return <div className="dashboard"><p className="dashboard-title">No comparison results available yet.</p></div>;
    }

    const { video1, video2 } = results;

    const video1YoutubeUrl = `https://www.youtube.com/watch?v=$${video1.video_id}`;
    const video1ThumbnailUrl = `https://i.ytimg.com/vi/${video1.video_id}/mqdefault.jpg`;
    const video1SentimentData = Object.entries(video1.sentiment_distribution)
        .map(([name, value]) => ({ name, value }));

    const video2YoutubeUrl = `https://www.youtube.com/watch?v=$${video2.video_id}`;
    const video2ThumbnailUrl = `https://i.ytimg.com/vi/${video2.video_id}/mqdefault.jpg`;
    const video2SentimentData = Object.entries(video2.sentiment_distribution)
        .map(([name, value]) => ({ name, value }));

    return (
        <div className="dashboard">
            <h1 className="dashboard-title">Comparison of Video Analysis</h1>

            <div className="comparison-container">
                <div className="video-comparison">
                    <h3>Video 1: {video1.video_id}</h3>
                    <a href={video1YoutubeUrl} target="_blank" rel="noopener noreferrer" className="video-link">
                        <img src={video1ThumbnailUrl} alt={`Thumbnail for ${video1.video_id}`} className="video-thumbnail" style={{ maxHeight: '150px' }} />
                        <div className="video-details">
                            <h4>Video Title 1 (Replace with actual title if available)</h4>
                        </div>
                    </a>
                    <div className="sentiment-chart">
                        <h4>Sentiment Distribution</h4>
                        {video1.sentiment_distribution && Object.keys(video1.sentiment_distribution).length > 0 ? (
                            <ResponsiveContainer width="100%" height={250}>
                                <PieChart>
                                    <Pie
                                        data={video1SentimentData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={renderCustomizedLabel}
                                        outerRadius={80}
                                        dataKey="value"
                                    >
                                        {video1SentimentData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        ) : (
                            <p>No sentiment data available.</p>
                        )}
                    </div>
                    <div className="summary-container-top">
                        <h4>Summary</h4>
                        {video1.summary && <p>{video1.summary}</p>}
                        {!video1.summary && <p>No summary available.</p>}
                    </div>
                </div>

                <div className="video-comparison">
                    <h3>Video 2: {video2.video_id}</h3>
                    <a href={video2YoutubeUrl} target="_blank" rel="noopener noreferrer" className="video-link">
                        <img src={video2ThumbnailUrl} alt={`Thumbnail for ${video2.video_id}`} className="video-thumbnail" style={{ maxHeight: '150px' }} />
                        <div className="video-details">
                            <h4>Video Title 2 (Replace with actual title if available)</h4>
                        </div>
                    </a>
                    <div className="sentiment-chart">
                        <h4>Sentiment Distribution</h4>
                        {video2.sentiment_distribution && Object.keys(video2.sentiment_distribution).length > 0 ? (
                            <ResponsiveContainer width="100%" height={250}>
                                <PieChart>
                                    <Pie
                                        data={video2SentimentData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={renderCustomizedLabel}
                                        outerRadius={80}
                                        dataKey="value"
                                    >
                                        {video2SentimentData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        ) : (
                            <p>No sentiment data available.</p>
                        )}
                    </div>
                    <div className="summary-container-top">
                        <h4>Summary</h4>
                        {video2.summary && <p>{video2.summary}</p>}
                        {!video2.summary && <p>No summary available.</p>}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Comparison;