#!/usr/bin/python3

from prometheus_client import start_http_server

if __name__ == '__main__':
    start_http_server(8000)
