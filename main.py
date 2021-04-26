import random
import time

from prometheus_client import start_http_server, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
from prometheus_client.core import REGISTRY, CounterMetricFamily

# unregister not used metrics
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])


class CollectSendBytesTotal(object):
    def collect(self):
        c = CounterMetricFamily('wireguard_sent_bytes_total', 'Bytes sent to the peer',
                                labels=['interface', 'public_key', 'allowed_ips'])
        for i in range(5):
            c.add_metric(['wg0', str(i), '192.168.0.100/32'], random.random())
        yield c


class CollectRecvBytesTotal(object):
    def collect(self):
        c = CounterMetricFamily('wireguard_received_bytes_total', 'Bytes received from the peer',
                                labels=['interface', 'public_key', 'allowed_ips'])
        for i in range(5):
            c.add_metric(['wg0', str(i), '192.168.0.100/32'], random.random())
        yield c


class CollectLatestHandshakeSeconds(object):
    def collect(self):
        c = CounterMetricFamily('wireguard_latest_handshake_seconds', 'Seconds from the last handshake',
                                labels=['interface', 'public_key', 'allowed_ips'])
        for i in range(5):
            c.add_metric(['wg0', str(i), '192.168.0.100/32'], random.random())
        yield c


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CollectSendBytesTotal())
    REGISTRY.register(CollectRecvBytesTotal())
    REGISTRY.register(CollectLatestHandshakeSeconds())
    while True:
        time.sleep(1)

# HELP wireguard_sent_bytes_total Bytes sent to the peer
# TYPE wireguard_sent_bytes_total counter
# wireguard_sent_bytes_total{interface="wg0",public_key="60PT8CLCbVWl4Aff/7gND5Z42z/1uddLdpYOQb1ArCw=",allowed_ips="192.168.0.100/32"} 12216644

# HELP wireguard_received_bytes_total Bytes received from the peer
# TYPE wireguard_received_bytes_total counter
# wireguard_received_bytes_total{interface="wg0",public_key="60PT8CLCbVWl4Aff/7gND5Z42z/1uddLdpYOQb1ArCw=",allowed_ips="192.168.0.100/32"} 1585564

# HELP wireguard_latest_handshake_seconds Seconds from the last handshake
# TYPE wireguard_latest_handshake_seconds gauge
# wireguard_latest_handshake_seconds{interface="wg0",public_key="60PT8CLCbVWl4Aff/7gND5Z42z/1uddLdpYOQb1ArCw=",allowed_ips="192.168.0.100/32"} 1618763104
