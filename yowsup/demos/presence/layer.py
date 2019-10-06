from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers import EventCallback
from yowsup.common.tools import Jid
from yowsup.layers.protocol_presence.protocolentities import *
from yowsup.layers.protocol_presence import YowPresenceProtocolLayer
# from yowsup import logger
from threading import Thread

import time
import logging
from datetime import date

logger = logging.getLogger(__name__)

# create console handler and set level to debug
filename = "{}.log".format(date.today().strftime("%Y%m%d"))
ch = logging.FileHandler(filename)
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(levelname).1s %(asctime)s %(name)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.setLevel(logging.INFO)

class PresenseLayer(YowInterfaceLayer):

    profile_number_map = {
        '91123456788': 'K',
        }

    # @ProtocolEntityCallback("message")
    # def onMessage(self, messageProtocolEntity):

    #     if messageProtocolEntity.getType() == 'text':
    #         self.onTextMessage(messageProtocolEntity)
    #     elif messageProtocolEntity.getType() == 'media':
    #         self.onMediaMessage(messageProtocolEntity)

    #     self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
    #     self.toLower(messageProtocolEntity.ack())
    #     self.toLower(messageProtocolEntity.ack(True))


    # @ProtocolEntityCallback("receipt")
    # def onReceipt(self, entity):
    #     self.toLower(entity.ack())

    # def onTextMessage(self,messageProtocolEntity):
    #     # just print info
    #     print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    # def onMediaMessage(self, messageProtocolEntity):
    #     # just print info
    #     if messageProtocolEntity.media_type == "image":
    #         print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

    #     elif messageProtocolEntity.media_type == "location":
    #         print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

    #     elif messageProtocolEntity.media_type == "contact":
    #         print("Echoing contact (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def on_connected(self, event):
        logger.info("Connected, starting Presense Change")
        # entity = SubscribePresenceProtocolEntity(self.aliasToJid('919842098371'))
        # self.toLower(entity)
    
    @ProtocolEntityCallback("presence")
    def onPresenceChange(self, entity):
        status="offline"
        if entity.getType() is None:
            status="online" 
        lastseen = time.time()
        ##
        profile_name = self.profile_number_map.get(entity.getFrom().replace('@s.whatsapp.net', ''))
        logger.info("|%s-%s: %s|" % (profile_name, status, lastseen))

    def aliasToJid(self, calias):
        return Jid.normalize(calias)

    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        logger.info("Success, starting Presense Change")
        entity = AvailablePresenceProtocolEntity()
        self.toLower(entity)
        for contact in self.profile_number_map.keys():
            entity = SubscribePresenceProtocolEntity(self.aliasToJid(contact))
            self.toLower(entity)
        # presence_thread = YowPresenceThread(self, 5)
        # presence_thread.start()
