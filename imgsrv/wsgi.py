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

from app import application

""" WSGI entry point

how to run:

for devel purpose you can run the command below from a terminal, use this
folder as root.

$ uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi

from your browser:

http://127.0.0.1:8080/
http://127.0.0.1:8080/api/v1/list

or from CMD:

curl http://127.0.0.1:8080/api/v1/list

"""

if __name__ == "__main__":
    application.run(host='0.0.0.0')
