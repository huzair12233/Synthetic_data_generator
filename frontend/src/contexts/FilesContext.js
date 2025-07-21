import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import toast from 'react-hot-toast';

const FilesContext = createContext();

export const useFiles = () => {
  const context = useContext(FilesContext);
  if (!context) {
    throw new Error('useFiles must be used within a FilesProvider');
  }
  return context;
};

export const FilesProvider = ({ children }) => {
  const { user } = useAuth();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchFiles = async () => {
    // Don't fetch if no user is logged in
    if (!user) {
      setFiles([]);
      return;
    }

    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/files', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch files');
      }

      const data = await response.json();
      setFiles(data.files || []);
    } catch (error) {
      console.error('Error fetching files:', error);
      toast.error('Failed to load files');
      setFiles([]);
    } finally {
      setLoading(false);
    }
  };

  const deleteFile = async (fileId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/files/${fileId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete file');
      }

      setFiles(files.filter(file => file._id !== fileId));
      toast.success('File deleted successfully!');
      return true;
    } catch (error) {
      console.error('Error deleting file:', error);
      toast.error('Failed to delete file');
      return false;
    }
  };

  const downloadFile = async (fileId, filename) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/files/${fileId}/download`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to download file');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success('File downloaded successfully!');
      
      // Refresh files to update download count
      await fetchFiles();
      return true;
    } catch (error) {
      console.error('Error downloading file:', error);
      toast.error('Failed to download file');
      return false;
    }
  };

  // Calculate stats from files
  const calculateStats = () => {
    const totalFiles = files.length;
    const totalDownloads = files.reduce((sum, file) => sum + (file.download_count || 0), 0);
    
    // Count by data type
    const dataTypeDistribution = {};
    files.forEach(file => {
      const dataType = file.data_type || 'unknown';
      dataTypeDistribution[dataType] = (dataTypeDistribution[dataType] || 0) + 1;
    });

    // Count by file type
    const fileTypeDistribution = {};
    files.forEach(file => {
      const fileType = file.file_type || 'unknown';
      fileTypeDistribution[fileType] = (fileTypeDistribution[fileType] || 0) + 1;
    });

    return {
      total_files: totalFiles,
      total_downloads: totalDownloads,
      total_generations: totalFiles, // Each file represents one generation
      data_type_distribution: dataTypeDistribution,
      file_type_distribution: fileTypeDistribution
    };
  };

  // Reset files when user changes
  useEffect(() => {
    if (user) {
      // User is logged in, fetch their files
      fetchFiles();
    } else {
      // User is logged out, clear files
      setFiles([]);
      setLoading(false);
    }
  }, [user]); // This will trigger when user changes

  const value = {
    files,
    loading,
    fetchFiles,
    deleteFile,
    downloadFile,
    calculateStats
  };

  return (
    <FilesContext.Provider value={value}>
      {children}
    </FilesContext.Provider>
  );
}; 