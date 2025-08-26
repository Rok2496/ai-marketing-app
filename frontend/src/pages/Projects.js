import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  PlusIcon,
  FolderIcon,
  PhotoIcon,
  EllipsisVerticalIcon,
  TrashIcon,
  PencilIcon,
  EyeIcon
} from '@heroicons/react/24/outline';
import { projectsAPI } from '../utils/api';
import { formatDate } from '../utils/api';
import toast from 'react-hot-toast';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await projectsAPI.getProjects();
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
      toast.error('Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProject = async (projectId) => {
    try {
      await projectsAPI.deleteProject(projectId);
      setProjects(projects.filter(p => p.id !== projectId));
      setShowDeleteModal(false);
      setSelectedProject(null);
      toast.success('Project deleted successfully');
    } catch (error) {
      console.error('Error deleting project:', error);
      toast.error('Failed to delete project');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading projects...</p>
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
          className="flex justify-between items-center mb-8"
        >
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Projects</h1>
            <p className="text-gray-600">
              Manage your marketing projects and product campaigns
            </p>
          </div>
          
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-primary flex items-center"
          >
            <PlusIcon className="w-5 h-5 mr-2" />
            New Project
          </button>
        </motion.div>

        {/* Projects Grid */}
        {projects.length > 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {projects.map((project, index) => (
              <motion.div
                key={project.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card p-6 hover-lift group relative"
              >
                {/* Project Actions */}
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  <div className="relative">
                    <button
                      onClick={() => setSelectedProject(project)}
                      className="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
                    >
                      <EllipsisVerticalIcon className="w-5 h-5 text-gray-400" />
                    </button>
                    
                    {selectedProject?.id === project.id && (
                      <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-10">
                        <Link
                          to={`/projects/${project.id}`}
                          className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                          onClick={() => setSelectedProject(null)}
                        >
                          <EyeIcon className="w-4 h-4 mr-3" />
                          View Details
                        </Link>
                        <button
                          className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                          onClick={() => {
                            setSelectedProject(null);
                            // Add edit functionality
                          }}
                        >
                          <PencilIcon className="w-4 h-4 mr-3" />
                          Edit Project
                        </button>
                        <button
                          className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                          onClick={() => {
                            setShowDeleteModal(true);
                          }}
                        >
                          <TrashIcon className="w-4 h-4 mr-3" />
                          Delete Project
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                <Link to={`/projects/${project.id}`} className="block">
                  {/* Project Icon */}
                  <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <FolderIcon className="w-8 h-8 text-white" />
                  </div>

                  {/* Project Info */}
                  <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors duration-200">
                    {project.name}
                  </h3>
                  
                  <p className="text-gray-600 mb-4 line-clamp-2">
                    {project.description || 'No description provided'}
                  </p>

                  {/* Project Meta */}
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center">
                      <PhotoIcon className="w-4 h-4 mr-1" />
                      <span>{project.product_images?.length || 0} images</span>
                    </div>
                    <span>{formatDate(project.created_at)}</span>
                  </div>

                  {/* Category Badge */}
                  {project.product_category && (
                    <div className="mt-3">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        {project.product_category}
                      </span>
                    </div>
                  )}
                </Link>
              </motion.div>
            ))}
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-center py-16"
          >
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <FolderIcon className="w-12 h-12 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No projects yet
            </h3>
            <p className="text-gray-600 mb-8 max-w-md mx-auto">
              Create your first project to start organizing your marketing campaigns and product content.
            </p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="w-5 h-5 mr-2" />
              Create Your First Project
            </button>
          </motion.div>
        )}

        {/* Create Project Modal */}
        <CreateProjectModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onSuccess={(newProject) => {
            setProjects([newProject, ...projects]);
            setShowCreateModal(false);
          }}
        />

        {/* Delete Confirmation Modal */}
        <DeleteConfirmationModal
          isOpen={showDeleteModal}
          project={selectedProject}
          onClose={() => {
            setShowDeleteModal(false);
            setSelectedProject(null);
          }}
          onConfirm={() => handleDeleteProject(selectedProject.id)}
        />

        {/* Click outside to close dropdown */}
        {selectedProject && (
          <div
            className="fixed inset-0 z-5"
            onClick={() => setSelectedProject(null)}
          />
        )}
      </div>
    </div>
  );
};

// Create Project Modal Component
const CreateProjectModal = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    product_category: '',
    target_audience: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) return;

    try {
      setLoading(true);
      const response = await projectsAPI.createProject(formData);
      onSuccess(response.data);
      setFormData({ name: '', description: '', product_category: '', target_audience: '' });
      toast.success('Project created successfully!');
    } catch (error) {
      console.error('Error creating project:', error);
      toast.error('Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
              onClick={onClose}
            />

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
            >
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                Create New Project
              </h3>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="input-field"
                    placeholder="Enter project name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="input-field"
                    rows={3}
                    placeholder="Describe your project"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Product Category
                  </label>
                  <input
                    type="text"
                    value={formData.product_category}
                    onChange={(e) => setFormData({ ...formData, product_category: e.target.value })}
                    className="input-field"
                    placeholder="e.g., Electronics, Fashion, Food"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Audience
                  </label>
                  <input
                    type="text"
                    value={formData.target_audience}
                    onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
                    className="input-field"
                    placeholder="e.g., Young professionals, Parents"
                  />
                </div>

                <div className="flex space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={onClose}
                    className="btn-secondary flex-1"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading || !formData.name.trim()}
                    className="btn-primary flex-1"
                  >
                    {loading ? 'Creating...' : 'Create Project'}
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
};

// Delete Confirmation Modal Component
const DeleteConfirmationModal = ({ isOpen, project, onClose, onConfirm }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
              onClick={onClose}
            />

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
            >
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
                  <TrashIcon className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Delete Project</h3>
                  <p className="text-sm text-gray-600">This action cannot be undone</p>
                </div>
              </div>

              <p className="text-gray-700 mb-6">
                Are you sure you want to delete "<strong>{project?.name}</strong>"? 
                All associated images and content will be permanently removed.
              </p>

              <div className="flex space-x-3">
                <button
                  onClick={onClose}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
                <button
                  onClick={onConfirm}
                  className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-xl font-semibold transition-colors duration-200 flex-1"
                >
                  Delete Project
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default Projects;