from ibmcloud_python_sdk.utils import softlayer as sl
from ibmcloud_python_sdk.utils.common import resource_error
from ibmcloud_python_sdk.utils.common import check_args


class Order():

    def __init__(self):
        self.client = sl.client()
        self.order = sl.SoftLayer.OrderingManager(self.client)

    def get_operating_systems(self, package=None):
        """Retrieve baremetal operating systems

        :param package: Package name.
        :return: Baremetal operating systems
        :rtype: dict
        """
        # Provided package should have "os" category code.
        pkg_name = "BARE_METAL_SERVER"
        if package:
            pkg_name = package

        filter = {"items": {"categories": {"categoryCode": {
            "operation": "_= os"}}}}
        mask = "keyName, description, id"

        try:
            images = {}
            images["operating_systens"] = self.order.list_items(
                pkg_name, filter=filter, mask=mask)

            return images

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_package_items(self, package=None, **kwargs):
        """Retrieve baremetal operating systems

        :param package: Package name.
        :param category: Filter by category.
        :return: Baremetal operating systems
        :rtype: dict
        """
        # Build dict of argument and assign default value when needed
        args = {
            'category': kwargs.get('category'),
            'mask': kwargs.get('mask'),
        }

        filter = None
        if args['category']:
            filter = {"items": {"categories": {"categoryCode": {
                "operation": "_= {}".format(args['category'])}}}}

        pkg_name = "BARE_METAL_SERVER"
        if package:
            pkg_name = package

        mask = "id, keyName, description"

        try:
            packages = {}
            packages["items"] = self.order.list_items(pkg_name, mask=mask,
                                                      filter=filter)

            return packages

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_package_presets(self, package=None):
        """Retrieve baremetal package presets

        :param package: Package name.
        :return: Baremetal presets from package
        :rtype: dict
        """
        pkg_name = "BARE_METAL_SERVER"
        if package:
            pkg_name = package

        try:
            packages = {}
            packages["presets"] = self.order.list_presets(pkg_name)

            return packages

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_locations(self):
        """Retrieve all datacenter locations

        :return: List of datacenter location
        :rtype: dict
        """
        mask = "id,name,regions[keyname,description]"
        try:
            locations = {}
            locations["datacenters"] = self.client.call(
                "SoftLayer_Location", "getDatacenters", mask=mask)

            return locations

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def verify(self, **kwargs):
        """Verify an order

        :param package: The package being ordered.
        :param location: The datacenter location string for ordering.
        :param items: The list of item keyname strings to order.
        :param complex_type: The complex type to send with the order.
        :param hourly: Optional. If true, uses hourly billing.
        :param preset: Optional. Specifies a preset to use for that package.
        :param extras: The extra data for the order in dictionary format.
        :param quantity: Optional. The number of resources to order.
        :return: The order verification
        :rtype: dict
        """
        args = ["package", "location", "items", "complex_type", "extras"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'package': kwargs.get('package'),
            'location': kwargs.get('location'),
            'items': kwargs.get('items'),
            'complex_type': kwargs.get('complex_type'),
            'hourly': kwargs.get('hourly', True),
            'preset': kwargs.get('preset'),
            'extras': kwargs.get('extras'),
            'quantity': kwargs.get('quantity', 1),
        }

        try:
            return self.order.verify_order(
                args['package'], args['location'], args['items'],
                hourly=args['hourly'], preset_keyname=args['preset'],
                complex_type=args['complex_type'], extras=args['extras'],
                quantity=args['quantity'])

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)