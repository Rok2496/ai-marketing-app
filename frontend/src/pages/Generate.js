import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  SparklesIcon,
  PhotoIcon,
  DocumentTextIcon,
  CalendarIcon,
  MegaphoneIcon,
  CloudArrowUpIcon,
  ArrowDownTrayIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { contentAPI, projectsAPI } from '../utils/api';
import toast from 'react-hot-toast';

const Generate = () => {
  const [activeTab, setActiveTab] = useState('text-to-image');
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getProjects();
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const tabs = [
    {
      id: 'text-to-image',
      name: 'Text to Image',
      icon: SparklesIcon,
      description: 'Generate stunning images from text descriptions'
    },
    {
      id: 'product-render',
      name: 'Product Render',
      icon: PhotoIcon,
      description: 'Transform product photos into professional renders'
    },
    {
      id: 'seo-content',
      name: 'SEO Content',
      icon: DocumentTextIcon,
      description: 'Create SEO-optimized captions and descriptions'
    },
    {
      id: 'content-plan',
      name: 'Content Plan',
      icon: CalendarIcon,
      description: 'Generate comprehensive content calendars'
    },
    {
      id: 'marketing-plan',
      name: 'Marketing Plan',
      icon: MegaphoneIcon,
      description: 'Create data-driven marketing strategies'
    }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'text-to-image':
        return <TextToImageForm onSubmit={handleTextToImage} loading={loading} projects={projects} />;
      case 'product-render':
        return <ProductRenderForm onSubmit={handleProductRender} loading={loading} projects={projects} />;
      case 'seo-content':
        return <SEOContentForm onSubmit={handleSEOContent} loading={loading} projects={projects} />;
      case 'content-plan':
        return <ContentPlanForm onSubmit={handleContentPlan} loading={loading} projects={projects} />;
      case 'marketing-plan':
        return <MarketingPlanForm onSubmit={handleMarketingPlan} loading={loading} projects={projects} />;
      default:
        return null;
    }
  };

  const handleTextToImage = async (data) => {
    try {
      setLoading(true);
      const response = await contentAPI.generateTextToImage(data);
      setResult(response.data);
      toast.success('Image generated successfully!');
    } catch (error) {
      console.error('Error generating image:', error);
      toast.error('Failed to generate image');
    } finally {
      setLoading(false);
    }
  };

  const handleProductRender = async (formData) => {
    try {
      setLoading(true);
      const response = await contentAPI.generateProductRender(formData);
      setResult(response.data);
      toast.success('Product render generated successfully!');
    } catch (error) {
      console.error('Error generating render:', error);
      toast.error('Failed to generate render');
    } finally {
      setLoading(false);
    }
  };

  const handleSEOContent = async (data) => {
    try {
      setLoading(true);
      const response = await contentAPI.generateSEOContent(data);
      setResult(response.data);
      toast.success('SEO content generated successfully!');
    } catch (error) {
      console.error('Error generating SEO content:', error);
      toast.error('Failed to generate SEO content');
    } finally {
      setLoading(false);
    }
  };

  const handleContentPlan = async (data) => {
    try {
      setLoading(true);
      const response = await contentAPI.generateContentPlan(data);
      setResult(response.data);
      toast.success('Content plan generated successfully!');
    } catch (error) {
      console.error('Error generating content plan:', error);
      toast.error('Failed to generate content plan');
    } finally {
      setLoading(false);
    }
  };

  const handleMarketingPlan = async (data) => {
    try {
      setLoading(true);
      const response = await contentAPI.generateMarketingPlan(data);
      setResult(response.data);
      toast.success('Marketing plan generated successfully!');
    } catch (error) {
      console.error('Error generating marketing plan:', error);
      toast.error('Failed to generate marketing plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Generate AI-Powered Content
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Transform your marketing with cutting-edge AI. Create stunning visuals, 
            optimize content, and develop comprehensive strategies in minutes.
          </p>
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-8"
        >
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'bg-primary-600 text-white shadow-lg'
                      : 'bg-white text-gray-600 hover:text-gray-900 hover:bg-gray-50 border border-gray-200'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="hidden sm:inline">{tab.name}</span>
                </button>
              );
            })}
          </div>

          {/* Tab description */}
          <div className="text-center">
            <p className="text-gray-600">
              {tabs.find(tab => tab.id === activeTab)?.description}
            </p>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="card p-8">
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeTab}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  {renderTabContent()}
                </motion.div>
              </AnimatePresence>
            </div>
          </motion.div>

          {/* Result Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="lg:col-span-1"
          >
            <div className="card p-6 sticky top-8">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Result</h3>
              
              {loading ? (
                <div className="text-center py-12">
                  <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-gray-600">Generating content...</p>
                </div>
              ) : result ? (
                <ResultDisplay result={result} />
              ) : (
                <div className="text-center py-12">
                  <SparklesIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">
                    Your generated content will appear here
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

// Text to Image Form Component
const TextToImageForm = ({ onSubmit, loading, projects }) => {
  const [formData, setFormData] = useState({
    prompt: '',
    style: 'Realistic',
    aspect_ratio: 'Square (1:1)',
    project_id: ''
  });

  const styles = ['Realistic', 'Cartoon', 'Oil Painting', 'Watercolor', 'Digital Art', 'Sketch', 'Abstract', 'Photorealistic', 'Anime', 'Comic Book'];
  const aspectRatios = ['Square (1:1)', 'Landscape (16:9)', 'Portrait (9:16)', 'Wide (21:9)', 'Classic (4:3)', 'Tall (2:3)'];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.prompt.trim()) return;
    
    const submitData = {
      ...formData,
      project_id: formData.project_id || null
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Describe what you want to create *
        </label>
        <textarea
          value={formData.prompt}
          onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
          className="input-field"
          rows={4}
          placeholder="A professional product photo of a smartphone on a clean white background with soft lighting..."
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Style
          </label>
          <select
            value={formData.style}
            onChange={(e) => setFormData({ ...formData, style: e.target.value })}
            className="input-field"
          >
            {styles.map(style => (
              <option key={style} value={style}>{style}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Aspect Ratio
          </label>
          <select
            value={formData.aspect_ratio}
            onChange={(e) => setFormData({ ...formData, aspect_ratio: e.target.value })}
            className="input-field"
          >
            {aspectRatios.map(ratio => (
              <option key={ratio} value={ratio}>{ratio}</option>
            ))}
          </select>
        </div>
      </div>

      {projects.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project (Optional)
          </label>
          <select
            value={formData.project_id}
            onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
            className="input-field"
          >
            <option value="">Select a project</option>
            {projects.map(project => (
              <option key={project.id} value={project.id}>{project.name}</option>
            ))}
          </select>
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !formData.prompt.trim()}
        className="w-full btn-primary flex items-center justify-center"
      >
        {loading ? (
          <div className="loading-dots">
            <div></div>
            <div></div>
            <div></div>
          </div>
        ) : (
          <>
            <SparklesIcon className="w-5 h-5 mr-2" />
            Generate Image
          </>
        )}
      </button>
    </form>
  );
};

// Product Render Form Component
const ProductRenderForm = ({ onSubmit, loading, projects }) => {
  const [formData, setFormData] = useState({
    render_type: '3d_render',
    instructions: '',
    project_id: '',
    image: null
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.image) return;

    const submitFormData = new FormData();
    submitFormData.append('render_type', formData.render_type);
    submitFormData.append('instructions', formData.instructions);
    submitFormData.append('project_id', formData.project_id || '');
    submitFormData.append('image', formData.image);

    onSubmit(submitFormData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload Product Image *
        </label>
        <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-primary-400 transition-colors duration-200">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFormData({ ...formData, image: e.target.files[0] })}
            className="hidden"
            id="image-upload"
            required
          />
          <label htmlFor="image-upload" className="cursor-pointer">
            <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">
              {formData.image ? formData.image.name : 'Click to upload or drag and drop'}
            </p>
            <p className="text-sm text-gray-500 mt-2">PNG, JPG, WEBP up to 10MB</p>
          </label>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Render Type
        </label>
        <select
          value={formData.render_type}
          onChange={(e) => setFormData({ ...formData, render_type: e.target.value })}
          className="input-field"
        >
          <option value="3d_render">3D Render</option>
          <option value="professional_product">Professional Product Photo</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Additional Instructions
        </label>
        <textarea
          value={formData.instructions}
          onChange={(e) => setFormData({ ...formData, instructions: e.target.value })}
          className="input-field"
          rows={3}
          placeholder="Add specific requirements, background preferences, lighting, etc..."
        />
      </div>

      {projects.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project (Optional)
          </label>
          <select
            value={formData.project_id}
            onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
            className="input-field"
          >
            <option value="">Select a project</option>
            {projects.map(project => (
              <option key={project.id} value={project.id}>{project.name}</option>
            ))}
          </select>
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !formData.image}
        className="w-full btn-primary flex items-center justify-center"
      >
        {loading ? (
          <div className="loading-dots">
            <div></div>
            <div></div>
            <div></div>
          </div>
        ) : (
          <>
            <PhotoIcon className="w-5 h-5 mr-2" />
            Generate Render
          </>
        )}
      </button>
    </form>
  );
};

// SEO Content Form Component
const SEOContentForm = ({ onSubmit, loading, projects }) => {
  const [formData, setFormData] = useState({
    product_description: '',
    target_keywords: '',
    platform: 'general',
    project_id: ''
  });

  const platforms = ['general', 'instagram', 'facebook', 'twitter', 'linkedin', 'tiktok', 'youtube'];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.product_description.trim()) return;

    const submitData = {
      ...formData,
      target_keywords: formData.target_keywords.split(',').map(k => k.trim()).filter(k => k),
      project_id: formData.project_id || null
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Product Description *
        </label>
        <textarea
          value={formData.product_description}
          onChange={(e) => setFormData({ ...formData, product_description: e.target.value })}
          className="input-field"
          rows={4}
          placeholder="Describe your product, its features, benefits, and target audience..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Keywords
        </label>
        <input
          type="text"
          value={formData.target_keywords}
          onChange={(e) => setFormData({ ...formData, target_keywords: e.target.value })}
          className="input-field"
          placeholder="smartphone, mobile phone, technology (comma-separated)"
        />
        <p className="text-sm text-gray-500 mt-1">Separate keywords with commas</p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Platform
        </label>
        <select
          value={formData.platform}
          onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
          className="input-field"
        >
          {platforms.map(platform => (
            <option key={platform} value={platform}>
              {platform.charAt(0).toUpperCase() + platform.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {projects.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project (Optional)
          </label>
          <select
            value={formData.project_id}
            onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
            className="input-field"
          >
            <option value="">Select a project</option>
            {projects.map(project => (
              <option key={project.id} value={project.id}>{project.name}</option>
            ))}
          </select>
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !formData.product_description.trim()}
        className="w-full btn-primary flex items-center justify-center"
      >
        {loading ? (
          <div className="loading-dots">
            <div></div>
            <div></div>
            <div></div>
          </div>
        ) : (
          <>
            <DocumentTextIcon className="w-5 h-5 mr-2" />
            Generate SEO Content
          </>
        )}
      </button>
    </form>
  );
};

// Content Plan Form Component
const ContentPlanForm = ({ onSubmit, loading, projects }) => {
  const [formData, setFormData] = useState({
    product_info: '',
    target_audience: '',
    goals: '',
    timeframe: 'monthly',
    project_id: ''
  });

  const timeframes = ['weekly', 'monthly', 'quarterly'];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.product_info.trim() || !formData.target_audience.trim()) return;

    const submitData = {
      ...formData,
      goals: formData.goals.split(',').map(g => g.trim()).filter(g => g),
      project_id: formData.project_id || null
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Product/Service Information *
        </label>
        <textarea
          value={formData.product_info}
          onChange={(e) => setFormData({ ...formData, product_info: e.target.value })}
          className="input-field"
          rows={3}
          placeholder="Describe your product or service, its key features and benefits..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Audience *
        </label>
        <input
          type="text"
          value={formData.target_audience}
          onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
          className="input-field"
          placeholder="Young professionals, parents, tech enthusiasts..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Marketing Goals
        </label>
        <input
          type="text"
          value={formData.goals}
          onChange={(e) => setFormData({ ...formData, goals: e.target.value })}
          className="input-field"
          placeholder="brand awareness, lead generation, sales (comma-separated)"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Timeframe
        </label>
        <select
          value={formData.timeframe}
          onChange={(e) => setFormData({ ...formData, timeframe: e.target.value })}
          className="input-field"
        >
          {timeframes.map(timeframe => (
            <option key={timeframe} value={timeframe}>
              {timeframe.charAt(0).toUpperCase() + timeframe.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {projects.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project (Optional)
          </label>
          <select
            value={formData.project_id}
            onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
            className="input-field"
          >
            <option value="">Select a project</option>
            {projects.map(project => (
              <option key={project.id} value={project.id}>{project.name}</option>
            ))}
          </select>
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !formData.product_info.trim() || !formData.target_audience.trim()}
        className="w-full btn-primary flex items-center justify-center"
      >
        {loading ? (
          <div className="loading-dots">
            <div></div>
            <div></div>
            <div></div>
          </div>
        ) : (
          <>
            <CalendarIcon className="w-5 h-5 mr-2" />
            Generate Content Plan
          </>
        )}
      </button>
    </form>
  );
};

// Marketing Plan Form Component
const MarketingPlanForm = ({ onSubmit, loading, projects }) => {
  const [formData, setFormData] = useState({
    product_info: '',
    target_audience: '',
    goal: 'sales',
    budget_range: '$1,000 - $5,000',
    timeline: '3 months',
    project_id: ''
  });

  const goals = ['outreach', 'sales', 'branding'];
  const budgetRanges = ['$500 - $1,000', '$1,000 - $5,000', '$5,000 - $10,000', '$10,000 - $25,000', '$25,000+'];
  const timelines = ['1 month', '3 months', '6 months', '1 year'];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.product_info.trim() || !formData.target_audience.trim()) return;

    const submitData = {
      ...formData,
      project_id: formData.project_id || null
    };
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Product/Service Information *
        </label>
        <textarea
          value={formData.product_info}
          onChange={(e) => setFormData({ ...formData, product_info: e.target.value })}
          className="input-field"
          rows={3}
          placeholder="Describe your product or service, its unique value proposition..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Audience *
        </label>
        <input
          type="text"
          value={formData.target_audience}
          onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
          className="input-field"
          placeholder="Demographics, interests, pain points..."
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Primary Goal
          </label>
          <select
            value={formData.goal}
            onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
            className="input-field"
          >
            {goals.map(goal => (
              <option key={goal} value={goal}>
                {goal.charAt(0).toUpperCase() + goal.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Budget Range
          </label>
          <select
            value={formData.budget_range}
            onChange={(e) => setFormData({ ...formData, budget_range: e.target.value })}
            className="input-field"
          >
            {budgetRanges.map(range => (
              <option key={range} value={range}>{range}</option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Timeline
        </label>
        <select
          value={formData.timeline}
          onChange={(e) => setFormData({ ...formData, timeline: e.target.value })}
          className="input-field"
        >
          {timelines.map(timeline => (
            <option key={timeline} value={timeline}>{timeline}</option>
          ))}
        </select>
      </div>

      {projects.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Project (Optional)
          </label>
          <select
            value={formData.project_id}
            onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
            className="input-field"
          >
            <option value="">Select a project</option>
            {projects.map(project => (
              <option key={project.id} value={project.id}>{project.name}</option>
            ))}
          </select>
        </div>
      )}

      <button
        type="submit"
        disabled={loading || !formData.product_info.trim() || !formData.target_audience.trim()}
        className="w-full btn-primary flex items-center justify-center"
      >
        {loading ? (
          <div className="loading-dots">
            <div></div>
            <div></div>
            <div></div>
          </div>
        ) : (
          <>
            <MegaphoneIcon className="w-5 h-5 mr-2" />
            Generate Marketing Plan
          </>
        )}
      </button>
    </form>
  );
};

// Result Display Component
const ResultDisplay = ({ result }) => {
  if (!result) return null;

  // Extract images from generation_metadata (same as backend structure)
  const images = result.generation_metadata?.images || [];
  const hasImages = images.length > 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className={`status-${result.status === 'completed' ? 'success' : result.status === 'failed' ? 'error' : 'warning'}`}>
          {result.status}
        </span>
        {result.model_used && (
          <span className="text-xs text-gray-500">
            {result.model_used}
          </span>
        )}
      </div>

      {/* Display generated images first (most important for image generation) */}
      {hasImages && (
        <div>
          <h4 className="font-medium text-gray-900 mb-3">Generated Images:</h4>
          <div className="space-y-3">
            {images.map((image, index) => (
              <div key={index} className="bg-white rounded-lg border border-gray-200 overflow-hidden">
                {image.type === 'base64' || image.url.startsWith('data:image') ? (
                  <div className="relative">
                    <img
                      src={image.url}
                      alt={`Generated ${index + 1}`}
                      className="w-full h-auto rounded-lg"
                      style={{ maxHeight: '400px', objectFit: 'contain' }}
                    />
                    <div className="absolute top-2 right-2">
                      <button
                        onClick={() => {
                          // Download the image
                          const link = document.createElement('a');
                          link.href = image.url;
                          link.download = `generated-image-${index + 1}.png`;
                          document.body.appendChild(link);
                          link.click();
                          document.body.removeChild(link);
                        }}
                        className="bg-white bg-opacity-90 hover:bg-opacity-100 text-gray-700 p-2 rounded-lg shadow-sm transition-all duration-200"
                        title="Download image"
                      >
                        <ArrowDownTrayIcon className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="p-4">
                    <a
                      href={image.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-700 font-medium flex items-center"
                    >
                      <PhotoIcon className="w-4 h-4 mr-2" />
                      View Image {index + 1}
                    </a>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Display text content */}
      {result.generated_content && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">
            {hasImages ? 'Additional Information:' : 'Generated Content:'}
          </h4>
          <div className="text-sm text-gray-700 whitespace-pre-wrap">
            {result.generated_content}
          </div>
          
          {/* Show tip if no images were generated */}
          {!hasImages && result.generated_content && (
            <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-sm text-blue-800 mb-2">
                💡 <strong>Tip:</strong> The AI returned a text description instead of an image. You can use this description with dedicated image generation tools:
              </p>
              <div className="text-xs text-blue-700 space-y-1">
                <div>• <a href="https://www.bing.com/images/create" target="_blank" rel="noopener noreferrer" className="underline">Bing Image Creator</a></div>
                <div>• <a href="https://aitestkitchen.withgoogle.com/tools/image-fx" target="_blank" rel="noopener noreferrer" className="underline">Google ImageFX</a></div>
                <div>• DALL-E 3, Midjourney, Stable Diffusion</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Processing time */}
      {result.processing_time && (
        <div className="text-xs text-gray-500 flex items-center">
          <ClockIcon className="w-3 h-3 mr-1" />
          Generated in {result.processing_time}s
        </div>
      )}

      {/* Success message for images */}
      {hasImages && (
        <div className="text-sm text-green-600 flex items-center">
          <CheckCircleIcon className="w-4 h-4 mr-1" />
          Successfully generated {images.length} image{images.length > 1 ? 's' : ''}!
        </div>
      )}
    </div>
  );
};

export default Generate;