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

from os.path import join, exists
from os import stat, listdir
from stat import ST_SIZE, ST_MTIME
import math
import time
from json import dumps, loads
from util import file_mgmt

""" Model layer """


def convert_size(size_bytes):
    """ Math function to convert bytes to GB"""
    if size_bytes == 0:
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    index = int(math.floor(math.log(size_bytes, 1024)))
    equation = math.pow(1024, index)
    size = round(size_bytes/equation, 2)
    return '%s %s' % (size, size_name[index])


def get_total_qcow(_root):
    """ List all QCOW files from _root folder and return the total found

    :param _root: full path for folder to list files
    :type _root: str
    :return: data
    :rtype: json
    """
    count = 0
    for file_qcow in listdir(_root):
        if file_qcow.lower().endswith(".qcow"):
            count = count + 1

    data = dumps(count)
    return loads(data)


def get_qcow_files(_root, url=None):
    """ Get all QCOW files available in _root folder.

    An valid image for PAWS QCOW Image Service is the combination of:
    - .qcow ( it is the actual QCOW file exported from Openstack )
    - .xml  ( it is the output from virsh dumpxml )
    - .paws ( it is the output from PAWS provision task used to create the
    VM in Openstack and consequently the source for snapshot export )

    example: a new QCOW image is extracted from Openstack for Windows_2016
    to be a valid Image for PAWS QCOW Image Service and ready to be consumed
    by PAWS for libvirt provider on the upload time it need:

    windows_2016.qcow
    windows_2016.xml
    windows_2016.paws

    This function retrieves all .qcow files from folder specified _root and
    map their .xml + .paws retrieving all informative fields for the user.
    The return is a json object

    :param _root: full path for folder to list files
    :type _root: str
    :return: data
    :rtype: json
    """
    _image = []
    for file_qcow in listdir(_root):
        if file_qcow.lower().endswith(".qcow"):
            _statinfo = None
            _dict_image = {'name': None,
                           'qcow': None,
                           'qcow_url': None,
                           'xml': None,
                           'size': None,
                           'mtime': None,
                           'win_username': None,
                           'win_password': None}

            _dict_image['name'] = file_qcow.replace('.qcow', '')
            _dict_image['qcow'] = file_qcow
            _dict_image['qcow_url'] = url + _dict_image['qcow']

            # map xml file by same name given to qcow
            xml_path = join(_root, file_qcow.replace('.qcow', '.xml'))
            if exists(xml_path):
                _dict_image['xml'] = file_qcow.replace('.qcow', '.xml')
            else:
                _dict_image['xml'] = 'not found'

            # map paws file by same name given to qcow
            paws_path = join(_root, file_qcow.replace('.qcow', '.paws'))
            if exists(paws_path):
                fcontent = file_mgmt('r', paws_path)
                resource = fcontent['resources'][0]
                _dict_image['win_username'] = resource['win_username']
                _dict_image['win_password'] = resource['win_password']
            else:
                _dict_image['win_username'] = 'not found'
                _dict_image['win_password'] = 'not found'

            _statinfo = stat(join(_root, file_qcow))
            _dict_image['size'] = convert_size(_statinfo[ST_SIZE])
            _dict_image['mtime'] = time.ctime(_statinfo[ST_MTIME])
            _image.append(_dict_image)

    data = dumps(_image)
    return loads(data)


def get_file(_root, name):
    """Check if file requested exists in root path on the server side
    and return the full path for the file if yes.

    :pram _root: full path for where all files are saved in the server
    :param name: file name with extension e.g.: test.qcow or test.xml
    :return f_path: full path for the file requested
    :rtype f_path: str
    """
    f_path = join(_root, name)

    if not exists(f_path):
        error_msg = {'error': "File " + name + " does not exist"}
        return error_msg

    return f_path
