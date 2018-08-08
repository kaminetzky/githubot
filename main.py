from flask_server import Website
from api_wrapper import Telegram, Github
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

telegram_token = os.environ['telegram_token']
authorized_chats = list(map(int, os.environ['authorized_chats'].split()))
broadcast_chats = list(map(int, os.environ['broadcast_chats'].split()))
main_chat = int(os.environ['main_chat'])
tareos_chat = int(os.environ['tareos_chat'])
channel_chat = int(os.environ['channel_chat'])

github_token = os.environ['github_token']
github_user = os.environ['github_user']
github_repo = os.environ['github_repo']

telegram = Telegram(telegram_token)
github = Github(github_user, github_repo, github_token)

app = Website(telegram, github, github_user, github_repo, authorized_chats,
              broadcast_chats, main_chat, tareos_chat, channel_chat)

if __name__ == '__main__':
    app.run()
