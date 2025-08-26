import React from 'react';
import { motion } from 'framer-motion';
import { ChartBarIcon } from '@heroicons/react/24/outline';

const Analytics = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center py-16"
        >
          <ChartBarIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Analytics Dashboard</h1>
          <p className="text-gray-600 mb-8">
            Comprehensive analytics and insights coming soon!
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default Analytics;