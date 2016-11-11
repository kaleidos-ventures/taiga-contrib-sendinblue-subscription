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

from django.apps import AppConfig



# Checks

def check_sendinblue_api_key(app_configs, **kwargs):
    from django.conf import settings

    sendinblue_api_key = getattr(settings, "SENDINBLUE_API_KEY", None)
    if sendinblue_api_key is not None:
        return []

    return [checks.Error("SENDINBLUE_API_KEY must be set on settings",
                         id="sendinblue_subscription.A001")]


def check_sendinblue_newsletter_list_id(app_configs, **kwargs):
    from django.conf import settings

    newsletter_list_id = getattr(settings, "SENDINBLUE_NEWSLETTER_LIST_ID", None)
    if newsletter_list_id is not None:
        return []

    return [checks.Error("SENDINBLUE_NEWSLETTER_LIST_ID must be set on settings",
                         id="sendinblue_subscription.A002")]


def check_sendinblue_taiga_users_list_id(app_configs, **kwargs):
    from django.conf import settings

    users_list_id = getattr(settings, "SENDINBLUE_TAIGA_USERS_LIST_ID", None)
    if users_list_id is not None:
        return []

    return [checks.Error("SENDINBLUE_TAIGA_USERS_LIST_ID must be set on settings",
                         id="sendinblue_subscription.A003")]


# Signals

def connect_signals():
    from taiga.auth.signals import user_registered as user_registered_signal
    from taiga.users.signals import user_change_email as user_change_email_signal
    from taiga.users.signals import user_cancel_account as user_cancel_account_signal
    from . import signal_handlers as handlers
    user_registered_signal.connect(handlers.subscribe_user_to_sendinblue,
                                   dispatch_uid="subscribe_user_to_sendinblue")
    user_change_email_signal.connect(handlers.change_user_email_in_sendinblue,
                                     dispatch_uid="change_user_email_in_sendinblue")
    user_cancel_account_signal.connect(handlers.unsubscribe_user_from_sendinblue,
                                       dispatch_uid="unsubscribe_user_from_sendinblue")


def disconnect_signals():
    from taiga.auth.signals import user_registered as user_registered_signal
    from taiga.users.signals import user_change_email as user_change_email_signal
    from taiga.users.signals import user_cancel_account as user_cancel_account_signal
    user_registered_signal.disconnect(dispatch_uid="subscribe_user_to_sendinblue")
    user_change_email_signal.disconnect(dispatch_uid="change_user_email_in_sendinblue")
    user_cancel_account_signal.disconnect(dispatch_uid="unsubscribe_user_from_sendinblue")


class SendinblueSubscriptionAppConfig(AppConfig):
    name = "taiga_contrib_sendinblue_subscription"
    verbose_name = "Sendinblue Subscription App Config"

    def ready(self):
        from django.core.checks import register

        register(check_sendinblue_api_key)
        register(check_sendinblue_newsletter_list_id)
        register(check_sendinblue_taiga_users_list_id)

        connect_signals()
