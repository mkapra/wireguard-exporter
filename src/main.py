"""
Imports

:random: For sample data output
:time: control sleep time in main function
"""
import random
import time

from prometheus_client import start_http_server, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
from prometheus_client.core import REGISTRY, CounterMetricFamily

import lib.wg_parser as wg_parser

# unregister not used metrics
# pylint: disable=protected-access
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(
    REGISTRY._names_to_collectors['python_gc_objects_collected_total'])


# pylint: disable=too-few-public-methods
class CollectSendBytesTotal:
    """
    Custom collector class for bytes sent to wireguard peer
    """
    @staticmethod
    def collect():
        """
        collects metrics

        :return: one metric collection per public_key
        """
        metric_collection = CounterMetricFamily('wireguard_sent_bytes_total',
                                                'Bytes sent to the peer',
                                                labels=['interface', 'public_key', 'allowed_ips'])
        for i in range(5):
            metric_collection.add_metric(
                ['wg0', str(i), '192.168.0.100/32'], random.random())
        yield metric_collection


# pylint: disable=too-few-public-methods
class CollectRecvBytesTotal:
    """
    Custom collector class for bytes received from wireguard peer
    """
    @staticmethod
    def collect():
        """
        collects metrics

        :return: one metric collection per public_key
        """
        metric_collection = CounterMetricFamily('wireguard_received_bytes_total',
                                                'Bytes received from the peer',
                                                labels=['interface', 'public_key', 'allowed_ips'])
        for i in range(5):
            metric_collection.add_metric(
                ['wg0', str(i), '192.168.0.100/32'], random.random())
        yield metric_collection


# pylint: disable=too-few-public-methods
class CollectLatestHandshakeSeconds:
    """
    Custom collector class for how many seconds ago the last wireguard handshake occured
    """
    @staticmethod
    def collect():
        """
        collects metrics

        :return: one metric collection per public_key
        """
        metric_collection = CounterMetricFamily('wireguard_latest_handshake_seconds',
                                                'Seconds from the last handshake',
                                                labels=['interface', 'public_key', 'allowed_ips'])
        for i in range(5):
            metric_collection.add_metric(
                ['wg0', str(i), '192.168.0.100/32'], random.random())
        yield metric_collection


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CollectSendBytesTotal())
    REGISTRY.register(CollectRecvBytesTotal())
    REGISTRY.register(CollectLatestHandshakeSeconds())

    parser = wg_parser.WGParser()
    parser.parse_output(test=True)

    while True:
        time.sleep(1)
