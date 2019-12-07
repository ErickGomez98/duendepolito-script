import requests
import webbrowser
import json
import time
from utils import getInputValue, getUrlValue
from datetime import datetime, timedelta

CINEPOLIS_TWITTER_URL = 'https://cinepolis.com/navidad-2019/Account/RedirectToTwitter'
CINEPOLIS_VALIDATE_GAME_URL = 'https://cinepolis.com/navidad-2019/InstructionsGame/ValidateGame'
CINEPOLIS_MAIN_URL = 'https://cinepolis.com/navidad-2019'
TWITTER_SESSION_URL = 'https://api.twitter.com/oauth/authenticate'
FATAL_ERROR = 'No se pudo obtener el status del juego'
WAITING_MSG = 'se logueo en twitter, se reviso la pagina, aun no hay premios'
TOKEN_FILE = 'token.txt'
EMAIL = 'tu_email'
PASSWORD = 'tu_contra'
TIME_INTERVAL = 60

session = requests.Session()


def get_stored_4auth_token():
    f = open(TOKEN_FILE, "r")
    content = f.read()
    f.close()
    return content


def set_stored_4auth_token(token):
    f = open(TOKEN_FILE, "w+")
    f.write(token)
    f.close()
    return True


def get_4auth_token_from_twitter():
    initTwitterLoginSession = session.get(CINEPOLIS_TWITTER_URL)
    text = initTwitterLoginSession.text
    oauth_token = getInputValue(text, "oauth_token")
    authenticity_token = getInputValue(text, "authenticity_token")
    redirect_after_login = getInputValue(text, "redirect_after_login")

    payload_twitter = {
        'session[username_or_email]': EMAIL,
        'session[password]': PASSWORD,
        'authenticity_token': authenticity_token,
        'oauth_token': oauth_token,
        'redirect_after_login': redirect_after_login,
    }

    twitter_request = session.post(
        TWITTER_SESSION_URL, data=payload_twitter,  cookies=initTwitterLoginSession.cookies)

    token_4auth = ""
    if(twitter_request.text.find("Olvidaste tu contraseña") > 0):
        return -1
    else:
        cinepolisUrlGetLastSession = getUrlValue(
            twitter_request.text, 'maintain-context').replace('&amp;', '&')
        cookies = dict(oAuthTwttr=oauth_token)
        session.get(cinepolisUrlGetLastSession)
        token_4auth = session.cookies['4uth']
    return token_4auth


def get_game_status(token_4auth):
    headers = {
        'cookie': f'4uth={token_4auth}',
    }
    get_status = requests.post(CINEPOLIS_VALIDATE_GAME_URL, headers=headers)
    try:
        my_json = json.loads(get_status.text)
        return my_json
    except ValueError as e:
        return -1


def start():
    game_status = get_game_status(get_stored_4auth_token())
    if game_status == -1:
        new_4auth_token = get_4auth_token_from_twitter()
        if new_4auth_token is not -1:
            set_stored_4auth_token(new_4auth_token)
            json_status = get_game_status(new_4auth_token)['status']
            if json_status is not -1:
                if json_status is not 3 and json_status is not 6:
                    webbrowser.open_new_tab(CINEPOLIS_MAIN_URL)
                    return -1
                print(WAITING_MSG)
                return 1
            else:
                print(FATAL_ERROR)
                return -1
        else:
            print(FATAL_ERROR)
            return -1
    else:
        if game_status is not -1:
            if game_status['status'] is not 3 and game_status['status'] is not 6:
                webbrowser.open_new_tab(CINEPOLIS_MAIN_URL)
                return -1
            print(WAITING_MSG)
            return 1
        else:
            print(FATAL_ERROR)


while True:
    st = start()
    if st is not -1:
        time.sleep(TIME_INTERVAL)
    else:
        break
