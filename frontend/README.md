# Frontend - AI Marketing Platform

Modern React application for comprehensive AI-powered marketing tools and image generation.

## 🚀 Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **User Dashboard**: Project management and generation history
- **Image Generation**: Advanced text-to-image and product render tools
- **Marketing Tools**: SEO optimization, content planning, marketing strategies
- **Real-time Updates**: Live generation status and progress tracking
- **Download Management**: Easy image downloads and content export

## 🏗️ Tech Stack

- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Icons**: Heroicons
- **Notifications**: React Hot Toast
- **State Management**: React Hooks

## 📁 Project Structure

```
frontend/
├── public/               # Static assets
├── src/
│   ├─�� components/       # Reusable components
│   │   ├── common/       # Common UI components
│   │   └── layout/       # Layout components
│   ├── pages/            # Page components
│   │   ├── Dashboard.js  # User dashboard
│   │   ├── Generate.js   # Content generation
│   │   ├── Projects.js   # Project management
│   │   ├── Login.js      # Authentication
│   │   └── Register.js   # User registration
│   ├── utils/            # Utility functions
│   │   ├── api.js        # API client
│   │   └── auth.js       # Authentication helpers
│   ├── styles/           # CSS files
│   ├── App.js            # Main app component
│   └── index.js          # Entry point
├── package.json          # Dependencies
├── tailwind.config.js    # Tailwind configuration
└── README.md             # This file
```

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_APP_NAME=AI Marketing Platform
```

### 3. Start Development Server

```bash
npm start
```

The application will open at `http://localhost:3000`

## 🎨 Available Scripts

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject (not recommended)
npm run eject

# Lint code
npm run lint

# Format code
npm run format
```

## 📱 Pages & Features

### 🏠 Dashboard (`/dashboard`)
- **Overview**: Generation statistics and recent activity
- **Quick Actions**: Fast access to common generation tools
- **Project Summary**: Active projects and their status
- **Usage Analytics**: API usage and generation metrics

### 🎨 Generate (`/generate`)
- **Text to Image**: Generate images from text descriptions
  - Multiple art styles (Realistic, Cartoon, Oil Painting, etc.)
  - Various aspect ratios (Square, Landscape, Portrait, etc.)
  - Style preview and recommendations
- **Product Render**: Transform product photos
  - 3D render generation
  - Professional product photography
  - Custom instructions and styling
- **SEO Content**: Optimize content for search engines
  - Platform-specific optimization
  - Keyword integration
  - Meta descriptions and hashtags
- **Content Planning**: Generate content calendars
  - Target audience analysis
  - Goal-based content strategies
  - Scheduling recommendations
- **Marketing Plans**: Comprehensive marketing strategies
  - Budget-based recommendations
  - Timeline planning
  - ROI projections

### 📁 Projects (`/projects`)
- **Project Management**: Create and organize marketing projects
- **Team Collaboration**: Share projects with team members
- **Asset Organization**: Manage generated content and images
- **Progress Tracking**: Monitor project milestones

### 👤 Authentication (`/login`, `/register`)
- **User Registration**: Create new accounts
- **Secure Login**: JWT-based authentication
- **Password Recovery**: Reset forgotten passwords
- **Profile Management**: Update user information

## 🎨 UI Components

### Form Components
- **TextToImageForm**: Image generation interface
- **ProductRenderForm**: Product photo transformation
- **SEOContentForm**: Content optimization tools
- **ContentPlanForm**: Calendar planning interface
- **MarketingPlanForm**: Strategy generation tools

### Display Components
- **ResultDisplay**: Show generated content and images
- **ImageGallery**: Display generated images with download options
- **ContentPreview**: Preview generated text content
- **ProgressIndicator**: Show generation progress
- **StatusBadge**: Display generation status

### Layout Components
- **Header**: Navigation and user menu
- **Sidebar**: Quick navigation and tools
- **Footer**: Links and information
- **LoadingSpinner**: Loading states
- **ErrorBoundary**: Error handling

## 🔌 API Integration

### Authentication
```javascript
// Login user
const response = await authAPI.login({ email, password });

// Register user
const response = await authAPI.register({ name, email, password });

// Get current user
const user = await authAPI.getCurrentUser();
```

### Content Generation
```javascript
// Generate image from text
const result = await contentAPI.generateTextToImage({
  prompt: "A beautiful sunset",
  style: "Realistic",
  aspect_ratio: "Landscape (16:9)"
});

// Generate product render
const formData = new FormData();
formData.append('image', imageFile);
formData.append('render_type', '3d_render');
const result = await contentAPI.generateProductRender(formData);
```

### Project Management
```javascript
// Get user projects
const projects = await projectsAPI.getProjects();

// Create new project
const project = await projectsAPI.createProject({
  name: "Summer Campaign",
  description: "Marketing campaign for summer products"
});
```

## 🎨 Styling & Theming

### Tailwind CSS Classes
- **Primary Colors**: `bg-primary-600`, `text-primary-600`
- **Success States**: `bg-green-500`, `text-green-700`
- **Error States**: `bg-red-500`, `text-red-700`
- **Warning States**: `bg-yellow-500`, `text-yellow-700`

### Custom Components
```css
/* Button styles */
.btn-primary {
  @apply bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200;
}

/* Card styles */
.card {
  @apply bg-white rounded-xl shadow-sm border border-gray-200 p-6;
}

/* Input styles */
.input-field {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent;
}
```

## 🔄 State Management

### Authentication State
```javascript
const [user, setUser] = useState(null);
const [isAuthenticated, setIsAuthenticated] = useState(false);
const [loading, setLoading] = useState(true);
```

### Generation State
```javascript
const [activeTab, setActiveTab] = useState('text-to-image');
const [loading, setLoading] = useState(false);
const [result, setResult] = useState(null);
const [error, setError] = useState(null);
```

### Project State
```javascript
const [projects, setProjects] = useState([]);
const [selectedProject, setSelectedProject] = useState(null);
const [projectLoading, setProjectLoading] = useState(false);
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: `sm:` (640px+)
- **Tablet**: `md:` (768px+)
- **Desktop**: `lg:` (1024px+)
- **Large Desktop**: `xl:` (1280px+)

### Mobile Optimizations
- Touch-friendly buttons and inputs
- Responsive navigation menu
- Optimized image display
- Swipe gestures for galleries

## 🚀 Performance Optimizations

### Code Splitting
```javascript
// Lazy load pages
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Generate = lazy(() => import('./pages/Generate'));
```

### Image Optimization
- Lazy loading for generated images
- Progressive image loading
- Optimized image formats (WebP support)
- Image compression for uploads

### API Optimizations
- Request debouncing for search
- Response caching
- Optimistic updates
- Error retry logic

## 🐛 Error Handling

### Global Error Boundary
```javascript
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### API Error Handling
```javascript
try {
  const result = await api.generateImage(data);
  setResult(result);
} catch (error) {
  if (error.response?.status === 401) {
    // Handle authentication error
    logout();
  } else {
    // Handle other errors
    toast.error(error.message);
  }
}
```

## 🔒 Security Features

- **JWT Token Management**: Automatic token refresh
- **Route Protection**: Private routes for authenticated users
- **Input Validation**: Client-side form validation
- **XSS Protection**: Sanitized user inputs
- **CSRF Protection**: Token-based request validation

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build
```

### Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Environment Variables for Production
```env
REACT_APP_API_URL=https://your-api-domain.com/api/v1
REACT_APP_APP_NAME=AI Marketing Platform
```

## 📊 Analytics & Monitoring

### User Analytics
- Page views and user interactions
- Generation usage patterns
- Feature adoption rates
- Error tracking and reporting

### Performance Monitoring
- Page load times
- API response times
- Image generation success rates
- User session duration

## 🔧 Development Tips

### Hot Reloading
The development server supports hot reloading for instant updates during development.

### Debugging
```javascript
// Enable debug mode
localStorage.setItem('debug', 'true');

// View API requests
console.log('API Request:', { url, method, data });
```

### Testing
```bash
# Run unit tests
npm test

# Run integration tests
npm run test:integration

# Generate coverage report
npm run test:coverage
```