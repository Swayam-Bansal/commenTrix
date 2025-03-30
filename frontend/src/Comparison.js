// src/Comparison.js
import React from 'react';
import './Comparison.css'; // Reusing the styling from DashboardTwo for a similar look
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend,
} from 'recharts';

function Comparison() {
  // Sales Overview Comparison Data (Line Chart)
  const salesComparisonData = [
    { month: 'Jan', video1: 3000, video2: 3200 },
    { month: 'Feb', video1: 4500, video2: 4200 },
    { month: 'Mar', video1: 4000, video2: 3800 },
    { month: 'Apr', video1: 5200, video2: 5000 },
    { month: 'May', video1: 4700, video2: 4900 },
    { month: 'Jun', video1: 6100, video2: 6000 },
    { month: 'Jul', video1: 5800, video2: 5900 },
    { month: 'Aug', video1: 6300, video2: 6400 },
    { month: 'Sep', video1: 7200, video2: 7000 },
    { month: 'Oct', video1: 6900, video2: 6800 },
    { month: 'Nov', video1: 8100, video2: 8000 },
    { month: 'Dec', video1: 7500, video2: 7600 },
  ];

  // Category Distribution Comparison Data (Grouped Bar Chart)
  const categoryComparisonData = [
    { category: 'Clothing', video1: 31, video2: 29 },
    { category: 'Electronics', video1: 28, video2: 30 },
    { category: 'Home & Garden', video1: 19, video2: 18 },
    { category: 'Sports & Outdoors', video1: 13, video2: 14 },
    { category: 'Books', video1: 9, video2: 9 },
  ];

  // Sales by Channel Comparison Data (Grouped Bar Chart)
  const channelComparisonData = [
    { channel: 'Online', video1: 5000, video2: 5200 },
    { channel: 'In-Store', video1: 3000, video2: 2900 },
    { channel: 'Wholesale', video1: 2000, video2: 2100 },
    { channel: 'Other', video1: 1000, video2: 1100 },
  ];

  // Colors for Video 1 and Video 2
  const colors = {
    video1: '#82ca9d',
    video2: '#8884d8',
  };

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">Comparison of Video 1 and Video 2</h1>
      <p>Below are the comparison graphs for both videos.</p>

      {/* Sales Overview (Line Chart) */}
      <div className="chart-container">
        <h3>Sales Overview Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={salesComparisonData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#374151" strokeDasharray="3 3" />
            <XAxis dataKey="month" stroke="#CBD5E1" />
            <YAxis stroke="#CBD5E1" />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="video1" stroke={colors.video1} strokeWidth={2} name="Video 1" />
            <Line type="monotone" dataKey="video2" stroke={colors.video2} strokeWidth={2} name="Video 2" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Category Distribution (Grouped Bar Chart) */}
      <div className="chart-container">
        <h3>Category Distribution Comparison (%)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={categoryComparisonData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#374151" strokeDasharray="3 3" />
            <XAxis dataKey="category" stroke="#CBD5E1" />
            <YAxis stroke="#CBD5E1" />
            <Tooltip />
            <Legend />
            <Bar dataKey="video1" fill={colors.video1} name="Video 1" />
            <Bar dataKey="video2" fill={colors.video2} name="Video 2" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Sales by Channel (Grouped Bar Chart) */}
      <div className="chart-container">
        <h3>Sales by Channel Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={channelComparisonData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#374151" strokeDasharray="3 3" />
            <XAxis dataKey="channel" stroke="#CBD5E1" />
            <YAxis stroke="#CBD5E1" />
            <Tooltip />
            <Legend />
            <Bar dataKey="video1" fill={colors.video1} name="Video 1" />
            <Bar dataKey="video2" fill={colors.video2} name="Video 2" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Comparison;
