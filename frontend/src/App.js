// frontend/src/App.js
import React, { useState } from 'react';
import VideoInput from './components/videoInput';
import ComparisonResults from './components/ComparisonResults';
import axios from 'axios';

function App() {
    const [comparisonResults, setComparisonResults] = useState(null);
    const backendUrl = 'http://127.0.0.1:5000'; // Your Flask backend URL

    const handleCompare = async (urlA, urlB) => {
      try {
          // Fetch comments for both videos
          await axios.post(`${backendUrl}/comments/fetch`, { urls: [urlA, urlB] });
          console.log("Comments fetched.");
  
          // Trigger analysis
          const videoIdA = urlA.split("v=")[1]?.split("&")[0];
          const videoIdB = urlB.split("v=")[1]?.split("&")[0];
          if (videoIdA && videoIdB) {
              await axios.post(`${backendUrl}/analysis/run?url=${urlA}`, { video_ids: [videoIdA] });
              await axios.post(`${backendUrl}/analysis/run?url=${urlB}`, { video_ids: [videoIdB] });
              console.log("Analysis run.");
  
              // Fetch comparison results
              const response = await axios.get(`${backendUrl}/analysis/compare?videoA=${videoIdA}&videoB=${videoIdB}`);
              setComparisonResults(response.data);
          } else {
              alert("Could not extract video IDs from URLs.");
          }
  
      } catch (error) {
          console.error("Error during comparison:", error);
          alert("An error occurred while fetching or comparing videos.");
      }
  };

    return (
        <div className="App">
            <h1>YouTube Video Comparison</h1>
            <VideoInput onCompare={handleCompare} />
            {comparisonResults && <ComparisonResults results={comparisonResults} />}
        </div>
    );
}

export default App;