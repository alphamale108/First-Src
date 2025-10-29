from flask import Flask
import threading
import os
import logging
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_started = False

def start_bot():
    """Start the Telegram bot"""
    global bot_started
    try:
        logger.info("Starting Telegram Restricted Content Bot...")
        # Import and run your main bot file
        from main import main
        bot_thread = threading.Thread(target=main, daemon=True)
        bot_thread.start()
        logger.info("Bot started successfully in background thread")
        bot_started = True
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        import traceback
        traceback.print_exc()

@app.route('/')
def home():
    return """
    <h1>🤖 Telegram Restricted Content Bot</h1>
    <p>Bot is running successfully!</p>
    <p><a href="/health">Check Health</a></p>
    <p><strong>Features:</strong> Save restricted content, Force subscribe, User management</p>
    """

@app.route('/health')
def health():
    if bot_started:
        return "✅ Bot is healthy and running", 200
    else:
        return "❌ Bot is not running", 500

@app.route('/status')
def status():
    return {
        "status": "running" if bot_started else "starting",
        "service": "Telegram Content Bot",
        "version": "1.0",
        "bot_started": bot_started
    }

# Start bot immediately when app starts
logger.info("Initializing Telegram Bot...")
start_bot()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
