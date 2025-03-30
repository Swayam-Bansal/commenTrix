// frontend/src/components/SingleVideoResults.js
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

function SingleVideoResults({ results }) {
    if (!results || !results.video_id) {
        return <p>No analysis results available yet.</p>;
    }

    const chartData = {
        labels: Object.keys(results.sentiment_distribution),
        datasets: [
            {
                label: 'Sentiment Distribution',
                data: Object.values(results.sentiment_distribution),
                backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
            },
        ],
    };

    return (
        <div>
            <h2>Analysis Results for Video: {results.video_id}</h2>
            {results.sentiment_distribution && (
                <Pie data={chartData} />
            )}
            <h4>Top Comments:</h4>
            <ul>
                {results.top_comments && results.top_comments.map((comment, index) => (
                    <li key={index}>
                        <strong>{comment.author}:</strong> {comment.text} (Likes: {comment.likes})
                    </li>
                ))}
            </ul>
            <p><strong>Summary:</strong> {results.summary}</p>
        </div>
    );
}

export default SingleVideoResults;