import logging
from formatter import Formatter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TelegramRequestProcessor:
    def __init__(self, github, github_user, github_repo):
        self.github = github
        self.github_user = github_user
        self.github_repo = github_repo

    def process_request(self, update):
        message_text = update['message']['text']
        first_name = update['message']['from']['first_name']

        reply_text = 'No reconozco ese comando, {}. :o'.format(first_name)

        commands = {'/start': TelegramRequestProcessor.start_command,
                    '/help': TelegramRequestProcessor.help_command,
                    '/get': self.get_command,
                    '/post': self.post_command,
                    '/label': self.label_command,
                    '/close': self.close_command,
                    '/open': self.open_command}

        command = message_text.split()[0]

        if command in commands:
            reply_text = commands[command](update)

        return reply_text

    @staticmethod
    def start_command(update):
        first_name = update['message']['from']['first_name']
        # TODO modify description
        reply_text = ('Hola {}!\nSoy GithuBot. A través de mí podrás '
                      'interactuar con el repo de Github IIC2233/Syllabus.'
                      '\nPuedes obtener información de alguna issue, como '
                      'también comentarla, etiquetarla, cerrarla y reabrirla.\n'
                      'Además, te informaré cada vez que se abra una issue '
                      'nueva.\nEscribe "/help" para obtener información sobre'
                      'los comandos. :)'.format(first_name))

        return reply_text

    @staticmethod
    def help_command(update):
        first_name = update['message']['from']['first_name']
        # TODO modify description
        reply_text = ('A continuación se muestra una lista de los comandos '
                      'que puedes utilizar, {}.\n\n'
                      '/start\nGithuBot da la bienvenida.\n\n'
                      '/help\nInformación sobre los comandos.\n\n'
                      '/get num_issue\nObtener información sobre la issue '
                      'solicitada.\n\n'
                      '/post num_issue comentario\nComentar la issue con el '
                      'comentario entregado.\n\n'
                      '/label num_issue etiqueta\nAgregar una etiqueta a la'
                      'issue.\n\n'
                      '/close num_issue\nCerrar la issue.\n\n'
                      '/open num_issue\nAbrir la issue.\n\n').format(
            first_name)

        return reply_text

    def get_command(self, update):
        message_text = update['message']['text']
        split_message = message_text.split(' ')
        if len(split_message) == 1:
            return 'Tienes que indicarme qué issue quieres que te busque.'
        elif not split_message[1].isdecimal():
            return ('Tienes que entregarme un número para que pueda encontrar '
                    'la issue.')
        number = int(split_message[1])
        issue, status_code = self.github.get_issue(number)

        if status_code == 200:
            author = issue['user']['login']
            number = issue['number']
            title = issue['title']
            text = issue['body']
            url = issue['html_url']

            message = Formatter.format_issue(author, number, title, text, url)
        elif status_code == 404:
            message = 'No encontré esa issue. :('
        else:
            message = ('Github nos ha entregado una respuesta no esperada. '
                       'Por favor vuelve a intentarlo.')

        return message

    def post_command(self, update):
        message_text = update['message']['text']
        split_message = message_text.split(' ', 2)
        if len(split_message) == 1:
            return ('Tienes que indicarme qué issue quieres que te busque y '
                    'qué quieres que comente.')
        elif not split_message[1].isdecimal():
            return ('Tienes que entregarme un número para que pueda encontrar '
                    'la issue.')
        elif len(split_message) == 2:
            return 'Tienes que decirme qué quieres que comente.'
        number = split_message[1]
        comment = split_message[2]
        status_code = self.github.comment_issue(number, comment)

        if status_code == 201:
            message = 'Issue comentada.'
        elif status_code == 404:
            message = 'No encontré esa issue. :('
        else:
            issue_url = ('https://github.com/{}/{}/issues/{}'.format(
                self.github_user, self.github_repo, number))
            message = ('Github nos ha entregado una respuesta no esperada. '
                       'Por favor confirma que la issue fue comentada en '
                       '{}.').format(issue_url)

        return message

    def label_command(self, update):
        message_text = update['message']['text']
        split_message = message_text.split(' ', 2)
        if len(split_message) == 1:
            return ('Tienes que indicarme qué issue quieres que te busque y '
                    'qué etiqueta quieres ponerle.')
        elif not split_message[1].isdecimal():
            return ('Tienes que entregarme un número para que pueda encontrar '
                    'la issue.')
        elif len(split_message) == 2:
            return 'Tienes que decirme el título de la etiqueta.'
        number = split_message[1]
        label_text = split_message[2]
        status_code = self.github.label_issue(number, label_text)

        if status_code == 200:
            message = 'Issue etiquetada.'
        elif status_code == 404:
            message = 'No encontré esa issue. :('
        else:
            issue_url = ('https://github.com/{}/{}/issues'
                         '/{}'.format(self.github_user, self.github_repo,
                                      number))
            message = ('Github nos ha entregado una respuesta no esperada. '
                       'Por favor confirma que la issue fue etiquetada en '
                       '{}.').format(issue_url)

        return message

    def close_command(self, update):
        message_text = update['message']['text']
        split_message = message_text.split(' ')
        if len(split_message) == 1:
            return 'Tienes que indicarme qué issue quieres que cierre.'
        elif not split_message[1].isdecimal():
            return ('Tienes que entregarme un número para que pueda encontrar '
                    'la issue.')
        number = split_message[1]
        status_code = self.github.close_issue(number)

        if status_code == 200:
            message = 'Issue cerrada.'
        elif status_code == 404:
            message = 'No encontré esa issue. :('
        else:
            issue_url = ('https://github.com/{}/{}/issues/{}'.format(
                self.github_user, self.github_repo, number))
            message = ('Github nos ha entregado una respuesta no esperada. '
                       'Por favor confirma que la issue fue cerrada en '
                       '{}.').format(issue_url)

        return message

    def open_command(self, update):
        message_text = update['message']['text']
        split_message = message_text.split(' ')
        if len(split_message) == 1:
            return 'Tienes que indicarme qué issue quieres que abra.'
        elif not split_message[1].isdecimal():
            return ('Tienes que entregarme un número para que pueda encontrar '
                    'la issue.')
        number = split_message[1]
        status_code = self.github.open_issue(number)

        if status_code == 200:
            message = 'Issue abierta.'
        elif status_code == 404:
            message = 'No encontré esa issue. :('
        else:
            issue_url = ('https://github.com/{}/{}/issues/{}'.format(
                self.github_user, self.github_repo, number))
            message = ('Github nos ha entregado una respuesta no esperada. '
                       'Por favor confirma que la issue fue abierta en '
                       '{}.').format(issue_url)

        return message


class GithubRequestProcessor:
    def __init__(self, github, telegram, chat_ids):
        self.github = github
        self.telegram = telegram
        self.chat_ids = chat_ids

    def process_request(self, update):
        action = update.get('action')
        issue = update['issue']
        if action == 'opened':
            title = issue['title']
            url = issue['html_url']
            message_text = 'Se ha creado una issue!\n'
            message_text += 'Título: {}\n'.format(title)
            message_text += 'URL: {}'.format(url)

            for chat_id in self.chat_ids:
                self.telegram.send_message(chat_id, message_text)
