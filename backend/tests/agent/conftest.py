"""Fail tests on any Internet attempt, including attempts swallowed by a library."""

import ipaddress
import socket

import pytest


@pytest.fixture(autouse=True)
def no_internet(monkeypatch):
    attempted = []

    def check(host):
        if host in (None, "localhost", "127.0.0.1", "::1", b"localhost"):
            return
        try:
            if ipaddress.ip_address(host).is_loopback:
                return
        except ValueError:
            pass
        attempted.append(host)
        raise AssertionError("Internet access is prohibited in offline tests")

    original_resolve = socket.getaddrinfo
    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex

    def resolve(host, *args, **kwargs):
        check(host)
        return original_resolve(host, *args, **kwargs)

    def connect(sock, address):
        if isinstance(address, tuple):
            check(address[0])
        return original_connect(sock, address)

    def connect_ex(sock, address):
        if isinstance(address, tuple):
            check(address[0])
        return original_connect_ex(sock, address)

    monkeypatch.setattr(socket, "getaddrinfo", resolve)
    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(socket.socket, "connect_ex", connect_ex)
    yield
    assert not attempted, "An Internet connection was attempted"
