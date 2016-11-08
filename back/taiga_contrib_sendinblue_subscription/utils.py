# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import wraps
import logging

logger = logging.getLogger(__name__)


def log_api_response(function):
    @wraps(function)
    def decorator(*args):
        res = function(*args)

        code = res.get("code", "error")
        if code == "success":
            logger.info("[Sendinblue] {call}{ars} - {message}:\n{data}".format(
                call=function.__name__,
                ars=str(args),
                message=res.get("message", "-no message-"),
                data=res.get("data", "-no data-")
            ))
        else:
            logger.error("[Sendinblue] error on {call}{ars} - {message}:\n{data}".format(
                call=function.__name__,
                ars=str(args),
                message=res.get("message", "-no message-"),
                data=res.get("data", "-no data-")
            ))

        return res

    return decorator


def catch_connection_errors(function):
    @wraps(function)
    def decorator(*args):
        try:
            function(*args)
        except Exception as e:
            logger.error("[Sendinblue] error on {call}{ars}:\n{err}".format(
                call=function.__name__,
                ars=str(args),
                err=e
            ))

    return decorator
