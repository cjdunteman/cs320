from math import sin, cos, asin, sqrt, pi
from zipfile import ZipFile
import pandas as pd


# Read zip files
with ZipFile('mmt_gtfs.zip') as zf:
    with zf.open("calendar.txt") as f:
        cal_df = pd.read_csv(f)
    with zf.open("trips.txt") as f:
        trips_df = pd.read_csv(f)
    with zf.open("stop_times.txt") as f:
        stop_times_df = pd.read_csv(f)
    with zf.open("stops.txt") as f:
        stops_df = pd.read_csv(f)
        
        
def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points on earth using the
    harversine distance (distance between points on a sphere)
    See: https://en.wikipedia.org/wiki/Haversine_formula

    :param lat1: latitude of point 1
    :param lon1: longitude of point 1
    :param lat2: latitude of point 2
    :param lon2: longitude of point 2
    :return: distance in miles between points
    """
    lat1, lon1, lat2, lon2 = (a/180*pi for a in [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * asin(min(1, sqrt(a)))
    d = 3956 * c
    return d


class Location:
    """Location class to convert lat/lon pairs to
    flat earth projection centered around capitol
    """
    capital_lat = 43.074683
    capital_lon = -89.384261

    def __init__(self, latlon=None, xy=None):
        if xy is not None:
            self.x, self.y = xy
        else:
            # If no latitude/longitude pair is given, use the capitol's
            if latlon is None:
                latlon = (Location.capital_lat, Location.capital_lon)

            # Calculate the x and y distance from the capital
            self.x = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     Location.capital_lat, latlon[1])
            self.y = haversine_miles(Location.capital_lat, Location.capital_lon,
                                     latlon[0], Location.capital_lon)

            # Flip the sign of the x/y coordinates based on location
            if latlon[1] < Location.capital_lon:
                self.x *= -1

            if latlon[0] < Location.capital_lat:
                self.y *= -1

    def dist(self, other):
        """Calculate straight line distance between self and other"""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return "Location(xy=(%0.2f, %0.2f))" % (self.x, self.y)
        

class BusDay():
    """Describes the bus trips and routes available in Madison for a specific day. 
    """
    def __init__(self, time):
        self.time = time
        
        # Format time and convert to int
        ftime = int(time.strftime("%Y%m%d"))

        service_ids_df = cal_df[(ftime > cal_df.start_date) & (ftime < cal_df.end_date) & (cal_df[time.strftime('%A').lower()] == 1)]
        
        self.service_ids = sorted(service_ids_df.service_id.tolist())

        self.trips = self.get_trips()
        self.stops = self.get_stops()
        
    def get_trips(self, route_id = None):
        trips_list = []
        if route_id == None:
            trips = trips_df[(trips_df.service_id.isin(self.service_ids))]
        else:
            trips = trips_df[(trips_df.service_id.isin(self.service_ids)) & (trips_df.route_short_name == int(route_id))]
        
        for row in trips.itertuples(index=True, name='Pandas'):
            trips_list.append(Trip(getattr(row, "trip_id"), getattr(row, "route_short_name"), getattr(row, "bikes_allowed")))
        
        return sorted(trips_list, key=lambda x: x.trip_id)
    
    def get_stops(self):
         pass
#         stops_list = []

#         stops = stop_times_df.loc[stop_times_df['trip_id']].isin(self.trips)
            
#         return stops


    def get_stops_rect():
        pass
    
    def get_stops_circ(self, origin, radius):
        """Return all stops in the circle defined by the center at (x, y) and radius"""        
        x = origin
        y = origin
        
        x = ((x - radius), (x + radius))
        y = ((y - radius), (y + radius))
        
        for i in self.get_stops_rect(x, y):
             if (i.location.x - x) ** 2 + (i.location.y - y) ** 2 <= radius ** 2:
                 stops_circ.append(i)
        
        return stops_circ
                                  
    def scatter_stops(self, ax):
        pass
             
    def scatter_stops(self, ax):
             pass
                                  
    def draw_tree(self, ax):
        pass
    

class Trip():
    def __init__(self, trip_id, routes_id, bikes_allowed):
        self.trip_id = trip_id
        self.routes_id = routes_id
        self.bikes_allowed = bikes_allowed
        
    def __repr__(self):
        return "Trip({}, {}, {})".format(self.trip_id, self.routes_id, self.bikes_allowed)


class Stop():
    def __init__(self, stop_id, location, wheelchair_boarding):
        self.stop_id = stop_id
        self.location = location
        self.wheelchair_boarding = wheelchair_boarding
        
    def __repr__(self):
        return "Stop({}, {}, {})".format(self.stop_id, self.location, self.wheelchair_boarding)
    
    
        
        
def iter_thing(first, second, third):
    list1 = []
    list1.append(Trip(df.loc[first], df.loc[second], df.loc[third]))
    return list1
