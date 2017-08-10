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

from os import getenv
from os.path import exists, splitext
from json import load as json_load
from json import dump as json_dump
import ConfigParser
from yaml import dump as yaml_dump
from yaml import load as yaml_load

""" Util module """


def file_mgmt(operation, file_path, content=None, cfg_parser=None):
    """A generic function to manage files (read/write).

    :param operation: File operation type to perform
    :type operation: str
    :param file_path: File name including path
    :type file_path: str
    :param content: Data to write to a file
    :type content: object
    :param cfg_parser: Config parser object (Only needed if the file being
        processed is a configuration file parser language)
    :type cfg_parser: bool
    :return: Data that was read from a file
    :rtype: object
    """

    # Determine file extension
    file_ext = splitext(file_path)[-1]

    if operation in ['r', 'read']:
        # Read
        if not exists(file_path):
            raise IOError("%s file not found!" % file_path)

        if file_ext == ".json":
            # json
            with open(file_path) as f_raw:
                return json_load(f_raw)
        elif file_ext in ['.yaml', '.yml', '.paws']:
            # yaml
            with open(file_path) as f_raw:
                return yaml_load(f_raw)
        else:
            # text
            with open(file_path) as f_raw:
                if cfg_parser is not None:
                    # Config parser file
                    return cfg_parser.readfp(f_raw)
                return f_raw.read()

    elif operation in ['w', 'write']:
        # Write
        mode = 'w+' if exists(file_path) else 'w'
        if file_ext == ".json":
            # json
            with open(file_path, mode) as f_raw:
                json_dump(content, f_raw, indent=4, sort_keys=True)
        elif file_ext in ['.yaml', '.yml', '.paws']:
            # yaml
            with open(file_path, mode) as f_raw:
                yaml_dump(content, f_raw, default_flow_style=False)
        else:
            # text
            with open(file_path, mode) as f_raw:
                if cfg_parser is not None:
                    # Config parser file
                    cfg_parser.write(f_raw)
                else:
                    f_raw.write(content)
    else:
        raise Exception("Unknown file operation: %s." % operation)


def load_properties_file():
    """Load variables from imgsrv.properties file"""
    imgsrv_properties = 'imgsrv.properties'
    properties = {}
    if not exists(imgsrv_properties):
        return properties
    config = ConfigParser.ConfigParser()
    config.read(imgsrv_properties)
    # footer section
    footer = {"doc": config.get('footer', 'doc'),
              "irc": config.get('footer', 'irc'),
              "email": config.get('footer', 'email'),
              "jira": config.get('footer', 'jira'),
              "bugzilla": config.get('footer', 'bugzilla')}
    # qcow_repo section
    path = config.get('qcow_repo', 'path').replace('$USER', getenv('USER'))
    properties = {'footer': footer, 'qcow_repo': path}
    return properties
