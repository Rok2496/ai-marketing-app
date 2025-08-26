# Streamlit - Simple AI Image Generator

A simple and intuitive Streamlit application for quick AI image generation with automatic model fallback.

## 🚀 Features

- **Text-to-Image Generation**: Create images from text descriptions
- **Image-to-Image Transformation**: Transform existing images with AI
- **Multiple Art Styles**: Realistic, Cartoon, Oil Painting, Watercolor, Digital Art, etc.
- **Aspect Ratio Options**: Square, Landscape, Portrait, Wide, Classic, Tall
- **Automatic Model Fallback**: 11+ AI models with intelligent switching
- **Rate Limit Monitoring**: Real-time API usage tracking
- **Direct Downloads**: Download generated images instantly
- **Error Handling**: Graceful fallback with helpful suggestions

## 🏗️ Tech Stack

- **Framework**: Streamlit
- **Image Processing**: Pillow (PIL)
- **HTTP Client**: Requests
- **AI Integration**: OpenRouter API
- **File Handling**: Base64 encoding/decoding

## 📁 Project Structure

```
streamlit/
├── app.py          # Main Streamlit application
├── config.py       # Configuration and API keys
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
cd streamlit
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` with your OpenRouter API keys:

```python
# API Configuration
API_KEY = "sk-or-v1-your-primary-api-key-here"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# You can add backup keys in the BACKUP_MODELS section
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 🎨 Features Overview

### Text-to-Image Generation
- **Simple Interface**: Just describe what you want to create
- **Style Selection**: Choose from 10+ artistic styles
- **Aspect Ratios**: Multiple format options for different use cases
- **Instant Results**: Fast generation with progress indicators

### Image-to-Image Transformation
- **Upload Support**: PNG, JPG, JPEG formats
- **Transformation Options**:
  - Generate Similar: Create variations of uploaded image
  - Change Style: Apply different artistic styles
  - Add Elements: Add new objects or features
  - Remove Elements: Remove unwanted parts
  - Change Colors: Modify color schemes
  - Transform Scene: Complete scene transformation
- **Custom Instructions**: Add specific requirements

### AI Model Management
- **Primary Model**: `google/gemini-2.5-flash-image-preview:free`
- **11 Backup Models**: Automatic fallback when rate limits hit
- **Smart Switching**: Seamless model transitions
- **Usage Tracking**: Monitor API consumption

## 🤖 Supported AI Models

### Primary Model
- **Gemini 2.5 Flash Image Preview**: High-quality image generation

### Backup Models (Auto-fallback)
1. **Qwen2.5 VL 72B**: Advanced vision-language model
2. **Qwen2.5 VL 32B**: Efficient vision processing
3. **Llama 3.2 11B Vision**: Meta's vision model
4. **Gemma 3 27B**: Google's language model
5. **Gemma 3 12B**: Optimized version
6. **Gemma 3 4B**: Lightweight option
7. **Mistral Small 3.2 24B**: Mistral's efficient model
8. **Kimi VL A3B Thinking**: Advanced reasoning model
9. **Llama 4 Maverick**: Latest Meta model
10. **Llama 4 Scout**: Specialized variant

## 🎨 Art Styles Available

- **Realistic**: Photorealistic images
- **Cartoon**: Animated/cartoon style
- **Oil Painting**: Classic oil painting effect
- **Watercolor**: Soft watercolor technique
- **Digital Art**: Modern digital artwork
- **Sketch**: Hand-drawn sketch style
- **Abstract**: Abstract artistic interpretation
- **Photorealistic**: Ultra-realistic photography
- **Anime**: Japanese animation style
- **Comic Book**: Comic book illustration style

## 📐 Aspect Ratios

- **Square (1:1)**: Perfect for social media posts
- **Landscape (16:9)**: Widescreen format
- **Portrait (9:16)**: Vertical format for mobile
- **Wide (21:9)**: Ultra-wide cinematic format
- **Classic (4:3)**: Traditional photo format
- **Tall (2:3)**: Portrait photography format

## 🔄 Rate Limit Management

### Automatic Handling
- **Real-time Monitoring**: Track API usage and limits
- **Smart Fallback**: Switch to backup models when needed
- **Error Recovery**: Graceful handling of rate limit errors
- **Usage Display**: Show remaining requests and reset times

### Rate Limit Information
- **50 Requests/Day**: Per API key (free tier)
- **Multiple Keys**: Use multiple keys for higher limits
- **Reset Schedule**: Daily reset at midnight UTC
- **Upgrade Options**: Information about paid tiers

## 🖼️ Image Processing

### Input Formats
- **PNG**: Lossless compression
- **JPG/JPEG**: Standard photo format
- **WEBP**: Modern web format (where supported)

### Output Features
- **Base64 Encoding**: Efficient image data handling
- **Download Buttons**: One-click image downloads
- **Preview Display**: Instant image preview
- **Error Handling**: Graceful handling of corrupted images

## 🔧 Configuration Options

### API Settings
```python
# Primary API key
API_KEY = "your-api-key-here"

# API endpoint
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Request headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://streamlit-image-generator.app",
    "X-Title": "Streamlit Image Generator",
}
```

### Model Configuration
```python
# Primary model for first attempts
ANALYSIS_MODEL = "google/gemini-2.5-flash-image-preview:free"

# Backup models for fallback
BACKUP_MODELS = [
    "qwen/qwen2.5-vl-72b-instruct:free",
    "qwen/qwen2.5-vl-32b-instruct:free",
    # ... more models
]
```

## 🐛 Troubleshooting

### Common Issues

**Rate Limit Exceeded**
- Wait for daily reset (shown in sidebar)
- Add more API keys to config.py
- Consider upgrading to paid tier

**No Images Generated**
- Check if API key is valid
- Verify internet connection
- Try different prompts or models

**Image Display Issues**
- Refresh the page
- Check browser console for errors
- Try different image formats

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Add secrets for API keys
4. Deploy automatically

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

## 📊 Usage Analytics

### Built-in Metrics
- **Generation Success Rate**: Track successful vs failed generations
- **Model Performance**: Monitor which models work best
- **Usage Patterns**: Understand popular styles and formats
- **Error Tracking**: Log and analyze failures

### Rate Limit Monitoring
- **Real-time Status**: Current usage and remaining requests
- **Reset Timers**: When limits will reset
- **Key Rotation**: Automatic switching between API keys
- **Usage History**: Track daily/weekly usage patterns

## 🔒 Security Notes

### API Key Protection
- Never commit API keys to version control
- Use environment variables in production
- Rotate keys regularly
- Monitor usage for unauthorized access

### Input Validation
- Sanitize user prompts
- Validate uploaded images
- Limit file sizes
- Check image formats

## �� Tips for Best Results

### Prompt Writing
- Be specific and descriptive
- Include style preferences
- Mention lighting and composition
- Use artistic terminology

### Image Uploads
- Use high-quality source images
- Ensure good lighting
- Crop to focus on subject
- Use supported formats

### Style Selection
- Match style to intended use
- Consider target audience
- Test different combinations
- Save successful prompts

## 🔄 Updates and Maintenance

### Regular Updates
- Monitor new AI models on OpenRouter
- Update model lists in config.py
- Test new features and capabilities
- Optimize performance based on usage

### Community Contributions
- Report bugs and issues
- Suggest new features
- Share successful prompts
- Contribute to documentation