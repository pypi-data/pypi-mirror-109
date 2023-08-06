import re
import json
from urllib import request

class IpLocation:
    '''
    Class IpLocation containes get_location & get_country method.

    '''

    # url - where to fetch ip-api data 
    url = 'http://ip-api.com/json/'

    # get_location method to get response of url in json formate return in a var data
    def get_location(self,ip):

        # Creating request object to GeoLocation API
        req = request.Request(self.url+ip)
        # Getting in response JSON
        response = request.urlopen(req).read()
        # Loading JSON from text to object
        data = json.loads(response.decode('utf-8'))
        return data

    # get_country method to get country from returned json data
    def get_country(self,ip):
        
        #getting ip details in data
        data = self.get_location(ip)
        # returning country
        return data['country']
        




