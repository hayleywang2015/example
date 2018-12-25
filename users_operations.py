import oci, os,random,string
from oci.identity.models import CreateUserDetails
from config_parse import getConfig

os.environ['http_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'
os.environ['https_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'


config=oci.config.from_file()
identity=oci.identity.IdentityClient(config)
compartment_id=config["tenancy"]


def get_user():
    user_id = getConfig("User","user_id")
    user = identity.get_user(user_id)
    return user


def list_user():
    compartment_id_ = getConfig("User", "compartment_id")
    user_list = identity.list_users(compartment_id_)
    return user_list


def create_user():
    request = CreateUserDetails()
    request.compartment_id = compartment_id
    request.name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    request.description = "The user "+request.name+" was created with Python SDK"
    user = identity.create_user(request)
    return user


if __name__ == '__main__':
    user=get_user()
    print user.data

