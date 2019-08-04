import os

# Set your api tokens and proxy through environmental variables
# (add lines to your .bashrc and restart terminal):
# export BOT_TOKEN='XXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# export BOT_ADD_ADMIN_PASSWORD='<password>'

token = os.getenv('BOT_TOKEN')
assert token is not None, 'Problem in reading BOT_TOKEN variable. Read tokens.py for information'

add_admin_password = os.getenv('BOT_ADD_ADMIN_PASSWORD')
assert add_admin_password is not None, 'Problem in reading BOT_ADD_ADMIN_PASSWORD variable.'
