from formatter import Formatter
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TelegramRequestProcessor:
    def __init__(self, github, chats):
        self.github = github
        self.chats = chats

    def process_request(self, update):
        message_text = update['message']['text']
        first_name = update['message']['chat']['first_name']

        reply_text = 'No reconozco ese comando, {}. :o'.format(first_name)

        commands = {'/start': TelegramRequestProcessor.start_command,
                    '/help': TelegramRequestProcessor.help_command,
                    '/sub': self.sub_command,
                    '/unsub': self.unsub_command,
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
        first_name = update['message']['chat']['first_name']

        reply_text = ('Hola {}!\nSoy NetzkyBot. A través de mí podrás '
                      'interactuar con el repo de Github NetzkyBot/test-repo.'
                      '\nPuedes obtener información de alguna issue, como '
                      'también comentarla, etiquetarla, cerrarla y reabrirla.\n'
                      'Además, si te suscribes con "/sub" te informaré '
                      'cada vez que se abra una issue nueva.\nEscribe "/help" '
                      'para obtener información sobre los comandos. :)'.format(
                       first_name))

        return reply_text

    @staticmethod
    def help_command(update):
        first_name = update['message']['chat']['first_name']

        reply_text = ('A continuación se muestra una lista de los comandos '
                      'que puedes utilizar, {}.\n\n'
                      '/start\nNetzkyBot da la bienvenida.\n\n'
                      '/help\nInformación sobre los comandos.\n\n'
                      '/sub\nSuscribirse a las notificaciones de cuando se '
                      'crea una issue.\n\n'
                      '/unsub\nCancelar la suscripción.\n\n'
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

    def sub_command(self, update):
        chat_id = update['message']['chat']['id']
        first_name = update['message']['chat']['first_name']

        if chat_id not in self.chats:
            self.chats.append(chat_id)
            reply_text = ('Ahora te informaré cada vez que se abra una issue '
                          'nueva en el repo NetzkyBot/test-repo. :)'.format(
                           first_name))
        else:
            reply_text = '{}, ya estás suscrito. ;)'.format(first_name)

        return reply_text

    def unsub_command(self, update):
        chat_id = update['message']['chat']['id']

        if chat_id in self.chats:
            self.chats.remove(chat_id)
            reply_text = ('Has cancelado tu suscripción. Puedes escribir '
                          '"/sub" para volver a suscribirte. ;)')
        else:
            reply_text = ('No estás suscrito. Puedes escribir "/sub" para '
                          'suscribirte! ;)')
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
                       'Por favor vuelve a intentarlo')

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
            issue_url = ('https://github.com/NetzkyBot/test-repo/issues'
                         '/{}'.format(number))
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
            issue_url = ('https://github.com/NetzkyBot/test-repo/issues'
                         '/{}'.format(number))
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
            issue_url = ('https://github.com/NetzkyBot/test-repo/issues'
                         '/{}'.format(number))
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
            issue_url = ('https://github.com/NetzkyBot/test-repo/issues'
                         '/{}'.format(number))
            message = ('Github nos ha entregado una respuesta no esperada. '
                       'Por favor confirma que la issue fue abierta en '
                       '{}.').format(issue_url)

        return message


class GithubRequestProcessor:
    def __init__(self, github, telegram, chat, google):
        self.github = github
        self.telegram = telegram
        self.google = google
        self.chat = chat

    def process_request(self, update):
        action = update.get('action')
        issue = update['issue']
        if action == 'opened':
            author = issue['user']['login']
            number = issue['number']
            title = issue['title']
            text = issue['body']
            url = issue['html_url']
            message_text = 'Se ha creado una issue!\n'
            message_text += Formatter.format_issue(author, number, title, text,
                                                   url)
            for chat_id in self.chat:
                self.telegram.send_message(chat_id, message_text)

            error_text = self.seek_exception(text)
            if error_text:
                self.post_helpful_link(error_text, number)
        elif action == 'closed':
            self.check_googleable(issue)

    @staticmethod
    def seek_exception(text):
        # Chequeamos si está la palabra "Traceback" entre dos "```".
        markdown_text = re.search('```((.|\n)+)?Traceback(.|\n)+```', text)
        if markdown_text:
            markdown_text = markdown_text.group(0)
            error_text = markdown_text.split('\n')[-2]
        else:
            error_text = ''
        return error_text

    def post_helpful_link(self, error_text, issue_number):
        link = self.google.get_first_link(error_text)
        second_link = ('http://orig12.deviantart.net/acf9/f/2008/251/1/e'
                       '/link_raep_face_by_linkrapefaceplz.png')
        if link:
            text = ('Veo que hay una excepción en tu código. :o\n'
                    'Quizás este [link]({}) te podría ayudar :)\n'
                    'Aquí va otro [link]({}).'.format(link, second_link))
        else:
            text = ('Vi que hay una excepción en tu código. :o\n'
                    'Sin embargo, no pude encontrar algún link que te pueda '
                    'ayudar. :(\n'
                    'Aquí va un [link]({}) (que no te va a ayudar).').format(
                second_link)
        self.github.comment_issue(issue_number, text)

    def check_googleable(self, issue):
        author = issue['user']['login']
        issue_number = issue['number']
        text = issue['body']

        # Chequeamos si la issue contiene una excepción.
        if re.search('```((.|\n)+)?Traceback(.|\n)+```', text):
            comments = self.github.get_comments(issue_number)
            if len(comments) == 1:
                # El comentario tiene que ser del bot, entregando el link.
                if (comments[0]['user']['login'] == 'NetzkyBot'
                        and comments[0]['body'].startswith('Veo que hay')):
                    self.github.label_issue(issue_number, 'Googleable')
            elif len(comments) == 2:
                # El primer comentario tiene que ser del bot, entregando el
                # link. El segundo debe ser del autor de la issue.
                if (comments[0]['user']['login'] == 'NetzkyBot'
                        and comments[0]['body'].startswith('Veo que hay')
                        and comments[1]['user']['login'] == author):
                    self.github.label_issue(issue_number, 'Googleable')
