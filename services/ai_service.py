"""
LEAH Concierge Demo Bot — AI Service
Handles Groq API integration, Weather API, and session management
"""

import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from groq import Groq
from config.settings import (
    GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS,
    WEATHER_API_KEY, WEATHER_API_URL, WEATHER_TIMEOUT,
    SYSTEM_PROMPT, SESSION_TIMEOUT, MAX_CONVERSATION_HISTORY,
    RESPONSE_TIMEOUT, DEMO_PROPERTY
)

logger = logging.getLogger(__name__)


class ConversationSession:
    """Manages a single user's conversation session"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.messages: List[Dict] = []
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.message_count = 0
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.messages.append({"role": role, "content": content})
        self.last_activity = datetime.now()
        self.message_count += 1
        
        # Keep only recent messages to prevent memory overflow
        if len(self.messages) > MAX_CONVERSATION_HISTORY:
            self.messages = self.messages[-MAX_CONVERSATION_HISTORY:]
    
    def is_expired(self) -> bool:
        """Check if session has expired"""
        return (datetime.now() - self.last_activity).total_seconds() > SESSION_TIMEOUT
    
    def reset(self):
        """Reset the conversation"""
        self.messages = []
        self.message_count = 0
        self.created_at = datetime.now()
        self.last_activity = datetime.now()


class AIService:
    """Manages AI interactions via Groq API and Weather API"""
    
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.sessions: Dict[int, ConversationSession] = {}
        logger.info("AIService initialized with Groq API")
    
    def get_session(self, user_id: int) -> ConversationSession:
        """Get or create a session for a user"""
        if user_id not in self.sessions:
            self.sessions[user_id] = ConversationSession(user_id)
            logger.info(f"Created new session for user {user_id}")
        return self.sessions[user_id]
    
    async def get_response(self, user_id: int, user_message: str) -> Optional[str]:
        """Get AI response using Groq API"""
        try:
            session = self.get_session(user_id)
            
            # Add user message to history
            session.add_message("user", user_message)
            
            # Check for weather request
            weather_info = await self._check_weather_request(user_message)
            
            # Prepare messages for Groq
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in session.messages]
            
            # Add weather context if available
            if weather_info:
                messages[-1]["content"] += f"\n\n[Weather Info: {weather_info}]"
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *messages
                ],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS,
                timeout=RESPONSE_TIMEOUT
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            
            # Add to history
            session.add_message("assistant", ai_response)
            
            logger.info(f"Generated response for user {user_id} (message #{session.message_count})")
            return ai_response
        
        except Exception as e:
            logger.error(f"Error getting Groq response: {str(e)}")
            return None
    
    async def _check_weather_request(self, message: str) -> Optional[str]:
        """Check if message asks about weather and fetch weather data"""
        weather_keywords = ["weather", "temperature", "rain", "sunny", "forecast", "climate"]
        
        if not any(keyword in message.lower() for keyword in weather_keywords):
            return None
        
        if not WEATHER_API_KEY:
            return "Weather information is not available at this time."
        
        try:
            params = {
                "q": "Miami,US",
                "appid": WEATHER_API_KEY,
                "units": "metric"
            }
            
            response = requests.get(
                WEATHER_API_URL,
                params=params,
                timeout=WEATHER_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                
                return f"Current weather in Miami: {temp}°C, {description.title()}, Humidity: {humidity}%"
            else:
                logger.warning(f"Weather API returned status {response.status_code}")
                return None
        
        except Exception as e:
            logger.error(f"Error fetching weather: {str(e)}")
            return None
    
    def get_session_stats(self, user_id: int) -> Optional[Dict]:
        """Get session statistics"""
        if user_id not in self.sessions:
            return None
        
        session = self.sessions[user_id]
        return {
            "user_id": user_id,
            "messages": session.message_count,
            "demo_stage": "active",
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "is_expired": session.is_expired()
        }
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        expired = [uid for uid, session in self.sessions.items() if session.is_expired()]
        for uid in expired:
            del self.sessions[uid]
            logger.info(f"Cleaned up expired session for user {uid}")
        return len(expired)


# Global instance
ai_service = AIService()
