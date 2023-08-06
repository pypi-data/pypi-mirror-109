import os
import json
import time

import adal
from msrestazure.azure_active_directory import AADTokenCredentials


class MishmashWrongCredentialsException(Exception):
    pass


class MishmashUnauthorizedException(Exception):
    pass


class MishmashAuth():

    def __init__(self):
        # access token is valid 1 hour

        self.authority_host_url = 'https://login.microsoftonline.com'
        
        config_data = self.get_configuration()
        self.__tenant_id = config_data["AZURE_TENANT_ID"]
        self.__client_id = config_data["AZURE_CLIENT_ID"]
        self.__client_secret = config_data["AZURE_CLIENT_SECRET"]
        self.__mishmash_api_resource_url = config_data["AZURE_RESOURCE_URL"]
        self.__authority_url = self.authority_host_url + '/' + self.__tenant_id
        self.__credentials = None

    def get_configuration(self):

        config_file_path = os.environ.get("AZURE_CONFIG_FILE_PATH", None)
        
        if config_file_path:
            config_data = self.get_configuration_from_file(config_file_path)
        else:
            config_data = self.get_configuration_from_env()

        if not config_data:
            raise MishmashUnauthorizedException("set azure config variables")

        if not config_data["AZURE_TENANT_ID"]:
            raise MishmashUnauthorizedException(
                "please add AZURE_TENANT_ID as config variable")

        if not config_data["AZURE_CLIENT_ID"]:
            raise MishmashUnauthorizedException(
                "please add AZURE_CLIENT_ID as config variable")

        if not config_data["AZURE_CLIENT_SECRET"]:
            raise MishmashUnauthorizedException(
                "please add AZURE_CLIENT_SECRET as config variable")

        if not config_data["AZURE_RESOURCE_URL"]:
            raise MishmashUnauthorizedException(
                "please add AZURE_RESOURCE_URL as config variable")

        return config_data

    def get_configuration_from_file(self, config_file_path):
        try:
            with open(config_file_path, "r") as f:
                return json.load(f)

        except FileNotFoundError:
            return None

    def get_configuration_from_env(self):

        config_data = {
            "AZURE_TENANT_ID": os.environ.get("AZURE_TENANT_ID", None),
            "AZURE_CLIENT_ID": os.environ.get("AZURE_CLIENT_ID", None),
            "AZURE_CLIENT_SECRET": os.environ.get("AZURE_CLIENT_SECRET", None),
            "AZURE_RESOURCE_URL": os.environ.get("AZURE_RESOURCE_URL", None),
        }

        return config_data

    def __generate_new_credentials_with_client_credentials(self):
        """
           generate new  AuthenticationContext credentials with client credentials
        """
        context = adal.AuthenticationContext( self.__authority_url, api_version=None)

        try:
            mgmt_token = context.acquire_token_with_client_credentials(self.__mishmash_api_resource_url,
                                                                       self.__client_id,
                                                                       self.__client_secret)
        except adal.adal_error.AdalError:
            raise MishmashWrongCredentialsException

        return AADTokenCredentials(mgmt_token, self.__client_id)

    def is_access_token_expired(self):
        
        expires_on = self.__credentials.token['expires_on']

        if expires_on -  time.time() < 0:
            return True

        return False

    def get_or_create_access_token(self):
        """
            Check if access token is outdated and create new one if so
        """

        if not self.__credentials:
            self.__credentials = self.__generate_new_credentials_with_client_credentials()
            return self.__credentials.token["access_token"]

        if self.is_access_token_expired():
            self.__credentials = self.__generate_new_credentials_with_client_credentials()
            return self.__credentials.token["access_token"]

        return self.__credentials.token["access_token"]

    @property
    def authorization_header(self):
        return f"Bearer {self.access_token}"

    @property
    def access_token(self):

        access_token = self.get_or_create_access_token()

        if not access_token:
            raise MishmashUnauthorizedException("invalid access token")

        return access_token

    @property
    def app_id(self):
        return self.__client_id
