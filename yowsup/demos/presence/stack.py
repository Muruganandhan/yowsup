from yowsup.stacks import  YowStackBuilder
from .layer import PresenseLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST

import sys
import time
class YowsupPresenseStack(object):
    def __init__(self, profile):
        """
        :param profile:
        :param messages: list of (jid, message) tuples
        :return:
        """
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(PresenseLayer)\
            .build()

        # self._stack.setProp(SendLayer.PROP_MESSAGES, messages)
        # self._stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self._stack.setProfile(profile)
        self._stack.setProp(PROP_IDENTITY_AUTOTRUST, True)
        print("Hey I am Here (^ _ ^) ^^")

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    def start(self):
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self._stack.loop()
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)
