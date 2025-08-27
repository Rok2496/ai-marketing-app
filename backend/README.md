# AI Marketing Platform - Backend

A clean, production-ready FastAPI backend for an AI-powered marketing platform that provides content generation, product image enhancement, and marketing assistance.

## 🚀 Features

### Content Generation
- **Text to Image**: Generate images from text descriptions using AI models
- **3D Product Rendering**: Transform product photos into professional 3D renders
- **Professional Product Photography**: Enhance product images with professional styling
- **SEO Content Generation**: Create SEO-optimized captions and content
- **Content Calendar Planning**: Generate comprehensive content plans
- **Marketing Strategy**: Create detailed marketing plans for different goals

### Technical Features
- **Multiple API Key Management**: Automatic fallback between 5 OpenRouter API keys
- **Rate Limit Handling**: Smart rotation when keys hit limits
- **PostgreSQL Database**: Robust data storage with SQLAlchemy ORM
- **File Upload Management**: Secure image upload and storage
- **JWT Authentication**: Secure user authentication
- **Admin Dashboard**: System monitoring and user management

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/v1/              # API routes
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── content.py       # Content generation endpoints
│   │   ├── projects.py      # Project management endpoints
│   │   └── admin.py         # Admin endpoints
│   ├── core/                # Core functionality
│   │   ├── config.py        # Application settings
│   │   ├── database.py      # Database configuration
│   │   └── security.py      # Security utilities
│   ├── models/              # Database models
│   │   ├── user.py          # User model
│   │   ├── project.py       # Project and ProductImage models
│   │   └── content.py       # Content generation models
│   ├── services/            # Business logic
│   │   ├── ai_service.py    # AI API integration
│   │   └── api_key_manager.py # API key management
│   └── main.py              # FastAPI application
├── alembic/                 # Database migrations
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── render.yaml             # Render deployment config
└── README.md               # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database
- OpenRouter API keys

### Local Development

1. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb ai_marketing_db
   
   # Run migrations
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 🌐 API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info

### Projects
- `POST /api/v1/projects/` - Create project
- `GET /api/v1/projects/` - List user projects
- `GET /api/v1/projects/{id}` - Get project details
- `POST /api/v1/projects/{id}/images` - Upload product images

### Content Generation
- `POST /api/v1/content/text-to-image` - Generate image from text
- `POST /api/v1/content/product-render` - Generate 3D render/professional photo
- `POST /api/v1/content/seo-content` - Generate SEO content
- `POST /api/v1/content/content-plan` - Generate content calendar
- `POST /api/v1/content/marketing-plan` - Generate marketing strategy

### Admin (Superuser only)
- `GET /api/v1/admin/stats` - System statistics
- `GET /api/v1/admin/api-keys/status` - API key status

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_marketing_db

# OpenRouter API Keys (5 keys for redundancy)
OPENROUTER_API_KEY_1=your-primary-key
OPENROUTER_API_KEY_2=your-backup-key-1
OPENROUTER_API_KEY_3=your-backup-key-2
OPENROUTER_API_KEY_4=your-backup-key-3
OPENROUTER_API_KEY_5=your-backup-key-4

# JWT Secret
JWT_SECRET_KEY=your-super-secret-key

# Application
DEBUG=false
CORS_ORIGINS=https://yourdomain.com
```

## 🚀 Deployment

### Render Deployment

1. **Connect your repository** to Render
2. **Set Root Directory** to `backend`
3. **Configure build settings**:
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `python main.py`
4. **Set environment variables** in Render dashboard
5. **Connect PostgreSQL database**

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password security
- **File Validation**: Strict file type and size limits
- **CORS Configuration**: Configurable cross-origin settings
- **Rate Limiting**: Built-in API key rate limit handling

## 📊 Database Schema

### Users
- User authentication and profile information
- API usage tracking
- Role-based permissions

### Projects
- User projects with product information
- Brand guidelines and target audience
- Product image storage

### Content Generations
- Track all AI-generated content
- Store generation parameters and results
- Performance metrics and model usage

## 🔑 API Key Management

The system supports multiple OpenRouter API keys with automatic fallback:

1. **Primary Key**: Used for initial requests
2. **Backup Keys**: Automatically used when primary hits rate limits
3. **Smart Rotation**: Tracks rate limits and errors for each key
4. **Auto-Recovery**: Reactivates keys when rate limits reset

## 🏥 Health Monitoring

- `GET /health` - Basic health check
- `GET /api/v1/admin/stats` - Detailed system statistics
- Comprehensive logging with different levels
- API key usage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review logs for error details
3. Monitor API key status in admin dashboard
4. Ensure database connectivity