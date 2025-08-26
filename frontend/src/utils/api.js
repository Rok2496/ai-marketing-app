import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    } else if (error.response?.status === 429) {
      // Rate limit exceeded
      toast.error('Rate limit exceeded. Please try again later.');
    } else if (error.response?.status >= 500) {
      // Server error
      toast.error('Server error. Please try again later.');
    } else if (error.code === 'ECONNABORTED') {
      // Timeout
      toast.error('Request timeout. Please try again.');
    } else if (!error.response) {
      // Network error
      toast.error('Network error. Please check your connection.');
    }
    
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: (credentials) => {
    // Convert to form data for OAuth2PasswordRequestForm
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  register: (userData) => api.post('/auth/register', userData),
  getProfile: () => api.get('/auth/me'),
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

// Projects API calls
export const projectsAPI = {
  getProjects: (params = {}) => api.get('/projects', { params }),
  getProject: (id) => api.get(`/projects/${id}`),
  createProject: (data) => api.post('/projects', data),
  updateProject: (id, data) => api.put(`/projects/${id}`, data),
  deleteProject: (id) => api.delete(`/projects/${id}`),
  uploadImage: (projectId, formData) => {
    return api.post(`/projects/${projectId}/images`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getProjectImages: (projectId) => api.get(`/projects/${projectId}/images`),
  deleteImage: (projectId, imageId) => api.delete(`/projects/${projectId}/images/${imageId}`),
  setPrimaryImage: (projectId, imageId) => api.put(`/projects/${projectId}/images/${imageId}/primary`),
};

// Content Generation API calls
export const contentAPI = {
  generateTextToImage: (data) => api.post('/content/text-to-image', data),
  generateProductRender: (formData) => {
    return api.post('/content/product-render', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  generateSEOContent: (data) => api.post('/content/seo-content', data),
  generateContentPlan: (data) => api.post('/content/content-plan', data),
  generateMarketingPlan: (data) => api.post('/content/marketing-plan', data),
  getGenerations: (params = {}) => api.get('/content/generations', { params }),
  getGeneration: (id) => api.get(`/content/generations/${id}`),
};

// Admin API calls
export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getAPIKeyStatus: () => api.get('/admin/api-keys/status'),
  rotateAPIKey: () => api.post('/admin/api-keys/rotate'),
  resetAPIKeyStatus: (keyIndex) => api.post(`/admin/api-keys/${keyIndex}/reset`),
  getUsers: (params = {}) => api.get('/admin/users', { params }),
  toggleUserActive: (userId) => api.put(`/admin/users/${userId}/toggle-active`),
};

// Utility functions
export const downloadImage = async (imageUrl, filename = 'generated-image.png') => {
  try {
    const response = await fetch(imageUrl);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    toast.success('Image downloaded successfully!');
  } catch (error) {
    console.error('Download failed:', error);
    toast.error('Failed to download image');
  }
};

export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  } catch (error) {
    console.error('Copy failed:', error);
    toast.error('Failed to copy to clipboard');
  }
};

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export default api;