import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk import resource_group


class Key():

    def __init__(self):
        self.cfg = params()
        self.rg = resource_group.Resource()

    def get_keys(self):
        """
        Retrieve key list
        """
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching keys. {}").format(error)
            raise

    def get_key(self, key):
        """
        Retrieve specific key
        :param key: Key name or ID
        """
        by_name = self.get_key_by_name(key)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_key_by_id(key)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_key_by_id(self, id):
        """
        Retrieve specific key by ID
        :param id: Key ID
        """
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching key with ID {}. {}").format(id, error)
            raise

    def get_key_by_name(self, name):
        """
        Retrieve specific key by name
        :param id: Key name
        """
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve keys data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over keys until filter match
            for key in data["keys"]:
                if key["name"] == name:
                    # Return data
                    return key

            # Return error if no key is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching key with name {}. {}").format(name, error)
            raise

    def create_key(self, **kwargs):
        """
        Create key
        :param name: Optional. The unique user-defined name for this key.

        :param resource_group: Optional. The resource group to use.

        :param public_key: A unique public SSH key to import, encoded in PEM
        format.

        :param type: Optional. The cryptosystem used by this key.
        """
        args = ["public_key"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'public_key': kwargs.get('public_key'),
            'resource_group': kwargs.get('resource_group'),
            'type': kwargs.get('type', 'rsa'),
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
            # Connect to api endpoint for keys
            path = ("/v1/keys?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating key. {}").format(error)
            raise

    def delete_key(self, key):
        """
        Delete key
        :param key: Key name or ID
        """
        try:
            # Check if key existskey
            key_info = self.get_key(key)
            if "errors" in key_info:
                return key_info

            # Connect to api endpoint for keys
            path = ("/v1/keys/{}?version={}&generation={}").format(
                key_info["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting key with name {}. {}").format(key, error)
            raise
