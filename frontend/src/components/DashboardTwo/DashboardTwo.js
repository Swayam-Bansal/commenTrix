// src/Dashboard.js
import React from 'react';
import './DashboardTwo.css'; // Make sure you have corresponding CSS if needed.
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
} from 'recharts';

function DashboardTwo() {
  // Dummy data for charts
  const salesData = [
    { month: 'Jan', sales: 3000 },
    { month: 'Feb', sales: 4500 },
    { month: 'Mar', sales: 4000 },
    { month: 'Apr', sales: 5200 },
    { month: 'May', sales: 4700 },
    { month: 'Jun', sales: 6100 },
    { month: 'Jul', sales: 5800 },
    { month: 'Aug', sales: 6300 },
    { month: 'Sep', sales: 7200 },
    { month: 'Oct', sales: 6900 },
    { month: 'Nov', sales: 8100 },
    { month: 'Dec', sales: 7500 },
  ];

  const categoryData = [
    { name: 'Clothing', value: 31 },
    { name: 'Electronics', value: 28 },
    { name: 'Home & Garden', value: 19 },
    { name: 'Sports & Outdoors', value: 13 },
    { name: 'Books', value: 9 },
  ];
  const COLORS = ['#f06292', '#ffc658','#82ca9d']; // Negative, Neutral, Positive

  const channelData = [
    { channel: 'Online', sales: 5000 },
    { channel: 'In-Store', sales: 3000 },
    { channel: 'Wholesale', sales: 2000 },
    { channel: 'Other', sales: 1000 },
  ];

  return (
    <div className="dashboard">
      <h1 className="dashboard-title">Dashboard Overview</h1>

      {/* Stats Cards */}
      <div className="stats-cards">
        <div className="card">
          <h2>$12,345</h2>
          <p>Sales</p>
        </div>
        <div className="card">
          <h2>1,234</h2>
          <p>New Users</p>
        </div>
        <div className="card">
          <h2>567</h2>
          <p>Total Products</p>
        </div>
        <div className="card">
          <h2>12.5%</h2>
          <p>Conversion Rate</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="charts-row">
        {/* Sales Overview (Line Chart) */}
        <div className="chart-container">
          <h3>Sales Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={salesData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="#374151" strokeDasharray="3 3" />
              <XAxis dataKey="month" stroke="#CBD5E1" />
              <YAxis stroke="#CBD5E1" />
              <Tooltip />
              <Line type="monotone" dataKey="sales" stroke="#82ca9d" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Category Distribution (Pie Chart) */}
        <div className="chart-container">
          <h3>Category Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
                fill="#8884d8"
                label
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Sales by Channel (Bar Chart) */}
      <div className="chart-container bar-chart">
        <h3>Sales by Channel</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={channelData} margin={{ top: 20 }}>
            <CartesianGrid stroke="#374151" strokeDasharray="3 3" />
            <XAxis dataKey="channel" stroke="#CBD5E1" />
            <YAxis stroke="#CBD5E1" />
            <Tooltip />
            <Bar dataKey="sales" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default DashboardTwo;