import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';

// Layout
import Layout from './components/Layout/Layout';

// Auth Components
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import ProtectedRoute from './components/Auth/ProtectedRoute';

// Pages
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import Generate from './pages/Generate';
import Analytics from './pages/Analytics';
import Profile from './pages/Profile';
import Settings from './pages/Settings';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            
            {/* Protected routes */}
            <Route path="dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            
            <Route path="projects" element={
              <ProtectedRoute>
                <Projects />
              </ProtectedRoute>
            } />
            
            <Route path="projects/:id" element={
              <ProtectedRoute>
                <ProjectDetail />
              </ProtectedRoute>
            } />
            
            <Route path="generate" element={
              <ProtectedRoute>
                <Generate />
              </ProtectedRoute>
            } />
            
            <Route path="analytics" element={
              <ProtectedRoute>
                <Analytics />
              </ProtectedRoute>
            } />
            
            <Route path="profile" element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } />
            
            <Route path="settings" element={
              <ProtectedRoute>
                <Settings />
              </ProtectedRoute>
            } />
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;