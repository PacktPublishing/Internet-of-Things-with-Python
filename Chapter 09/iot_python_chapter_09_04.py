__author__ = 'Gaston C. Hillar'


import time
from pubnub import Pubnub


class Client:
    command_key = "command"

    def __init__(self, channel):
        self.channel = channel
        # Publish key is the one that usually starts with the "pub-c-" prefix
        publish_key = "pub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        # Subscribe key is the one that usually starts with the "sub-c" prefix
        # Do not forget to replace the string with your subscribe key
        subscribe_key = "sub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        self.pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key)
        self.pubnub.subscribe(channels=self.channel,
                              callback=self.callback,
                              error=self.callback,
                              connect=self.connect,
                              reconnect=self.reconnect,
                              disconnect=self.disconnect)

    def callback_command_message(self, message):
        print("I've received the following response from PubNub cloud: {0}".format(message))

    def error_command_message(self, message):
        print("There was an error when working with the PubNub cloud: {0}".format(message))

    def publish_command(self, command_name, key, value):
        command_message = {
            self.__class__.command_key: command_name,
            key: value}
        self.pubnub.publish(
            channel=self.channel,
            message=command_message,
            callback=self.callback_command_message,
            error=self.error_command_message)

    def callback(self, message, channel):
        if channel == self.channel:
            print("I've received the following message: {0}".format(message))

    def error(self, message):
        print("Error: " + str(message))

    def connect(self, message):
        print("Connected to the {0} channel".
              format(self.channel))
        print(self.pubnub.publish(
            channel=self.channel,
            message="Listening to messages in the PubNub Python Client"))

    def reconnect(self, message):
        print("Reconnected to the {0} channel".
              format(self.channel))

    def disconnect(self, message):
        print("Disconnected from the {0} channel".
              format(self.channel))


if __name__ == "__main__":
    client = Client("temperature")
    client.publish_command(
        "print_temperature_fahrenheit",
        "temperature_fahrenheit",
        45)
    client.publish_command(
        "print_information_message",
        "text",
        "Python IoT"
    )
    # Sleep 60 seconds (60000 milliseconds)
    time.sleep(60)
