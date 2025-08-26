import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  SparklesIcon, 
  PhotoIcon, 
  ChartBarIcon, 
  RocketLaunchIcon,
  CheckIcon,
  ArrowRightIcon,
  PlayIcon
} from '@heroicons/react/24/outline';

const Home = () => {
  const features = [
    {
      icon: SparklesIcon,
      title: 'AI Content Generation',
      description: 'Generate stunning images, professional product photos, and marketing content with advanced AI models.',
      color: 'from-primary-500 to-primary-600'
    },
    {
      icon: PhotoIcon,
      title: '3D Product Rendering',
      description: 'Transform your product photos into professional 3D renders and high-quality marketing visuals.',
      color: 'from-secondary-500 to-secondary-600'
    },
    {
      icon: ChartBarIcon,
      title: 'Marketing Analytics',
      description: 'Get data-driven insights, SEO optimization, and comprehensive marketing strategies tailored to your goals.',
      color: 'from-accent-500 to-accent-600'
    },
    {
      icon: RocketLaunchIcon,
      title: 'Automated Workflows',
      description: 'Streamline your marketing process with automated content calendars and campaign management.',
      color: 'from-green-500 to-green-600'
    }
  ];

  const benefits = [
    'Generate professional content in seconds',
    'Multiple AI models with automatic fallback',
    'SEO-optimized captions and descriptions',
    'Comprehensive marketing strategies',
    'Real-time analytics and insights',
    'Team collaboration tools'
  ];

  const stats = [
    { label: 'Content Generated', value: '10M+' },
    { label: 'Active Users', value: '50K+' },
    { label: 'Time Saved', value: '2M+ hrs' },
    { label: 'Success Rate', value: '99.9%' }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-secondary-50 pt-20 pb-32">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold text-gray-900 mb-6">
                Transform Your Marketing with{' '}
                <span className="gradient-text">AI Power</span>
              </h1>
              
              <p className="text-xl sm:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Generate stunning visuals, optimize content for SEO, and create data-driven marketing strategies 
                that convert—all powered by cutting-edge AI technology.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
                <Link
                  to="/register"
                  className="btn-primary text-lg px-8 py-4 group"
                >
                  Start Creating Free
                  <ArrowRightIcon className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform duration-200" />
                </Link>
                
                <button className="btn-secondary text-lg px-8 py-4 group">
                  <PlayIcon className="w-5 h-5 mr-2" />
                  Watch Demo
                </button>
              </div>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="grid grid-cols-2 lg:grid-cols-4 gap-8 max-w-4xl mx-auto"
            >
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl sm:text-4xl font-bold gradient-text mb-2">
                    {stat.value}
                  </div>
                  <div className="text-gray-600 text-sm sm:text-base">
                    {stat.label}
                  </div>
                </div>
              ))}
            </motion.div>
          </div>
        </div>

        {/* Floating elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-primary-200 rounded-full opacity-20 animate-float"></div>
        <div className="absolute top-40 right-20 w-16 h-16 bg-secondary-200 rounded-full opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute bottom-20 left-20 w-12 h-12 bg-accent-200 rounded-full opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl sm:text-5xl font-bold text-gray-900 mb-4">
                Everything You Need to{' '}
                <span className="gradient-text">Scale Your Marketing</span>
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Our comprehensive AI platform provides all the tools you need to create, 
                optimize, and scale your marketing efforts.
              </p>
            </motion.div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="card p-8 hover-lift group"
                >
                  <div className={`w-16 h-16 bg-gradient-to-br ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">
                    {feature.title}
                  </h3>
                  
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-24 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl sm:text-5xl font-bold text-gray-900 mb-6">
                Why Choose Our{' '}
                <span className="gradient-text">AI Platform?</span>
              </h2>
              
              <p className="text-xl text-gray-600 mb-8">
                Join thousands of marketers and creators who trust our platform 
                to deliver exceptional results every time.
              </p>
              
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    viewport={{ once: true }}
                    className="flex items-center space-x-3"
                  >
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <CheckIcon className="w-4 h-4 text-green-600" />
                    </div>
                    <span className="text-gray-700 text-lg">{benefit}</span>
                  </motion.div>
                ))}
              </div>
              
              <div className="mt-8">
                <Link
                  to="/register"
                  className="btn-primary text-lg px-8 py-4 group"
                >
                  Get Started Today
                  <ArrowRightIcon className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform duration-200" />
                </Link>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="relative z-10 bg-white rounded-3xl shadow-2xl p-8">
                <div className="aspect-video bg-gradient-to-br from-primary-100 to-secondary-100 rounded-2xl flex items-center justify-center">
                  <div className="text-center">
                    <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
                      <PlayIcon className="w-10 h-10 text-primary-600" />
                    </div>
                    <p className="text-gray-600 font-medium">Watch Platform Demo</p>
                  </div>
                </div>
              </div>
              
              {/* Background decorations */}
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-primary-200 rounded-full opacity-20 animate-pulse"></div>
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-secondary-200 rounded-full opacity-20 animate-pulse" style={{ animationDelay: '1s' }}></div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-br from-primary-600 to-secondary-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        
        <div className="relative max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl sm:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Marketing?
            </h2>
            
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of creators and marketers who are already using AI 
              to create stunning content and drive better results.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/register"
                className="bg-white text-primary-600 hover:bg-gray-50 px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 hover:scale-105 shadow-lg group"
              >
                Start Free Trial
                <ArrowRightIcon className="w-5 h-5 ml-2 inline group-hover:translate-x-1 transition-transform duration-200" />
              </Link>
              
              <Link
                to="/contact"
                className="border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200"
              >
                Contact Sales
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-20 h-20 border border-white rounded-full animate-pulse"></div>
          <div className="absolute top-20 right-20 w-16 h-16 border border-white rounded-full animate-pulse" style={{ animationDelay: '1s' }}></div>
          <div className="absolute bottom-20 left-1/4 w-12 h-12 border border-white rounded-full animate-pulse" style={{ animationDelay: '2s' }}></div>
          <div className="absolute bottom-10 right-1/3 w-24 h-24 border border-white rounded-full animate-pulse" style={{ animationDelay: '3s' }}></div>
        </div>
      </section>
    </div>
  );
};

export default Home;