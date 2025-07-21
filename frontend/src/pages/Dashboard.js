import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useFiles } from '../contexts/FilesContext';
import { 
  Brain, 
  Database, 
  MessageSquare, 
  FileText, 
  Download, 
  TrendingUp,
  Sparkles,
  ArrowRight
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const { files, loading, fetchFiles, calculateStats } = useFiles();
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Calculate stats whenever files change
    const calculatedStats = calculateStats();
    setStats(calculatedStats);
  }, [files, calculateStats]);

  const handleRefresh = async () => {
    await fetchFiles();
  };

  const features = [
    {
      title: 'Tabular Data',
      description: 'Generate structured data for Ecommerce, Education, Finance, and Medical domains',
      icon: Database,
      href: '/tabular',
      color: 'bg-blue-500',
    },
    {
      title: 'Chat Data',
      description: 'Create synthetic conversations and emails for training and testing',
      icon: MessageSquare,
      href: '/chat',
      color: 'bg-green-500',
    },
    {
      title: 'My Files',
      description: 'View and download all your generated synthetic data files',
      icon: FileText,
      href: '/files',
      color: 'bg-purple-500',
    },
  ];

  const StatCard = ({ title, value, icon: Icon, color }) => (
    <div className="card-hover">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${color} text-white`}>
          <Icon className="w-6 h-6" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">
            {loading ? '...' : value}
          </p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Welcome Section */}
      <div className="text-center mb-12">
        <div className="flex justify-center mb-4">
          <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-3xl">
            <Sparkles className="w-10 h-10 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to SmartSynth, {user?.username}! 👋
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-6">
          Generate high-quality synthetic data for your AI and machine learning projects
        </p>
        <button
          onClick={handleRefresh}
          disabled={loading}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Updating...
            </>
          ) : (
            <>
              <TrendingUp className="w-4 h-4 mr-2" />
              Refresh Stats
            </>
          )}
        </button>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <StatCard
          title="Total Files"
          value={stats?.total_files || 0}
          icon={FileText}
          color="bg-blue-500"
        />
        {/* <StatCard
          title="Total Downloads"
          value={stats?.total_downloads || 0}
          icon={Download}
          color="bg-green-500"
        /> */}
        <StatCard
          title="Total Generations"
          value={stats?.total_generations || 0}
          icon={TrendingUp}
          color="bg-purple-500"
        />
      </div>

      {/* Features Section */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          What would you like to generate today?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link
                key={feature.title}
                to={feature.href}
                className="card-hover group"
              >
                <div className="flex items-start">
                  <div className={`p-4 rounded-xl ${feature.color} text-white group-hover:scale-110 transition-transform duration-200`}>
                    <Icon className="w-8 h-8" />
                  </div>
                  <div className="ml-4 flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors duration-200">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 mb-4">
                      {feature.description}
                    </p>
                    <div className="flex items-center text-primary-600 font-medium group-hover:translate-x-1 transition-transform duration-200">
                      Get Started
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Quick Actions
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            to="/tabular"
            className="flex items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors duration-200"
          >
            <Database className="w-5 h-5 text-blue-600 mr-3" />
            <span className="font-medium text-blue-900">Generate Tabular Data</span>
          </Link>
          <Link
            to="/chat"
            className="flex items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors duration-200"
          >
            <MessageSquare className="w-5 h-5 text-green-600 mr-3" />
            <span className="font-medium text-green-900">Generate Chat Data</span>
          </Link>
          <Link
            to="/files"
            className="flex items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors duration-200"
          >
            <FileText className="w-5 h-5 text-purple-600 mr-3" />
            <span className="font-medium text-purple-900">View My Files</span>
          </Link>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200"
          >
            <Brain className="w-5 h-5 text-gray-600 mr-3" />
            <span className="font-medium text-gray-900">API Documentation</span>
          </a>
        </div>
      </div>

      {/* Data Type Breakdown */}
      {stats?.data_type_distribution && Object.keys(stats.data_type_distribution).length > 0 && (
        <div className="card mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Your Data Generation Breakdown
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(stats.data_type_distribution).map(([type, count]) => (
              <div key={type} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-700 capitalize">
                  {type.replace('_', ' ')}
                </span>
                <span className="text-2xl font-bold text-primary-600">
                  {count}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 