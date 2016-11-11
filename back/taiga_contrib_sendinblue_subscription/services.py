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

from django.conf import settings

import mailin

from .import utils


def _get_sendinblue_api():
    sendinblue_api_url = getattr(settings, "SENDINBLUE_API_URL", "https://api.sendinblue.com/v2.0")
    sendinblue_api_key = settings.SENDINBLUE_API_KEY
    return mailin.Mailin(sendinblue_api_url, sendinblue_api_key)


@utils.catch_connection_errors
@utils.log_api_response
def subscribe_new_user(username, full_name, email):
    data = {
        "email": email,
        "attributes": {
            "USERNAME": username,
            "FULL_NAME": full_name,
        },
        "listid": [
            settings.SENDINBLUE_TAIGA_USERS_LIST_ID,
            settings.SENDINBLUE_NEWSLETTER_LIST_ID
        ]
    }

    api = _get_sendinblue_api()
    return api.create_update_user(data)


@utils.catch_connection_errors
@utils.log_api_response
def update_user_info(old_email, new_email, username, full_name):
    api = _get_sendinblue_api()

    data = {
        "email": old_email
    }
    listid = api.get_user(data).get("data", {}).get("listid", [])

    api.delete_user(data)

    data = {
        "email": new_email,
        "attributes": {
            "USERNAME": username,
            "FULL_NAME": full_name,
        },
        "listid": listid or [
            settings.SENDINBLUE_TAIGA_USERS_LIST_ID,
            settings.SENDINBLUE_NEWSLETTER_LIST_ID
        ]
    }
    return api.create_update_user(data)


@utils.catch_connection_errors
@utils.log_api_response
def unsubscribe_user_from_newsletter_list(email):
    data = {
        "id": settings.SENDINBLUE_NEWSLETTER_LIST_ID,
        "users": [email]
    }

    api = _get_sendinblue_api()
    return api.delete_users_list(data)


@utils.catch_connection_errors
@utils.log_api_response
def unsubscribe_user_from_taiga_user_list(email):
    data = {
        "id": settings.SENDINBLUE_TAIGA_USERS_LIST_ID,
        "users": [email]
    }

    api = _get_sendinblue_api()
    return api.delete_users_list(data)


@utils.catch_connection_errors
@utils.log_api_response
def delete_user(email):
    data = {
        "email": email
    }

    api = _get_sendinblue_api()
    return api.delete_user(data)
