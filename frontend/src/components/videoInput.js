// frontend/src/components/VideoInput.js
import React, { useState } from 'react';

function VideoInput({ onCompare }) {
    const [urlA, setUrlA] = useState('');
    const [urlB, setUrlB] = useState('');

    const handleCompareClick = () => {
        onCompare(urlA, urlB);
    };

    return (
        <div>
            <h2>Enter YouTube Video URLs</h2>
            <div>
                <label htmlFor="urlA">Video A URL:</label>
                <input
                    type="text"
                    id="urlA"
                    value={urlA}
                    onChange={(e) => setUrlA(e.target.value)}
                    placeholder="Enter URL for Video A"
                />
            </div>
            <div>
                <label htmlFor="urlB">Video B URL:</label>
                <input
                    type="text"
                    id="urlB"
                    value={urlB}
                    onChange={(e) => setUrlB(e.target.value)}
                    placeholder="Enter URL for Video B"
                />
            </div>
            <button onClick={handleCompareClick}>Compare Videos</button>
        </div>
    );
}

export default VideoInput;