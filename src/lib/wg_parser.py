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
    @staticmethod
    def parse_output(test=False):
        """
        parses output of wg show all dump

        :param: test: get actual data or get 'fake' data from the file test/out.txt
        :return: list of dictionaries
        """

        command = ["wg", "show", "all", "dump"]
        if test:
            command = ["cat", "test/wg_dump_test_out.txt"]

        with subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as child:

            lines = child.stdout.readlines()
            # we don't need the first line since it is related to the peer
            # on which the command was run.
            lines.pop(0)

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
            ignore_keys = ["persistent-keepalive", "preshared-key"]
            result = []

            for line in lines:
                fields = line.strip().split(b"\t")
                res = dict()
                for i, key in enumerate(keys):
                    if key in ignore_keys:
                        continue
                    if fields[i].decode() == "(none)":
                        res[key] = ""
                    else:
                        res[key] = fields[i].decode()
                result.append(res)

            return result
