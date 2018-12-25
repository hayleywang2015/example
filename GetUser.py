import oci, os
from oci.identity.models import CreateUserDetails
from config_parse import getConfig

os.environ['http_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'
os.environ['https_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'


config=oci.config.from_file()
identity=oci.identity.IdentityClient(config)

compartment_id=config["tenancy"]


user_id=getConfig("User","user_id")
user=identity.get_user(user_id)


userList=identity.list_users(compartment_id)
print(userList.data)
