import asyncio
import logging
import json
import base64
from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx
from PIL import Image
import io

from ..core.config import settings, PRIMARY_MODEL, BACKUP_MODELS, FREE_VISION_MODELS
from .api_key_manager import api_key_manager

logger = logging.getLogger(__name__)

class AIService:
    """Service for handling AI API calls with automatic fallback - EXACT COPY OF STREAMLIT LOGIC"""
    
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.site_url = settings.OPENROUTER_SITE_URL
        self.site_name = settings.OPENROUTER_SITE_NAME
    
    async def generate_text_to_image(
        self, 
        prompt: str, 
        style: str = "Realistic", 
        aspect_ratio: str = "Square (1:1)",
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate image from text prompt - EXACT SAME AS STREAMLIT"""
        
        # Use EXACT same prompt format as working Streamlit app
        full_prompt = f"Generate an image: {prompt}. Style: {style}. Aspect ratio: {aspect_ratio}."
        
        messages = [{"role": "user", "content": full_prompt}]
        
        result = await self._make_api_call(messages, user_id=user_id)
        
        if result and result.get('success'):
            return {
                'success': True,
                'content': result.get('content'),
                'images': result.get('images', []),
                'model_used': result.get('model_used'),
                'processing_time': result.get('processing_time')
            }
        
        return {'success': False, 'error': result.get('error', 'Unknown error')}
    
    async def generate_product_render(
        self, 
        image_data: bytes, 
        render_type: str = "3d_render",
        instructions: str = "",
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate 3D render or professional product image"""
        
        # Convert image to base64
        image_base64 = self._encode_image_to_base64(image_data)
        
        if render_type == "3d_render":
            prompt = f"Generate a professional 3D render of this product. Make it look modern, clean, and suitable for e-commerce. {instructions}"
        else:
            prompt = f"Generate a professional product photograph of this item. Use professional lighting, clean background, and commercial photography style. {instructions}"
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_base64}}
                ]
            }
        ]
        
        result = await self._make_api_call(messages, user_id=user_id)
        
        if result and result.get('success'):
            return {
                'success': True,
                'content': result.get('content'),
                'images': result.get('images', []),
                'model_used': result.get('model_used'),
                'processing_time': result.get('processing_time')
            }
        
        return {'success': False, 'error': result.get('error', 'Unknown error')}
    
    async def generate_seo_content(
        self, 
        product_description: str,
        target_keywords: List[str] = None,
        platform: str = "general",
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate SEO-optimized captions and content"""
        
        keywords_text = ", ".join(target_keywords) if target_keywords else ""
        
        prompt = f"""
        Create SEO-optimized content for this product: {product_description}
        
        Target keywords: {keywords_text}
        Platform: {platform}
        
        Please provide:
        1. SEO-optimized title (60 characters max)
        2. Meta description (160 characters max)
        3. Product description with natural keyword integration
        4. 5-10 relevant hashtags
        5. Alt text for images
        6. Social media captions for different platforms
        
        Format the response as JSON with clear sections.
        """
        
        messages = [{"role": "user", "content": prompt}]
        
        result = await self._make_api_call(messages, user_id=user_id)
        
        if result and result.get('success'):
            return {
                'success': True,
                'content': result.get('content'),
                'model_used': result.get('model_used'),
                'processing_time': result.get('processing_time')
            }
        
        return {'success': False, 'error': result.get('error', 'Unknown error')}
    
    async def generate_content_plan(
        self,
        product_info: str,
        target_audience: str,
        goals: List[str],
        timeframe: str = "monthly",
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate content calendar and plan"""
        
        prompt = f"""
        Create a comprehensive content plan for:
        
        Product/Service: {product_info}
        Target Audience: {target_audience}
        Goals: {', '.join(goals)}
        Timeframe: {timeframe}
        
        Please provide:
        1. Content calendar with specific post ideas for each week
        2. Content types and formats (images, videos, stories, etc.)
        3. Posting schedule and frequency
        4. Key themes and messaging
        5. Seasonal/event-based content opportunities
        6. Engagement strategies
        7. Performance metrics to track
        
        Format as a detailed JSON structure with dates and specific content ideas.
        """
        
        messages = [{"role": "user", "content": prompt}]
        
        result = await self._make_api_call(messages, user_id=user_id)
        
        if result and result.get('success'):
            return {
                'success': True,
                'content': result.get('content'),
                'model_used': result.get('model_used'),
                'processing_time': result.get('processing_time')
            }
        
        return {'success': False, 'error': result.get('error', 'Unknown error')}
    
    async def generate_marketing_plan(
        self,
        product_info: str,
        target_audience: str,
        goal: str,  # outreach, sales, branding
        budget_range: str,
        timeline: str,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive marketing plan"""
        
        prompt = f"""
        Create a comprehensive marketing plan for:
        
        Product/Service: {product_info}
        Target Audience: {target_audience}
        Primary Goal: {goal}
        Budget Range: {budget_range}
        Timeline: {timeline}
        
        Please provide a detailed marketing strategy including:
        
        1. SITUATION ANALYSIS
           - Market overview
           - Competitor analysis
           - SWOT analysis
        
        2. MARKETING OBJECTIVES
           - Specific, measurable goals
           - KPIs to track
        
        3. TARGET AUDIENCE ANALYSIS
           - Demographics and psychographics
           - Customer personas
           - Pain points and motivations
        
        4. MARKETING MIX STRATEGY
           - Product positioning
           - Pricing strategy
           - Distribution channels
           - Promotional tactics
        
        5. DIGITAL MARKETING STRATEGY
           - Social media strategy
           - Content marketing
           - SEO/SEM approach
           - Email marketing
           - Influencer partnerships
        
        6. BUDGET ALLOCATION
           - Channel-wise budget distribution
           - Expected ROI
        
        7. IMPLEMENTATION TIMELINE
           - Phase-wise execution plan
           - Milestones and deadlines
        
        8. MEASUREMENT & ANALYTICS
           - Success metrics
           - Tracking methods
           - Reporting schedule
        
        Format as a comprehensive JSON structure with actionable recommendations.
        """
        
        messages = [{"role": "user", "content": prompt}]
        
        result = await self._make_api_call(messages, user_id=user_id)
        
        if result and result.get('success'):
            return {
                'success': True,
                'content': result.get('content'),
                'model_used': result.get('model_used'),
                'processing_time': result.get('processing_time')
            }
        
        return {'success': False, 'error': result.get('error', 'Unknown error')}
    
    async def _make_api_call(
        self, 
        messages: List[Dict], 
        max_retries: int = 3,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Make API call with automatic key rotation and retry logic - EXACT SAME AS STREAMLIT"""
        
        models_to_try = [PRIMARY_MODEL] + BACKUP_MODELS
        start_time = datetime.now()
        
        for model in models_to_try:
            for attempt in range(max_retries):
                api_key = api_key_manager.get_current_key()
                
                if not api_key:
                    logger.error("No available API keys")
                    return {'success': False, 'error': 'No available API keys'}
                
                try:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit-image-generator.app",
                        "X-Title": "Streamlit Image Generator",
                    }
                    
                    data = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": 1000
                    }
                    
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        response = await client.post(
                            self.base_url,
                            headers=headers,
                            json=data
                        )
                    
                    # Update key status from response headers
                    api_key_manager.update_key_status(api_key, dict(response.headers))
                    
                    if response.status_code == 429:
                        # Rate limit hit
                        error_data = response.json()
                        if "free-models-per-day" in error_data.get('error', {}).get('message', ''):
                            # Global rate limit, mark key as rate limited
                            api_key_manager.mark_key_rate_limited(api_key)
                            
                            # Try next key
                            next_key = api_key_manager.get_next_key()
                            if not next_key:
                                return {'success': False, 'error': 'All API keys rate limited'}
                            continue
                        else:
                            # Model-specific rate limit, try next model
                            break
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    # Process successful response
                    processing_time = (datetime.now() - start_time).total_seconds()
                    
                    # Log which model was used (like Streamlit)
                    model_name = next((name for name, id in FREE_VISION_MODELS.items() if id == model), model)
                    logger.info(f"✅ Using model: {model_name}")
                    
                    return {
                        'success': True,
                        'content': self._extract_content(result),
                        'images': self._extract_images(result),
                        'model_used': model,
                        'api_key_used': api_key[-8:],  # Last 8 chars for logging
                        'processing_time': processing_time
                    }
                
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error with key {api_key[-8:]}: {e}")
                    api_key_manager.mark_key_error(api_key, str(e))
                    
                    if attempt == max_retries - 1:
                        # Try next key
                        next_key = api_key_manager.get_next_key()
                        if not next_key:
                            return {'success': False, 'error': f'HTTP error: {e}'}
                
                except Exception as e:
                    logger.error(f"Unexpected error with key {api_key[-8:]}: {e}")
                    api_key_manager.mark_key_error(api_key, str(e))
                    
                    if attempt == max_retries - 1:
                        return {'success': False, 'error': f'Unexpected error: {e}'}
                
                # Wait before retry
                await asyncio.sleep(1)
        
        return {'success': False, 'error': 'All models and keys exhausted'}
    
    def _encode_image_to_base64(self, image_data: bytes) -> str:
        """Convert image bytes to base64 string - EXACT SAME AS STREAMLIT"""
        try:
            # Verify it's a valid image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to PNG format for consistency
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            img_str = base64.b64encode(img_buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            logger.error(f"Error encoding image to base64: {e}")
            raise
    
    def _extract_content(self, result: Dict) -> Optional[str]:
        """Extract text content from API response - EXACT SAME AS STREAMLIT"""
        try:
            if 'choices' in result and result['choices']:
                message = result['choices'][0].get('message', {})
                return message.get('content')
        except Exception as e:
            logger.error(f"Error extracting content: {e}")
        return None
    
    def _extract_images(self, result: Dict) -> List[Dict]:
        """Extract image data from API response - EXACT SAME LOGIC AS WORKING STREAMLIT APP"""
        images = []
        try:
            if 'choices' in result and result['choices']:
                message = result['choices'][0].get('message', {})
                
                # Check for images in the message (same as Streamlit app)
                if 'images' in message and message['images']:
                    for img_data in message['images']:
                        if 'image_url' in img_data and 'url' in img_data['image_url']:
                            image_url = img_data['image_url']['url']
                            images.append({
                                'url': image_url,
                                'type': 'base64' if image_url.startswith('data:image') else 'url'
                            })
                
                # Also check if the content itself contains image data
                content = message.get('content', '')
                if content and 'data:image' in content:
                    # Extract base64 image data from content
                    import re
                    image_pattern = r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+'
                    found_images = re.findall(image_pattern, content)
                    for img_url in found_images:
                        images.append({
                            'url': img_url,
                            'type': 'base64'
                        })
                        
        except Exception as e:
            logger.error(f"Error extracting images: {e}")
            logger.error(f"Result structure: {result}")
        return images

# Global instance
ai_service = AIService()