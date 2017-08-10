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
import threading
from os import remove
from os.path import exists
import time
from datetime import datetime
import logging
from requests import HTTPError, RequestException, get

"""
How to run: $pytest -r test_download_image.py
Requirement: IMGSRV running in IP address and PORT as specified below
"""

LOG = logging.getLogger(__name__)

# List of files to download
FLIST = ['test.qcow', 'test.xml']
URL = 'http://127.0.0.1:5000/'
API = 'api/v1/'
URL_XML = URL + API + 'get?name=test.xml'
URL_QCOW = URL + API + 'get?name=test.qcow'
DST_XML = '/tmp/test.xml'
DST_QCOW = '/tmp/test.qcow'


class TestDownloadImage(unittest.TestCase):

    @staticmethod
    def cleanup(fdel):
        """Delete file"""
        if exists(fdel):
            LOG.info('deleting %s', fdel)
            remove(fdel)

    @staticmethod
    def download(link, file_dst):
        """Create HTTP request to download the file"""
        try:
            resp = get(link, stream=True)
            LOG.info("downloading %s at %s" % (link, file_dst))
            with open(file_dst, 'wb') as fread:
                for chunk in resp.iter_content(1024):
                    if chunk:
                        fread.write(chunk)
        except HTTPError, ex:
            raise HTTPError("HTTP Error:", ex.code, link)
        except RequestException, ex:
            raise RequestException("Request Error:", ex.reason, link)

    def create_download_thread(self, link, file_dst):
        """create multi-threads to download files"""
        LOG.info("starting thread %s for %s" % (datetime.now(), link))
        download_thread = threading.Thread(target=self.download,
                                           args=(link, file_dst))
        # daemonize thread, it is needed to be able to interrupt download
        # before the whole file is saved
        download_thread.setDaemon(True)
        download_thread.start()

    def test_access(self):
        """Test HTTP is up and response has success status code"""
        resp = get(URL)
        self.assertEqual(resp.status_code, 200,
                         "Request failed: {0}\n{1}".format(resp.status_code,
                                                           resp.content))

    def test_download_image_xml(self):
        """Test download image XML definition file"""
        self.cleanup(DST_XML)
        self.create_download_thread(URL_XML, DST_XML)
        self.cleanup(DST_XML)

    def test_download_image_qcow(self):
        """Test download image QCOW definition file. this function is handled
        by a multi-threading and will be terminated on purpused after 5 seconds
        as the QCOW file usually is > 4GB sometimes >8GB this function is not
        testing the content of file after being donwloaded.
        """
        self.cleanup(DST_QCOW)
        self.create_download_thread(URL_QCOW, DST_QCOW)
        # wait 5 seconds before terminate the threads still acitve
        time.sleep(5)
        self.cleanup(DST_QCOW)

if __name__ == '__main__':
    unittest.main()
