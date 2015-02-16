import android
import time
from datetime import datetime
from urllib import request
from parsehtml import strip_tags

droid = android.Android()
methods = []

class services():
    """Available services are defined here"""
    def ts(arg):
        """Returns the current timestamp"""
        return str(int(time.time()))

    def ping(arg):
        """Tells the time at which the message was received"""
        return "Message received at " + str(datetime.now().hour) + 'h' + str(datetime.now().minute) + 'm' + str(datetime.now().second) + '.' + str(datetime.now().microsecond) + 's'

    def wifi(arg):
        """Tells if the Wifi is enabled or not"""
        return "Enabled" if droid.checkWifiState().result else "Disabled"

    def battery(arg):
        """Returns the phone's battery level"""
        droid.batteryStartMonitoring()
        time.sleep(1)
        droid.batteryStopMonitoring()
        return str(droid.batteryGetLevel().result) + " %"

    def _wiki(page):
        """Returns the first 500 characters of an english wikipedia page (not currently working)"""
        page = request.urlopen("https://en.m.wikipedia.org/wiki/" + page)
        lines = page.readlines()
        text = ''.join([i.decode("utf-8").strip() for i in lines])
        content = strip_tags(text).strip()[:300]
        print(content)
        return content

    def reverse(s):
        """Reverses the input"""
        return s[::-1]

    def hello(name):
        """Says hello to the given name"""
        return "Hello to you, " + name

    def echo(words):
        """Echoes a line of text"""
        return words

    def help(arg):
        """Displays help about this script"""
        if arg in methods:
            return eval("services." + arg + ".__doc__")
        return "*SmsBot help* Available services : " + str(methods)

# Already parsed messages
parsed_messages = []

# Available methods
methods = [method for method in dir(services) if not method.startswith('_')]

while True:
    messages = droid.smsGetMessages(True).result

    for sms in messages:
        if sms["_id"] in parsed_messages:
            # Ignore previously parsed messages
            continue

        parsed_messages.append(sms["_id"])
        txt = sms["body"].split(' ')

        command = txt[0][1:]
        if txt[0][0] == '!' and command in methods:
            args = ' '.join(txt[1:])
            out = eval("services." + command + "(" + repr(args) + ")")

            if out:
                droid.smsSend(sms["address"], out)
                droid.vibrate()

    time.sleep(1)
