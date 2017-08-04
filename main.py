from flask_server import MyApp
from api_wrapper import Telegram, Github
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

telegram_token = os.environ['telegram_token']
chat_ids = os.environ['chat_ids']

github_token = os.environ['github_token']
github_user = os.environ['github_user']
github_repo = os.environ['github_repo']

telegram = Telegram(telegram_token)
github = Github(github_user, github_repo, github_token)

app = MyApp(telegram, github, github_user, github_repo, chat_ids)

if __name__ == '__main__':
    app.run()
