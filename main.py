import time
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token for the bot (replace with your actual token)
TOKEN = '7099387246:AAHvkLRjfztzrMTBdD3nMz_-dOtUkwRrTCU'

# Wallet addresses
WALLETS = {
    'pay_USDT_TRC20': 'TSq9rYr1xAiiNoPbhXZVEt1i6Z9omp9xyh',
    'pay_USDT_TON': 'UQCQWfecAmNAcqNO0EbCAiv1YwRcnpw7uLmxzPcxlUmoo7wc',
}

# Texts for each plan
PLAN_TEXTS = {
    'Basic_Daily': '''
💼 Basic Daily 
  - 💵 Price: $4 
  - 📊 Concurrent Usage: 1 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 60 seconds 
    - Layer 7:  300 seconds 
  - 🔓 Access Level: Standard
''',
    'Basic_Weekly': '''
💼 Basic Weekly 
  - 💵 Price: $12 
  - 📊 Concurrent Usage: 1 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 60 seconds 
    - Layer 7:  300 seconds 
  - 🔓 Access Level: Standard
''',
    'Basic_Monthly': '''
💼 Basic Monthly 
  - 💵 Price: $24 
  - 📊 Concurrent Usage: 1 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 60 seconds 
    - Layer 7:  300 seconds 
  - 🔓 Access Level: Standard
''',
    'Premium_Daily': '''
💎 Premium Daily 
  - 💵 Price: $8 
  - 📊 Concurrent Usage: 2 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 150 seconds 
    - Layer 7:  1000 seconds 
  - 🔓 Access Level: VIP
''',
    'Premium_Weekly': '''
💎 Premium Weekly 
  - 💵 Price: $20 
  - 📊 Concurrent Usage: 2 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 150 seconds 
    - Layer 7:  1000 seconds 
  - 🔓 Access Level: VIP
''',
    'Premium_Monthly': '''
💎 Premium Monthly 
  - 💵 Price: $52 
  - 📊 Concurrent Usage: 2 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 150 seconds 
    - Layer 7:  1000 seconds 
  - 🔓 Access Level: VIP
''',
    'Ultima_Daily': '''
🚀 Ultima Daily 
  - 💵 Price: $12 
  - 📊 Concurrent Usage: 2 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 250 seconds 
    - Layer 7:  3600 seconds 
  - 🔓 Access Level: VIP
''',
    'Ultima_Weekly': '''
🚀 Ultima Weekly 
  - 💵 Price: $28 
  - 📊 Concurrent Usage: 2 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 250 seconds 
    - Layer 7:  3600 seconds 
  - 🔓 Access Level: VIP
''',
    'Ultima_Monthly': '''
🚀 Ultima Monthly 
  - 💵 Price: $72 
  - 📊 Concurrent Usage: 2 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 250 seconds 
    - Layer 7:  3600 seconds 
  - 🔓 Access Level: VIP
''',
    'Business_Daily': '''
🏢 Business Monthly 
  - 💵 Price: $136 
  - 📊 Concurrent Usage: 3 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 250 seconds 
    - Layer 7:  7200 seconds 
  - 🔓 Access Level: VIP
''',
    'Elite_Weekly': '''
🏆 Elite Monthly 
  - 💵 Price: $200 
  - 📊 Concurrent Usage: 5 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 250 seconds 
    - Layer 7:  10800 seconds 
  - 🔓 Access Level: VIP
''',
    'Enterprise_Monthly': '''
💼 Enterprise Monthly 
  - 💵 Price: $400 
  - 📊 Concurrent Usage: 6 
  - ⏳ Attack Duration Limit: 
    - Layer 4 : 250 seconds 
    - Layer 7: 18000 seconds 
  - 🔓 Access Level: VIP
'''
}

async def start(update: Update, context) -> None:
    keyboard = [[InlineKeyboardButton("💳 Buy plan", callback_data='buy_plan')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Hello! Welcome to Kraken Autobuy bot.\n\nThis is an anonymous bot for instant purchases.",
        reply_markup=reply_markup
    )

async def button(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'buy_plan':
        keyboard = [
            [InlineKeyboardButton("💼 Basic Daily", callback_data='Basic_Daily'),
             InlineKeyboardButton("💼 Basic Weekly", callback_data='Basic_Weekly'),
             InlineKeyboardButton("💼 Basic Monthly", callback_data='Basic_Monthly')],
            [InlineKeyboardButton("💎 Premium Daily", callback_data='Premium_Daily'),
             InlineKeyboardButton("💎 Premium Weekly", callback_data='Premium_Weekly'),
             InlineKeyboardButton("💎 Premium Monthly", callback_data='Premium_Monthly')],
            [InlineKeyboardButton("🚀 Ultima Daily", callback_data='Ultima_Daily'),
             InlineKeyboardButton("🚀 Ultima Weekly", callback_data='Ultima_Weekly'),
             InlineKeyboardButton("🚀 Ultima Monthly", callback_data='Ultima_Monthly')],
            [InlineKeyboardButton("🏢 Business Daily", callback_data='Business_Daily'),
             InlineKeyboardButton("🏆 Elite Weekly", callback_data='Elite_Weekly'),
             InlineKeyboardButton("💼 Enterprise Monthly", callback_data='Enterprise_Monthly')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Select plan to purchase.", reply_markup=reply_markup)
    
    elif query.data in PLAN_TEXTS:
        await query.edit_message_text(
            text=f"{PLAN_TEXTS[query.data]}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Process payment", callback_data=f'payment_{query.data}')],
                [InlineKeyboardButton("🔙 Back", callback_data='buy_plan')]
            ])
        )
    
    elif query.data.startswith('payment_'):
        plan = query.data.replace('payment_', '')
        price_line = next(line for line in PLAN_TEXTS[plan].split('\n') if 'Price' in line)
        price = price_line.split(':')[1].strip()

        context.user_data['price'] = price
        context.user_data['plan'] = plan

        keyboard = [
            [InlineKeyboardButton("💰 USDT TRC20", callback_data='pay_USDT_TRC20')],
            [InlineKeyboardButton("💰 USDT TON", callback_data='pay_USDT_TON')],
            [InlineKeyboardButton("🔙 Back", callback_data='buy_plan')]
        ]
        await query.edit_message_text(text=f"The price is {price}.\n\nSelect payment method.", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data.startswith('pay_'):
        wallet_address = WALLETS[query.data]
        plan = context.user_data.get('plan', 'N/A')
        price = context.user_data.get('price', 'N/A')

        await query.edit_message_text(
            text=f"💳 **Order awaiting payment**\n"
                 f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                 f"Payment Method:** {query.data.replace('pay_', '').replace('_', ' ').upper()}\n\n"
                 f"Payment Address:** `{wallet_address}`\n\n"
                 f"Payment Amount:** {price} USDT\n\n"
                 f"👆 **Click to copy [Payment Address / Amount]**\n"
                 f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                 f"⚠️ The order payment timeout is 60 minutes\n"
                 f"🚀 Plan will be activated immediately after successful payment."
        )
    
    elif query.data == 'back':
        await start(update, context)

def run_bot():
    while True:
        try:
            application = Application.builder().token(TOKEN).build()

            application.add_handler(CommandHandler('start', start))
            application.add_handler(CallbackQueryHandler(button))

            application.run_polling()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(5)  # Wait 5 seconds before restarting

if __name__ == '__main__':
    run_bot()
