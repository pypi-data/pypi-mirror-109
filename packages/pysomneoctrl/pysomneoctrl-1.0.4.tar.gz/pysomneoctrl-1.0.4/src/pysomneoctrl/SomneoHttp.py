#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: @pijiulaoshi
Somneo HTTP

USAGE: Load SomneoHttp, with or without IP.

somneo_http = SomneoHttp(ip: (optional) if Somneo has static IP, use it here.)
somneo_http._get(path: path to data needed, target: (optional) "device" or "system")
somneo_http._put(path: path to settings, payload: (dict) keys and values that need to be changed, target: (optional) "device" or "system")
"""
import requests
from requests.adapters import HTTPAdapter
import urllib3
from requests.packages.urllib3.util.retry import Retry
import socket
import json
import logging
import time

forcelist=[413, 429, 500, 502, 503, 504]
backoff = 1
retries = 3
adapt_set = Retry(total=retries, backoff_factor=backoff, status_forcelist=forcelist)


_LOGGER = logging.getLogger('pysomneoctrl_http')

class SomneoHttp:
    """HTTP Client for Somneo"""
    def __init__(self, ip=None, cooldown=0):
        self._cd = cooldown
        self._adapt = HTTPAdapter(max_retries=adapt_set)
        urllib3.disable_warnings()
        self._session = requests.Session()
        self._session.mount("https://", self._adapt)
        self._ip = self._validateIP(ip) if ip else self._getIP()
        self._base_url = f'https://{self._ip}/di/v1/products/'
        self._system_url = f"{self._base_url}0/"
        self._device_url = f"{self._base_url}1/"
        self._headers = {"Content-Type": "application/json"}
        
    def _url(self, target, path):
        if target == "device":
            url = self._device_url + path
        elif target == "system":
            url = self._system_url + path
        return(url)

    def _get(self, path, target="device"):
        url = self._url(target, path)
        try:
            r = self._session.request('GET', url, verify=False)
            if r.status_code == 200:            
                data = r.json()
                time.sleep(self._cd)
                return(data)
            else:
                _LOGGER.error('Connection error or Invallid request')
        except:
            _LOGGER.error('Could not connect to Somneo')

    def _put(self, path, payload={}, target="device"):
        url = self._url(target, path)
        j_payload = json.dumps(payload)
        try:
            r = self._session.request('PUT', url, data=j_payload, headers=self._headers, verify=False)
            if r.status_code == 200:            
                data = r.json()
                time.sleep(self._cd)
                return(data)
            else:
                _LOGGER.error('Connection error or Invallid request')
        except:
            _LOGGER.error('Could not connect to Somneo')

    def _validateIP(self, ip):
        try:
            url = f'https://{ip}/di/v1/products/'
            data = self._session.request('GET', url, verify=False)
            if data.status_code == 200:
                return ip
            else:
                _LOGGER.error('Invalid Somneo IP address')
        except ():
            _LOGGER.error('Invalid Somneo IP address')

    @staticmethod
    def _getIP():
        MC_HOST = '239.255.255.250'
        MC_PORT = 1900
        MC_ST = 'urn:philips-com:device:DiProduct:1'
        MC_MSG = f'M-SEARCH * HTTP/1.1\r\nHOST:{MC_HOST}:1900\r\nST:{MC_ST}\r\nMX:5\r\nMAN:"ssdp:discover"\r\n\r\n'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(20)
        s.sendto(MC_MSG.encode(), (MC_HOST, MC_PORT) )
        try:
            while True:
                data, addr = s.recvfrom(12000)
                dev_ip = addr[0]
                return dev_ip
        except socket.timeout:
            _LOGGER.error('Connection to Somneo timed out')


