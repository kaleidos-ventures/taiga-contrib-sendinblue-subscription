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

from . import services


def subscribe_user_to_sendinblue(sender, **kwargs):
    user = kwargs["user"]

    services.subscribe_new_user(user.username, user.full_name, user.email)


def change_user_email_in_sendinblue(sender, **kwargs):
    user = kwargs["user"]
    old_email = kwargs["old_email"]
    new_email = kwargs["new_email"]

    services.update_user_info(old_email, new_email, user.username, user.full_name)


def unsubscribe_user_from_sendinblue(sender, **kwargs):
    user = kwargs["user"]

    services.unsubscribe_user_from_taiga_user_list(user.email)

    request_data = kwargs.get("request_data", None)
    if not request_data:
        return

    unsuscribe_from_newsletter = request_data.get("unsuscribe", None)
    if unsuscribe_from_newsletter:
        services.unsubscribe_user_from_newsletter_list(user.email)
