# -*- coding: utf-8 -*-

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace


@namespace('/sondage')
class SondageNamespace(BaseNamespace, BroadcastMixin):

    def initialize(self):
        print('coucou')

    def on_coucou(self, param, integer):
        self.emit("ouaisCoucou", "salut")
        print(u'ah tiens, j ai reçu : ' + param + " et " + str(integer))
