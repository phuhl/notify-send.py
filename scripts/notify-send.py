#!/usr/bin/env python3

import argparse
from multiprocessing.connection import Client, Listener

import notify2
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


def clean_up_text(text):
    return text.replace("\\n", "\n").replace("\\t", "\t")


def action(n, text):
    print(text)
    global loop
    loop.quit()


def close(n):
    print('closed')
    global loop
    loop.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--urgency', metavar='LEVEL',
        help='Specifies the urgency level (low, normal, critical).')
    parser.add_argument(
        '-t', '--expire-time', metavar='TIME',
        help=('Specifies the timeout in milliseconds at which'
              ' to expire the notification.'))
    parser.add_argument(
        '-a', '--app-name', metavar='APP_NAME',
        help='Specifies the app name for the icon')
    parser.add_argument(
        '-i', '--icon', metavar='ICON[,ICON...]',
        help='Specifies an icon filename or stock icon to display.')
    parser.add_argument(
        '-c', '--category', metavar='TYPE[,TYPE...]',
        help='Specifies the notification category.')
    parser.add_argument(
        '--hint', metavar='TYPE:NAME:VALUE', nargs='*',
        help=('Specifies basic extra data to pass. Valid types'
              ' are int, double, string, boolean and byte.'))
    parser.add_argument(
        '-r', '--replaces-id', metavar='ID',
        help='Specifies the id of the notification that should be replaced.')
    parser.add_argument(
        '--replaces-process', metavar='NAME',
        help=('Specifies the name of a notification.'
              ' Every notification that gets created with the same NAME will'
              ' replace every notification before it with the same NAME.'))
    parser.add_argument(
        '--action', metavar='KEY:NAME', nargs='*',
        help=('Specifies actions for the notification. The action with the key'
              ' "default" will be dispatched on click of the notification.'
              ' Key is the return value, name is the display-name on the button.'))
    parser.add_argument(
        'SUMMARY',
        help=('Summary of the notification. Usage of \\n and \\t is possible.'))
    parser.add_argument(
        'BODY', nargs='?',
        help=('Body of the notification. Usage of \\n and \\t is possible.'))


    args = parser.parse_args()
    urgency = args.urgency
    expirey = args.expire_time
    app_name = args.app_name
    category = args.category
    hints = args.hint
    actions = args.action
    replaces_process = args.replaces_process
    replaces_id = args.replaces_id
    icon = args.icon

    summary = clean_up_text(args.SUMMARY or "")
    body = clean_up_text(args.BODY or "")

    global loop
    loop = GLib.MainLoop()

    notify2.init(app_name or "", 'glib')
    if icon and body:
        n = notify2.Notification(summary, message=body, icon=icon)
    elif icon:
        n = notify2.Notification(summary, icon=icon)
    elif body:
        n = notify2.Notification(summary, message=body)
    else:
        n = notify2.Notification(summary)

    if urgency == "low":
        n.set_urgency(notify2.URGENCY_LOW)
    elif urgency == "normal":
        n.set_urgency(notify2.URGENCY_NORMAL)
    elif urgency == "critical":
        n.set_urgency(notify2.URGENCY_CRITICAL)
    elif urgency is not None:
        print("urgency must be low|normal|critical")
        exit()

    if expirey:
        try:
            n.set_timeout(int(expirey))
        except ValueError:
            print("expire-time must be integer")
            exit()

    if category:
        n.set_category(category)

    if hints:
        for hint in hints:
            try:
                hintparts = hint.split(':')
                type = hintparts[0]
                key = hintparts[1]
                value = ':'.join(hintparts[2:])

                if type == "boolean":
                    if (value == "True") or (value == "true"):
                        n.set_hint(key, True)
                    else:
                        if (value == "False") or (value == "false"):
                            n.set_hint(key, False)
                        else:
                            print("valid types for boolean are: True|true|False|false")
                            exit()
                if type == "int":
                    n.set_hint(key, int(value))
                if type == "string":
                    n.set_hint(key, value)
                if type == "byte":
                    n.set_hint_byte(key, int(value))
            except ValueError:
                print("hint has to be in the format TYPE:KEY:VALUE")
                exit()


    if replaces_id is not None:
        try:
            n.id = int(replaces_id)
        except ValueError:
            print("replaces-id has to be an integer")
            exit()

    if actions:
        n.connect("closed", close)
        for action in actions:
            [key, value] = action.split(':')
            n.add_action(key, value, action)

    if replaces_process:
        # address = ('localhost', 6000)
        try:
            with open('/tmp/notify-send.py.address', 'r') as pidf:
                conn = Client(pidf.read())
                conn.send([n, replaces_process])
                conn.close()
        except:
            listener = Listener()
            with open('/tmp/notify-send.py.address', 'w') as pidf:
                pidf.write(listener.address)
            replaces_processes = {}
            n.show()
            replaces_processes[replaces_process] = n.id
            # stuff
            while True:
                conn = listener.accept()
                [n, replaces_process] = conn.recv()
                if replaces_process in replaces_processes:
                    n.id = replaces_processes[replaces_process]
                n.show()
                replaces_processes[replaces_process] = n.id
                conn.close()
    else:
        n.show()
        print(n.id)
        if actions:
            loop.run()


if __name__ == '__main__':
    main()
