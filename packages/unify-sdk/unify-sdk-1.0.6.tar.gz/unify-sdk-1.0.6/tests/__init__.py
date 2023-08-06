import os
import uuid

from unify.orgadmin import OrgAdmin
from unify.properties import Properties
from unify.properties import ClusterSetting

cluster_name = "qa"
props = Properties(clusterSetting=ClusterSetting.MEMORY)

props.store_cluster(
    username=os.environ.get("username"),
    password=os.environ.get("password"),
    name=cluster_name,
    cluster=os.environ.get("cluster")
)

org_admin = OrgAdmin(props=props, cluster=cluster_name)
props.set_auth_token(
    token=org_admin.auth_token(),
    cluster=cluster_name
)
test_org = org_admin.create_organization(
    org_name="zQA-{}".format(str(uuid.uuid4()))
)

print("--------Created organization {} for testing------", format(test_org))
