.. _changelog:

Changelog
=========

This changelog covers all Kegbot components (pykeg, kegweb, kegboard, docs).

Version 0.8.0 (2010-06-12)
--------------------------

*Note:* Due to changes in the Kegbot core, you must run the following commands
after updating::
  
  $ kegbot-admin.py migrate
  $ kegbot-admin.py kb_regen_events

Core/General
^^^^^^^^^^^^
* Support for per-tap relay control (solenoid valve control for authenticated
  users.)
* ``kegbot_core.py`` now uses the RESTful web API backend interface by default.
* Kegbot daemons now perform automatic log rotation, every night at midnight.
* When executed with ``--verbose``, daemons now show less spam.
* The drink "endtime" column has been removed (not user-visible).
* Flag names have changed; ``--api_url`` and ``--api_key`` now control the base
  API url and the API access key for any program which uses the Kegbot Web API.
* The "soundserver" application has been improved and once again works. Yay.
* Each keg record now has a "spilled" volume counter. This can be used to store
  the total amount of wasted or lost beverage which is not associated with a
  drink record.
* When running ``kegbot-admin``, ``PYTHONPATH`` now has higher precedence than
  ``/etc/kegbot`` and ``~/.kegbot``. This makes it possible to provide an
  alternate location for ``common_settings.py``. (If the preceding was nonsense
  to you, you are normal..)
* Django 1.3 is now supported.

Kegweb
^^^^^^
* The account page for a logged-in admin now displays the API key for that user.
* Various CSS changes and aesthetic tweaks.
* System events are shown on the Kegweb main page.
* Automatic AJAX refresh of drinks (and now events) on the main page has been
  improved.
* Session detail pages show individual pours from that session.
* Session detail pages show the total number of authenticated drinkers.
  (Guest/anonymous pours do not contribute to this count.)
* Fixed a bug where previous keg was not being marked offline after a keg
  change.
* The values in the pints-per-session histogram are now less ambiguous.
* The background image is now included in version control, and could be replaced
  locally.
* Beer type images rendering has been cleaned up.

API
^^^
* API keys are now calculated differently.  As a result, previously-used
  API keys are invalid.  To determine your API key, visit ``/account/`` while
  logged in as an admin user.
* System events are now exposed in the web api.
* Sessions are now exposed in the web api.
* Date/time fields reported in the web api are now always expressed in UTC,
  regardless of the system/Django time zone.

Version 0.7.8 (2010-12-01)
--------------------------
*Note:* Due to changes in the Kegbot core, you must run the following commands
after updating::
  
  $ kegbot-admin.py migrate
  $ kegbot-admin.py kb_regen_stats

*Note:* If you have installed using ``./setup.py develop``, you will need to
issue that command again; new versions of some dependencies are required.

Core/General
^^^^^^^^^^^^
* Added SystemStats table.
* Now requires the ``pytz`` module; use ``pip install pytz`` to install.
* System, keg, session, and drinker statistics are now recalculated quickly
  after every pour.

Kegweb
^^^^^^
* Added slightly more info to the "all-time stats" page.
* Used cached stats on the "all-time stats" page, making it more responsive.
* Fixed the AJAX auto-update of the drink list on the homepage.
* Fixed a crash in the LCD daemon, encountered when an active tap did not have a
  temperature sensor assigned to it.
* Fixed a crash on the keg admin page.
* Fixed a regression introduced in v0.7.6 that caused kegweb to crash when a
  chart could not be displayed; the chart is once again replaced with a
  descriptive error message.
* Fixed "known drinkers" statistic on the keg detail page.
* Set time zone UTC offset in ISO8601-formatted timestamps.  This fixes an issue
  where drinks appear to be poured in the future when the local timezone is
  behind the server timezone.

Version 0.7.7 (2010-11-28)
--------------------------
*Note:* This is a quick patch release to v0.7.6.  See changelog for v0.7.6 for
major changes.

Core/General
^^^^^^^^^^^^
* Fixes a bug discovered with stats generation in v0.7.6.


Version 0.7.6 (2010-11-28)
--------------------------

*Note:* An update to the kegboard firmware is included in this version.
Reflashing your kegboard is recommended.

*Note:* It is recommended that you rebuild all session and statistical data
after updating to this version::
  
  $ kegbot-admin.py kb_regen_sessions
  $ kegbot-admin.py kb_regen_stats
  $ kegbot-admin.py kb_regen_events

Core/General
^^^^^^^^^^^^
* Improved token handling, resolving multiple bugs related to token timeouts and
  multi-tap authentication.
* Added SessionStats table.  Statistics are now continuously computed for
  drinking sessions, to go along with per-user and per-keg stats.
* Removed protobuf dependency.
* rfid_daemon: added ``--toggle_output`` option, to enable the external output
  whenever an ID is present.
* LCD daemon improvements.

Kegweb
^^^^^^
* Sessions can now be assigned a title, and have descriptive permalinks.
* Sessions are now prominently featured on Kegweb pages.  Various improvements
  to session display.
* Replaced Google image charts with javascript/SVG `Highcharts
  <http://highcharts.com>`_ package.
* Various bugfixes to the web API.
* Added an example WSGI configuration file.

Kegboard
^^^^^^^^
* Improved stability in kegboard_daemon when malformed or unknown messages are
  received.
* Added the :ref:`auth-token-message` type to the serial protocol.
* Fixed reporting for negative temperatures.
* Fixed kegboard reader/daemon to not crash when ``EAGAIN`` is received from the
  OS.
* Update Makefiles.

Version 0.7.5 (2010-09-11)
--------------------------

*Note:* Due to changes to the third-party ``socialregistration`` dependency,
existing users will need to issue the following command after updating::
  
  $ kegbot-admin.py migrate --fake socialregistration 0001
  $ kegbot-admin.py migrate

*Note:* If you have installed using ``./setup.py develop``, you will need to
issue that command again; new versions of some dependencies are required.

Core / General
^^^^^^^^^^^^^^
* Fixed a race condition which could cause the kegbot core to crash due to an
  erroneous watchdog error.
* Fixed a crash in ``kegbot_admin.py kb_regen_stats`` that would occur when
  computing stats for a keg with no recorded drinks.  (The workaround was to go
  have a beer..)
* Fixed issue #50 (do not record drinks below minimum volume threshold.)

Kegweb
^^^^^^
* Updated to use ``django-socialregistration`` version 0.4.2, and the official
  ``facebook-python-sdk`` package.  Removed mirror of pyfacebook.
* The number of recent pours shown on the main page is now configurable.  See
  ``KEGWEB_LAST_DRINK_COUNT`` in ``common_settings.py.example``


Version 0.7.4 (2010-09-08)
--------------------------

Core / General
^^^^^^^^^^^^^^
* Backend: extensive under-the-hood changes to support multiple sites in a
  single backend instance.  This isn't yet used by anything.
* Fixed issue with pykeg.core migration 0031.
* Improvements to session record keeping.
* Added new SystemEvent table.

Kegweb
^^^^^^
* Improved keg detail page, with better-looking sessions.


Version 0.7.3 (2010-09-01)
--------------------------

*Note:* Existing users upgrading from a previous kegbot version will need to
issue the migrate command to update their database schema.  Also, statistics and
sessions need to be regenerated::
  
  $ kegbot_admin.py migrate
  $ kegbot_admin.py kb_regen_sessions
  $ kegbot_admin.py kb_regen_stats

Core / General
^^^^^^^^^^^^^^
* Fixed issue authentication tokens for consecutive pours not being reported
  correctly.
* Improved stats reporting; fixed drinker breakdown graph on keg detail page.
* Added a notes field for Keg records.
* Internal cleanups to the backend APIs.
* Schema change: Started record auth token details used for each pour.
* Schema change: Guest pours are now represented by a ``null`` user (rather than
  a specific guest account) in the database.

Kegweb
^^^^^^
* Fixed issue causing kegweb to break when used without proper Facebook
  credentials.
* Improvements to the currently undocumented kegweb API.

Kegboard
^^^^^^^^
* Update KegShield schematics to include Arduino and Arduino Mega shield
  designs.

Version 0.7.2 (2010-06-29)
--------------------------

Core / General
^^^^^^^^^^^^^^
* Django v1.2 is now **required**.
* Added new dependency on ``django_nose`` for running unittests; ``make test``
  works once again to run unittests
* Improved LCD UI; now shows tap status, last pour information.
* Fixed SoundServer, which had stopped working some time ago.
* Miscellaneous packaging fixes, which should make installation with ``pip`` work
  a bit better.

Kegweb
^^^^^^
* Fix for bug #48: Facebook connect login broken.
* Fixed/update CSRF detection on forms for Django 1.2.
* Bugfixes for the Kegweb REST ('krest') API.

Twitter
^^^^^^^
* Moved Twitter add-on out of the core and into a new daemon,
  ``kegbot_twitter``, similar to Facebook app ``fb_publisher``.


Version 0.7.1 (2010-06-04)
--------------------------

Core / General
^^^^^^^^^^^^^^
* Added missing dependencies to `setup.py`.
* Removed a few locally-mirrored dependencies.
* Added protobuf source mirror to `setup.py`.

Kegweb
^^^^^^
* Reorganized account settings views.
* Add password reset forms.

Version 0.7.0 (2010-05-23)
--------------------------

Initial numbered release! (Changes are since hg revision 500:525e06329039).

Core / General
^^^^^^^^^^^^^^
* Vastly improved authentication device support.
* New network protocol for Kegbot status and control (kegnet).
* Temperatures are once again recorded. Temperature sensors can be associated
  with a specific keg tap.
* Support for Phidgets RFID reader.
* Flowmeter resolution is now set on a tap-by-tap basis (in KegTap table).
* Twitter: added config option to suppress tweets for unknown users.
* Started using django-south for schema migrations.
* Sound playback on flow events: added the sound_server application.
* Added kegbot_master program, to control and monitor full suite of kegbot
  daemons.
* Improved support for CrystalFontz LCD devices; new support for Matrix-Orbital
  serial LCD displays.
* Added Facebook publisher add-on.
* Packaging improvements; `setup.py install` works.

Kegboard
^^^^^^^^
* Bumped firmware version to v5.
* Fixed packet CRCs.
* Added support for OneWire presence detect/authentication device.
* Improved DS1820 temperature sensing.
* Improved responsiveness of OneWire presence detect.
* Shrunk size of firmware significantly.
* Added experimental support for serial LCDs.
* Added schematic files for Kegboard Arduino shield.

Kegweb
^^^^^^
* Design refresh; new HTML/CSS and many more graphs and stats.
* Added keg administration tab.
* Added experimental support for Facebook connect.
* Fixed broken relative time display.
* Fixed bug on submitting new user registration.

Docs
^^^^
* Improved documentation.
* Added changelog :)

