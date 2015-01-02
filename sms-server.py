import android
import time

droid = android.Android()

methods = []

class services():
    """Available services are defined here"""

    def reverse(s):
        """Reverses the input"""
        out = ""
        for letter in s:
            out = letter + out
        return out

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

        return "SmsBot help\n-------\nAvailable services : " + str(methods) + "\n\nSend '!service args' to run a service or '!help service' for help with a specific service"

# Already parsed messages
parsed_messages = set()

# Available methods
methods = [method for method in dir(services) if not method.startswith('_')]

while True:
    messages = droid.smsGetMessages(True).result

    for sms in messages:
        if sms["_id"] in parsed_messages:
            # Ignore previously parsed messages
            continue

        parsed_messages.add(sms["_id"])
        txt = sms["body"].split(' ')

        command = txt[0][1:]
        if txt[0][0] == '!' and command in methods:
            args = ' '.join(txt[1:])
            out = eval("services." + command + "(" + repr(args) + ")")
            droid.smsSend(sms["address"], out)
            droid.vibrate(1000)

    time.sleep(10)
