import oci
import os
from oci.identity.models import CreateUserDetails

os.environ['http_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'
os.environ['https_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'


config=oci.config.from_file()
identity=oci.identity.IdentityClient(config)

compartment_id=config["tenancy"]

request = CreateUserDetails()
request.compartment_id=compartment_id
request.name="my-test-user-sdk-1"
request.description="Created with Python SDK1"
user=identity.create_user(request)
print(user.data)
