# Backend - AI Marketing Platform API

FastAPI-based backend with PostgreSQL database for comprehensive AI marketing tools.

## 🚀 Features

- **User Management**: Registration, authentication, JWT tokens
- **Project Organization**: Create and manage marketing projects
- **AI Image Generation**: Text-to-image and product render generation
- **Marketing Tools**: SEO content, marketing plans, content calendars
- **API Key Management**: Automatic rotation and fallback system
- **Database Storage**: Persistent storage of all generations and user data

## 🏗️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **AI Integration**: OpenRouter API
- **Image Processing**: Pillow (PIL)
- **Async**: httpx for API calls

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/v1/           # API endpoints
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── content.py    # Content generation endpoints
│   │   ├── projects.py   # Project management
│   │   └── users.py      # User management
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings and AI models
│   │   ├── database.py   # Database connection
│   │   └── security.py   # JWT and password handling
│   ├── models/           # Database models
│   │   ├── user.py       # User model
│   │   ├── project.py    # Project model
│   │   └── content.py    # Content generation model
│   └── services/         # Business logic
│       ├── ai_service.py # AI API integration
│       └── api_key_manager.py # API key rotation
├── alembic/              # Database migrations
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── main.py              # Application entry point
```

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Install PostgreSQL (macOS)
brew install postgresql
brew services start postgresql

# Create database
createdb ai_marketing_db
```

### 3. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/ai_marketing_db
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# OpenRouter API Keys (6 keys for rotation)
OPENROUTER_API_KEY_1=sk-or-v1-your-first-key-here
OPENROUTER_API_KEY_2=sk-or-v1-your-second-key-here
OPENROUTER_API_KEY_3=sk-or-v1-your-third-key-here
OPENROUTER_API_KEY_4=sk-or-v1-your-fourth-key-here
OPENROUTER_API_KEY_5=sk-or-v1-your-fifth-key-here
OPENROUTER_API_KEY_6=sk-or-v1-your-sixth-key-here
```

### 4. Database Migration

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create and run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 5. Run the Server

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Content Generation
- `POST /api/v1/content/text-to-image` - Generate image from text
- `POST /api/v1/content/product-render` - Generate product renders
- `POST /api/v1/content/seo-content` - Generate SEO content
- `POST /api/v1/content/content-plan` - Generate content calendar
- `POST /api/v1/content/marketing-plan` - Generate marketing strategy
- `GET /api/v1/content/generations` - Get user's generations

### Projects
- `GET /api/v1/projects/` - List user projects
- `POST /api/v1/projects/` - Create new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

## 🤖 AI Models

The backend supports 11+ AI models with automatic fallback:

**Primary Model**: `google/gemini-2.5-flash-image-preview:free`

**Backup Models**:
- `qwen/qwen2.5-vl-72b-instruct:free`
- `qwen/qwen2.5-vl-32b-instruct:free`
- `meta-llama/llama-3.2-11b-vision-instruct:free`
- `google/gemma-3-27b-it:free`
- `mistralai/mistral-small-3.2-24b-instruct:free`
- And more...

## 🔄 API Key Management

- **6 API Keys**: Automatic rotation for high availability
- **Rate Limit Handling**: Automatic fallback when limits hit
- **Error Recovery**: Retry logic with exponential backoff
- **Usage Tracking**: Monitor API key performance

## 📊 Database Schema

### Users Table
- User authentication and profile information
- JWT token management
- Usage statistics

### Projects Table
- Project organization and metadata
- User association
- Creation and update timestamps

### Content Generations Table
- All AI-generated content and images
- Generation parameters and results
- Processing time and model tracking
- Image metadata storage

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt for password security
- **CORS Protection**: Configurable CORS origins
- **Input Validation**: Pydantic models for request validation
- **Rate Limiting**: Built-in protection against abuse

## 🐛 Debugging

### Check Database Connection
```bash
# Test database connection
python -c "from app.core.database import engine; print('Database connected!' if engine else 'Connection failed')"
```

### View Logs
```bash
# Enable debug logging
export DEBUG=true
uvicorn main:app --reload --log-level debug
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚀 Deployment

### Docker (Recommended)
```bash
# Build image
docker build -t ai-marketing-backend .

# Run container
docker run -p 8000:8000 --env-file .env ai-marketing-backend
```

### Manual Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📈 Performance

- **Async Operations**: All AI API calls are asynchronous
- **Connection Pooling**: Database connection optimization
- **Caching**: Response caching for repeated requests
- **Batch Processing**: Efficient handling of multiple requests

## 🔧 Configuration

Key configuration options in `app/core/config.py`:

- **AI Models**: Configure available models and fallback order
- **Rate Limits**: Adjust API call limits and retry logic
- **Database**: Connection settings and pool configuration
- **Security**: JWT settings and CORS configuration