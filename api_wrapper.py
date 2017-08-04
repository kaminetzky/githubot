import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Telegram:
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot{}'.format(token)

    def send_message(self, chat_id, text):
        url = self.url + '/sendMessage'
        payload = {'chat_id': chat_id, 'text': text}
        print(text)
        response = requests.post(url, json=payload)
        logger.debug('Send message: {}'.format(response.json()))


class Github:
    def __init__(self, user, repo, token):
        self.user = user
        self.repo = repo
        self.auth = (user, token)

        self.url = 'https://api.github.com/repos/{}/{}/issues'.format(
            self.user, self.repo)

    def get_issue(self, number):
        url = '{}/{}'.format(self.url, number)
        response = requests.get(url, auth=self.auth)
        logger.debug('Get issue: {}'.format(response))
        return response.json(), response.status_code

    def comment_issue(self, number, text):
        url = '{}/{}/comments'.format(self.url, number)
        payload = {'body': text}
        response = requests.post(url, json=payload, auth=self.auth)
        logger.debug('Comment issue: {}'.format(response))
        return response.status_code

    def label_issue(self, number, label):
        url = '{}/{}/labels'.format(self.url, number)
        # Usamos strip porque a Github no le gustan los labels con espacios o
        # saltos de lineas al final o al comienzo.
        payload = [label.strip()]
        response = requests.post(url, json=payload, auth=self.auth)
        logger.debug('Label issue: {}'.format(response))
        return response.status_code

    def close_issue(self, number):
        url = '{}/{}'.format(self.url, number)
        payload = {'state': 'closed'}
        response = requests.patch(url, json=payload, auth=self.auth)
        logger.debug('Close issue: {}'.format(response))
        return response.status_code

    def open_issue(self, number):
        url = '{}/{}'.format(self.url, number)
        payload = {'state': 'open'}
        response = requests.patch(url, json=payload, auth=self.auth)
        logger.debug('Open issue: {}'.format(response))
        return response.status_code

    def get_comments(self, number):
        url = '{}/{}/comments'.format(self.url, number)
        response = requests.get(url, auth=self.auth)
        return response.json()


class Google:
    def __init__(self, id_, key):
        self.id_ = id_
        self.key = key

    def get_first_link(self, search):
        url = ('https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}'
               .format(self.key, self.id_, search))
        response = requests.get(url)
        response_json = response.json()
        if 'items' in response_json:
            link = response_json['items'][0]['link']
            return link
        else:
            return ''
