import streamlit as st
import requests
import json
import base64
from PIL import Image
import io
from datetime import datetime
from config import *

# Set page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def check_rate_limit_status():
    """Check current rate limit status"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": ANALYSIS_MODEL,
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 1
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
        
        rate_info = {
            'limit': response.headers.get('X-RateLimit-Limit', 'Unknown'),
            'remaining': response.headers.get('X-RateLimit-Remaining', 'Unknown'),
            'reset': response.headers.get('X-RateLimit-Reset', None),
            'status_code': response.status_code
        }
        
        if response.status_code == 429:
            error_data = response.json()
            metadata = error_data.get('error', {}).get('metadata', {})
            if 'headers' in metadata:
                rate_info.update({
                    'limit': metadata['headers'].get('X-RateLimit-Limit', rate_info['limit']),
                    'remaining': metadata['headers'].get('X-RateLimit-Remaining', rate_info['remaining']),
                    'reset': metadata['headers'].get('X-RateLimit-Reset', rate_info['reset'])
                })
        
        return rate_info
        
    except Exception as e:
        return {'error': str(e), 'status_code': 500}

def format_reset_time(reset_timestamp):
    """Format reset timestamp to readable time"""
    if not reset_timestamp:
        return "Unknown"
    
    try:
        reset_time = datetime.fromtimestamp(int(reset_timestamp) / 1000)
        now = datetime.now()
        time_until_reset = reset_time - now
        
        if time_until_reset.total_seconds() <= 0:
            return "Now (should be reset)"
        
        hours = int(time_until_reset.total_seconds() // 3600)
        minutes = int((time_until_reset.total_seconds() % 3600) // 60)
        
        return f"{hours}h {minutes}m ({reset_time.strftime('%I:%M %p')})"
    except:
        return "Unknown"

def show_rate_limit_status():
    """Display rate limit status in sidebar"""
    st.sidebar.markdown("### 📊 Rate Limit Status")
    
    with st.spinner("Checking rate limits..."):
        rate_info = check_rate_limit_status()
    
    if 'error' in rate_info:
        st.sidebar.error(f"Error checking status: {rate_info['error']}")
        return False
    
    remaining = rate_info.get('remaining', 'Unknown')
    limit = rate_info.get('limit', 'Unknown')
    reset_time = format_reset_time(rate_info.get('reset'))
    
    if rate_info['status_code'] == 429:
        st.sidebar.error("🚫 **Rate Limit Exceeded**")
        st.sidebar.markdown(f"**Limit:** {limit} requests/day")
        st.sidebar.markdown(f"**Remaining:** {remaining}")
        st.sidebar.markdown(f"**Resets in:** {reset_time}")
        return False
    else:
        st.sidebar.success("✅ **API Available**")
        st.sidebar.markdown(f"**Limit:** {limit} requests/day")
        st.sidebar.markdown(f"**Remaining:** {remaining}")
        st.sidebar.markdown(f"**Resets in:** {reset_time}")
        return True

def show_alternatives():
    """Show alternative solutions when rate limited"""
    st.error("🚫 **Daily Rate Limit Exceeded**")
    st.markdown("You've used all 50 free requests for today. Here are your options:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 **Upgrade Options**")
        st.markdown("**OpenRouter Credits:**")
        st.markdown("- Add $10 credits → 1000 requests/day")
        st.markdown("- Pay per use after that")
        st.markdown("- [Add Credits](https://openrouter.ai/credits)")
        
        st.markdown("**Alternative APIs:**")
        st.markdown("- OpenAI API (DALL-E 3)")
        st.markdown("- Anthropic Claude")
        st.markdown("- Google Gemini API")
        st.markdown("- Stability AI")
    
    with col2:
        st.markdown("### 🆓 **Free Alternatives**")
        st.markdown("**Online Tools:**")
        st.markdown("- [Bing Image Creator](https://www.bing.com/images/create)")
        st.markdown("- [Google ImageFX](https://aitestkitchen.withgoogle.com/tools/image-fx)")
        st.markdown("- [Craiyon](https://www.craiyon.com/)")
        st.markdown("- [Leonardo AI](https://leonardo.ai/) (free tier)")
        
        st.markdown("**Local Solutions:**")
        st.markdown("- Stable Diffusion WebUI")
        st.markdown("- ComfyUI")
        st.markdown("- Ollama with vision models")

def call_api_with_fallback(messages, max_retries=3):
    """Make API call with automatic fallback to backup models on rate limit"""
    models_to_try = [ANALYSIS_MODEL] + BACKUP_MODELS
    
    for i, model in enumerate(models_to_try[:max_retries]):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit-image-generator.app",
            "X-Title": "Streamlit Image Generator",
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
            
            if response.status_code == 429:
                # Global rate limit hit
                error_data = response.json()
                if "free-models-per-day" in error_data.get('error', {}).get('message', ''):
                    st.error("🚫 Global daily rate limit exceeded for all free models")
                    return None
                else:
                    # Individual model rate limit, try next
                    model_name = next((name for name, id in FREE_VISION_MODELS.items() if id == model), model)
                    st.warning(f"Rate limit hit for {model_name}. Trying backup model...")
                    continue
            
            response.raise_for_status()
            result = response.json()
            
            # Show which model was used
            model_name = next((name for name, id in FREE_VISION_MODELS.items() if id == model), model)
            st.info(f"✅ Using model: **{model_name}**")
            
            return result
            
        except requests.exceptions.RequestException as e:
            if i == len(models_to_try) - 1:  # Last model failed
                st.error(f"All models failed. Last error: {str(e)}")
                return None
            else:
                model_name = next((name for name, id in FREE_VISION_MODELS.items() if id == model), model)
                st.warning(f"Error with {model_name}: {str(e)}. Trying backup model...")
                continue
    
    return None

def process_image_response(result):
    """Process API response and display images"""
    if not result or 'choices' not in result or not result['choices']:
        st.error("No response from API")
        return False
    
    choice = result['choices'][0]
    message = choice.get('message', {})
    
    # Check for images in the message
    if 'images' in message and message['images']:
        st.success("Image generated successfully!")
        
        # Process each image
        for i, img_data in enumerate(message['images']):
            if 'image_url' in img_data and 'url' in img_data['image_url']:
                image_url = img_data['image_url']['url']
                
                # Handle base64 image data
                if image_url.startswith('data:image'):
                    try:
                        # Extract base64 data
                        header, data_part = image_url.split(',', 1)
                        img_bytes = base64.b64decode(data_part)
                        img = Image.open(io.BytesIO(img_bytes))
                        
                        # Display the image
                        st.image(img, caption=f"Generated Image {i+1}", use_column_width=True)
                        
                        # Provide download button
                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=img_bytes,
                            file_name=f"generated_image_{i+1}.png",
                            mime="image/png",
                            key=f"download_{i}"
                        )
                        
                    except Exception as e:
                        st.error(f"Error processing image {i+1}: {str(e)}")
                
                # Handle regular URL
                elif image_url.startswith('http'):
                    try:
                        img_response = requests.get(image_url)
                        img_response.raise_for_status()
                        img = Image.open(io.BytesIO(img_response.content))
                        
                        # Display the image
                        st.image(img, caption=f"Generated Image {i+1}", use_column_width=True)
                        
                        # Provide download button
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format='PNG')
                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=img_bytes.getvalue(),
                            file_name=f"generated_image_{i+1}.png",
                            mime="image/png",
                            key=f"download_{i}"
                        )
                        
                    except Exception as e:
                        st.error(f"Error loading image {i+1} from URL: {str(e)}")
        return True
    
    # If no images found, show the text response
    else:
        if 'content' in message and message['content']:
            st.info("The model returned a text description instead of an image:")
            st.write(message['content'])
            st.markdown("---")
            st.markdown("**💡 Tip:** You can copy this description and use it with dedicated image generation tools like:")
            st.markdown("- [Bing Image Creator](https://www.bing.com/images/create)")
            st.markdown("- [Google ImageFX](https://aitestkitchen.withgoogle.com/tools/image-fx)")
            st.markdown("- DALL-E 3, Midjourney, Stable Diffusion")
        else:
            st.warning("No image or text content found in the response.")
        return False

def text_to_image_interface():
    """Text to Image Generation Interface"""
    st.header("📝 Text to Image Generation")
    
    # Text input
    prompt = st.text_area(
        "Enter your image description:",
        placeholder="Describe the image you want to generate...",
        height=100
    )
    
    # Generation parameters
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("Art Style:", ART_STYLES)
    
    with col2:
        aspect_ratio = st.selectbox("Aspect Ratio:", ASPECT_RATIOS)
    
    if st.button("Generate Image", type="primary"):
        if prompt:
            # Construct the full prompt
            full_prompt = f"Generate an image: {prompt}. Style: {style}. Aspect ratio: {aspect_ratio}."
            
            with st.spinner("Generating image..."):
                messages = [{"role": "user", "content": full_prompt}]
                result = call_api_with_fallback(messages)
                process_image_response(result)
        else:
            st.warning("Please enter a description for the image.")

def image_to_image_interface():
    """Image to Image Generation Interface"""
    st.header("🖼️ Image to Image Generation")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload an image:",
        type=SUPPORTED_IMAGE_TYPES,
        help="Upload an image to generate variations or edits"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)
        
        with col2:
            st.subheader("Generation Options")
            
            # Edit options
            generation_type = st.selectbox(
                "Generation Type:",
                ["Generate Similar", "Change Style", "Add Elements", "Remove Elements", "Change Colors", "Transform Scene"]
            )
            
            # Style selection for style changes
            if generation_type == "Change Style":
                new_style = st.selectbox("New Style:", ART_STYLES)
            
            # Custom instruction option
            custom_instruction = st.text_area(
                "Custom Instructions:",
                placeholder="Describe what changes you want to make to the image...",
                height=100
            )
            
            # Build the generation prompt based on selection
            prompts = {
                "Generate Similar": "Generate a new image similar to this one, keeping the same style and composition but with variations.",
                "Change Style": f"Generate a new image based on this one but change the style to {new_style if generation_type == 'Change Style' else 'different style'}.",
                "Add Elements": "Generate a new image based on this one but add new elements as described.",
                "Remove Elements": "Generate a new image based on this one but remove the specified elements.",
                "Change Colors": "Generate a new image based on this one but with different colors as described.",
                "Transform Scene": "Generate a new image that transforms this scene as described."
            }
            
            base_prompt = prompts[generation_type]
            full_instruction = f"{base_prompt} {custom_instruction}" if custom_instruction else base_prompt
        
        if st.button("Generate New Image", type="primary"):
            with st.spinner("Generating new image..."):
                # Convert image to base64
                image_base64 = encode_image_to_base64(image)
                
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": full_instruction},
                            {"type": "image_url", "image_url": {"url": image_base64}}
                        ]
                    }
                ]
                
                result = call_api_with_fallback(messages)
                process_image_response(result)

def sidebar_info():
    """Display sidebar information"""
    # Rate limit status
    api_available = show_rate_limit_status()
    
    if not api_available:
        show_alternatives()
        st.stop()
    
    # Available models
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Available Models")
    st.sidebar.markdown("The app will try these models in order:")
    for i, (name, model_id) in enumerate(FREE_VISION_MODELS.items()):
        if i == 0:
            st.sidebar.markdown(f"🥇 **{name}** (Primary)")
        elif model_id in BACKUP_MODELS[:3]:
            st.sidebar.markdown(f"🥈 {name} (Backup)")
        else:
            st.sidebar.markdown(f"• {name}")
    
    # App info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Features")
    st.sidebar.markdown("- **Text to Image Generation**")
    st.sidebar.markdown("- **Image to Image Generation**")
    st.sidebar.markdown("- **Automatic Model Fallback**")
    st.sidebar.markdown("- **Multiple Free Models**")
    st.sidebar.markdown("- **Image Download**")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Tips")
    st.sidebar.markdown("- Be specific in your descriptions")
    st.sidebar.markdown("- Try different art styles")
    st.sidebar.markdown("- Use high-quality images for better results")
    st.sidebar.markdown("- If rate limited, the app will try backup models")

def main():
    """Main application"""
    st.title("🎨 AI Image Generator & Analyzer")
    st.markdown("Generate and analyze images using multiple free AI models with automatic fallback")
    
    # Sidebar
    sidebar_info()
    
    # Mode selection
    st.sidebar.title("Select Mode")
    mode = st.sidebar.radio(
        "Choose operation:",
        ["Text to Image", "Image to Image"]
    )
    
    # Main interface
    if mode == "Text to Image":
        text_to_image_interface()
    else:
        image_to_image_interface()

if __name__ == "__main__":
    main()