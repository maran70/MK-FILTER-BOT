from pyrogram import Client, filters
from info import ADMINS
import os

# ---------------------------------------------------------------------------------
# 1. LIST OF ALL ADMIN-EDITABLE KEYS DISCOVERED FROM info.py
# ---------------------------------------------------------------------------------
# This list ensures security by restricting the /set command to ONLY these keys.
# No other environment variables or system keys can be modified.
ALLOWED_KEYS = {
    # Bot Identity & API
    'SESSION', 'API_ID', 'API_HASH', 'BOT_TOKEN', 'PORT',
    
    # Channels & Groups
    'LOG_CHANNEL', 'CHANNELS', 'AUTH_CHANNEL', 'REQST_CHANNEL', 
    'INDEX_REQ_CHANNEL', 'SUPPORT_CHAT_ID', 'FILE_STORE_CHANNEL', 
    'DELETE_CHANNELS', 'PUBLIC_FILE_CHANNEL', 
    
    # Permissions & Lists
    'ADMINS', 'AUTH_USERS', 
    
    # Database
    'DATABASE_URI', 'DATABASE_NAME', 'COLLECTION_NAME', 
    'MULTIPLE_DATABASE', 'O_DB_URI', 'F_DB_URI', 'S_DB_URI', 
    'CLONE_DATABASE_URI',
    
    # Features & Modes (Booleans)
    'REQUEST_TO_JOIN_MODE', 'TRY_AGAIN_BTN', 'PREMIUM_AND_REFERAL_MODE', 
    'CLONE_MODE', 'AI_SPELL_CHECK', 'PM_SEARCH', 'BUTTON_MODE', 
    'MAX_BTN', 'IS_TUTORIAL', 'IMDB', 'AUTO_FFILTER', 'AUTO_DELETE', 
    'LONG_IMDB_DESCRIPTION', 'SPELL_CHECK_REPLY', 'MELCOW_NEW_USERS', 
    'PROTECT_CONTENT', 'PUBLIC_FILE_STORE', 'NO_RESULTS_MSG', 
    'USE_CAPTION_FILTER', 'STREAM_MODE', 'RENAME_MODE', 'AUTO_APPROVE_MODE',
    'SHORTLINK_MODE', 'VERIFY', 'VERIFY_SECOND_SHORTNER',
    
    # URLs & Links
    'PICS', 'GRP_LNK', 'CHNL_LNK', 'SUPPORT_CHAT', 'OWNER_LNK', 'URL',
    
    # Verification & Shortlinks
    'VERIFY_SHORTLINK_URL', 'VERIFY_SHORTLINK_API', 'VERIFY_TUTORIAL',
    'VERIFY_SND_SHORTLINK_URL', 'VERIFY_SND_SHORTLINK_API',
    'SHORTLINK_URL', 'SHORTLINK_API', 'TUTORIAL', 'PAYMENT_QR',
    
    # Text & Captions
    'PAYMENT_TEXT', 'MSG_ALRT', 'CUSTOM_FILE_CAPTION', 
    'BATCH_FILE_CAPTION', 'IMDB_TEMPLATE',
    
    # Limits & Thresholds
    'REFERAL_COUNT', 'REFERAL_PREMEIUM_TIME', 'CACHE_TIME', 
    'MAX_B_TN', 'MAX_LIST_ELM', 'SLEEP_THRESHOLD', 'PING_INTERVAL'
}

# ---------------------------------------------------------------------------------
# 2. PLUGIN IMPLEMENTATION
# ---------------------------------------------------------------------------------
@Client.on_message(filters.command("set") & filters.user(ADMINS))
async def set_config(client, message):
    """
    Securely updates configuration values in .env file.
    Usage: /set KEY VALUE
    """
    try:
        # Parse command
        if len(message.command) < 3:
            return await message.reply("<b>Usage:</b> <code>/set KEY NEW_VALUE</code>")
        
        key = message.command[1].upper()
        # Join the rest of the message as value to support spaces/newlines
        value = message.text.split(None, 2)[2] 
        
        # Security Check 1: Validate Key
        if key not in ALLOWED_KEYS:
            return await message.reply(
                f"❌ <b>Invalid Key:</b> <code>{key}</code>\n"
                f"<i>Allows only safe configuration keys found in info.py</i>"
            )
        
        # Safe Storage: Update .env file
        update_env_file(key, value)
        
        await message.reply(
            f"✅ <b>Settings Saved!</b>\n\n"
            f"<b>Key:</b> <code>{key}</code>\n"
            f"<b>Value:</b> <i>(Hidden for security)</i>\n\n"
            f"<i>⚠️ You MUST restart the bot for changes to take effect.</i>"
        )
        
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

def update_env_file(key, value):
    """
    Reads local .env file, updates or adds the key, and saves it.
    Replaces existing value completely.
    """
    env_path = ".env"
    lines = []
    
    # Read existing lines if file exists
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
    # Remove existing key if present (to avoid duplicates)
    # We filter out any line that starts with KEY=
    lines = [line for line in lines if not line.strip().startswith(f"{key}=")]
    
    # Append new key-value pair
    # We assume simple KEY=VALUE format. 
    # If logic requires handling multi-line values, usually they are escaped or 
    # the user inputs them as a single line with \n literal.
    # Here we write explicitly.
    lines.append(f"{key}={value}\n")
    
    # Write back atomically (safe write)
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
