# -*- coding: utf-8 -*-
from builtins import bytes
from builtins import range
from builtins import object
import platform
import socket
import struct
import time
import threading

class ErrorReporter(object):
    """
    Reports errors by emitting metrics, and if logger is provided,
    logging the error message once every log_interval_minutes

    N.B. metrics will be deprecated in the future
    """

    def __init__(self, logger=None, log_interval_minutes=15):
        self.logger = logger
        self.log_interval_minutes = log_interval_minutes
        self._last_error_reported_at = time.time()

    def error(self, *args):
        if self.logger is None:
            return

        next_logging_deadline = \
            self._last_error_reported_at + (self.log_interval_minutes * 60)
        current_time = time.time()
        if next_logging_deadline >= current_time:
            # If we aren't yet at the next logging deadline
            return

        self.logger.error(*args)
        self._last_error_reported_at = current_time

def get_boolean(string, default):
    string = str(string).lower()
    if string in ['false', '0', 'none']:
        return False
    elif string in ['true', '1']:
        return True
    else:
        return default
        
def gethostname():
    return socket.gethostname()
    
if platform.system().lower().find("windows") != -1:
    
    def local_ip():
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]    
        finally:
            s.close()
        return ip
    
elif platform.system().lower().find("linux") != -1:
    import fcntl

    def local_ip():
        """Get the local network IP of this machine"""
        try:
            ip = socket.gethostbyname(gethostname())
        except IOError:
            ip = socket.gethostbyname('localhost')
        if ip.startswith('127.'):
            # Check eth0, eth1, eth2, en0, ...
            interfaces = [
                i + str(n) for i in ('eth', 'en', 'wlan') for n in range(3)
            ]  # :(
            for interface in interfaces:
                try:
                    ip = interface_ip(interface)
                    break
                except IOError:
                    pass
        return ip

    def interface_ip(interface):
        """Determine the IP assigned to us by the given network interface."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(
            fcntl.ioctl(
                sock.fileno(), 0x8915, struct.pack('256s', interface[:15])
            )[20:24]
        )
        # Explanation:
        # http://stackoverflow.com/questions/11735821/python-get-localhost-ip
        # http://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python

def ip2long(ip):
    packedIP = socket.inet_aton(ip)  
    return struct.unpack("!L", packedIP)[0]
