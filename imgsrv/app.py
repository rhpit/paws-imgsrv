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

from flask import Flask, render_template, jsonify, abort, make_response
from flask import request, send_file
from model import get_qcow_files, get_total_qcow, get_file
from util import load_properties_file

""" main application layer and web routes """

APP = Flask(__name__)
IMGSRV_PROP = load_properties_file()


@APP.route("/")
def main():
    """ Home """
    total = get_total_qcow(IMGSRV_PROP['qcow_repo'])
    return render_template('home.html',
                           data={"total": total,
                                 "properties": IMGSRV_PROP},
                           title="Home")


@APP.route('/list')
def list_images():
    """ List All Windows Images """
    url_qcow = request.url_root + "qcow/"
    images = get_qcow_files(IMGSRV_PROP['qcow_repo'], url_qcow)
    return render_template('list.html',
                           data={"images": images,
                                 "properties": IMGSRV_PROP},
                           title="List all Windows images")


@APP.route('/api/v1/list', methods=['GET'])
def api_list_images():
    """
    List all metadata for available Windows QCOW images to run on Libvirt
    provider for PAWS

    :return data: list of dictionary contains info from all available
    windows images
    :rtype data: json

    how to run:

    curl http://127.0.0.1:5000/api/v1/list
    elinks http://127.0.0.1:5000/api/v1/list
    firefox http://127.0.0.1:5000/api/v1/list
    """
    # prepare message error
    error_msg = {
        'help': request.url_root + 'faq',
        'url_received': request.url,
        'url_example': request.url_root + 'api/v1/list'}

    req_url = request.url_root + 'api/v1/list/'
    data = get_qcow_files(IMGSRV_PROP['qcow_repo'], url=req_url)
    if data.len() == 0:
        abort(404)

    if 'error' in data:
        error_msg['error'] = data['error']
        return jsonify(error_msg)

    return jsonify(data)


@APP.route('/api/v1/find', methods=['GET'])
def api_find_by_name():
    """
    Find image metadata by image name

    :return data: dictionary with info from available windows image
    :rtype data: json

    how to run:

    curl http://127.0.0.1:5000/api/v1/find?name=test
    elinks http://127.0.0.1:5000/api/v1/find?name=test
    firefox http://127.0.0.1:5000/api/v1/find?name=test
    """
    # prepare message error
    error_msg = {
        'help': request.url_root + 'faq',
        'url_received': request.url,
        'url_example': request.url_root + 'api/v1/find?name=test'}

    # this request must have only one parameter
    if len(request.args) != 1:
        error_msg['error'] = "Required parameter name"
        return jsonify(error_msg)

    # the parameter name must be passed as request argument
    if 'name' not in request.args:
        error_msg['error'] = "name not especified, parameter name is required"
        return jsonify(error_msg)

    data = get_qcow_files(IMGSRV_PROP['qcow_repo'])
    if data.len() == 0:
        abort(404)

    if 'error' in data:
        error_msg['error'] = data['error']
        return jsonify(error_msg)

    for image in data:
        if request.args['name'] in image['name']:
            return jsonify(image)

    error_msg['error'] = 'image name %s not found' % request.args['name']
    return jsonify(error_msg)


@APP.route('/api/v1/get', methods=['GET'])
def api_get_images():
    """
    how to run:
    curl -o file1.xml http://127.0.0.1:5000/api/v1/get?name=test.xml
    curl -o file1.qcow http://127.0.0.1:5000/api/v1/get?name=test.qcow

    :param name: file name with extension e.g.: test.qcow or test.xml
    it might be the fields qcow or xml from result of call
    curl -i http://127.0.0.1:5000/api/v1.0/list
    :type name: str

    """
    # prepare message error
    error_msg = {
        'help': request.url_root + 'faq',
        'url_received': request.url,
        'url_example': request.url_root + 'api/v1/get?name=test.xml'}

    # this request must have only one parameter
    if len(request.args) != 1:
        error_msg['error'] = "Required parameter name"
        return jsonify(error_msg)

    # the parameter name must be passed as request argument
    if 'name' not in request.args:
        error_msg['error'] = "name not especified, parameter name is required"
        return jsonify(error_msg)

    # redir to nginx as he treats large file much better than flask even using
    # streamming content
    data = get_file(IMGSRV_PROP['qcow_repo'], request.args['name'])

    if not data:
        abort(404)

    if 'error' in data:
        error_msg['error'] = data['error']
        return jsonify(error_msg)

    try:
        return send_file(data, attachment_filename=request.args['name'],
                         as_attachment=True)
    except Exception as ex:
        return str(ex)


@APP.errorhandler(404)
def not_found(error):
    """Generic not found 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.route('/api')
def api():
    """
    List all url for REST API and show how to consume it
    --
    by cli:
    $ curl http://127.0.0.1:5000/api/v1/list
    $ elinks http://127.0.0.1:5000/api/v1/list
    $ firefox http://127.0.0.1:5000/api/v1/list
    --
    Finding image by name:
    $ curl http://127.0.0.1:5000/api/v1/find?name=test
    $ elinks http://127.0.0.1:5000/api/v1/find?name=test
    $ firefox http://127.0.0.1:5000/api/v1/find?name=test
    --
    Get/Retrieve image files (xml and qcow):
    $ curl -o file1.xml http://127.0.0.1:5000/api/v1/get?name=test.xml
    $ curl -o file1.qcow http://127.0.0.1:5000/api/v1/get?name=test.qcow
    """
    return render_template('api.html', title="REST API doc")


if __name__ == "__main__":
    APP.run(host='0.0.0.0')
