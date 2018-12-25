import oci, os,random,string,time
from oci.identity.models import CreateUserDetails
from config_parse import getConfig
from oci.core.models import LaunchInstanceDetails,CreateVcnDetails,CreateSubnetDetails

def get_instance():
    instance_id=getConfig("INSTANCE","instance_id")
    instance=compute_client.get_instance(instance_id)
    return instance

def list_instances():
    compartment_id=getConfig("INSTANCE","compartment_id")
    instance_list=compute_client.list_instances(compartment_id)
    return instance_list


def lanche_instance():
    compartment_id = getConfig("INSTANCE", "compartment_id")
    availability_domain = getConfig("INSTANCE","availability_domain")
    shape = getConfig("INSTANCE","shape")
    request = LaunchInstanceDetails()
    request.compartment_id=compartment_id
    request.availability_domain=availability_domain
    request.shape=shape
    instance = compute_client.launch_instance(request)
    return instance

def create_vcn():
    cidr_block = getConfig("VCN","cidr_block")
    vcn_client = oci.core.VirtualNetworkClient(config)
    vcn_details = CreateVcnDetails()
    vcn_details.cidr_block=cidr_block
    vcn_details.display_name="".join(random.sample(string.ascii_letters+string.digits,8))
    vcn_details.compartment_id=getConfig("VCN", "compartment_id")
    vcn_result=vcn_client.create_vcn(vcn_details)
    get_vcn_response = oci.wait_until(vcn_client,vcn_client.get_vcn(vcn_result.data.id),'lifecycle_state','AVAILABLE')
    print ('Created VCN:{}'.format(get_vcn_response.data.id))
    return get_vcn_response


def delete_vcn(vcn):
    vcn_client = oci.core.VirtualNetworkClient(config)
    vcn_client.delete_vcn(vcn.id)
    vcn_result = wait_time(get_vcn,vcn.id,2)
    if vcn_result :
        print ('Deleted VCN:{}'.format(vcn.id))


def get_vcn(vcn_id):
    vcn_client = oci.core.VirtualNetworkClient(config)
    try:
        vcn=vcn_client.get_vcn(vcn_id)
        print ('Get VCN:{}'.format(vcn.data.id))
    except oci.exceptions.ServiceError as e:
        print ('{} is not found!'.format(vcn_id))
        vcn=None
    finally:
         return vcn


def wait_time(method,method_arg,times):
    n=0
    rct=False
    while n < times:
        result=method(method_arg)
        if result is None:
            rct = True
            break
        time.sleep(5)
        n=n+1
    return rct



def create_subnet(vcn):
    subnet_client = oci.core.VirtualNetworkClient(config)
    subnet_details = CreateSubnetDetails()
    subnet_details.cidr_block = getConfig("SUBNET", "cidr_block")
    subnet_details.display_name = "".join(random.sample(string.ascii_letters + string.digits, 8))
    subnet_details.compartment_id = getConfig("SUBNET", "compartment_id")
    subnet_details.availability_domain = getConfig("SUBNET", "availability_domain")
    subnet_details.vcn_id=vcn.id
    subnet_result = subnet_client.create_subnet(subnet_details)
    get_subnet_response = oci.wait_until(subnet_client, subnet_client.get_subnet(subnet_result.data.id), 'lifecycle_state',
                                      'AVAILABLE')
    print ('Created Subnet:{}'.format(get_subnet_response.data.id))
    return get_subnet_response





"""
Configure proxy
"""
os.environ['http_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'
os.environ['https_proxy'] = 'http://www-proxy-hqdc.us.oracle.com:80'


config=oci.config.from_file()
compute_client = oci.core.ComputeClient(config)

if __name__ == '__main__':
   # instance_list=list_instances()
    #instance=lanche_instance()

    vcn=get_vcn('ocid1.vcn.oc1.iad.aaaaaaaaxjpjiof62dpkbnrj24rrae5jo4qyhgk6jspc3cu4kjduxv2poifq')
    create_subnet(vcn.data)
  #delete_vcn(vcn.data)
  # vcn=create_vcn()
   #print vcn.data
   #delete_vcn(vcn.data)



