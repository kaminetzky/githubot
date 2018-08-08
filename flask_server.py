import flask
from request_processor import TelegramRequestProcessor, GithubRequestProcessor
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Website(flask.Flask):

    def __init__(self, telegram, github, github_user, github_repo,
                 authorized_chats, broadcast_chats, main_chat, tareos_chat,
                 channel_chat):
        super().__init__(__name__)

        self.telegram = telegram
        self.github = github
        self.authorized_chats = authorized_chats
        self.broadcast_chats = broadcast_chats
        self.main_chat = main_chat
        self.tareos_chat = tareos_chat
        self.channel_chat = channel_chat

        self.telegram_request_processor = TelegramRequestProcessor(self.github,
                                                                   github_user,
                                                                   github_repo)
        self.github_request_processor = GithubRequestProcessor(
            self.github, self.telegram, self.broadcast_chats, self.main_chat,
            self.tareos_chat, self.channel_chat)
        self.configure_routes()

    def configure_routes(self):
        @self.route('/')
        def home():
            return flask.render_template('home.html')

        @self.route('/post/telegram', methods=['POST'])
        def telegram_post():
            update = flask.request.get_json()
            if 'message' in update:
                if 'text' in update['message']:
                    chat_id = update['message']['chat']['id']
                    if update['message']['text'].startswith('/'):
                        if chat_id in self.authorized_chats:
                            reply_text = (self.telegram_request_processor
                                          .process_request(update))
                        else:
                            reply_text = ('Solo tengo permitido hablar con '
                                          'ciertos grupos. ¡Lo siento!')
                        self.telegram.send_message(chat_id, reply_text)
            return ''

        @self.route('/post/github', methods=['POST'])
        def github_post():
            update = flask.request.get_json()
            self.github_request_processor.process_request(update)
            return ''
