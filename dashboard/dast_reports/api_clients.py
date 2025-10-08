# dast_reports/api_clients.py
import time
import requests
import json
from django.core.cache import cache
from requests.exceptions import RequestException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class DeepSeekAPIClient:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.max_retries = 3
        self.retry_delay = 2
        
    def call_with_retry(self, prompt, max_tokens=4000, temperature=0.7):
        """Call DeepSeek API dengan retry mechanism untuk handle 429"""
        for attempt in range(self.max_retries):
            try:
                # Rate limiting check
                cache_key = f"deepseek_rate_limit"
                request_count = cache.get(cache_key, 0)
                
                if request_count >= getattr(settings, 'MAX_REQUESTS_PER_MINUTE', 10):
                    wait_time = 60
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "deepseek/deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                # Update rate limit counter
                cache.set(cache_key, request_count + 1, 60)
                
                if response.status_code == 429:
                    wait_time = self.retry_delay * (2 ** attempt)
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        wait_time = int(retry_after)
                    
                    logger.warning(f"Rate limited. Attempt {attempt + 1}. Waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                    
                elif response.status_code == 200:
                    return response.json()
                    
                else:
                    logger.error(f"API error {response.status_code}: {response.text}")
                    response.raise_for_status()
                    
            except RequestException as e:
                logger.error(f"API request failed on attempt {attempt + 1}: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay)
        
        return None

# Singleton instance
deepseek_client = DeepSeekAPIClient()
