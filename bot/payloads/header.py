import sys
from uuid import uuid4
from . import BasePayload


class Header(BasePayload):
    def __init__(self, payload_type, payload, uuid=None, *args, **kwargs):
        super(Header, self).__init__(*args, **kwargs)
        self.payload_type = payload_type
        self.payload = payload
        if uuid is None:
            self.uuid = uuid4()
        else:
            self.uuid = uuid

    @classmethod
    def de_json(cls, data):
        if data is None:
            return

        payload_class = getattr(sys.modules['bot'], data['payload_type'])
        data['payload'] = payload_class.de_json(data['payload'])

        return cls(**data)
