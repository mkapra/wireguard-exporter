"""
Imports

:time: control sleep time in main function
"""
import time
from datetime import datetime, timedelta

from prometheus_client import start_http_server, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
from prometheus_client.core import REGISTRY, GaugeMetricFamily

import lib.wg_parser as wg_parser

# unregister not used metrics
# pylint: disable=protected-access
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])


# pylint: disable=too-few-public-methods
class CollectSendBytesTotal:
    """
    Custom collector class for bytes sent to wireguard peer
    """

    def __init__(self, wgparser: wg_parser.WGParser):
        self.parser = wgparser

    def collect(self):
        """
        collects metrics

        :return: one metric collection per public_key
        """
        result, device_result = self.parser.parse_result
        metric_collection = GaugeMetricFamily('wireguard_sent_bytes_total',
                                              'Bytes sent to the peer',
                                              labels=['interface', 'public_key', 'allowed_ips'])
        for peer_dict in result:
            metric_collection.add_metric([peer_dict['interface'], peer_dict['public-key'],
                                          peer_dict['allowed-ips']], peer_dict['transfer-tx'])
        yield metric_collection


# pylint: disable=too-few-public-methods
class CollectRecvBytesTotal:
    """
    Custom collector class for bytes received from wireguard peer
    """

    def __init__(self, wgparser: wg_parser.WGParser):
        self.parser = wgparser

    def collect(self):
        """
        collects metrics

        :return: one metric collection per public_key
        """
        result, device_result = self.parser.parse_result
        metric_collection = GaugeMetricFamily('wireguard_received_bytes_total',
                                              'Bytes received from the peer',
                                              labels=['interface', 'public_key', 'allowed_ips'])
        for peer_dict in result:
            metric_collection.add_metric([peer_dict['interface'], peer_dict['public-key'],
                                          peer_dict['allowed-ips']], peer_dict['transfer-rx'])
        yield metric_collection


# pylint: disable=too-few-public-methods
class CollectLatestHandshakeSeconds:
    """
    Custom collector class for how many seconds ago the last wireguard handshake occured
    """

    def __init__(self, wgparser: wg_parser.WGParser):
        self.parser = wgparser

    def collect(self):
        """
        collects metrics

        :return: one metric collection per public_key
        """
        result, device_result = self.parser.parse_result
        metric_collection = GaugeMetricFamily('wireguard_latest_handshake_seconds',
                                              'Seconds from the last handshake',
                                              labels=['interface', 'public_key', 'allowed_ips'])
        for peer_dict in result:
            metric_collection.add_metric([peer_dict['interface'], peer_dict['public-key'],
                                          peer_dict['allowed-ips']], peer_dict['latest-handshake'])
        yield metric_collection


# pylint: disable=too-few-public-methods
class CollectPeerInfo:
    """
    Custom collector class for how many seconds ago the last wireguard handshake occured
    """

    def __init__(self, wgparser: wg_parser.WGParser):
        self.parser = wgparser

    def collect(self):
        """
        collects metrics

        :return: one metric collection per public_key
        """
        result, device_result = self.parser.parse_result
        metric_collection = GaugeMetricFamily('wireguard_peer_info',
                                              'WireGuard Peer Info',
                                              labels=['interface', 'public_key', 'allowed_ips'])
        for peer_dict in result:
            local_time = datetime.fromtimestamp(int(peer_dict['latest-handshake']))
            if datetime.now() - local_time < timedelta(minutes=10):
                online_state = 1
            else:
                online_state = 0
            metric_collection.add_metric([peer_dict['interface'], peer_dict['public-key'],
                                          peer_dict['allowed-ips']], int(online_state))
        yield metric_collection


# pylint: disable=too-few-public-methods
class CollectDeviceInfo:
    """
    Custom collector class for how many seconds ago the last wireguard handshake occured
    """

    def __init__(self, wgparser: wg_parser.WGParser):
        self.parser = wgparser

    def collect(self):
        """
        collects metrics

        :return: one metric collection per public_key
        """
        result, device_result = self.parser.parse_result
        metric_collection = GaugeMetricFamily('wireguard_device_info',
                                              'WireGuard device Info',
                                              labels=['interface', 'public_key'])
        for device_dict in device_result:
            print(device_dict)
            metric_collection.add_metric([device_dict['interface'],
                                          device_dict['public-key']], int(123))

        yield metric_collection


if __name__ == '__main__':

    parser = wg_parser.WGParser()
    parser.parse_output()
    print("Started parser")

    start_http_server(8000)
    REGISTRY.register(CollectSendBytesTotal(parser))
    REGISTRY.register(CollectRecvBytesTotal(parser))
    REGISTRY.register(CollectLatestHandshakeSeconds(parser))
    REGISTRY.register(CollectPeerInfo(parser))
    print("Registering CollectDeviceInfo collector")
    REGISTRY.register(CollectDeviceInfo(parser))
    print("Registered Collectors")

    while True:
        time.sleep(1)
        parser.parse_output(test=True)
