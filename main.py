from flask_server import MyApp
from api_wrapper import Telegram, Github, Google  # Remove google
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

telegram_token = os.environ['telegram_token']

github_token = os.environ['github_token']
github_user = os.environ['github_user']
github_repo = os.environ['github_repo']

google_id = os.environ['google_id']  # Remove
google_key = os.environ['google_key']  # Remove

telegram = Telegram(telegram_token)
github = Github(github_user, github_repo, github_token)
google = Google(google_id, google_key)  # Remove

app = MyApp(telegram, github, google)  # Remove google

if __name__ == '__main__':
    app.run()
