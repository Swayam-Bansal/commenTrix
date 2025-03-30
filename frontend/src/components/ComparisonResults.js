// frontend/src/components/ComparisonResults.js
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

function ComparisonResults({ results }) {
    if (!results || !results.videoA || !results.videoB) {
        return <p>No comparison results available yet.</p>;
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
        <div>
            <h2>Comparison Results</h2>
            <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                <div>
                    <h3>Video A ({results.videoA.video_id})</h3>
                    {results.videoA.sentiment_distribution && (
                        <Pie data={chartDataA} />
                    )}
                    <h4>Top Comments:</h4>
                    <ul>
                        {results.videoA.top_comments && results.videoA.top_comments.map((comment, index) => (
                            <li key={index}>
                                <strong>{comment.author}:</strong> {comment.text} (Likes: {comment.likes})
                            </li>
                        ))}
                    </ul>
                    <p><strong>Summary:</strong> {results.videoA.summary}</p>
                </div>
                <div>
                    <h3>Video B ({results.videoB.video_id})</h3>
                    {results.videoB.sentiment_distribution && (
                        <Pie data={chartDataB} />
                    )}
                    <h4>Top Comments:</h4>
                    <ul>
                        {results.videoB.top_comments && results.videoB.top_comments.map((comment, index) => (
                            <li key={index}>
                                <strong>{comment.author}:</strong> {comment.text} (Likes: {comment.likes})
                            </li>
                        ))}
                    </ul>
                    <p><strong>Summary:</strong> {results.videoB.summary}</p>
                </div>
            </div>
        </div>
    );
}

export default ComparisonResults;