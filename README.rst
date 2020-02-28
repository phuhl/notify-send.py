==============
notify-send.py
==============

A python script for sending desktop notifications from the shell.

About
=====

Libnotify is part of many scripts in the Linux world. It utilizes many
of the specified features of the Desktop Notifications Specification
and makes them accessible to shell-scripts. It does **not** however
allow to replace an existing notification with the ``replaces-id``. This
is a known bug_ since 2008 and has a patch_ since 2012. The patch is still not
upstream though (2018).

.. _bug: https://bugs.launchpad.net/ubuntu/+source/libnotify/+bug/257135

.. _patch: https://bugs.launchpad.net/ubuntu/+source/libnotify/+bug/257135/comments/10

This python script utilizes the ``notify2`` package and exposes the
functionality to the shell.

Differences between notify-send.py and notify-send
==================================================

-  In ``notify-send.py -h`` shows help instead of being the parameter for
   hints. For hints use ``--hint``.
-  In ``notify-send.py -r ID`` and ``notify-send.py --replaces-id ID``
   exists. In order to replace a notification call ``notify-send.py``
   with the ID that was returned by the notification to be replaced.
-  ``notify-send.py`` returns the ID of the newly created notification.
-  ``notify-send.py --replaces-process NAME`` exists.
   Every notification that gets created with the same NAME will replace
   every notification before it with the same NAME. If called with this
   parameter ``notify-send.py`` might block, best to be called with a
   trailing ``&``.
-  ``notify-send.py -h`` has action-support (buttons). Try
   ``notify-send.py "Yes or no?" --action ok:OK cancel:Cancel``

Installation
============

Requires python 3.

From PyPI:

.. code:: bash

   pip install notify-send.py

From repo:

.. code:: bash

   git clone https://github.com/phuhl/notify-send.py
   cd notify-send.py
   pip install .

Usage
=====

.. code:: console

   $ notify-send.py -h

::

   usage: notify-send.py [-h] [-u LEVEL] [-t TIME] [-a APP_NAME]
                         [-i ICON[,ICON...]] [-c TYPE[,TYPE...]]
                         [--hint [TYPE:NAME:VALUE [TYPE:NAME:VALUE ...]]]
                         [-r ID] [--replaces-process NAME]
                         [--action [KEY:NAME [KEY:NAME ...]]]
                         SUMMARY [BODY]

   positional arguments:
     SUMMARY               Summary of the notification. Usage of \n and \t
                           is possible.
     BODY                  Body of the notification. Usage of \n and \t is
                           possible.

   optional arguments:
     -h, --help            show this help message and exit
     -u LEVEL, --urgency LEVEL
                           Specifies the urgency level (low, normal,
                           critical).
     -t TIME, --expire-time TIME
                           Specifies the timeout in milliseconds at which
                           to expire the notification.
     -a APP_NAME, --app-name APP_NAME
                           Specifies the app name for the icon
     -i ICON[,ICON...], --icon ICON[,ICON...]
                           Specifies an icon filename or stock icon to
                           display.
     -c TYPE[,TYPE...], --category TYPE[,TYPE...]
                           Specifies the notification category.
     --hint [TYPE:NAME:VALUE [TYPE:NAME:VALUE ...]]
                           Specifies basic extra data to pass. Valid types
                           are int, double, string, boolean and byte.
     -r ID, --replaces-id ID
                           Specifies the id of the notification that should
                           be replaced.
     --replaces-process NAME
                           Specifies the name of a notification. Every
                           notification that gets created with the same
                           NAME will replace every notification before it
                           with the same NAME.
     --action [KEY:NAME [KEY:NAME ...]]
                           Specifies actions for the notification. The
                           action with the key "default" will be dispatched
                           on click of the notification. Key is the return
                           value, name is the display-name on the button.

notify-send[.py] as root user
=============================

In order to display notifications, even if libnotify or
``notify-send.py`` is used from the root user this script is helpful.
You need to customize it with your username and userid (which probably is
1000 but can be found out by running ``cat /etc/passwd | grep <username>``).

``notify-send-from-root.sh``:

.. code:: bash

   #!/bin/bash
   USERNAME=<your username here>
   USERID=1000

   export XAUTHORITY=/home/$USERNAME/.Xauthority
   export DISPLAY=:0
   export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$USERID/bus

   if [ "$(/usr/bin/id -u)" != "$USERID" ] ; then
       sudo -u $USERNAME XAUTHORITY=/home/$USERNAME/.Xauthority DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$USERID/bus /usr/bin/notify-send.py "$@"
   else
       /usr/bin/notify-send.py "$@"
   fi

Examples (Volume and Brightness pop-ups)
========================================

-  Volume control-pop-ups:
   https://github.com/phuhl/linux_notification_center#example-volume-indicator
-  Brightness control-pop-ups:
   https://github.com/phuhl/linux_notification_center#example-brightness-indicator

See also
========

Also take a look at my notification-daemon_ inspired by Dunst_, but with several improvements, including the possibility of a transparent background and a notification center that stores notifications.

.. _notification-daemon: https://github.com/phuhl/linux_notification_center

.. _Dunst: https://wiki.archlinux.org/index.php/Dunst
