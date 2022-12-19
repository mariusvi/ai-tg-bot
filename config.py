from dotenv import load_dotenv
import os

load_dotenv('.env')
bot_token = os.getenv('BOT_TOKEN')
web3_rpc = os.getenv('WEB3_RPC')
fetch_balances = os.getenv('FETCH_BALANCE')