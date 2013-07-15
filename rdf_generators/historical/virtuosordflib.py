# coding=utf-8
import httplib
import urllib


class VirtuosoManager:
    def __init__(self, host, user='', password=''):
        self.host = host
        self.user = user
        self.password = password

    def get_request(self, params={}, headers={}):
        host_array = self.host.split('/')
        if host_array[0].startswith('http'):
            conn = httplib.HTTPConnection(host_array[2])
            conn.request("GET", '/' + host_array[3] + '?'
            + urllib.urlencode(params), "", headers)
        else:
            conn = httplib.HTTPConnection(host_array[0])
            conn.request("GET", '/' + host_array[1] + '?'
            + urllib.urlencode(params), "", headers)

        response = conn.getresponse()
        data = response.read()
        return data

    def select(self, query, accept):
        params = {'query': query.encode("utf-8")}
        headers = {"Accept": accept}
        return self.get_request(params, headers)

    def update(self, query, graph):
        params = {'query': query, 'default-graph-uri': graph}
        return self.get_request(params=params)
