import time
from uuid import uuid4

from domainpy.utils.constructable import Constructable
from domainpy.utils.immutable import Immutable
from domainpy.utils.dictable import Dictable
from domainpy.utils.traceable import Traceable


class IntegrationEvent(Constructable, Immutable, Dictable, Traceable):

    def __init__(self, *args, **kwargs):
        self.__dict__.update({
            '__trace_id__': kwargs.pop('__trace_id__', Traceable.__trace_id__),
            '__timestamp__': time.time(),
            '__message__': 'integration',
            '__error__': kwargs.pop('__error__', None)
        })
        
        super(IntegrationEvent, self).__init__(*args, **kwargs)
