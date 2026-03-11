"""
LEAH Concierge Demo Bot — Configuration Settings
Centralized configuration for Groq API, Weather API, and bot behavior
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# API CONFIGURATION
# ============================================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BOT_ID = os.getenv("BOT_ID", "leah_carodemo_bot")

# ============================================================================
# GROQ API SETTINGS
# ============================================================================

GROQ_MODEL = "mixtral-8x7b-32768"
GROQ_TEMPERATURE = 0.7
GROQ_MAX_TOKENS = 1024

# ============================================================================
# WEATHER API SETTINGS
# ============================================================================

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_TIMEOUT = 10

# ============================================================================
# BOT BEHAVIOR
# ============================================================================

SESSION_TIMEOUT = 1800  # 30 minutes
MAX_CONVERSATION_HISTORY = 20
RESPONSE_TIMEOUT = 30

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "leah_bot.log"

# ============================================================================
# DEMO PROPERTY DATA (Casa Lumina)
# ============================================================================

DEMO_PROPERTY = {
    "name": "Casa Lumina",
    "location": "Miami Beach, Florida",
    "description": "A stunning 5-star luxury property with breathtaking ocean views",
    "check_in": "4:00 PM",
    "check_out": "11:00 AM",
    "amenities": {
        "wifi": "CASA_LUMINA_5G",
        "wifi_password": "LuxuryStay2024!",
        "pool": "Heated infinity pool with ocean views",
        "spa": "Full-service spa with massage services",
        "gym": "State-of-the-art fitness center",
        "parking": "Complimentary valet parking",
        "concierge": "24/7 AI-powered concierge service"
    },
    "restaurants": [
        {
            "name": "Juvia",
            "cuisine": "Peruvian-Japanese-Spanish Fusion",
            "distance": "0.5 km",
            "rating": 4.7,
            "description": "Award-winning fusion restaurant with stunning views"
        },
        {
            "name": "Casa Tua",
            "cuisine": "Mediterranean",
            "distance": "1.2 km",
            "rating": 4.8,
            "description": "Intimate dining in a historic mansion"
        },
        {
            "name": "The Surf Club",
            "cuisine": "French",
            "distance": "2.1 km",
            "rating": 4.9,
            "description": "Thomas Keller's Michelin-starred restaurant"
        }
    ],
    "attractions": [
        "Miami Beach Boardwalk (0.2 km)",
        "Art Deco Historic District (1.5 km)",
        "Vizcaya Museum & Gardens (8 km)",
        "Wynwood Walls Street Art (12 km)",
        "Everglades National Park (50 km)"
    ],
    "emergency_contacts": {
        "front_desk": "+1-305-555-0100",
        "medical": "+1-305-555-0911",
        "police": "911"
    }
}

# ============================================================================
# SYSTEM PROMPT FOR GROQ
# ============================================================================

SYSTEM_PROMPT = """You are LEAH, an AI concierge assistant for Casa Lumina, a luxury 5-star property in Miami Beach.

Your role is to assist guests with:
- Property information (amenities, check-in/out, WiFi, parking)
- Restaurant recommendations and reservations
- Local attractions and activities
- Emergency support and assistance
- General guest services

PERSONALITY:
- Professional yet warm and approachable
- Knowledgeable about the property and local area
- Responsive and helpful
- Elegant and sophisticated in tone

GUIDELINES:
- Always provide accurate information about the property
- Offer personalized recommendations based on guest preferences
- Be proactive in suggesting services and experiences
- Maintain guest privacy and confidentiality
- Respond within seconds to create a seamless experience

When guests ask about the property, weather, or local information, provide helpful, accurate responses that enhance their stay."""

# ============================================================================
# DEMO FLOW CONFIGURATION
# ============================================================================

DEMO_TOPICS = {
    "website": {
        "description": "website development",
        "options": [
            "A simple high-converting landing page",
            "A full business website",
            "A website integrated with AI and automation"
        ]
    },
    "automation": {
        "description": "automation systems",
        "options": [
            "Automating customer communications",
            "Automating internal workflows",
            "Automating marketing campaigns"
        ]
    },
    "marketing": {
        "description": "marketing strategy",
        "options": [
            "Lead generation and nurturing",
            "Content creation and distribution",
            "Campaign optimization and analytics"
        ]
    }
}

PERSUASION_MESSAGES = {
    "time_savings": "Many businesses spend weeks trying to build these systems manually. LEAH was designed to simplify that process by combining AI assistance with automation frameworks.",
    "cost_efficiency": "Instead of hiring additional staff, LEAH handles these tasks automatically, saving you significant operational costs while improving service quality.",
    "competitive_advantage": "Your competitors are still managing these tasks manually. LEAH gives you a competitive edge by automating what they're doing by hand.",
    "scalability": "As your business grows, LEAH scales with you without proportional cost increases. One system can handle 10x the volume."
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    "api_error": "I apologize, but I'm having trouble connecting to my services. Please try again in a moment.",
    "unknown_error": "Something unexpected happened. Please try again or contact support.",
    "timeout": "I'm taking longer than usual to respond. Please try again."
}
