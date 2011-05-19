# Copyright 2010 Mike Wakerly <opensource@hoho.com>
#
# This file is part of the Pykeg package of the Kegbot project.
# For more information on Pykeg or Kegbot, see http://kegbot.org/
#
# Pykeg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Pykeg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pykeg.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *

urlpatterns = patterns('pykeg.web.api.views',

    url(r'^auth-tokens/(?P<auth_device>[\w\.]+)\.(?P<token_value>\w+)/?$',
        'get_auth_token'),
    url(r'^cancel-drink/?$', 'cancel_drink'),
    url(r'^drinks/?$', 'all_drinks'),
    url(r'^drinks/(?P<drink_id>\d+)/?$', 'get_drink'),
    url(r'^sessions/?$', 'all_sessions'),
    url(r'^sessions/(?P<session_id>\d+)/?$', 'get_session'),
    url(r'^events/?$', 'all_events'),
    url(r'^events/html/?$', 'recent_events_html'),
    url(r'^sound-events/?$', 'all_sound_events'),
    url(r'^kegs/?$', 'all_kegs'),
    url(r'^kegs/(?P<keg_id>\d+)/?$', 'get_keg'),
    url(r'^kegs/(?P<keg_id>\d+)/drinks/?$', 'get_keg_drinks'),
    url(r'^kegs/(?P<keg_id>\d+)/events/?$', 'get_keg_events'),
    url(r'^kegs/(?P<keg_id>\d+)/sessions/?$', 'get_keg_sessions'),
    url(r'^kegs/(?P<keg_id>\d+)/stats/?$', 'get_keg_stats'),
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
    url(r'^taps/?$', 'all_taps'),
    url(r'^taps/(?P<tap_id>[\w\.]+)/?$', 'tap_detail'),
    url(r'^thermo-sensors/?$', 'all_thermo_sensors'),
    url(r'^thermo-sensors/(?P<sensor_name>[^/]+)/?$', 'get_thermo_sensor'),
    url(r'^thermo-sensors/(?P<sensor_name>[^/]+)/logs/?$', 'get_thermo_sensor_logs'),
    url(r'^users/(?P<username>\w+)/?$', 'get_user'),
    url(r'^users/(?P<username>\w+)/drinks/?$', 'get_user_drinks'),
    url(r'^users/(?P<username>\w+)/events/?$', 'get_user_events'),
    url(r'^users/(?P<username>\w+)/stats/?$', 'get_user_stats'),

    url(r'^last-drink-id/?$', 'last_drink_id'),
    url(r'^last-drinks/?$', 'last_drinks'),
    url(r'^last-drinks-html/?$', 'last_drinks_html'),

    url(r'^get-api-key/?$', 'get_api_key'),

    url(r'', 'default_handler'),

)
