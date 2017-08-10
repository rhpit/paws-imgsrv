#
# paws image service -- optional component for paws
# Copyright (C) 2016 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
from requests import get

"""
How to run: $pytest -r test_connect.py
Requirement: IMGSRV running in IP address and PORT as specified below
"""

URL = 'http://127.0.0.1:5000/'
API = 'api/v1/'


class TestConnect(unittest.TestCase):

    def test_access(self):
        """Test HTTP is up and response has success status code"""
        resp = get(URL)
        self.assertEqual(resp.status_code, 200,
                         "Request failed: {0}\n{1}".format(resp.status_code,
                                                           resp.content))

    def test_content_home_page(self):
        """Test content of home page in HTTP response to make sure it is not
        empty so has data"""
        resp = get(URL)
        self.assertTrue(resp.content, "Request failed: {0}\n{1}".
                        format(resp.status_code, resp.content))

if __name__ == '__main__':
    unittest.main()
