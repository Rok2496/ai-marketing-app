import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../utils/api';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      const savedUser = localStorage.getItem('user');
      
      if (token && savedUser) {
        try {
          // Verify token is still valid
          const response = await authAPI.getProfile();
          const userData = response.data;
          setUser(userData);
          setIsAuthenticated(true);
          localStorage.setItem('user', JSON.stringify(userData));
        } catch (error) {
          // Token is invalid, clear storage
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          setUser(null);
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await authAPI.login(credentials);
      const { access_token } = response.data;
      
      // Store token
      localStorage.setItem('token', access_token);
      
      // Get user profile
      const profileResponse = await authAPI.getProfile();
      const userData = profileResponse.data;
      
      setUser(userData);
      setIsAuthenticated(true);
      localStorage.setItem('user', JSON.stringify(userData));
      
      toast.success(`Welcome back, ${userData.full_name || userData.username}!`);
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      let message = 'Login failed';
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          message = error.response.data.detail.map(err => {
            if (typeof err === 'string') return err;
            return err.msg || err.message || 'Validation error';
          }).join(', ');
        } else if (typeof error.response.data.detail === 'string') {
          message = error.response.data.detail;
        } else {
          message = 'Login failed';
        }
      } else if (error.response?.data?.message) {
        message = error.response.data.message;
      } else if (error.message) {
        message = error.message;
      }
      
      toast.error(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      await authAPI.register(userData);
      
      // Auto-login after registration
      const loginResult = await login({
        username: userData.username,
        password: userData.password,
      });
      
      if (loginResult.success) {
        toast.success('Account created successfully!');
      }
      
      return loginResult;
    } catch (error) {
      console.error('Registration error:', error);
      let message = 'Registration failed';
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          message = error.response.data.detail.map(err => {
            if (typeof err === 'string') return err;
            return err.msg || err.message || 'Validation error';
          }).join(', ');
        } else if (typeof error.response.data.detail === 'string') {
          message = error.response.data.detail;
        } else {
          message = 'Registration failed';
        }
      } else if (error.response?.data?.message) {
        message = error.response.data.message;
      } else if (error.message) {
        message = error.message;
      }
      
      toast.error(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
    setIsAuthenticated(false);
    toast.success('Logged out successfully');
  };

  const updateUser = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};