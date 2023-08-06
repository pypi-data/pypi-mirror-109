"""
Contains cluster definition
"""

class Cluster:
    """
    Class to store cluster data on memory
    """

    def __init__(self, userName, password, cluster, token):
        """
        Constructor

        :param userName: Cluster login username
        :type userName: str
        :param password: Cluster login password
        :type password: str
        :param cluster: Cluster url, format http://host
        :type cluster: str
        :param token: Auth token
        :type token: str
        """
        self.userName = userName
        self.password = password
        self.cluster = cluster
        self.token = token

    def get_password(self):
        """
        Get cluster password

        :return:
        """
        return self.password

    def get_username(self):
        """
        Get cluster password

        :return:
        """
        return self.userName
