import requests

from py_zipkin.transport import BaseTransportHandler


class HttpTransport(BaseTransportHandler):

    def get_max_payload_bytes(self):
        return None

    def send(self, encoded_span):
        # The collector expects a thrift-encoded list of spans.
        requests.post(
            'http://194.210.120.176:32256/api/v1/spans',
            data=encoded_span,
            headers={'Content-Type': 'application/x-thrift'},
        )
