from bs4 import BeautifulSoup
import json
import requests
import urllib.parse


class Scrapper(object):
    def __init__(self, email, password, cookie_jar=None):
        super(Scrapper, self).__init__()
        self.email = email
        self.password = password
        self.session = requests.Session()
        if cookie_jar is not None:
            self.session.cookies = cookie_jar
        self.login()

    def login(self):
        html = self.session.get('https://www.linkedin.com/').text
        soup = BeautifulSoup(html, 'html.parser')
        csrf = soup.select_one('#loginCsrfParam-login').attrs['value']

        self.session.post('https://www.linkedin.com/uas/login-submit', data={
            'session_key': self.email,
            'session_password': self.password,
            'isJsEnabled': False,
            'loginCsrfParam': csrf
        })

    def retry_login(tries=3):
        def wrapped(f):
            def f_retry(self, *args, **kwargs):
                h_tries = tries
                while True:
                    try:
                        return f(self, *args, **kwargs)
                    except Exception as e:
                        print('retry')
                        self.login()
                        if h_tries > 1:
                            h_tries -= 1
                        else:
                            raise(e)
            return f_retry
        return wrapped

    def _fast_method(self, email_to_get):
        trying = self.session.get(f'https://www.linkedin.com/sales/gmail/profile/proxy/{email_to_get}')
        if (trying.url.startswith('https://www.linkedin.com/in/')):
            return trying.url
        else:
            return False

    def _safe_method(self, email_to_get):
        def buildSearchUrl(term):
            return 'https://www.linkedin.com/voyager/api/search/cluster?blendedSrpEnabled=true&count=10&guides=List()&keywords={}&origin=GLOBAL_SEARCH_HEADER&q=guided&start=0'.format(urllib.parse.quote_plus(term))

        html = self.session.get(f'https://www.linkedin.com/sales/gmail/profile/viewByEmail/{email_to_get}').text
        soup = BeautifulSoup(html, 'html.parser')

        user_id = soup.select_one('.li-img-profile-large').attrs['src'].split('/profile-displayphoto')[0].split('/')[-1]

        terms = []
        for selector in ['.li-user-name > a', '.li-user-title']:
            try:
                terms.append(soup.select_one(selector).text)
            except Exception:
                pass
        term = ' '.join(terms)

        raw = self.session.get(buildSearchUrl(term), headers={'csrf-token': self.session.cookies['JSESSIONID'][1:-1]}).text
        search_result = json.loads(raw)

        profile_id = None
        for each1 in search_result['elements']:
            for each2 in each1['elements']:
                if user_id in each2['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['rootUrl']:
                    profile_id = each2['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['publicIdentifier']

        if profile_id is not None:
            return f'https://www.linkedin.com/in/{profile_id}'


    @retry_login(3)
    def get_profile(self, email_to_get):
        fast = self._fast_method(email_to_get)
        if fast:
            return fast
        else:
            return self._safe_method(email_to_get)
