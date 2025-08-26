import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  SparklesIcon,
  FolderIcon,
  PhotoIcon,
  ChartBarIcon,
  PlusIcon,
  ArrowRightIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';
import { projectsAPI, contentAPI } from '../utils/api';
import { formatDate } from '../utils/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    projects: 0,
    generations: 0,
    totalImages: 0,
    successRate: 0
  });
  const [recentProjects, setRecentProjects] = useState([]);
  const [recentGenerations, setRecentGenerations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch projects
      const projectsResponse = await projectsAPI.getProjects({ limit: 5 });
      const projects = projectsResponse.data;
      setRecentProjects(projects);
      
      // Fetch recent generations
      const generationsResponse = await contentAPI.getGenerations({ limit: 10 });
      const generations = generationsResponse.data;
      setRecentGenerations(generations);
      
      // Calculate stats
      const completedGenerations = generations.filter(g => g.status === 'completed');
      const successRate = generations.length > 0 ? (completedGenerations.length / generations.length) * 100 : 0;
      
      setStats({
        projects: projects.length,
        generations: generations.length,
        totalImages: completedGenerations.length,
        successRate: Math.round(successRate)
      });
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Create Project',
      description: 'Start a new marketing project',
      icon: FolderIcon,
      href: '/projects',
      color: 'from-primary-500 to-primary-600',
      action: 'create'
    },
    {
      title: 'Generate Content',
      description: 'Create AI-powered content',
      icon: SparklesIcon,
      href: '/generate',
      color: 'from-secondary-500 to-secondary-600'
    },
    {
      title: 'Upload Images',
      description: 'Add product photos',
      icon: PhotoIcon,
      href: '/projects',
      color: 'from-accent-500 to-accent-600'
    },
    {
      title: 'View Analytics',
      description: 'Check performance metrics',
      icon: ChartBarIcon,
      href: '/analytics',
      color: 'from-green-500 to-green-600'
    }
  ];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'processing':
        return <ClockIcon className="w-5 h-5 text-yellow-500 animate-spin" />;
      case 'failed':
        return <ExclamationTriangleIcon className="w-5 h-5 text-red-500" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'status-success';
      case 'processing':
        return 'status-warning';
      case 'failed':
        return 'status-error';
      default:
        return 'status-info';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.full_name || user?.username}! 👋
          </h1>
          <p className="text-gray-600">
            Here's what's happening with your AI marketing projects today.
          </p>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Projects</p>
                <p className="text-3xl font-bold text-gray-900">{stats.projects}</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <FolderIcon className="w-6 h-6 text-primary-600" />
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Generations</p>
                <p className="text-3xl font-bold text-gray-900">{stats.generations}</p>
              </div>
              <div className="w-12 h-12 bg-secondary-100 rounded-xl flex items-center justify-center">
                <SparklesIcon className="w-6 h-6 text-secondary-600" />
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Images Created</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalImages}</p>
              </div>
              <div className="w-12 h-12 bg-accent-100 rounded-xl flex items-center justify-center">
                <PhotoIcon className="w-6 h-6 text-accent-600" />
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Success Rate</p>
                <p className="text-3xl font-bold text-gray-900">{stats.successRate}%</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <ChartBarIcon className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <Link
                  key={index}
                  to={action.href}
                  className="card p-6 hover-lift group transition-all duration-300"
                >
                  <div className={`w-12 h-12 bg-gradient-to-br ${action.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">{action.title}</h3>
                  <p className="text-sm text-gray-600">{action.description}</p>
                </Link>
              );
            })}
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Projects */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">Recent Projects</h2>
              <Link
                to="/projects"
                className="text-primary-600 hover:text-primary-700 font-medium text-sm flex items-center group"
              >
                View all
                <ArrowRightIcon className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform duration-200" />
              </Link>
            </div>

            {recentProjects.length > 0 ? (
              <div className="space-y-4">
                {recentProjects.map((project) => (
                  <Link
                    key={project.id}
                    to={`/projects/${project.id}`}
                    className="flex items-center p-4 rounded-xl hover:bg-gray-50 transition-colors duration-200 group"
                  >
                    <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mr-4">
                      <FolderIcon className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 group-hover:text-primary-600 transition-colors duration-200">
                        {project.name}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {project.description || 'No description'}
                      </p>
                    </div>
                    <div className="text-xs text-gray-400">
                      {formatDate(project.created_at)}
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <FolderIcon className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">No projects yet</p>
                <Link
                  to="/projects"
                  className="btn-primary inline-flex items-center"
                >
                  <PlusIcon className="w-4 h-4 mr-2" />
                  Create Your First Project
                </Link>
              </div>
            )}
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="card p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">Recent Activity</h2>
              <Link
                to="/generate"
                className="text-primary-600 hover:text-primary-700 font-medium text-sm flex items-center group"
              >
                Generate more
                <ArrowRightIcon className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform duration-200" />
              </Link>
            </div>

            {recentGenerations.length > 0 ? (
              <div className="space-y-4">
                {recentGenerations.slice(0, 5).map((generation) => (
                  <div
                    key={generation.id}
                    className="flex items-center p-4 rounded-xl hover:bg-gray-50 transition-colors duration-200"
                  >
                    <div className="mr-4">
                      {getStatusIcon(generation.status)}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 capitalize">
                        {generation.content_type.replace('_', ' ')}
                      </h3>
                      <p className="text-sm text-gray-500 truncate">
                        {generation.prompt || 'No prompt'}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className={`${getStatusColor(generation.status)} capitalize`}>
                        {generation.status}
                      </span>
                      <p className="text-xs text-gray-400 mt-1">
                        {formatDate(generation.created_at)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <SparklesIcon className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">No content generated yet</p>
                <Link
                  to="/generate"
                  className="btn-primary inline-flex items-center"
                >
                  <SparklesIcon className="w-4 h-4 mr-2" />
                  Start Generating
                </Link>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;