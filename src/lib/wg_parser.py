"""
Imports

:subprocess: run wg show all dump command on shell
"""
import subprocess


# pylint: disable=too-few-public-methods
class WGParser:
    """
    Parses output of wg show all dump
    """

    def __init__(self):
        self.parse_result = []

    def parse_output(self, test=False):
        """
        parses output of wg show all dump

        :param: test: get actual data or get 'fake' data from the file test/out.txt
        :return: list of dictionaries
        """
        command = ["wg", "show", "all", "dump"]
        if test:
            command = ["cat", "test/wg_dump_test_out.txt"]

        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ) as child:

            lines = child.stdout.readlines()
            keys = [
                "interface",
                "public-key",
                "preshared-key",
                "endpoint",
                "allowed-ips",
                "latest-handshake",
                "transfer-rx",
                "transfer-tx",
                "persistent-keepalive",
            ]
            device_keys = [
                "interface",
                "private-key",
                "public-key",
                "listen-port",
                "fwmark",
            ]
            ignore_keys = ["persistent-keepalive", "preshared-key"]
            result = []
            device_result = []

            for line in lines:
                fields = line.strip().split(b"\t")
                res = dict()

                if len(fields) == 5:
                    for i, key in enumerate(device_keys):
                        res[key] = fields[i].decode()
                    device_result.append(res)
                    continue

                for i, key in enumerate(keys):
                    if key in ignore_keys:
                        continue
                    if fields[i].decode() == "(none)":
                        res[key] = ""
                    else:
                        res[key] = fields[i].decode()
                result.append(res)

            self.parse_result = result, device_result
