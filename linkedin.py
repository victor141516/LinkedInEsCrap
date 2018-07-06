from bs4 import BeautifulSoup
import config
import json
import requests
import sys
import urllib.parse

def buildSearchUrl(term):
    return 'https://www.linkedin.com/voyager/api/search/cluster?blendedSrpEnabled=true&count=10&guides=List()&keywords={}&origin=GLOBAL_SEARCH_HEADER&q=guided&start=0'.format(urllib.parse.quote_plus(term))


def get_profile(email):
    session = requests.Session()
    html = session.get('https://www.linkedin.com/').text
    soup = BeautifulSoup(html, 'html.parser')
    csrf = soup.select_one('#loginCsrfParam-login').attrs['value']

    session.post('https://www.linkedin.com/uas/login-submit', data={
        'session_key': config.SCRAP_EMAIL,
        'session_password': config.SCRAP_PASS,
        'isJsEnabled': False,
        'loginCsrfParam': csrf
    })
    trying = session.get('https://www.linkedin.com/sales/gmail/profile/proxy/' + email)
    if (trying.url.startswith('https://www.linkedin.com/in/')):
        return trying.url
    html = session.get('https://www.linkedin.com/sales/gmail/profile/viewByEmail/' + email).text
    soup = BeautifulSoup(html, 'html.parser')

    user_id = soup.select_one('.li-img-profile-large').attrs['src'].split('/profile-displayphoto')[0].split('/')[-1]

    terms = []
    for selector in ['.li-user-name > a', '.li-user-title']:
        try:
            terms.append(soup.select_one(selector).text)
        except Exception:
            pass
    term = ' '.join(terms)

    raw = session.get(buildSearchUrl(term), headers={'csrf-token': session.cookies['JSESSIONID'][1:-1]}).text
    search_result = json.loads(raw)

    profile_id = None
    for each1 in search_result['elements']:
        for each2 in each1['elements']:
            if user_id in each2['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['rootUrl']:
                profile_id = each2['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['publicIdentifier']

    if profile_id is not None:
        return 'https://www.linkedin.com/in/' + profile_id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()
    email = sys.argv[1]
    print(get_profile(email))
