import flask
from request_processor import TelegramRequestProcessor, GithubRequestProcessor
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MyApp(flask.Flask):

    def __init__(self, telegram, github, google):
        super().__init__(__name__)
        self.chats = []

        self.telegram = telegram
        self.github = github
        self.google = google

        self.telegram_request_processor = TelegramRequestProcessor(self.github,
                                                                   self.chats)
        self.github_request_processor = GithubRequestProcessor(self.github,
                                                               self.telegram,
                                                               self.chats,
                                                               self.google)
        self.configure_routes()

    def configure_routes(self):
        @self.route('/')
        def home():
            return '''
                <h1>Netzky Bot</h1>
                <p>Github: akaminetzkyp</p>
                '''

        @self.route('/post/telegram', methods=['POST'])
        def telegram_post():
            update = flask.request.get_json()
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                reply_text = self.telegram_request_processor.process_request(
                    update)
                self.telegram.send_message(chat_id, reply_text)
            return ''

        @self.route('/post/github', methods=['POST'])
        def github_post():
            update = flask.request.get_json()
            self.github_request_processor.process_request(update)
            return ''
