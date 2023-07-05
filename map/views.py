import math
import os
from geopy.geocoders import Nominatim
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
import googlemaps
from datetime import datetime

class GetDirections(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            gmaps = googlemaps.Client(os.environ.get('SECRET_KEY_MAP'))

            lat = str(request.query_params.get('latitude'))
            long = str(request.query_params.get('longitude'))

            coords_0 = '21.5257912579491, -78.22317337147534'
            coords_1 = '21.52635016634832, -78.22920297717373'
            now = datetime.now()
            directions_result = gmaps.directions(coords_0, coords_1, mode="driving", departure_time=now, avoid='tolls')

            listPoints = []
            steps = directions_result[0]["legs"][0]["steps"]
            for s in steps:
                listPoints.append(s["polyline"]["points"])

            return Response(['agkbCt}l|MfCjB', 'ybkbC`am|MqAxB{A`C{@pAW`@i@|@e@x@oAtBs@pAeBrC', 'utkbCd{m|M`DxBlA|@vAdA'],
                status=status.HTTP_200_OK)

            return Response({"points":['agkbCt}l|MfCjB', 'ybkbC`am|MqAxB{A`C{@pAW`@i@|@e@x@oAtBs@pAeBrC', 'utkbCd{m|M`DxBlA|@vAdA']},
                status=status.HTTP_200_OK
            )
        except:
            return Response(['agkbCt}l|MfCjB', 'ybkbC`am|MqAxB{A`C{@pAW`@i@|@e@x@oAtBs@pAeBrC', 'utkbCd{m|M`DxBlA|@vAdA'],
                status=status.HTTP_200_OK)



"""class GetAddress(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        #try:
            lat = str(request.query_params.get('latitude'))
            long = str(request.query_params.get('longitude'))
            
            gmaps = googlemaps.Client(os.environ.get('SECRET_KEY_MAP'))
                        
            coords_0 = '21.5257912579491, -78.22317337147534'
            coords_1 = '21.52635016634832, -78.22920297717373'
            now = datetime.now()
            directions_result = gmaps.directions(coords_0, coords_1, mode="driving", departure_time=now, avoid='tolls')
            
            # Get distance
            distance = 0
            legs = directions_result[0].get("legs")
            for leg in legs:
                distance = distance + leg.get("distance").get("value")

            # Look up an address with reverse geocoding
            listPoints = []
            steps = directions_result[0]["legs"][0]["steps"]
            for s in steps:
                listPoints.append(s["polyline"]["points"])

            print(listPoints)
            return Response("address",
                status=status.HTTP_200_OK
            )
        #except:
            return Response('Error--',
                status=status.HTTP_200_OK
            )"""


class GetAddressGeopy(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            lat = str(request.query_params.get('latitude'))
            long = str(request.query_params.get('longitude'))

            geolocator = Nominatim(user_agent="CityMarket")
            
            address = geolocator.reverse(lat + ", " + long).address
            addressList = address.split(",")

            if addressList[-1] == " Cuba":
                addressList = addressList[:-1]
            if isCP(addressList[-1]):
                addressList = addressList[:-1]

            address = ",".join(addressList)
            
            return Response(address,
                status=status.HTTP_200_OK
            )
        except:
            return Response('Error',
                status=status.HTTP_200_OK
            )


def isCP(n):
    try:
        int(n)
        return True
    except:
        return False



def getAddressStr(location):
    try:
        geolocator = Nominatim(user_agent="Reevo")
        address = geolocator.reverse(location).address
        return address
    except:
        return "Errorq"

def calculate_distance(lon1,lat1,lon2,lat2):
    dLat = (lat2 - lat1) * math.pi/180.0
    dLon = (lon2 - lon1) * math.pi/180.0

    lat1 = (lat1) * math.pi/180.0
    lat2 = (lat2) * math.pi/180.0

    a = (pow(math.sin(dLat/2), 2) + pow(math.sin(dLon/2), 2) * math.cos(lat1) * math.cos(lat2))
    c = 2 * math.asin(math.sqrt(a))
    return round(c * 6378,1)

def getDirections(coords_0=str,coords_1=str):
    try:
        gmaps = googlemaps.Client(os.environ.get('SECRET_KEY_MAP'))
        now = datetime.now()
        directions_result = gmaps.directions(coords_0, coords_1, mode="driving", departure_time=now, avoid='tolls')

        listPoints = []
        steps = directions_result[0]["legs"][0]["steps"]
        for s in steps:
            listPoints.append(s["polyline"]["points"])
        return listPoints
    except:
        print("Error en getDirections funtion")
        return []