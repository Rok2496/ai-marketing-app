import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
import json
from ..core.config import settings

logger = logging.getLogger(__name__)

class APIKeyManager:
    """Manages multiple OpenRouter API keys with automatic fallback"""
    
    def __init__(self):
        self.api_keys = settings.openrouter_api_keys
        self.current_key_index = 0
        self.key_status = {}  # Track rate limits and errors for each key
        self.last_check = {}  # Last time we checked each key
        
        # Initialize key status
        for i, key in enumerate(self.api_keys):
            self.key_status[i] = {
                'active': True,
                'rate_limit_reset': None,
                'requests_remaining': None,
                'last_error': None,
                'error_count': 0
            }
    
    def get_current_key(self) -> Optional[str]:
        """Get the current active API key"""
        if not self.api_keys:
            return None
        
        # Find the first active key
        for i in range(len(self.api_keys)):
            key_index = (self.current_key_index + i) % len(self.api_keys)
            if self._is_key_available(key_index):
                self.current_key_index = key_index
                return self.api_keys[key_index]
        
        return None
    
    def _is_key_available(self, key_index: int) -> bool:
        """Check if a key is available for use"""
        status = self.key_status[key_index]
        
        # If key is marked as inactive, check if it should be reactivated
        if not status['active']:
            if status['rate_limit_reset']:
                if datetime.now() > status['rate_limit_reset']:
                    status['active'] = True
                    status['rate_limit_reset'] = None
                    status['error_count'] = 0
                    logger.info(f"API key {key_index + 1} reactivated after rate limit reset")
        
        return status['active']
    
    def mark_key_rate_limited(self, key: str, reset_time: Optional[datetime] = None):
        """Mark a key as rate limited"""
        try:
            key_index = self.api_keys.index(key)
            self.key_status[key_index]['active'] = False
            self.key_status[key_index]['rate_limit_reset'] = reset_time or (datetime.now() + timedelta(hours=24))
            logger.warning(f"API key {key_index + 1} marked as rate limited until {self.key_status[key_index]['rate_limit_reset']}")
        except ValueError:
            logger.error(f"Attempted to mark unknown API key as rate limited")
    
    def mark_key_error(self, key: str, error: str):
        """Mark a key as having an error"""
        try:
            key_index = self.api_keys.index(key)
            self.key_status[key_index]['last_error'] = error
            self.key_status[key_index]['error_count'] += 1
            
            # If too many errors, temporarily disable the key
            if self.key_status[key_index]['error_count'] >= 3:
                self.key_status[key_index]['active'] = False
                self.key_status[key_index]['rate_limit_reset'] = datetime.now() + timedelta(minutes=30)
                logger.warning(f"API key {key_index + 1} temporarily disabled due to repeated errors")
        except ValueError:
            logger.error(f"Attempted to mark unknown API key with error")
    
    def update_key_status(self, key: str, headers: Dict[str, str]):
        """Update key status from API response headers"""
        try:
            key_index = self.api_keys.index(key)
            status = self.key_status[key_index]
            
            # Update rate limit info from headers
            if 'X-RateLimit-Remaining' in headers:
                status['requests_remaining'] = int(headers['X-RateLimit-Remaining'])
            
            if 'X-RateLimit-Reset' in headers:
                reset_timestamp = int(headers['X-RateLimit-Reset']) / 1000
                status['rate_limit_reset'] = datetime.fromtimestamp(reset_timestamp)
            
            # Reset error count on successful request
            status['error_count'] = 0
            status['last_error'] = None
            
        except (ValueError, KeyError) as e:
            logger.error(f"Error updating key status: {e}")
    
    def get_next_key(self) -> Optional[str]:
        """Get the next available API key"""
        original_index = self.current_key_index
        
        # Try next key
        for i in range(1, len(self.api_keys)):
            next_index = (self.current_key_index + i) % len(self.api_keys)
            if self._is_key_available(next_index):
                self.current_key_index = next_index
                logger.info(f"Switched to API key {next_index + 1}")
                return self.api_keys[next_index]
        
        return None
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get a summary of all API key statuses"""
        summary = {
            'total_keys': len(self.api_keys),
            'active_keys': 0,
            'rate_limited_keys': 0,
            'error_keys': 0,
            'keys': []
        }
        
        for i, key in enumerate(self.api_keys):
            status = self.key_status[i]
            key_info = {
                'index': i + 1,
                'active': status['active'],
                'requests_remaining': status['requests_remaining'],
                'rate_limit_reset': status['rate_limit_reset'].isoformat() if status['rate_limit_reset'] else None,
                'error_count': status['error_count'],
                'last_error': status['last_error']
            }
            
            summary['keys'].append(key_info)
            
            if status['active']:
                summary['active_keys'] += 1
            elif status['rate_limit_reset']:
                summary['rate_limited_keys'] += 1
            elif status['error_count'] > 0:
                summary['error_keys'] += 1
        
        return summary

# Global instance
api_key_manager = APIKeyManager()