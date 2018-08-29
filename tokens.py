import os

# Set your api tokens and proxy through environmental variables
# (add lines to your .bashrc and restart terminal):
# export BOT_TOKEN='XXXXX:XXXXXXXXXXX'
# export BOT_PROXY='<proxy_address>:<proxy_port>'

token = os.getenv('BOT_TOKEN')
assert token is not None, 'Problem in reading BOT_TOKEN variable. Read tokens.py for information'

proxy = os.getenv('BOT_PROXY')
assert proxy is not None, 'Problem in reading BOT_PROXY variable. Read tokens.py for information'
