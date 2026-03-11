"""
LEAH Concierge Demo Bot — Message Handlers
Implements world-class demo flow with Groq API
"""

import logging
from telegram import Update, ParseMode
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from telegram.error import TelegramError

from services.ai_service import ai_service
from config.settings import ERROR_MESSAGES, DEMO_PROPERTY

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - World-class welcome"""
    try:
        user = update.effective_user
        user_id = user.id
        
        logger.info(f"User {user_id} ({user.first_name}) started bot")
        
        # World-class welcome message
        welcome_message = f"""Welcome to LEAH Concierge.

You're now experiencing LEAH as a guest at the magnificent **{DEMO_PROPERTY['name']}**, located in {DEMO_PROPERTY['location']}.

This is a demonstration of an AI-powered concierge assistant designed to help luxury properties automate guest services while maintaining 5-star quality.

**To see what I can do, try asking one of these:**

• "What are the best fine-dining restaurants near here?"
• "I can't figure out the coffee machine, can you help?"
• "What's the WiFi password?"
• "What's the weather like today?"
• "What attractions should I visit?"

Pay close attention to the speed and quality of the responses. This is the experience that earns 5-star reviews and frees up 90% of your time managing guest requests."""
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"Sent welcome message to user {user_id}")
    
    except TelegramError as e:
        logger.error(f"Telegram error in start_command: {str(e)}")
        await update.message.reply_text("Sorry, I encountered an issue. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error in start_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGES["unknown_error"])


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    try:
        help_text = """🤖 LEAH Concierge Demo

I'm here to demonstrate how LEAH assists luxury properties with guest services.

**Available commands:**
/start - Start the demo
/help - Show this help message
/reset - Start a new conversation
/status - Check your session

**Just type naturally** to ask me anything a guest would ask!"""
        
        await update.message.reply_text(help_text)
        logger.info(f"Sent help message to user {update.effective_user.id}")
    
    except Exception as e:
        logger.error(f"Error in help_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGES["unknown_error"])


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reset command"""
    try:
        user_id = update.effective_user.id
        session = ai_service.get_session(user_id)
        session.reset()
        
        welcome_message = f"""🔄 Conversation reset.

You're back at the beginning of your experience at **{DEMO_PROPERTY['name']}**.

Feel free to ask me anything a guest would ask!"""
        
        await update.message.reply_text(welcome_message)
        logger.info(f"Reset conversation for user {user_id}")
    
    except Exception as e:
        logger.error(f"Error in reset_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGES["unknown_error"])


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command"""
    try:
        user_id = update.effective_user.id
        stats = ai_service.get_session_stats(user_id)
        
        if not stats:
            status_text = "No active session. Type /start to begin."
        else:
            status_text = f"""📊 Session Status

Messages: {stats['messages']}
Created: {stats['created_at']}
Last Activity: {stats['last_activity']}
Session Active: {not stats['is_expired']}"""
        
        await update.message.reply_text(status_text)
        logger.info(f"Sent status to user {user_id}")
    
    except Exception as e:
        logger.error(f"Error in status_command: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGES["unknown_error"])


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages - Core demo experience"""
    try:
        user = update.effective_user
        user_id = user.id
        user_message = update.message.text
        
        logger.info(f"Message from user {user_id}: {user_message[:50]}...")
        
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        # Get AI response using Groq API
        ai_response = await ai_service.get_response(user_id, user_message)
        
        if not ai_response:
            ai_response = ERROR_MESSAGES["api_error"]
        
        # Add value-reinforcing commentary for key features
        session = ai_service.get_session(user_id)
        if session.message_count >= 3 and session.message_count <= 5:
            # Add subtle meta-commentary
            if "wifi" in user_message.lower() or "password" in user_message.lower():
                ai_response += "\n\n_That's one less message you have to answer. LEAH handles these instantly, 24/7._"
            elif "restaurant" in user_message.lower() or "dining" in user_message.lower():
                ai_response += "\n\n_Notice the personalized recommendations? Your guests get this level of service automatically._"
            elif "weather" in user_message.lower():
                ai_response += "\n\n_Real-time information delivered instantly. No delays, no frustration._"
        
        # Send response
        await update.message.reply_text(
            ai_response,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Trigger sales pivot after 5 messages
        if session.message_count == 5:
            pivot_message = """
And... **scene**. 

You've just experienced what your guests will feel: instant, professional, 24/7 service. That's the magic of LEAH.

Now, would you like me to show you how this all works from your side as the host? I can explain the setup, pricing, and how you can have this running for your properties in under 10 minutes.

Just type **"Yes, show me"** to continue."""
            
            await update.message.reply_text(
                pivot_message,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.info(f"Triggered sales pivot for user {user_id}")
        
        logger.info(f"Sent response to user {user_id} ({len(ai_response)} chars)")
    
    except TelegramError as e:
        logger.error(f"Telegram error in handle_message: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGES["api_error"])
    except Exception as e:
        logger.error(f"Unexpected error in handle_message: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGES["unknown_error"])


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                ERROR_MESSAGES["unknown_error"]
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {str(e)}")


def setup_handlers(application):
    """Register all handlers with the application"""
    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    logger.info("All handlers registered successfully")
