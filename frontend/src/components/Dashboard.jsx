import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import api from '../api';

const Dashboard = () => {
    const [stats, setStats] = useState([]);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const res = await api.get('/status');
            setIsAuthenticated(res.data.authenticated);
            if (res.data.authenticated) {
                fetchStats();
            }
        } catch (error) {
            console.error("Auth check failed", error);
        }
    };

    const fetchStats = async () => {
        try {
            const res = await api.get('/stats?days=30');
            setStats(res.data);
        } catch (error) {
            console.error("Failed to fetch stats", error);
        }
    };

    const handleSync = async () => {
        setLoading(true);
        try {
            await api.post('/sync');
            await fetchStats();
        } catch (error) {
            console.error("Sync failed", error);
        }
        setLoading(false);
    };

    if (!isAuthenticated) {
        return (
            <div className="flex flex-col items-center justify-center h-screen">
                <h1 className="text-3xl font-bold mb-8">Gmail Tracking Dashboard</h1>
                <a href="http://localhost:8000/login" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Login with Google
                </a>
            </div>
        );
    }

    const todayCount = stats.length > 0 ? stats[stats.length - 1].count : 0;
    const last7Days = stats.slice(-7).reduce((acc, curr) => acc + curr.count, 0);
    const last15Days = stats.slice(-15).reduce((acc, curr) => acc + curr.count, 0);
    const last30Days = stats.slice(-30).reduce((acc, curr) => acc + curr.count, 0);
    const totalReplied = stats.reduce((acc, curr) => acc + (curr.replied_count || 0), 0);
    const replyRate = stats.reduce((acc, curr) => acc + curr.count, 0) > 0 
        ? ((totalReplied / stats.reduce((acc, curr) => acc + curr.count, 0)) * 100).toFixed(1) 
        : 0;

    return (
        <div className="container mx-auto p-4">
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">Email Dashboard</h1>
                <div className="flex items-center gap-4">
                    <div className="text-right">
                        <p className="text-sm text-gray-500">Avg Reply Rate</p>
                        <p className="text-xl font-bold text-blue-600">{replyRate}%</p>
                    </div>
                    <button 
                        onClick={handleSync} 
                        disabled={loading}
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                    >
                        {loading ? 'Syncing...' : 'Sync Now'}
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-gray-500 text-sm">Today</h3>
                    <p className="text-3xl font-bold">{todayCount}</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-gray-500 text-sm">Last 7 Days</h3>
                    <p className="text-3xl font-bold">{last7Days}</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-gray-500 text-sm">Last 15 Days</h3>
                    <p className="text-3xl font-bold">{last15Days}</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-gray-500 text-sm">Last 30 Days</h3>
                    <p className="text-3xl font-bold">{last30Days}</p>
                </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md h-96 mb-8">
                <h3 className="text-xl font-bold mb-4">Sent Emails Trend</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={stats}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="count" stroke="#8884d8" name="Sent" />
                        <Line type="monotone" dataKey="replied_count" stroke="#82ca9d" name="Replies" />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-bold mb-4">Last 7 Days Analysis</h3>
                <div className="overflow-x-auto">
                    <table className="min-w-full table-auto">
                        <thead>
                            <tr className="bg-gray-100">
                                <th className="px-4 py-2 text-left">Date</th>
                                <th className="px-4 py-2 text-left">Sent</th>
                                <th className="px-4 py-2 text-left">Replies</th>
                                <th className="px-4 py-2 text-left">Rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            {stats.slice(-7).reverse().map((stat, index) => (
                                <tr key={index} className="border-b">
                                    <td className="px-4 py-2">{stat.date}</td>
                                    <td className="px-4 py-2 font-bold">{stat.count}</td>
                                    <td className="px-4 py-2 text-green-600 font-bold">{stat.replied_count || 0}</td>
                                    <td className="px-4 py-2 text-gray-500">
                                        {stat.count > 0 ? (( (stat.replied_count || 0) / stat.count) * 100).toFixed(0) : 0}%
                                    </td>
                                </tr>
                            ))}
                            {stats.length === 0 && (
                                <tr>
                                    <td colSpan="4" className="px-4 py-2 text-center text-gray-500">No data available</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
