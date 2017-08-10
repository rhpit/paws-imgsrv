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
import urllib2
from click import style
from click.termui import progressbar
from clint.textui import progress
from requests import get

"""
How to run: $python test_progress_bar.py
Requirement: IMGSRV running in IP address and PORT as specified below
"""

URL = 'http://127.0.0.1:5000/api/v1/get?name=test.qcow'
PATH_SAVE = '/tmp/test.qcow'


class TestProgressBar(unittest.TestCase):

    def test_click_lib_bar(self):
        """click lib"""
        resp = get(URL, stream=True)
        self.assertEqual(resp.status_code, 200,
                         "Request failed: {0}\n{1}".format(resp.status_code,
                                                           resp.content))
        total_length = int(resp.headers.get('content-length'))
        # progress using python-click lib
        print 'PROGRESS BAR from click lib'
        with open(PATH_SAVE, 'wb+') as fread:
            expected_size = (total_length / 1024) + 1
            with progressbar(resp.iter_content(1024), length=expected_size,
                             label='test.qcow') as chunks:
                for chunk in chunks:
                    fread.write(chunk)
                    fread.flush()

    def test_clint_lib_bar(self):
        """clint lib"""
        resp = get(URL, stream=True)
        self.assertEqual(resp.status_code, 200,
                         "Request failed: {0}\n{1}".format(resp.status_code,
                                                           resp.content))
        total_length = int(resp.headers.get('content-length'))
        # progress using python-clint lib
        print 'PROGRESS BAR from clint lib'
        with open(PATH_SAVE, 'wb') as fread:
            total_length = int(resp.headers.get('content-length'))
            for chunk in progress.bar(resp.iter_content(chunk_size=1024),
                                      expected_size=(total_length/1024) + 1):
                if chunk:
                    fread.write(chunk)
                    fread.flush()

    def test_urllib_lib_bar(self):
        """urllib lib"""
        # progress using python-clint lib
        print 'PROGRESS BAR from clint lib and URLLIB2'
        _chunk = 16 * 1024

        req = urllib2.urlopen(URL)
        meta = req.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (URL, file_size)
        total_remote_length = int(req.headers.get('content-length'))
        self.assertEqual(req.code, 200,
                         "Request failed: {0}\n{1}".format(req.code,
                                                           req.headers))
        pbar_label = 'test.qcow'
        with open(PATH_SAVE, 'wb') as fread:
            with progressbar(length=total_remote_length,
                             fill_char=style('#', fg='green'),
                             empty_char=' ',
                             label=pbar_label) as barr:

                while True:
                    chunk = req.read(_chunk)
                    if not chunk:
                        break
                    fread.write(chunk)
                    barr.update(len(chunk))

if __name__ == '__main__':
    unittest.main()
