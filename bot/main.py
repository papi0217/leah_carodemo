"""
LEAH Concierge Demo Bot — Main Entry Point
Initializes and runs the Telegram bot with Groq API
"""

import logging
import signal
import sys
from telegram.ext import Application
from bot.handlers import setup_handlers
from config.settings import TELEGRAM_BOT_TOKEN, BOT_ID, LOG_LEVEL, LOG_FILE

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


# ============================================================================
# SIGNAL HANDLERS
# ============================================================================

def signal_handler(sig, frame):
    """Handle graceful shutdown"""
    logger.info("Received shutdown signal, cleaning up...")
    sys.exit(0)


# ============================================================================
# BOT INITIALIZATION
# ============================================================================

async def post_init(application: Application) -> None:
    """Post-initialization setup"""
    logger.info(f"LEAH Concierge Demo Bot started successfully")
    logger.info(f"Bot is ready to accept messages")


async def post_stop(application: Application) -> None:
    """Cleanup on shutdown"""
    logger.info(f"LEAH Concierge Demo Bot shutting down")
    from services.ai_service import ai_service
    expired_count = ai_service.cleanup_expired_sessions()
    logger.info(f"Cleaned up {expired_count} expired sessions")


async def main():
    """Main function to run the bot"""
    try:
        logger.info("=" * 70)
        logger.info(f"Starting LEAH Concierge Demo Bot")
        logger.info("=" * 70)
        
        # Create application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Setup handlers
        setup_handlers(application)
        
        # Post-initialization and shutdown hooks
        application.post_init = post_init
        application.post_stop = post_stop
        
        logger.info(f"Bot configuration loaded successfully")
        logger.info(f"Starting bot polling...")
        
        # Start the bot
        await application.run_polling(
            allowed_updates=["message", "callback_query", "error"]
        )
    
    except KeyError as e:
        logger.error(f"Configuration error: Missing environment variable {str(e)}")
        logger.error("Please ensure all required environment variables are set in .env")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        logger.error("Bot failed to start")
        sys.exit(1)


if __name__ == "__main__":
    import asyncio
    
    try:
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
