# AI Marketing Platform - Backend API

A comprehensive FastAPI backend for an AI-powered marketing platform that provides content generation, product image enhancement, and marketing assistance.

## Features

### 🎨 Content Generation
- **Text to Image**: Generate images from text descriptions
- **3D Product Rendering**: Transform product photos into professional 3D renders
- **Professional Product Photography**: Enhance product images with professional styling

### 📈 Marketing Assistant
- **SEO Content Generation**: Create SEO-optimized captions and content
- **Content Calendar Planning**: Generate comprehensive content plans
- **Marketing Strategy**: Create detailed marketing plans for different goals (outreach, sales, branding)

### 🔧 Technical Features
- **Multiple API Key Management**: Automatic fallback between 5-6 API keys
- **Rate Limit Handling**: Smart rotation when keys hit limits
- **PostgreSQL Database**: Robust data storage with SQLAlchemy ORM
- **File Upload Management**: Secure image upload and storage
- **JWT Authentication**: Secure user authentication
- **Admin Dashboard**: System monitoring and user management

## Quick Start

### 1. Environment Setup

```bash
# Clone the repository
cd backend

# Install dependencies
pip install -r backend_requirements.txt

# Copy environment file
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your settings:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ai_marketing_db

# API Keys (Add 5-6 keys for redundancy)
OPENROUTER_API_KEY_1=sk-or-v1-your-primary-key
OPENROUTER_API_KEY_2=sk-or-v1-your-backup-key-1
OPENROUTER_API_KEY_3=sk-or-v1-your-backup-key-2
# ... add more keys

# JWT Secret
JWT_SECRET_KEY=your-super-secret-key-change-this
```

### 3. Database Setup

```bash
# Install PostgreSQL and create database
createdb ai_marketing_db

# Run migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development mode
python run.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

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
- `POST /api/v1/admin/api-keys/rotate` - Force key rotation

## Database Schema

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

### Marketing Plans
- Comprehensive marketing strategies
- Goal-based planning (outreach, sales, branding)
- SEO analysis and recommendations

## API Key Management

The system supports multiple OpenRouter API keys with automatic fallback:

1. **Primary Key**: Used for initial requests
2. **Backup Keys**: Automatically used when primary hits rate limits
3. **Smart Rotation**: Tracks rate limits and errors for each key
4. **Auto-Recovery**: Reactivates keys when rate limits reset

### Key Status Tracking
- Rate limit monitoring
- Error count tracking
- Automatic deactivation/reactivation
- Admin dashboard for manual management

## File Upload System

- **Secure Storage**: Files stored in organized project directories
- **Image Validation**: Type and size validation
- **Metadata Extraction**: Automatic width/height detection
- **Primary Image**: Support for main product image designation

## Development

### Project Structure
```
backend/
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Core functionality
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   └── main.py          # FastAPI app
├── alembic/             # Database migrations
├── uploads/             # File storage
└── requirements.txt     # Dependencies
```

### Adding New Features

1. **Models**: Add to `app/models/`
2. **API Routes**: Add to `app/api/v1/`
3. **Services**: Add business logic to `app/services/`
4. **Migrations**: `alembic revision --autogenerate -m "description"`

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend_requirements.txt .
RUN pip install -r backend_requirements.txt

COPY backend/ .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

```env
DEBUG=False
DATABASE_URL=postgresql://user:pass@db:5432/ai_marketing_db
JWT_SECRET_KEY=production-secret-key
CORS_ORIGINS=https://yourdomain.com
```

## Monitoring

### Health Checks
- `GET /health` - Basic health check
- `GET /api/v1/admin/stats` - Detailed system stats

### Logging
- Structured logging with different levels
- API key usage tracking
- Error monitoring and alerting

## Security

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt for password security
- **File Validation**: Strict file type and size limits
- **CORS Configuration**: Configurable cross-origin settings
- **Rate Limiting**: Built-in API key rate limit handling

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review logs for error details
3. Monitor API key status in admin dashboard
4. Ensure database connectivity

## License

This project is licensed under the MIT License.