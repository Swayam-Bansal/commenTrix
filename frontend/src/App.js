import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar/NavBar';
import LandingPage from './components/LandingPage/LandingPage';
import DashboardOne from './components/DashboardOne/DashboardOne';
import DashboardTwo from './components/DashboardTwo/DashboardTwo';
import Comparison from './components/Comparision/Comparision';


function App() {
    const [comparisonResults, setComparisonResults] = useState(null);
    const [singleVideoResults, setSingleVideoResults] = useState(null);
    const [dataRetrieved, setDataRetrieved] = useState(false);

    return (
        <Router>
            <NavBar dataRetrieved={dataRetrieved} />
            <Routes>
                <Route path="/" element={<LandingPage setDataRetrieved={setDataRetrieved} setComparisonResults={setComparisonResults} setSingleVideoResults={setSingleVideoResults} />} />
                <Route path="/video1" element={<DashboardOne results={singleVideoResults} />} />
                <Route path="/video2" element={<DashboardTwo results={singleVideoResults} />} />
                <Route path="/comparison" element={<Comparison results={comparisonResults} />} />
            </Routes>
        </Router>
    );
}

export default App;