import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Telegram:
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot{}'.format(token)

    def send_message(self, chat_id, text):
        url = self.url + '/sendMessage'
        payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
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


class CryptoMKT:
    @staticmethod
    def get_prices():
        payload = {'market': 'ETHCLP'}
        response = requests.get('https://api.cryptomkt.com/v1/ticker',
                                params=payload)
        response_json = response.json()
        price_dict = {'bid': int(response_json['data'][0]['bid']),
                      'ask': int(response_json['data'][0]['ask'])}
        return price_dict


class SurBTC:
    @staticmethod
    def get_prices():
        response = requests.get(
            'https://www.surbtc.com/api/v2/markets/eth-clp/ticker.json')
        response_json = response.json()
        price_dict = {'bid': int(float(response_json['ticker']['max_bid'][0])),
                      'ask': int(float(response_json['ticker']['min_ask'][0]))}
        return price_dict


class Orionx:
    @staticmethod
    def get_prices():
        url = 'http://api.orionx.io/graphql'
        query = '''
        query getOrderBook($marketCode: ID!) {
            orderBook: marketOrderBook(marketCode: $marketCode) {
                spread
                mid
            }
        }
        '''
        request_json = {'query': query,
                        'operationName': 'getOrderBook',
                        'variables': {'marketCode': 'ETHCLP'}}

        response = requests.post(url=url, json=request_json)
        response_json = response.json()
        spread = response_json['data']['orderBook']['spread']
        mid = response_json['data']['orderBook']['mid']
        price_dict = {'bid': int(mid - spread / 2),
                      'ask': int(mid + spread / 2)}
        return price_dict
