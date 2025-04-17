import requests
from datetime import datetime
from pyindia_stock import StockAnalysis
import pandas as pd
import sys

# Hardcoded Telegram configuration
TELEGRAM_BOT_TOKEN = '8017759392:AAEwM-W-y83lLXTjlPl8sC_aBmizuIrFXnU'
TELEGRAM_CHAT_ID = '711856868'

# List of stocks (as per original script)
STOCKS = ['SBIN', 'RELIANCE', 'HDFCBANK', 'INFY', 'TCS']

# Date range for analysis (last 5 years to present)
FROM_DATE = '01/01/2020,09'
TO_DATE = datetime.now().strftime('%d/%m/%Y,15')

def send_telegram_message(message):
    """Send a message to Telegram with MarkdownV2 formatting."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing. Skipping notification.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'MarkdownV2'
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Telegram message sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

def escape_markdown(text):
    """Escape special characters for Telegram MarkdownV2."""
    chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in chars:
        text = text.replace(char, f'\\{char}')
    return text

def analyze_stock(symbol):
    """Analyze a single stock and return a recommendation."""
    try:
        # Initialize StockAnalysis
        analysis = StockAnalysis(index=symbol, period_from=FROM_DATE, period_to=TO_DATE)
        
        # Check if data is available
        if not analysis.is_data_available:
            return f"⚠️ *{symbol}*: No data available or invalid format."
        
        # Access the DataFrame
        df = analysis.read_data
        if df.empty:
            return f"⚠️ *{symbol}*: Empty data returned."
        
        # Get FBProphet forecast
        prophet_model = analysis.fbprophet
        future = prophet_model.make_future_dataframe(periods=1)
        forecast = prophet_model.predict(future)
        
        # Get the latest predicted value
        latest_forecast = forecast.iloc[-1]
        predicted_price = latest_forecast['yhat']
        current_price = df['y'].iloc[-1] if 'y' in df.columns else None
        
        if current_price is None:
            return f"⚠️ *{symbol}*: Unable to retrieve current price."
        
        # Simple recommendation logic
        if predicted_price > current_price * 1.02:  # 2% expected rise
            recommendation = "🟢 *Buy*"
            reason = "Predicted price rise based on FBProphet forecast."
        elif predicted_price < current_price * 0.98:  # 2% expected fall
            recommendation = "🔴 *Sell*"
            reason = "Predicted price drop based on FBProphet forecast."
        else:
            recommendation = "🟡 *Hold*"
            reason = "Stable price predicted by FBProphet."
        
        return (f"{recommendation} *{escape_markdown(symbol)}*\n"
                f"Current Price: ₹{current_price:.2f}\n"
                f"Predicted Price: ₹{predicted_price:.2f}\n"
                f"Reason: {escape_markdown(reason)}")
    
    except ImportError as e:
        return f"⚠️ *{symbol}*: Dependency error - {str(e)}. Ensure FBProphet is installed."
    except Exception as e:
        return f"⚠️ *{symbol}*: Error during analysis - {str(e)}"

def main():
    """Main function to analyze stocks and send Telegram notifications."""
    try:
        # Check if FBProphet is installed
        import fbprophet
    except ImportError:
        error_msg = "🚨 *Critical Error*: FBProphet not installed. Please check workflow setup."
        send_telegram_message(error_msg)
        sys.exit(1)

    # Send start notification
    send_telegram_message(f"📊 *Stock Analysis Started* at {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")

    # Analyze each stock
    recommendations = []
    for symbol in STOCKS:
        result = analyze_stock(symbol)
        recommendations.append(result)
        send_telegram_message(result)
    
    # Send summary with disclaimer
    summary = (f"📈 *Stock Analysis Summary* ({datetime.now().strftime('%Y-%m-%d')})\n\n"
               f"{'-' * 50}\n"
               f"Disclaimer: This analysis is for educational purposes only. "
               f"Not SEBI-registered advice. Always conduct your own research before trading.\n"
               f"Data source: pyindia_stock with FBProphet forecasting.")
    send_telegram_message(summary)

    print("Analysis completed and notifications sent.")

if __name__ == '__main__':
    main()
