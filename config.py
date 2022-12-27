from dotenv import load_dotenv
import os

load_dotenv('.env')
bot_token = os.getenv('BOT_TOKEN')
web3_rpc = os.getenv('WEB3_RPC')
admin = os.getenv('ADMIN_ID')
bnc_api_key=os.getenv('BNC_API_KEY')
bnc_api_secret=os.getenv('BNC_API_SECRET')

if os.getenv('FETCH_BALANCES') == "0":
    fetch_balances = False
else:
    fetch_balances = True




