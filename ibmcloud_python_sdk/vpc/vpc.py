import json

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group


class Vpc():

    def __init__(self):
        self.cfg = params()
        self.rg = resource_group.ResourceGroup()

    def get_vpcs(self):
        """
        Retrieve VPC list
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching VPCs. {}".format(error))
            raise

    def get_vpc(self, vpc):
        """
        Retrieve specific VPC by name or by ID
        :param vpc: VPC name or ID
        """
        by_name = self.get_vpc_by_name(vpc)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_vpc_by_id(vpc)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_vpc_by_id(self, id):
        """
        Retrieve specific VPC by ID
        :param id: VPC ID
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching VPC with ID {}. {}".format(id, error))
            raise

    def get_vpc_by_name(self, name):
        """
        Retrieve specific VPC by name
        :param name: VPC name
        """
        try:
            # Retrieve VPCs
            data = self.get_vpcs()
            if "errors" in data:
                return data

            # Loop over VPCs until filter match
            for vpc in data['vpcs']:
                if vpc["name"] == name:
                    # Return data
                    return vpc

            # Return error if no VPC is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching VPC with name {}. {}".format(name, error))
            raise

    def get_default_network_acl(self, vpc):
        """
        Retrieve VPC's default network ACL
        :param vpc: VPC name or ID
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_network_acl?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching default network ACL for VPC"
                  " {}. {}".format(vpc, error))
            raise

    def get_default_security_group(self, vpc):
        """
        Retrieve VPC's default security group
        :param vpc: VPC name or ID
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_security_group?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching default security group for VPC"
                  " {}. {}".format(vpc, error))
            raise

    def get_address_prefixes(self, vpc):
        """Retrieve VPC address pool prefix list

        :param vpc: VPC name or ID
        :return Address prefix list
        :rtype dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching address prefixes in VPC {}. {}".format(
                vpc, error))
            raise

    def get_address_prefix(self, vpc, prefix):
        """Retrieve specific VPC address prefix by name or by ID

        :param vpc: VPC name or ID
        :param prefix: Address prefix name or ID
        :return Address prefix information
        :rtype dict
        """
        by_name = self.get_address_prefix_by_name(vpc, prefix)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_address_prefix_by_id(vpc, prefix)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_address_prefix_by_id(self, vpc, id):
        """Retrieve specific VPC address prefix by ID

        :param vpc: VPC name or ID
        :param id: Address prefix ID
        :return Address prefix information
        :rtype dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes/{}?version={}"
                    "&generation={}".format(vpc_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching adress prefix with ID {} in VPC {}."
                  " {}".format(vpc, id, error))
            raise

    def get_address_prefix_by_name(self, vpc, name):
        """Retrieve specific VPC address prefix by name

        :param vpc: VPC name or ID
        :param name: Address prefix name
        :return Address prefix information
        :rtype dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Retrieve address prefixes
            data = self.get_address_prefixes(vpc_info["id"])
            if "errors" in data:
                return data

            # Loop over address prefixes until filter match
            for prefix in data['address_prefixes']:
                if prefix["name"] == name:
                    # Return data
                    return prefix

            # Return error if no address prefix is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching address prefix with name {} in VPC {}."
                  " {}".format(vpc, name, error))
            raise

    def create_vpc(self, **kwargs):
        """
        Create VPC (Virtual Private Cloud)
        :param name: Optional. The unique user-defined name for this VPC.

        :param resource_group: Optional. The resource group to use.

        :param address_prefix_management: Optional. Indicates whether a
        default address prefix should be automatically created for
        each zone in this VPC.

        :param classic_access: Optional. Indicates whether this VPC should
        be connected to Classic Infrastructure.
        """
        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'address_prefix_management': kwargs.get(
                'address_prefix_management', 'auto'),
            'classic_access': kwargs.get('classic_access', False),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating VPC. {}".format(error))
            raise

    def create_address_prefix(self, **kwargs):
        """Create address prefix

        :param vpc: VPC name or ID.
        :param name: Optional. The user-defined name for this address prefix.
        :param cidr: The CIDR block for this address prefix.
        :param is_default: Optional. Indicates whether this is the default
        prefix for this zone in this VPC.
        :param zone: The zone this address prefix is to belong to.
        :return Address prefix information
        :rtype dict
        """
        args = ["vpc", "cidr", "zone"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'vpc': kwargs.get('vpc'),
            'name': kwargs.get('name'),
            'cidr': kwargs.get('cidr'),
            'is_default': kwargs.get('is_default', False),
            'zone': kwargs.get('zone'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "vpc" and value is not None:
                payload[key] = value

        # Check if VPC exists and get information
        vpc_info = self.get_vpc(args['vpc'])
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes?version={}"
                    "&generation={}".format(self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating address prefix in VPC {}. {}".format(
                args['vpc'], error))
            raise

    def delete_vpc(self, vpc):
        """
        Delete VPC
        :param vpc: VPC name or ID
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}".format(
                vpc_info["id"], self.cfg["version"], self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting VPC {}. {}".format(vpc, error))
            raise

    def delete_address_prefix(self, vpc, prefix):
        """Delete address prefix

        :param vpc: VPC name or ID
        :param prefix: Address prefix name or ID
        :return Deletion status
        :rtype dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        # Check if address prefix exists and get information
        prefix_info = self.get_address_prefix(vpc, prefix)
        if "errors" in prefix_info:
            return prefix_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes/{}?version={}"
                    "&generation={}".format(vpc_info["id"], prefix_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting adress prefix {} in VPC {}. {}".format(
                prefix, vpc, error))
            raise
