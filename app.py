from flask import Flask, request
import threading
import subprocess
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to track bot process
bot_process = None

def start_bot():
    """Start the bot in a separate process"""
    global bot_process
    try:
        logger.info("Starting Telegram bot...")
        bot_process = subprocess.Popen(["python", "bot.py"])
        logger.info("Bot started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

@app.route('/')
def home():
    return "🤖 Telegram Bot is Running!"

@app.route('/health')
def health():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return "✅ Bot is healthy and running"
    else:
        return "❌ Bot is not running", 500

@app.route('/restart')
def restart_bot():
    global bot_process
    try:
        if bot_process:
            bot_process.terminate()
            bot_process.wait()
        
        start_bot()
        return "🔄 Bot restarted successfully"
    except Exception as e:
        return f"❌ Failed to restart bot: {e}", 500

# Start bot when app starts
@app.before_first_request
def startup():
    start_bot()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
