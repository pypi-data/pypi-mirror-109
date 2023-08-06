import re
import json
from urllib import request

# import urllib

class IpLocation:
    url = 'http://ip-api.com/json/'

    def get_location(self,ip):
        # Creating request object to GeoLocation API
        req = request.Request(self.url+ip)
        # Getting in response JSON
        response = request.urlopen(req).read()
        # Loading JSON from text to object
        data = json.loads(response.decode('utf-8'))
        return data

    def get_country(self,ip):
        data = self.get_location(ip)
        return data['country']
        




