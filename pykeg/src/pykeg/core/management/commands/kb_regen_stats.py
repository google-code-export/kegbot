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

from django.core.management.base import CommandError
from django.core.management.base import NoArgsCommand

from pykeg.core import models
from pykeg.core.management.commands.common import progbar


class Command(NoArgsCommand):
  help = u'Regenerate all cached stats.'
  args = '<none>'

  def handle(self, **options):
    drinks = models.Drink.objects.all()

    models.KegStats.objects.all().delete()
    kegs = models.Keg.objects.all()
    count = kegs.count()
    pos = 0
    for k in kegs:
      pos += 1
      progbar('recalc keg stats', pos, count)
      last_drinks = k.drinks.valid().order_by('-endtime')
      if last_drinks:
        last_drinks[0]._UpdateKegStats()
    print ''

    models.UserStats.objects.all().delete()
    users = models.User.objects.all()
    count = users.count()
    pos = 0
    for user in users:
      pos += 1
      progbar('recalc user stats', pos, count)
      user_drinks = user.drinks.valid().order_by('-endtime')
      if user_drinks:
        last = user_drinks[0]
        last._UpdateUserStats()
    print ''

    models.SessionStats.objects.all().delete()
    sessions = models.DrinkingSession.objects.all()
    count = sessions.count()
    pos = 0
    for session in sessions:
      pos += 1
      progbar('recalc session stats', pos, count)
      session_drinks = session.drinks.valid().order_by('-endtime')
      if session_drinks:
        last = session_drinks[0]
        last._UpdateSessionStats()
    print ''

    print 'done!'
