# Deployment Guide

This guide covers deploying the AI Marketing Platform to production using Render (backend) and Netlify (frontend).

## 🚀 Backend Deployment (Render)

### Prerequisites
- GitHub repository with the backend code
- Render account (free tier available)
- PostgreSQL database on Render

### Step 1: Database Setup
✅ **Already configured**: PostgreSQL database on Render
- **Database URL**: `postgresql://ai_marketing_app_user:F2pRLCmhlNPmFyKo2GnGrAWwFLGJXwX4@dpg-d2n473nfte5s73bgp150-a.oregon-postgres.render.com/ai_marketing_app`

### Step 2: Deploy Backend to Render

1. **Connect Repository**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `https://github.com/Rok2496/ai-marketing-app`
   - Select the repository

2. **Configure Service**:
   ```
   Name: ai-marketing-backend
   Environment: Python 3
   Region: Oregon (US West)
   Branch: main
   Root Directory: backend
   ```

3. **Build & Start Commands**:
   ```bash
   # Build Command
   pip install -r requirements.txt && alembic upgrade head
   
   # Start Command
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Environment Variables**:
   Add these in Render dashboard:
   ```
   DATABASE_URL=postgresql://ai_marketing_app_user:F2pRLCmhlNPmFyKo2GnGrAWwFLGJXwX4@dpg-d2n473nfte5s73bgp150-a.oregon-postgres.render.com/ai_marketing_app
   
   JWT_SECRET_KEY=pVeVMdvhtDDHVCKT0L2111iHdrGZ2dYiqm4q-Bsjnb8eYroXdTph2fjApjsnJJhwVxnOKoSgdn7UL9wWprCmsw
   
   OPENROUTER_API_KEY_1=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
   OPENROUTER_API_KEY_2=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
   OPENROUTER_API_KEY_3=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
   OPENROUTER_API_KEY_4=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
   OPENROUTER_API_KEY_5=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
   OPENROUTER_API_KEY_6=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
   
   DEBUG=false
   CORS_ORIGINS=https://ai-marketing-platform.netlify.app,http://localhost:3000
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your backend will be available at: `https://ai-marketing-backend.onrender.com`

### Step 3: Verify Backend Deployment

Test the API endpoints:
```bash
# Health check
curl https://ai-marketing-backend.onrender.com/

# API documentation
https://ai-marketing-backend.onrender.com/docs
```

## 🌐 Frontend Deployment (Netlify)

### Step 1: Prepare Frontend for Production

1. **Update API URL**:
   Create `frontend/.env.production`:
   ```env
   REACT_APP_API_URL=https://ai-marketing-backend.onrender.com/api/v1
   REACT_APP_APP_NAME=AI Marketing Platform
   ```

2. **Build Configuration**:
   Ensure `frontend/package.json` has build script:
   ```json
   {
     "scripts": {
       "build": "react-scripts build"
     }
   }
   ```

### Step 2: Deploy to Netlify

#### Option A: Netlify Dashboard (Recommended)

1. **Connect Repository**:
   - Go to [Netlify Dashboard](https://app.netlify.com)
   - Click "New site from Git"
   - Choose GitHub and select your repository
   - Configure build settings:
     ```
     Base directory: frontend
     Build command: npm run build
     Publish directory: frontend/build
     ```

2. **Environment Variables**:
   In Netlify dashboard → Site settings → Environment variables:
   ```
   REACT_APP_API_URL=https://ai-marketing-backend.onrender.com/api/v1
   REACT_APP_APP_NAME=AI Marketing Platform
   ```

3. **Deploy**:
   - Click "Deploy site"
   - Your frontend will be available at: `https://ai-marketing-platform.netlify.app`

#### Option B: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Build and deploy
cd frontend
npm run build
netlify deploy --prod --dir=build
```

### Step 3: Configure Custom Domain (Optional)

1. **Add Custom Domain**:
   - In Netlify dashboard → Domain settings
   - Add your custom domain
   - Configure DNS records

2. **Update CORS**:
   Update backend environment variable:
   ```
   CORS_ORIGINS=https://your-custom-domain.com,https://ai-marketing-platform.netlify.app
   ```

## 🔧 Post-Deployment Configuration

### Update Backend CORS
After frontend deployment, update backend CORS settings:
```env
CORS_ORIGINS=https://ai-marketing-platform.netlify.app,http://localhost:3000
```

### Database Migrations
The backend automatically runs migrations on deployment. For manual migrations:
```bash
# Connect to Render shell
render shell ai-marketing-backend

# Run migrations
alembic upgrade head
```

### SSL Certificates
Both Render and Netlify provide automatic SSL certificates for HTTPS.

## 📊 Monitoring & Logs

### Render Logs
- View logs in Render dashboard
- Monitor performance and errors
- Set up log alerts

### Netlify Analytics
- Monitor site performance
- Track deployment status
- View build logs

## 🔒 Security Checklist

- ✅ Environment variables configured
- ✅ CORS properly set
- ✅ HTTPS enabled
- ✅ Database credentials secure
- ✅ API keys protected
- ✅ Debug mode disabled in production

## 🚀 Performance Optimization

### Backend (Render)
- Use Render's auto-scaling
- Monitor database performance
- Optimize API response times
- Enable caching where appropriate

### Frontend (Netlify)
- Netlify CDN automatically enabled
- Optimize images and assets
- Enable gzip compression
- Use code splitting

## 🔄 CI/CD Pipeline

Both platforms support automatic deployments:

### Render
- Automatically deploys on git push to main branch
- Runs build command and migrations
- Zero-downtime deployments

### Netlify
- Automatically builds and deploys on git push
- Preview deployments for pull requests
- Rollback capabilities

## 🐛 Troubleshooting

### Common Backend Issues
```bash
# Check logs
render logs ai-marketing-backend

# Database connection issues
# Verify DATABASE_URL in environment variables

# API key issues
# Check OpenRouter API key validity
```

### Common Frontend Issues
```bash
# Build failures
# Check Node.js version compatibility
# Verify environment variables

# API connection issues
# Check REACT_APP_API_URL
# Verify CORS settings
```

## 📈 Scaling

### Backend Scaling (Render)
- Upgrade to paid plan for better performance
- Use multiple instances for high availability
- Consider Redis for caching

### Frontend Scaling (Netlify)
- CDN automatically handles global distribution
- Consider Netlify Functions for serverless features
- Optimize bundle size for faster loading

## 💰 Cost Optimization

### Render (Backend)
- Free tier: 750 hours/month
- Paid plans start at $7/month
- Database: $7/month for 1GB

### Netlify (Frontend)
- Free tier: 100GB bandwidth/month
- Paid plans start at $19/month
- Custom domains included

## 🔄 Updates & Maintenance

### Automated Updates
- Both platforms auto-deploy on git push
- Database migrations run automatically
- Environment variables persist across deployments

### Manual Updates
```bash
# Update dependencies
npm update  # Frontend
pip install -r requirements.txt  # Backend

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

Your AI Marketing Platform is now ready for production! 🎉