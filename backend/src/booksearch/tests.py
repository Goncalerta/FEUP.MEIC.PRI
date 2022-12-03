# pylint: disable=no-member
"""Booksearch Unit Tests"""

from rest_framework.test import APITestCase

# Create your tests here.
class TestCase(APITestCase):
    """Example Test Case"""

    def setUp(self):
        """Setup the test case"""
        self.two = 2

    def test_one_plus_one_equals_two(self):
        """Example of a test"""
        self.assertEqual(1+1, self.two)
