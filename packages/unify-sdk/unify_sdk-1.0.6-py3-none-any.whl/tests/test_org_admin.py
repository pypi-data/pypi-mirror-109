"""
This script contains some test cases for organization administration for the SDK
"""
import unittest
import os
import uuid

from unify.orgadmin import OrgAdmin
from unify.properties import Properties
from unify.properties import ClusterSetting


class TestOrgAdmin(unittest.TestCase):

    def test_can_login(self):
        """
        Verify sdk can login
        :return:
        """
        with Properties(clusterSetting=ClusterSetting.MEMORY) as props:
            cluster_name = "qa"

            props.store_cluster(
                username=os.environ.get("username"),
                password=os.environ.get("password"),
                name=cluster_name,
                cluster=os.environ.get("cluster")
            )
            with OrgAdmin(props=props, cluster=cluster_name) as org_admin:
                props.set_auth_token(
                    token=org_admin.auth_token(),
                    cluster=cluster_name
                )

                token = props.get_auth_token(cluster=cluster_name)

                org_admin.close_session()

                self.assertNotEqual(token, None, "Token is None")

    def test_can_create_org(self):
        """
        Verify sdk can create org
        :return:
        """
        with Properties(clusterSetting=ClusterSetting.MEMORY) as props:
            cluster_name = "qa"

            props.store_cluster(
                username=os.environ.get("username"),
                password=os.environ.get("password"),
                name=cluster_name,
                cluster=os.environ.get("cluster")
            )

            with OrgAdmin(props=props, cluster=cluster_name) as org_admin:
                props.set_auth_token(
                    token=org_admin.auth_token(),
                    cluster=cluster_name
                )

                org_id = org_admin.create_organization(
                    org_name="sdk-tests-{}".format(str(uuid.uuid4()))
                )

                org_admin.close_session()

                self.assertTrue(
                    str(org_id).strip().isdigit(),
                    "Org Id is created and its a number"
                )


if __name__ == '__main__':
    unittest.main()
