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

"""Routines from converting data to and from Protocol Buffer format."""

import sys
import time

from pykeg.beerdb import models as bdb_models
from pykeg.core import models
from pykeg.core.util import AttrDict
from pykeg.contrib.soundserver import models as soundserver_models

_CONVERSION_MAP = {}

def converts(kind):
  def decorate(f):
    global _CONVERSION_MAP
    _CONVERSION_MAP[kind] = f
    return f
  return decorate

def ToProto(obj, full=False):
  """Converts the object to protocol format."""
  if obj is None:
    return None
  kind = obj.__class__
  if hasattr(obj, '__iter__'):
    return (ToProto(item, full) for item in obj)
  elif kind in _CONVERSION_MAP:
    return _CONVERSION_MAP[kind](obj, full)
  else:
    raise ValueError, "Unknown object type: %s" % kind

### Model conversions

@converts(models.AuthenticationToken)
def AuthTokenToProto(record, full=False):
  ret = AttrDict()
  ret.id = str(record.seqn)
  ret.auth_device = record.auth_device
  ret.token_value = record.token_value
  if record.user:
    ret.username = str(record.user.username)
  else:
    ret.username = None
  ret.nice_name = record.nice_name
  if full:
    ret.enabled = record.enabled
    ret.created_time = record.created
    ret.expire_time = record.expires
    if record.pin:
      ret.pin = record.pin
  return ret

@converts(bdb_models.BeerStyle)
def BeerStyleToProto(style, full=False):
  ret = AttrDict()
  ret.id = str(style.id)
  ret.name = style.name
  return ret

@converts(bdb_models.BeerType)
def BeerTypeToProto(beertype, full=False):
  ret = AttrDict()
  ret.id = str(beertype.id)
  ret.name = beertype.name
  ret.brewer_id = str(beertype.brewer.id)
  ret.style_id = str(beertype.style.id)
  ret.edition = beertype.edition
  # TODO(mikey): guarantee this at DB level
  abv = beertype.abv or 0.0
  ret.abv = max(min(abv * 100.0, 100.0), 0.0)
  ret.calories_oz = beertype.calories_oz
  ret.carbs_oz = beertype.carbs_oz
  ret.specific_gravity = beertype.specific_gravity
  ret.original_gravity = beertype.original_gravity
  return ret

@converts(bdb_models.Brewer)
def BrewerToProto(brewer, full=False):
  ret = AttrDict()
  ret.id = str(brewer.id)
  ret.name = brewer.name
  ret.country = brewer.country or ''
  ret.origin_state = brewer.origin_state or ''
  ret.origin_city = brewer.origin_city or ''
  ret.production = brewer.production or ''
  ret.url = brewer.url or ''
  ret.description = brewer.description or ''
  return ret

@converts(models.Drink)
def DrinkToProto(drink, full=False):
  ret = AttrDict()
  ret.id = str(drink.seqn)
  ret.ticks = drink.ticks
  ret.volume_ml = drink.volume_ml
  ret.session_id = str(drink.session.seqn)
  ret.pour_time = drink.starttime
  ret.duration = drink.duration
  ret.status = drink.status
  # TODO(mikey): still needed?
  ret.keg_id = str(drink.keg.seqn)
  ret.user_id = None
  ret.auth_token_id = None
  if drink.user:
    ret.user_id = drink.user.username
  if drink.auth_token:
    ret.auth_token_id = str(drink.auth_token.id)
  return ret

@converts(models.Keg)
def KegToProto(keg, full=False):
  ret = AttrDict()
  ret.id = str(keg.seqn)
  ret.type_id = str(keg.type.id)
  ret.size_id = str(keg.size.id)
  ret.size_name = keg.size.name
  ret.size_volume_ml = keg.size.volume_ml
  rem = float(keg.remaining_volume())
  ret.volume_ml_remain = rem
  ret.percent_full = keg.percent_full()
  ret.started_time = keg.startdate
  ret.finished_time = keg.enddate
  ret.status = keg.status
  ret.description = keg.description
  ret.spilled_ml = keg.spilled_ml
  return ret

@converts(models.KegSize)
def KegSizeToProto(size, full=False):
  ret = AttrDict()
  ret.id = str(size.id)
  ret.name = size.name
  ret.volume_ml = size.volume_ml
  return ret

@converts(models.KegTap)
def KegTapToProto(tap, full=False):
  ret = AttrDict()
  ret.id = str(tap.seqn)
  ret.name = tap.name
  ret.meter_name = tap.meter_name
  ret.ml_per_tick = tap.ml_per_tick
  ret.description = tap.description
  ret.current_keg_id = None
  ret.thermo_sensor_id = None
  ret.last_temperature = None
  if tap.current_keg:
    ret.current_keg_id = str(tap.current_keg.seqn)
  if tap.temperature_sensor:
    ret.thermo_sensor_id = str(tap.temperature_sensor.seqn)
    log = tap.temperature_sensor.LastLog()
    if log:
      ret.last_temperature = ToProto(log)
  return ret

@converts(models.DrinkingSession)
def SessionToProto(record, full=False):
  ret = AttrDict()
  ret.id = str(record.seqn)
  ret.start_time = record.starttime
  ret.end_time = record.endtime
  ret.volume_ml = record.volume_ml
  ret.name = record.name or ''
  ret.slug = record.slug or ''
  return ret

@converts(models.Thermolog)
def ThermoLogToProto(record, full=False):
  ret = AttrDict()
  ret.id = str(record.seqn)
  ret.sensor_id = str(record.sensor.seqn)
  ret.temperature_c = record.temp
  ret.record_time = record.time
  return ret

@converts(models.ThermoSensor)
def ThermoSensorToProto(record, full=False):
  ret = AttrDict()
  ret.id = str(record.seqn)
  ret.sensor_name = record.raw_name
  ret.nice_name = record.nice_name
  return ret

@converts(models.ThermoSummaryLog)
def ThermoSummaryLogToProto(record, full=False):
  ret = AttrDict()
  ret.id = str(record.seqn)
  ret.sensor_id = str(record.sensor.seqn)
  ret.date = record.date
  ret.period = record.period
  ret.num_readings = record.num_readings
  ret.min_temp = record.min_temp
  ret.max_temp = record.max_temp
  ret.mean_temp = record.mean_temp
  return ret

@converts(models.User)
def UserToProto(user, full=False):
  ret = AttrDict()
  ret.username = user.username
  ret.mugshot_url = user.get_profile().MugshotUrl()
  ret.is_active = user.is_active
  if full:
    ret.first_name = user.first_name
    ret.last_name = user.last_name
    ret.email = user.email
    ret.password = user.password
    ret.is_staff = user.is_staff
    ret.is_active = user.is_active
    ret.is_superuser = user.is_superuser
    ret.last_login = user.last_login
    ret.date_joined = user.date_joined
  return ret

@converts(models.UserProfile)
def UserProfileToProto(record, full=False):
  ret = AttrDict()
  ret.username = record.user.username
  ret.gender = record.gender
  ret.weight = record.weight
  return ret

@converts(models.SessionChunk)
def SessionChunkToProto(record, full=False):
  ret = AttrDict()
  ret.id = str(record.seqn)
  ret.session_id = str(record.session.seqn)
  ret.username = record.user.username
  ret.keg_id = str(record.keg.seqn)
  ret.start_time = record.starttime
  ret.end_time = record.endtime
  ret.volume_ml = record.volume_ml
  return ret

@converts(models.SystemEvent)
def SystemEventToProto(record, full=False):
  ret = AttrDict()
  ret.id = str(record.seqn)
  ret.kind = record.kind
  ret.time = record.when
  ret.drink_id = None
  ret.keg_id = None
  ret.session_id = None
  ret.user_id = None

  if record.drink:
    ret.drink_id = str(record.drink.seqn)
  if record.keg:
    ret.keg_id = str(record.keg.seqn)
  if record.session:
    ret.session_id = str(record.session.seqn)
  if record.user:
    ret.user_id = str(record.user.username)

  return ret

@converts(soundserver_models.SoundEvent)
def SoundEventToProto(record, full=False):
  ret = AttrDict()
  ret.event_name = record.event_name
  ret.event_predicate = record.event_predicate
  ret.sound_url = record.soundfile.sound.url
  ret.user = record.user
  return ret
