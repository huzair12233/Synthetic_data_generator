import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useFiles } from '../contexts/FilesContext';
import LoadingSpinner from '../components/LoadingSpinner';

const ChatGeneration = () => {
  const navigate = useNavigate();
  const { fetchFiles } = useFiles();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    type: 'chat',
    domain: 'customer_support',
    numConversations: 10,
    avgMessagesPerConversation: 5,
    includeMetadata: true,
    format: 'json'
  });

  const types = [
    { value: 'chat', label: 'Chat Conversations' },
    { value: 'email', label: 'Emails' }
  ];

  const chatDomains = [
    { value: 'customer_support', label: 'Customer Support' },
    { value: 'chatbot_training', label: 'Chatbot Training' },
    { value: 'general_conversation', label: 'General Conversation' }
  ];

  const emailDomains = [
    { value: 'spam_detection', label: 'Spam Detection' },
    { value: 'business_communication', label: 'Business Communication' },
    { value: 'personal_emails', label: 'Personal Emails' }
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
      const response = await fetch('http://localhost:8000/api/v1/generate/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          domain: formData.domain,
          topic: formData.type,
          num_samples: formData.numConversations,
          num_turns: formData.avgMessagesPerConversation,
          format: formData.format
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate data');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `synthetic_${formData.type}_${formData.domain}_${Date.now()}.${formData.format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success('Synthetic chat data generated and downloaded successfully!');
      fetchFiles();
      navigate('/files');
    } catch (error) {
      console.error('Error generating data:', error);
      toast.error('Failed to generate synthetic data. Please try again.');
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
            Generate Synthetic Chat Data
          </h1>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Data Type
              </label>
              <select
                name="type"
                value={formData.type}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {types.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

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
                {formData.type === 'chat' 
                  ? chatDomains.map(domain => (
                      <option key={domain.value} value={domain.value}>
                        {domain.label}
                      </option>
                    ))
                  : emailDomains.map(domain => (
                      <option key={domain.value} value={domain.value}>
                        {domain.label}
                      </option>
                    ))
                }
              </select>
            </div>

            {/* Number of Conversations */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of {formData.type === 'chat' ? 'Conversations' : 'Emails'}
              </label>
              <input
                type="number"
                name="numConversations"
                value={formData.numConversations}
                onChange={handleInputChange}
                min="1"
                max="1000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-sm text-gray-500 mt-1">
                Enter a number between 1 and 1,000
              </p>
            </div>

            {/* Average Messages per Conversation */}
            {formData.type === 'chat' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Average Messages per Conversation
                </label>
                <input
                  type="number"
                  name="avgMessagesPerConversation"
                  value={formData.avgMessagesPerConversation}
                  onChange={handleInputChange}
                  min="2"
                  max="50"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Enter a number between 2 and 50
                </p>
              </div>
            )}

            {/* Include Metadata */}
            <div className="flex items-center">
              <input
                type="checkbox"
                name="includeMetadata"
                checked={formData.includeMetadata}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label className="ml-2 block text-sm text-gray-900">
                Include metadata (timestamps, user info, etc.)
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
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
              </select>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
            >
              {loading ? 'Generating...' : 'Generate Synthetic Chat Data'}
            </button>
          </form>

          {/* Info Section */}
          <div className="mt-8 p-4 bg-green-50 rounded-md">
            <h3 className="text-lg font-semibold text-green-900 mb-2">
              About Chat Data Generation
            </h3>
            <p className="text-green-800 text-sm">
              Generate synthetic chat conversations and emails for various use cases including customer support, 
              chatbot training, spam detection, and business communication. The generated data maintains 
              realistic conversation patterns while ensuring privacy and compliance.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatGeneration; 