// src/components/Comparison/Comparision.js
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import './Comparision.css'; // Or whichever CSS file you are using (e.g., Dashboard.css)

ChartJS.register(ArcElement, Tooltip, Legend);

function Comparison({ results }) {
    if (!results || !results.videoA || !results.videoB) {
        return <div className="dashboard"><p className="dashboard-title">No comparison results available yet.</p></div>;
    }

    const chartDataA = {
        labels: Object.keys(results.videoA.sentiment_distribution),
        datasets: [
            {
                label: 'Sentiment Distribution',
                data: Object.values(results.videoA.sentiment_distribution),
                backgroundColor: ['#4CAF50', '#FFC107', '#F44336'], // Positive, Neutral, Negative
            },
        ],
    };

    const chartDataB = {
        labels: Object.keys(results.videoB.sentiment_distribution),
        datasets: [
            {
                label: 'Sentiment Distribution',
                data: Object.values(results.videoB.sentiment_distribution),
                backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
            },
        ],
    };

    return (
        <div className="dashboard">
            <h1 className="dashboard-title">Comparison of Video 1 and Video 2</h1>
            <p>Below is a comparison of the sentiment analysis for both videos.</p>

            <div className="stats-cards">
                <div className="card">
                    <h2>Video 1</h2>
                    {results.videoA.summary && <p><strong>Summary:</strong> {results.videoA.summary}</p>}
                </div>
                <div className="card">
                    <h2>Video 2</h2>
                    {results.videoB.summary && <p><strong>Summary:</strong> {results.videoB.summary}</p>}
                </div>
            </div>

            <div className="chart-container">
                <h3>Sentiment Distribution Comparison</h3>
                <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                    <div style={{ width: '45%' }}>
                        <h4>Video 1 ({results.videoA.video_id})</h4>
                        {results.videoA.sentiment_distribution && (
                            <Pie data={chartDataA} />
                        )}
                    </div>
                    <div style={{ width: '45%' }}>
                        <h4>Video 2 ({results.videoB.video_id})</h4>
                        {results.videoB.sentiment_distribution && (
                            <Pie data={chartDataB} />
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Comparison;