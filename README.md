# AI Image Platform

A comprehensive AI-powered image generation and marketing platform with three separate applications:

## 🏗️ Architecture

```
ai-image-platform/
├── backend/          # FastAPI backend with database
├── frontend/         # React frontend application  
├── streamlit/        # Simple Streamlit image generator
└── README.md         # This file
```

## 🚀 Applications

### 1. **Backend** (FastAPI + PostgreSQL)
- **Purpose**: Full-featured API with user management, project organization, and comprehensive marketing tools
- **Features**: 
  - User authentication & authorization
  - Project management
  - Image generation with database storage
  - SEO content generation
  - Marketing plan creation
  - Content calendar planning
  - API key management with automatic fallback
- **Tech Stack**: FastAPI, PostgreSQL, SQLAlchemy, JWT authentication
- **Port**: `http://localhost:8000`

### 2. **Frontend** (React)
- **Purpose**: Professional web interface for the full marketing platform
- **Features**:
  - Modern React UI with Tailwind CSS
  - User dashboard and project management
  - Advanced image generation with multiple styles
  - Product render generation
  - SEO content optimization
  - Marketing strategy planning
  - Content calendar management
- **Tech Stack**: React, Tailwind CSS, Framer Motion, React Router
- **Port**: `http://localhost:3000`

### 3. **Streamlit** (Simple Image Generator)
- **Purpose**: Quick and simple image generation tool
- **Features**:
  - Text-to-image generation
  - Image-to-image transformation
  - Multiple art styles and aspect ratios
  - Automatic model fallback
  - Rate limit monitoring
  - Direct image download
- **Tech Stack**: Streamlit, PIL, OpenRouter API
- **Port**: `http://localhost:8501`

## 🔧 Setup Instructions

Each application has its own setup instructions in their respective directories:

- [Backend Setup](./backend/README.md)
- [Frontend Setup](./frontend/README.md)  
- [Streamlit Setup](./streamlit/README.md)

## 🔑 API Keys

All applications use the same OpenRouter API keys. Configure them in:
- Backend: `backend/.env`
- Streamlit: `streamlit/config.py`

## 🌟 Key Features

### Image Generation
- **Multiple AI Models**: Automatic fallback between 11+ free vision models
- **Style Options**: Realistic, Cartoon, Oil Painting, Watercolor, Digital Art, etc.
- **Aspect Ratios**: Square, Landscape, Portrait, Wide, Classic, Tall
- **Format Support**: PNG, JPG, WEBP

### Marketing Tools (Backend + Frontend)
- **SEO Optimization**: Generate optimized titles, descriptions, hashtags
- **Content Planning**: Automated content calendars and strategies  
- **Marketing Plans**: Comprehensive marketing strategy generation
- **Product Renders**: Transform product photos into professional images

### Technical Features
- **Rate Limit Management**: Automatic API key rotation and fallback
- **Error Handling**: Graceful degradation with helpful error messages
- **Performance**: Optimized API calls with caching and retry logic
- **Security**: JWT authentication, input validation, CORS protection

## 📊 Usage Statistics

- **6 API Keys**: Automatic rotation for high availability
- **50+ Requests/Day**: Per API key (300+ total daily requests)
- **11 AI Models**: Automatic fallback system
- **Multiple Formats**: Support for various image and content types

## 🔄 Development Workflow

1. **Start Backend**: Database + API server
2. **Start Frontend**: React development server  
3. **Start Streamlit**: Simple image generator (optional)

Each can run independently or together for full functionality.

## 📝 License

This project is for educational and development purposes.