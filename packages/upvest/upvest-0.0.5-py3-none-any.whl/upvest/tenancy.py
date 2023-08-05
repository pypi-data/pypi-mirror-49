from upvest.config import API_VERSION, UPVEST_API_TARGET
from upvest.authentication import KeyAuth
from upvest.model import UserInstance, Users, Assets

class UpvestTenancyAPI(object):
    def __init__(self, api_key, api_secret, api_passphrase, base_url=None):
        base_url = base_url or UPVEST_API_TARGET
        self.auth_instance = KeyAuth(api_key=api_key, api_secret=api_secret, api_passphrase=api_passphrase, base_url=base_url)
        self.users = Users(self.auth_instance)
        self.assets = Assets(self.auth_instance)
