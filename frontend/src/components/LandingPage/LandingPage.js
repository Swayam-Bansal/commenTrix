// src/LandingPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LandingPage.css'; // Your landing page CSS

function LandingPage({ setDataRetrieved, setComparisonResults, setSingleVideoResults }) {
    const [youtubeUrl1, setYoutubeUrl1] = useState('');
    const [youtubeUrl2, setYoutubeUrl2] = useState('');
    const navigate = useNavigate();
    const backendUrl = 'http://127.0.0.1:5000';

    const handleSubmit = async (e) => {
        e.preventDefault();
        setDataRetrieved(false); // Reset dataRetrieved on new submission
        setComparisonResults(null);
        setSingleVideoResults(null);

        const urls = [youtubeUrl1, youtubeUrl2].filter(url => url.trim() !== '');

        if (urls.length === 1) {
            const videoId = urls[0].split("v=")[1]?.split("&")[0];
            if (videoId) {
                try {
                    await axios.post(`${backendUrl}/comments/fetch`, { urls: [urls[0]] });
                    await axios.post(`${backendUrl}/analysis/run?url=${urls[0]}`, { video_ids: [videoId] });
                    const response = await axios.get(`${backendUrl}/analysis/single/${videoId}`);
                    setSingleVideoResults(response.data);
                    setDataRetrieved(true);
                    navigate('/video1'); // Or a dedicated single video dashboard route
                } catch (error) {
                    console.error("Error during single video analysis:", error);
                    alert("An error occurred during single video analysis.");
                }
            } else {
                alert("Could not extract video ID from the URL.");
            }
        } else if (urls.length === 2) {
            const videoIdA = urls[0].split("v=")[1]?.split("&")[0];
            const videoIdB = urls[1].split("v=")[1]?.split("&")[0];
            if (videoIdA && videoIdB) {
                try {
                    await axios.post(`${backendUrl}/comments/fetch`, { urls: [urls[0], urls[1]] });
                    await axios.post(`${backendUrl}/analysis/run?url=${urls[0]}`, { video_ids: [videoIdA] });
                    await axios.post(`${backendUrl}/analysis/run?url=${urls[1]}`, { video_ids: [videoIdB] });
                    const response = await axios.get(`${backendUrl}/analysis/compare?videoA=${videoIdA}&videoB=${videoIdB}`);
                    setComparisonResults(response.data);
                    setDataRetrieved(true);
                    navigate('/comparison');
                } catch (error) {
                    console.error("Error during comparison:", error);
                    alert("An error occurred during comparison.");
                }
            } else {
                alert("Could not extract video IDs from the URLs.");
            }
        } else {
            alert("Please enter one or two YouTube video URLs.");
        }
    };

    return (
        <div className="landing-page">
            <h1 className="landing-title">YouTube Video Analysis</h1>
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
                    <label htmlFor="youtubeUrl2">YouTube Video URL 2 (Optional):</label>
                    <input
                        type="text"
                        id="youtubeUrl2"
                        value={youtubeUrl2}
                        onChange={(e) => setYoutubeUrl2(e.target.value)}
                        placeholder="Enter second YouTube video URL (optional)"
                    />
                </div>
                <button type="submit">Retrieve Data</button>
            </form>
        </div>
    );
}

export default LandingPage;