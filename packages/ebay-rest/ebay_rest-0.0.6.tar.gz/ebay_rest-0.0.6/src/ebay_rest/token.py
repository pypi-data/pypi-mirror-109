# Standard library imports
from datetime import timezone
import os
import json
import time
import threading
from urllib.parse import parse_qs

# Third party imports
from selenium import webdriver  # match webdriver & chrome version https://sites.google.com/chromium.org/driver/
# on Mac, in a terminal, brew install chromedriver

# Local imports
from .date_time import DateTime
from .error import Error
from .oath.credentialutil import CredentialUtil
from .oath.model.model import Environment
from .oath.oauth2api import OAuth2Api


class Token:
    """ Initialize, refresh and supply an eBay OAuth application token.

    This is a facade for the oath module. Instantiation is not required.
    """
    _lock = threading.Lock()
    _oauth2api_inst = None
    _token_application = dict()
    _token_user_access = dict()
    _user_credential_list = dict()

    @staticmethod
    def get_application(sandbox: bool):
        """
        Get an eBay Application Token.

        Object instantiation is not required and is discouraged.

        :param
        sandbox (bool): {True, False} For the sandbox True, for production False.
        """

        with Token._lock:
            try:
                Token._instantiate()
            except Error:
                raise

            if sandbox not in Token._token_application:
                try:
                    Token._refresh_application(sandbox)
                except Error:
                    raise

            if Token._token_application[sandbox].token_expiry.replace(tzinfo=timezone.utc) <= DateTime.now():
                try:
                    Token._refresh_application(sandbox)
                except Error:
                    raise

            token = Token._token_application[sandbox].access_token

        return token

    @staticmethod
    def _refresh_application(sandbox: bool):
        """
        Refresh the eBay Application Token and update all that comes with it.

        :param
        sandbox (bool): {True, False} For the sandbox True, for production False.
        """

        url = "https://api.ebay.com/oauth/api_scope"
        if sandbox:
            env = Environment.SANDBOX
        else:
            env = Environment.PRODUCTION

        token_application = Token._oauth2api_inst.get_application_token(env, [url])
        if token_application.error is not None:
            reason = 'token_application.error ' + token_application.error
            raise Error(number=1, reason=reason)
        if (token_application.access_token is None) or (len(token_application.access_token) == 0):
            raise Error(number=1, reason='token_application.access_token is missing.')

        Token._token_application[sandbox] = token_application

    @staticmethod
    def get_user_access(sandbox: bool):
        """
        Get an eBay User Access Token.

        Object instantiation is not required and is discouraged.

        :param
        sandbox (bool): {True, False} For the sandbox True, for production False.
        """

        with Token._lock:
            try:
                Token._instantiate()
            except Error:
                raise

            if sandbox not in Token._token_user_access:
                try:
                    Token._refresh_user_access(sandbox)
                except Error:
                    raise

            if Token._token_user_access[sandbox].token_expiry.replace(tzinfo=timezone.utc) <= DateTime.now():
                try:
                    Token._refresh_user_access(sandbox)
                except Error:
                    raise

            token = Token._token_user_access[sandbox].access_token

        return token

    @staticmethod
    def _refresh_user_access(sandbox: bool):
        """
        Refresh the eBay User Access Token and update all that comes with it.

        :param
        sandbox (bool): {True, False} For the sandbox True, for production False.
        """

        app_scopes = ["https://api.ebay.com/oauth/api_scope",
                      "https://api.ebay.com/oauth/api_scope/sell.inventory",
                      "https://api.ebay.com/oauth/api_scope/sell.marketing",
                      "https://api.ebay.com/oauth/api_scope/sell.account",
                      "https://api.ebay.com/oauth/api_scope/sell.fulfillment"]
        if sandbox:
            env = Environment.SANDBOX
        else:
            env = Environment.PRODUCTION

        sign_in_url = Token._oauth2api_inst.generate_user_authorization_url(env, app_scopes)
        if sign_in_url is None:
            raise Error(number=1, reason='sign_in_url is None.')

        code = Token._get_authorization_code(sign_in_url)

        token_user_access = Token._oauth2api_inst.exchange_code_for_access_token(env, code)

        if token_user_access.access_token is None:
            raise Error(number=1, reason='user_token.access_token is None.')
        if len(token_user_access.access_token) == 0:
            raise Error(number=1, reason='user_token.access_token is of length zero.')
        Token._token_user_access[sandbox] = token_user_access

    @staticmethod
    def _get_authorization_code(sign_in_url):

        Token._read_user_info()

        if "sandbox" in sign_in_url:
            env_key = "sandbox-user"
        else:
            env_key = "production-user"

        userid = Token._user_credential_list[env_key][0]
        password = Token._user_credential_list[env_key][1]

        delay = 5       # delay seconds to give the page an opportunity to render

        # open browser and load the initial page
        browser = webdriver.Chrome()
        browser.get(sign_in_url)
        time.sleep(delay)

        # fill in the username then click continue
        form_userid = browser.find_element_by_name('userid')
        form_userid.send_keys(userid)
        browser.find_element_by_id('signin-continue-btn').click()
        time.sleep(delay)

        # fill in the password then submit
        form_pw = browser.find_element_by_name('pass')
        form_pw.send_keys(password)
        browser.find_element_by_id('sgnBt').submit()
        time.sleep(delay)

        # get the result url and then close browser
        parsed = parse_qs(browser.current_url, encoding='utf-8')
        browser.quit()

        is_auth_successful = False
        if 'isAuthSuccessful' in parsed:
            if 'true' == parsed['isAuthSuccessful'][0]:
                is_auth_successful = True
        if not is_auth_successful:
            reason = "Authorization unsuccessful, check userid & password: " + userid + " " + password
            raise Error(number=1, reason=reason)

        code = None
        if 'code' in parsed:
            if parsed['code'][0]:
                code = parsed['code'][0]
        if not code:
            raise Error(number=1, reason="Unable to obtain code.")

        return code

    @staticmethod
    def _read_user_info():

        directory = os.getcwd()  # get the current working directory
        user_config_path = os.path.join(directory, 'ebay_rest_user.json')
        try:
            with open(user_config_path, 'r') as f:
                content = json.loads(f.read())

                for key in content:
                    if key in ['production-user', 'sandbox-user']:
                        userid = content[key]['username']
                        password = content[key]['password']
                        Token._user_credential_list.update({key: [userid, password]})
        except IOError:
            raise Error(number=1, reason='Unable to open ' + user_config_path)

    @staticmethod
    def _instantiate():

        if Token._oauth2api_inst is None:
            directory = os.getcwd()  # get the current working directory
            CredentialUtil.load(os.path.join(directory, 'ebay_rest.json'))
            Token._oauth2api_inst = OAuth2Api()
