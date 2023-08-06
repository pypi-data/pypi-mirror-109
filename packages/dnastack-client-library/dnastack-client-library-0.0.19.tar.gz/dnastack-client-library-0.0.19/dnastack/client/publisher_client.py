from dnastack.client import *
from dnastack import constants
from pandas import DataFrame
from getpass import getpass
import json


class PublisherClient:
    def __init__(
        self,
        email=None,
        personal_access_token=None,
        dataconnect_url=None,
        collections_url=None,
        auth_params=auth_params,
    ):
        self.email = email
        self.personal_access_token = personal_access_token
        self.dataconnect_url = dataconnect_url
        self.collections_url = collections_url
        self.auth_params = auth_params
        self.oauth_token = {}
        self.dataconnect = self.dataconnect(self)
        self.collections = self.collections(self)

    """
    def login(self, server=None, email=None, personal_access_token=None):
        # if the user did not provide a PAT or email, get that from input
        if not server:
            server = input("Enter your DRS Server: ")

        if not (personal_access_token or self.personal_access_token):
            personal_access_token = getpass("Enter your Personal Access Token (PAT): ")

        if not (email or self.email):
            email = input("Enter your Email: ")

        drs_host = get_host(server)

        self.oauth_token[drs_host] = login(
            email=email if email else self.email,
            personal_access_token=personal_access_token
            if personal_access_token
            else self.personal_access_token,
            auth_params=self.auth_params,
            dataconnect_url=self.dataconnect_url,
            drs_url=server,
        )
    """

    class dataconnect:
        def __init__(self, parent):
            self.parent = parent

        def query(self, q, download=False, use_json=False, raw=False):
            return json.loads(
                dataconnect_client.query(
                    self.parent.dataconnect_url,
                    q,
                    download,
                    use_json,
                    raw,
                    self.parent.oauth_token,
                )
            )

        def list_tables(self):
            return json.loads(
                dataconnect_client.list_tables(
                    self.parent.dataconnect_url, self.parent.oauth_token
                )
            )

        def get_table(self, table_name):
            return json.loads(
                dataconnect_client.get_table(
                    self.parent.dataconnect_url, table_name, self.parent.oauth_token
                )
            )

    class collections:
        def __init__(self, parent):
            self.parent = parent

        def list(self):
            return collections_client.list_collections(self.parent.collections_url)

        def list_tables(self, collection_name):
            return collections_client.list_tables(
                self.parent.collections_url, collection_name
            )

        def query(self, collection_name, query):
            return collections_client.query(
                self.parent.collections_url, collection_name, query
            )

    def load(self, urls, output_dir=downloads_directory):
        download_content = []
        download_files(
            urls,
            output_dir,
            self.oauth_token,
            self.email,
            self.personal_access_token,
            self.auth_params,
            download_content,
        )
        return download_content

    def download(self, urls, output_dir=downloads_directory):
        return download_files(
            urls,
            output_dir,
            self.oauth_token,
            self.email,
            self.personal_access_token,
            self.auth_params,
        )
