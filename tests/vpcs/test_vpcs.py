# import unittest

# from mock import patch

# # import ibmcloud_python_sdk.config
# from ibmcloud_python_sdk.vpc.vpc import Vpc

# import tests.Common as Common
# # from tests.Vpc import Vpc as vpc


# class VPCTestCase(unittest.TestCase):
#     """Test case for the client methods."""

#     def setUp(self):
#         self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
#                              vpc.authentication)
#         self.patcher.start()
#         self.vpc = Vpc()

#     def tearDown(self):
#         self.patcher.stop()

    # @patch('ibmcloud_python_sdk.vpc.vpc.qw', common.fake_get_call)
    # def test_get_vpcs(self):
    #     """Test get_vpcs ."""
    #     response = self.vpc.get_vpcs()
    #     self.assertIsNotNone(response)

    # @patch('ibmcloud_python_sdk.vpc.vpc.qw', common.fake_get_call)
    # def test_get_vpc_with_name(self):
    #     """Test get_vpc with name as parameter."""
    #     response = self.vpc.get_vpc(self.fake_vpc['name'])
    #     self.assertEqual(response['name'], self.fake_vpc['name'])

    # @patch('ibmcloud_python_sdk.vpc.vpc.Vpc.get_vpc', custom.fake_get_vpc)
    # @patch('ibmcloud_python_sdk.vpc.vpc.qw', common.fake_get_one)
    # def test_get_vpc_with_id(self):
    #     """Test get_vpc with id as parameter."""
    #     response = self.vpc.get_vpc(self.fake_vpc['id'])
    #     self.assertEqual(response['id'], self.fake_vpc['id'])

    # @patch('ibmcloud_python_sdk.vpc.vpc.Vpc.get_vpc', custom.fake_get_vpc)
    # @patch('ibmcloud_python_sdk.vpc.vpc.qw', common.fake_get_one)
    # def test_get_vpc_default_security_group(self):
    #     """Test get_vpc_default_security_group."""
    #     response = self.vpc.get_default_security_group(self.fake_vpc['id'])
    #     print(response)
    #     self.assertEqual(response['default_security_group']['name'],
    #                      self.fake_vpc['default_security_group'])

    # @patch('ibmcloud_python_sdk.vpc.vpc.Vpc.get_vpc', custom.fake_get_vpc)
    # @patch('ibmcloud_python_sdk.vpc.vpc.qw', common.fake_get_one)
    # def test_get_vpc_default_network_acl(self):
    #     """Test get_vpc_default_network_acl."""
    #     response = self.vpc.get_default_network_acl(self.fake_vpc['id'])
    #     print(response)
    #     self.assertEqual(response['default_network_acl']['name'],
    #                      self.fake_vpc['default_network_acl'])

    # @patch('ibmcloud_python_sdk.vpc.vpc.qw', common.fake_create)
    # def test_create_vpc_working(self):
    #     """Test create_vpc should work."""
    #     response = self.vpc.create_vpc(name=self.fake_vpc['name'])
    #     self.assertEqual(response['name'], self.fake_vpc['name'])

    # @patch('ibmcloud_python_sdk.vpc.vpc.qw', common.fake_create)
    # def test_create_vpc_not_working(self):
    #     """Test create_vpc should not work."""
    #     response = self.vpc.create_vpc(name=self.fake_vpc['name'])
    #     self.assertNotEqual(response['id'], self.fake_vpc['name'])
