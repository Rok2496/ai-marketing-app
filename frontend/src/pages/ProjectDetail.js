import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowLeftIcon,
  PhotoIcon,
  PlusIcon,
  TrashIcon,
  StarIcon,
  ArrowDownTrayIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';
import { projectsAPI } from '../utils/api';
import { formatDate, formatFileSize } from '../utils/api';
import toast from 'react-hot-toast';

const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const fetchProjectDetails = async () => {
      try {
        setLoading(true);
        const [projectResponse, imagesResponse] = await Promise.all([
          projectsAPI.getProject(id),
          projectsAPI.getProjectImages(id)
        ]);
        
        setProject(projectResponse.data);
        setImages(imagesResponse.data);
      } catch (error) {
        console.error('Error fetching project details:', error);
        toast.error('Failed to load project details');
      } finally {
        setLoading(false);
      }
    };

    fetchProjectDetails();
  }, [id]);

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    if (files.length === 0) return;

    try {
      setUploading(true);
      
      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('is_primary', images.length === 0 ? 'true' : 'false');
        
        const response = await projectsAPI.uploadImage(id, formData);
        setImages(prev => [...prev, response.data]);
      }
      
      toast.success(`${files.length} image(s) uploaded successfully!`);
    } catch (error) {
      console.error('Error uploading images:', error);
      toast.error('Failed to upload images');
    } finally {
      setUploading(false);
    }
  };

  const handleSetPrimary = async (imageId) => {
    try {
      await projectsAPI.setPrimaryImage(id, imageId);
      setImages(prev => prev.map(img => ({
        ...img,
        is_primary: img.id === imageId
      })));
      toast.success('Primary image updated!');
    } catch (error) {
      console.error('Error setting primary image:', error);
      toast.error('Failed to update primary image');
    }
  };

  const handleDeleteImage = async (imageId) => {
    try {
      await projectsAPI.deleteImage(id, imageId);
      setImages(prev => prev.filter(img => img.id !== imageId));
      toast.success('Image deleted successfully!');
    } catch (error) {
      console.error('Error deleting image:', error);
      toast.error('Failed to delete image');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading project...</p>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Project not found</h2>
          <p className="text-gray-600 mb-4">The project you're looking for doesn't exist.</p>
          <Link to="/projects" className="btn-primary">
            Back to Projects
          </Link>
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
          <Link
            to="/projects"
            className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-4 group"
          >
            <ArrowLeftIcon className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform duration-200" />
            Back to Projects
          </Link>
          
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{project.name}</h1>
              <p className="text-gray-600 mb-4">
                {project.description || 'No description provided'}
              </p>
              
              <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                <span>Created {formatDate(project.created_at)}</span>
                {project.product_category && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                    {project.product_category}
                  </span>
                )}
              </div>
            </div>
            
            <Link
              to={`/generate?project=${project.id}`}
              className="btn-primary flex items-center"
            >
              <SparklesIcon className="w-5 h-5 mr-2" />
              Generate Content
            </Link>
          </div>
        </motion.div>

        {/* Project Info Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Images</p>
                <p className="text-3xl font-bold text-gray-900">{images.length}</p>
              </div>
              <PhotoIcon className="w-8 h-8 text-primary-600" />
            </div>
          </div>
          
          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Target Audience</p>
                <p className="text-lg font-semibold text-gray-900">
                  {project.target_audience || 'Not specified'}
                </p>
              </div>
            </div>
          </div>
          
          <div className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Last Updated</p>
                <p className="text-lg font-semibold text-gray-900">
                  {formatDate(project.updated_at || project.created_at)}
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Images Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card p-6"
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">Product Images</h2>
            
            <div className="flex items-center space-x-4">
              <input
                type="file"
                id="file-upload"
                multiple
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
              />
              <label
                htmlFor="file-upload"
                className={`btn-primary flex items-center cursor-pointer ${
                  uploading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                {uploading ? 'Uploading...' : 'Upload Images'}
              </label>
            </div>
          </div>

          {images.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {images.map((image, index) => (
                <motion.div
                  key={image.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className="relative group"
                >
                  <div className="aspect-square bg-gray-100 rounded-xl overflow-hidden">
                    <img
                      src={`/uploads/${image.file_path}`}
                      alt={image.original_filename}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      onError={(e) => {
                        e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0xMDAgMTAwTDEwMCAxMDBaIiBzdHJva2U9IiM5Q0EzQUYiIHN0cm9rZS13aWR0aD0iMiIvPgo8L3N2Zz4K';
                      }}
                    />
                  </div>
                  
                  {/* Image overlay */}
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-300 rounded-xl flex items-center justify-center">
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-2">
                      <button
                        onClick={() => handleSetPrimary(image.id)}
                        className="p-2 bg-white rounded-lg hover:bg-gray-100 transition-colors duration-200"
                        title="Set as primary"
                      >
                        {image.is_primary ? (
                          <StarIconSolid className="w-5 h-5 text-yellow-500" />
                        ) : (
                          <StarIcon className="w-5 h-5 text-gray-600" />
                        )}
                      </button>
                      
                      <a
                        href={`/uploads/${image.file_path}`}
                        download={image.original_filename}
                        className="p-2 bg-white rounded-lg hover:bg-gray-100 transition-colors duration-200"
                        title="Download"
                      >
                        <ArrowDownTrayIcon className="w-5 h-5 text-gray-600" />
                      </a>
                      
                      <button
                        onClick={() => handleDeleteImage(image.id)}
                        className="p-2 bg-white rounded-lg hover:bg-red-100 transition-colors duration-200"
                        title="Delete"
                      >
                        <TrashIcon className="w-5 h-5 text-red-600" />
                      </button>
                    </div>
                  </div>
                  
                  {/* Primary badge */}
                  {image.is_primary && (
                    <div className="absolute top-2 left-2 bg-yellow-500 text-white px-2 py-1 rounded-lg text-xs font-medium flex items-center">
                      <StarIconSolid className="w-3 h-3 mr-1" />
                      Primary
                    </div>
                  )}
                  
                  {/* Image info */}
                  <div className="mt-3">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {image.original_filename}
                    </p>
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>{formatFileSize(image.file_size)}</span>
                      {image.width && image.height && (
                        <span>{image.width} × {image.height}</span>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <PhotoIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                No images uploaded yet
              </h3>
              <p className="text-gray-600 mb-6">
                Upload product images to start generating AI-powered content
              </p>
              <label
                htmlFor="file-upload"
                className="btn-primary inline-flex items-center cursor-pointer"
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                Upload Your First Image
              </label>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default ProjectDetail;