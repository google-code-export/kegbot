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

"""Methods to generate cached statistics from drinks."""

import inspect
import itertools

def stat(name, default=None):
  def decorate(f):
    setattr(f, 'statname', name)
    setattr(f, 'statdefault', default)
    return f
  return decorate

class StatsBuilder(object):

  def __init__(self, prev_stats=None):
    if prev_stats is None:
      prev_stats = {}
    self._prev_stats = prev_stats

  def AllStats(self):
    for name, method in inspect.getmembers(self, inspect.ismethod):
      if hasattr(method, 'statname'):
        yield (method.statname, method.statdefault, method)

  def Build(self, obj, prev_stats=None, prev_objs=None):
    new_stats = {}
    if prev_stats is None:
      if prev_objs is None:
        prev_objs = self._PrevObjs(obj).order_by('starttime')
      if prev_objs:
        for i in xrange(len(prev_objs)):
          prev_stats = self.Build(prev_objs[i], prev_stats, prev_objs[:i])
      else:
        prev_stats = {}
    for statname, statdefault, fn in self.AllStats():
      prev_val = prev_stats.get(statname, statdefault)
      res = fn(obj, prev_val)
      if res is not None:
        new_stats[statname] = res
    return new_stats


class BaseStatsBuilder(StatsBuilder):
  """Builder which generates a variety of stats from object information."""

  def _PrevObjs(self, obj):
    raise NotImplementedError

  @stat('total-volume', default=0)
  def TotalVolume(self, obj, prev):
    """Updates the total volume."""
    return prev + float(obj.Volume())

  @stat('total-count', default=0)
  def TotalPours(self, obj, prev):
    return prev + 1

  @stat('volume-avg', default=(0, 0))
  def AverageVolume(self, obj, prev):
    prev_count, prev_avg = prev
    curr_vol = float(obj.Volume())
    curr_count = prev_count + 1.0
    curr_avg = ((prev_avg * prev_count) + curr_vol) / curr_count
    return (curr_count, curr_avg)

  @stat('volume-max')
  def LargestVolume(self, obj, prev):
    vol = float(obj.Volume())
    if prev:
      prev_vol, prev_id = prev
      if prev_vol >= vol:
        return prev
    return vol, obj.id

  @stat('volume-min')
  def SmallestPour(self, obj, prev):
    vol = float(obj.Volume())
    if prev:
      prev_vol, prev_id = prev
      if prev_vol <= vol:
        return prev
    return vol, obj.id

  @stat('date-first')
  def FirstDate(self, obj, prev):
    if prev:
      d_date, d_id = prev
      if d_date <= obj.starttime:
        return prev
    return obj.starttime, obj.id

  @stat('date-last')
  def LastDate(self, obj, prev):
    if prev:
      d_date, d_id = prev
      if d_date >= obj.starttime:
        return prev
    return obj.starttime, obj.id

  @stat('volume-by-day-of-week')
  def VolumeByDayOfweek(self, obj, prev):
    volmap = prev
    if not volmap:
      volmap = dict((i, 0) for i in xrange(7))
    weekday = obj.starttime.weekday()
    volmap[weekday] += float(obj.Volume())
    return volmap

  @stat('ids')
  def Ids(self, obj, prev):
    if prev is None:
      prev = []
    obj_id = obj.id
    if obj_id not in prev:
      prev.append(obj_id)
    return prev


class DrinkerStatsBuilder(BaseStatsBuilder):
  """Builder of user-specific stats by drink."""
  REVISION = 1

  def _PrevObjs(self, drink):
    qs = drink.user.drink_set.filter(starttime__lt=drink.starttime)
    qs = qs.order_by('starttime')
    return qs

  #@stat('volume-per-user-session')
  def VolumePerSession(self, drink, prev):
    if not prev:
      prev = []
    sess = drink.GetSession()
    user_sess = drink.user.session_parts.filter(session=sess)[0]
    res = [itertools.ifilter(lambda x: x[0] != user_sess.id, prev)]
    res.append((user_sess.id, float(user_sess.Volume())))


class KegStatsBuilder(BaseStatsBuilder):
  """Builder of keg-specific stats."""
  REVISION = 1

  def _PrevObjs(self, drink):
    qs = drink.keg.drink_set.filter(starttime__lt=drink.starttime)
    qs = qs.order_by('starttime')
    return qs


def main():
  from pykeg.core import models

  for user in models.User.objects.all():
    last_drink = user.drink_set.all().order_by('-starttime')
    if not last_drink:
      continue
    last_drink = last_drink[0]
    builder = DrinkerStatsBuilder()
    stats = builder.Build(last_drink)
    print '-'*72
    print 'stats for %s' % user
    for k, v in stats.iteritems():
      print '   %s: %s' % (k, v)
    print ''

if __name__ == '__main__':
  import cProfile
  command = """main()"""
  cProfile.runctx( command, globals(), locals(), filename="stats.profile" )

