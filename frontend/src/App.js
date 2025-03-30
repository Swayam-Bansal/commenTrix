// frontend/src/App.js
import React, { useState } from 'react';
import VideoInput from './components/videoInput';
import ComparisonResults from './components/ComparisonResults';
import SingleVideoResults from './components/SingleVideoResults';
import axios from 'axios';

function App() {
    const [comparisonResults, setComparisonResults] = useState(null);
    const [singleVideoResults, setSingleVideoResults] = useState(null);
    const backendUrl = 'http://127.0.0.1:5000';

    const handleCompare = async (urlA, urlB) => {
        setComparisonResults(null);
        setSingleVideoResults(null);

        const urls = [urlA, urlB].filter(url => url.trim() !== '');

        if (urls.length === 1) {
            const videoId = urls[0].split("v=")[1]?.split("&")[0];
            if (videoId) {
                try {
                    await axios.post(`${backendUrl}/comments/fetch`, { urls: [urls[0]] });
                    await axios.post(`${backendUrl}/analysis/run?url=${urls[0]}`, { video_ids: [videoId] });
                    const response = await axios.get(`${backendUrl}/analysis/single/${videoId}`);
                    setSingleVideoResults(response.data);
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
                    const response = await axios.get(`${backendUrl}/analysis/compare?videoA=${videoIdA}&videoB=${videoIdB}`);;
                    setComparisonResults(response.data);
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
        <div className="App">
            <h1>YouTube Video Comparison</h1>
            <VideoInput onCompare={handleCompare} />
            {comparisonResults && <ComparisonResults results={comparisonResults} />}
            {singleVideoResults && <SingleVideoResults results={singleVideoResults} />}
        </div>
    );
}

export default App;