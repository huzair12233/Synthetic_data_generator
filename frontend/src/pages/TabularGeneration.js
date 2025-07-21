import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useFiles } from '../contexts/FilesContext';
import LoadingSpinner from '../components/LoadingSpinner';

const TabularGeneration = () => {
  const navigate = useNavigate();
  const { fetchFiles } = useFiles();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    domain: 'ecommerce',
    numRecords: 100,
    includeHeaders: true,
    format: 'csv'
  });

  const domains = [
    { value: 'ecommerce', label: 'E-commerce' },
    { value: 'education', label: 'Education' },
    { value: 'finance', label: 'Finance' },
    { value: 'medical', label: 'Medical' }
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      
      // Create AbortController for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
      
      const response = await fetch('http://localhost:8000/api/v1/generate/tabular', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          domain: formData.domain,
          num_samples: formData.numRecords,
          format: formData.format
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Response error:', response.status, errorText);
        throw new Error(`Failed to generate data: ${response.status} ${errorText}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `synthetic_${formData.domain}_${Date.now()}.${formData.format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success('Synthetic data generated and downloaded successfully!');
      fetchFiles();
      navigate('/files');
    } catch (error) {
      console.error('Error generating data:', error);
      if (error.name === 'AbortError') {
        toast.error('Request timed out. Please try again with fewer records.');
      } else {
        toast.error(`Failed to generate synthetic data: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            Generate Synthetic Tabular Data
          </h1>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Domain Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Domain
              </label>
              <select
                name="domain"
                value={formData.domain}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {domains.map(domain => (
                  <option key={domain.value} value={domain.value}>
                    {domain.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Number of Records */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Records
              </label>
              <input
                type="number"
                name="numRecords"
                value={formData.numRecords}
                onChange={handleInputChange}
                min="1"
                max="10000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-sm text-gray-500 mt-1">
                Enter a number between 1 and 10,000
              </p>
            </div>

            {/* Include Headers */}
            <div className="flex items-center">
              <input
                type="checkbox"
                name="includeHeaders"
                checked={formData.includeHeaders}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label className="ml-2 block text-sm text-gray-900">
                Include column headers
              </label>
            </div>

            {/* Format Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Output Format
              </label>
              <select
                name="format"
                value={formData.format}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="csv">CSV</option>
                <option value="json">JSON</option>
                <option value="excel">Excel</option>
              </select>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
            >
              {loading ? 'Generating...' : 'Generate Synthetic Data'}
            </button>
          </form>

          {/* Info Section */}
          <div className="mt-8 p-4 bg-blue-50 rounded-md">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">
              About Tabular Data Generation
            </h3>
            <p className="text-blue-800 text-sm">
              Generate synthetic tabular data for various domains including e-commerce, education, finance, and medical data. 
              The generated data maintains statistical properties similar to real datasets while ensuring privacy and compliance.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TabularGeneration; 