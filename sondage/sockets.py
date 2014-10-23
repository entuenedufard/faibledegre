from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace

@namespace('/sondage')
class SondageNamespace(BaseNamespace, BroadcastMixin):    
    pass
    
