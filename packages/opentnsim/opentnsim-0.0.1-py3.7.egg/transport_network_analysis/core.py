"""Main module."""

# package(s) related to time, space and id
import json
import logging
import uuid

# you need these dependencies (you can get these from anaconda)
# package(s) related to the simulation
import simpy
import networkx as nx

# spatial libraries
import pyproj
import shapely.geometry

# additional packages
import datetime, time

logger = logging.getLogger(__name__)


class SimpyObject:
    """General object which can be extended by any class requiring a simpy environment

    env: a simpy Environment
    """
    def __init__(self, env, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = env


class Identifiable:
    """Something that has a name and id

    name: a name
    id: a unique id generated with uuid"""

    def __init__(self, name, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.name = name
        # generate some id, in this case based on m
        self.id = id if id else str(uuid.uuid1())


class Locatable:
    """Something with a geometry (geojson format)

    geometry: can be a point as well as a polygon"""

    def __init__(self, geometry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.geometry = geometry


class Neighbours:
    """Can be added to a locatable object (list)
    
    travel_to: list of locatables to which can be travelled"""

    def ___init(self, travel_to, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.neighbours = travel_to


class HasContainer(SimpyObject):
    """Container class

    capacity: amount the container can hold
    level: amount the container holds initially
    container: a simpy object that can hold stuff"""

    def __init__(self, capacity, level=0, total_requested=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.container = simpy.Container(self.env, capacity, init=level)
        self.total_requested = total_requested
    
    @property
    def is_loaded(self):
        return True if self.container.level > 0 else False
    
    @property
    def filling_degree(self):
        return self.container.level / self.container.capacity


class VesselProperties:
    """
    Add information on possible restrictions to the vessels.
    Height, width, etc.
    """

    def __init__(self, vessel_type, installed_power,
                 width, length,
                 height_empty, height_full, 
                 draught_empty, draught_full, 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        """Initialization"""
        self.vessel_type = vessel_type
        self.installed_power = installed_power

        self.width = width
        self.length = length

        self.height_empty = height_empty
        self.height_full = height_full

        self.draught_empty = draught_empty
        self.draught_full = draught_full

    @property
    def current_height(self):
        """ Calculate current height based on filling degree """

        return self.filling_degree * (self.height_full - self.height_empty) + self.height_empty

    @property
    def current_draught(self):
        """ Calculate current draught based on filling degree """

        return self.filling_degree * (self.draught_full - self.draught_empty) + self.draught_empty

class HasEnergy:
    """
    Add information on energy use and effects on energy use.
    """

    def __init__(self, emissionfactor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        """Initialization"""
        self.emissionfactor = emissionfactor
        self.energy_use = {'total': 0,'stationary': 0}
        self.co2_footprint = {'total_footprint': 0,'stationary': 0}
        self.mki_footprint = {'total_footprint': 0,'stationary': 0}
    
    @property
    def power(self):
        return 2 * (self.current_speed * self.resistance * 10**-3)  #kW
    
    def calculate_energy_consumption(self):
        """Calculation of energy consumption based on total time in system and properties"""

        stationary_phase_indicator = ['Doors closing stop', 'Converting chamber stop', 'Doors opening stop', 'aiting to pass lock stop']
        
        times = self.log['Timestamp']
        messages = self.log['Message']
        
        for i in range(len(times) - 1):
            delta_t = times[i+1] - times[i]
            
            if messages[i + 1] in stationary_phase_indicator:
                energy_delta =  self.power *  delta_t / 3600 # KJ/3600

                self.energy_use['total_energy'] += energy_delta * 0.15
                self.energy_use['stationary'] += energy_delta * 0.15
            
            else:
                self.energy_use['total_energy'] += self.power * delta_t / 3600


class Routeable:
    """Something with a route (networkx format)
    route: a networkx path"""

    def __init__(self, route, complete_path = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.route = route
        self.complete_path = complete_path


class IsLock:
    """
    Create a lock object
    """

    def __init__(self, nodes, neighbour_lock, lock_length, lock_width, 
                 doors_open, doors_close, operating_time, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        """Initialization"""
        self.nodes = nodes
        self.neighbour_lock = neighbour_lock
        self.lock_length = lock_length
        self.lock_width = lock_width
        self.doors_open = doors_open
        self.doors_close = doors_close
        self.operating_time = operating_time


class Movable(SimpyObject, Locatable, Routeable):
    """Movable class

    Used for object that can move with a fixed speed
    geometry: point used to track its current location
    v: speed"""

    def __init__(self, v=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.v = v
        self.wgs84 = pyproj.Geod(ellps='WGS84')

    def move(self):
        """determine distance between origin and destination, and
        yield the time it takes to travel it
        
        Assumption is that self.path is in the right order - vessel moves from route[0] to route[-1].
        """
        self.distance = 0

        # Check if vessel is at correct location - if note, move to location
        if self.geometry != nx.get_node_attributes(self.env.FG, "geometry")[self.route[0]]:
            orig = self.geometry
            dest = nx.get_node_attributes(self.env.FG, "geometry")[self.route[0]]
            
            print("Origin", orig)
            print("Destination", dest)

            self.distance += self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
                                            shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]
    
            yield self.env.timeout(self.distance / self.current_speed)
            self.log_entry("Sailing to start", self.env.now, self.distance, dest)

        # Move over the path and log every step
        for node in enumerate(self.route):
            origin = self.route[node[0]]
            destination = self.route[node[0] + 1]
            edge = self.env.FG.edges[origin, destination]

            if "Object" in edge.keys():
                if edge["Object"] == "Lock":
                    yield from self.pass_lock(origin, destination)
                elif edge["Object"] == "Waiting Area":
                    yield from self.pass_waiting_area(origin, destination, self.route[node[0] + 2])
                else:
                    yield from self.pass_edge(origin, destination)
            else:
                yield from self.pass_edge(origin, destination)

            if node[0] + 2 == len(self.route):
                break

        self.geometry = nx.get_node_attributes(self.env.FG, "geometry")[destination]
        logger.debug('  distance: ' + '%4.2f' % self.distance + ' m')
        logger.debug('  sailing:  ' + '%4.2f' % self.current_speed + ' m/s')
        logger.debug('  duration: ' + '%4.2f' % ((self.distance / self.current_speed) / 3600) + ' hrs')

    
    def pass_edge(self, origin, destination):
        edge = self.env.FG.edges[origin, destination]
        orig = nx.get_node_attributes(self.env.FG, "geometry")[origin]
        dest = nx.get_node_attributes(self.env.FG, "geometry")[destination]

        distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
                                  shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]

        self.distance += distance
        arrival = self.env.now
        
        # Act based on resources
        if "Resources" in edge.keys():
            with self.env.FG.edges[origin, destination]["Resources"].request() as request:
                yield request

                if arrival != self.env.now:
                    self.log_entry("Waiting to pass edge {} - {} start".format(origin, destination), arrival, 0, orig)
                    self.log_entry("Waiting to pass edge {} - {} stop".format(origin, destination), self.env.now, 0, orig)  

                self.log_entry("Sailing from node {} to node {} start".format(origin, destination), self.env.now, 0, orig)
                yield self.env.timeout(distance / self.current_speed)
                self.log_entry("Sailing from node {} to node {} stop".format(origin, destination), self.env.now, 0, dest)
        
        else:
            self.log_entry("Sailing from node {} to node {} start".format(origin, destination), self.env.now, 0, orig)
            yield self.env.timeout(distance / self.current_speed)
            self.log_entry("Sailing from node {} to node {} start".format(origin, destination), self.env.now, 0, dest)
        

    def pass_lock(self, origin, destination):
        edge = self.env.FG.edges[origin, destination]
        edge_opposite = self.env.FG.edges[destination, origin]
        orig = nx.get_node_attributes(self.env.FG, "geometry")[origin]
        dest = nx.get_node_attributes(self.env.FG, "geometry")[destination]
        water_level = origin

        distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
                                  shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]

        self.distance += distance
        arrival = self.env.now
        
        if "Water level" in edge.keys():
            if edge["Water level"] == water_level:
                priority = 0
            else:
                priority = 1
        else:
            priority = 0

        with self.env.FG.edges[origin, destination]["Resources"].request(priority = priority) as request:
            yield request

            if arrival != self.env.now:
                self.log_entry("Waiting to pass lock start".format(origin, destination), arrival, 0, orig)
                self.log_entry("Waiting to pass lock stop".format(origin, destination), self.env.now, 0, orig)

            # Check direction 
            if "Water level" in edge.keys():
                
                # If water level at origin is not similar to lock-water level --> change water level and wait
                if water_level != edge["Water level"]:
                    
                    # Doors closing
                    self.log_entry("Doors closing start", self.env.now, 0, orig)
                    yield self.env.timeout(10 * 60)
                    self.log_entry("Doors closing stop", self.env.now, 0, orig)

                    # Converting chamber
                    self.log_entry("Converting chamber start", self.env.now, 0, orig)
                    yield self.env.timeout(20 * 60)
                    self.log_entry("Converting chamber stop", self.env.now, 0, orig)

                    # Doors opening
                    self.log_entry("Doors opening start", self.env.now, 0, orig)
                    yield self.env.timeout(10 * 60)
                    self.log_entry("Doors opening start", self.env.now, 0, orig)

                    # Change edge water level
                    self.env.FG.edges[origin, destination]["Water level"] = water_level

            # If direction is similar to lock-water level --> pass the lock
            if not "Water level" in edge.keys() or edge["Water level"] == water_level:
                chamber = shapely.geometry.Point((orig.x + dest.x) / 2, (orig.y + dest.y) / 2)
                
                # Sailing in
                self.log_entry("Sailing into lock start", self.env.now, 0, orig)
                yield self.env.timeout(5 * 60)
                self.log_entry("Sailing into lock stop", self.env.now, 0, chamber)

                # Doors closing
                self.log_entry("Doors closing start", self.env.now, 0, chamber)
                yield self.env.timeout(10 * 60)
                self.log_entry("Doors closing stop", self.env.now, 0, chamber)

                # Converting chamber
                chamber = shapely.geometry.Point((orig.x + dest.x) / 2, (orig.y + dest.y) / 2)
                self.log_entry("Converting chamber start", self.env.now, 0, chamber)
                yield self.env.timeout(20 * 60)
                self.log_entry("Converting chamber stop", self.env.now, 0, chamber)

                # Doors opening
                self.log_entry("Doors opening start", self.env.now, 0, chamber)
                yield self.env.timeout(10 * 60)
                self.log_entry("Doors opening stop", self.env.now, 0, chamber)

                # Sailing out
                self.log_entry("Sailing out of lock start", self.env.now, 0, chamber)
                yield self.env.timeout(5 * 60)
                self.log_entry("Sailing out of lock stop", self.env.now, 0, dest)

                # Change edge water level
                self.env.FG.edges[origin, destination]["Water level"] = destination
        
            # Change edge water level
            self.env.FG.edges[origin, destination]["Water level"] = destination
    
    def pass_waiting_area(self, origin, destination, lock):
        edge = self.env.FG.edges[origin, destination]
        edge_lock = self.env.FG.edges[destination, lock]
        orig = nx.get_node_attributes(self.env.FG, "geometry")[origin]
        dest = nx.get_node_attributes(self.env.FG, "geometry")[destination]
        water_level = destination

        distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
                                  shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]

        self.distance += distance
        arrival = self.env.now
        
        # Act based on resources
        if "Resources" in edge.keys():
            with self.env.FG.edges[origin, destination]["Resources"].request() as request:
                yield request

                if arrival != self.env.now:
                    self.log_entry("Waiting to pass edge {} - {} start".format(origin, destination), arrival, 0, orig)
                    self.log_entry("Waiting to pass edge {} - {} stop".format(origin, destination), self.env.now, 0, orig)  

                if "Water level" in edge_lock.keys():
                    if edge_lock["Water level"] != water_level:
                        self.log_entry("Waiting to pass lock start".format(origin, destination), self.env.now, 0, orig)

                        while edge_lock["Water level"] != water_level:
                            yield self.env.timeout(60)
                        
                        self.log_entry("Waiting to pass lock stop".format(origin, destination), self.env.now, 0, dest)
                    
                    else:
                        self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
                        yield self.env.timeout(distance / self.current_speed)
                        self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
                    
                else:
                    self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
                    yield self.env.timeout(distance / self.current_speed)
                    self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
        
        else:
            yield self.env.timeout(distance / self.current_speed)
            self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)


    def is_at(self, locatable, tolerance=100):
        current_location = shapely.geometry.asShape(self.geometry)
        other_location = shapely.geometry.asShape(locatable.geometry)
        _, _, distance = self.wgs84.inv(current_location.x, current_location.y,
                                        other_location.x, other_location.y)
        return distance < tolerance

    @property
    def current_speed(self):
        return self.v


class ContainerDependentMovable(Movable, HasContainer):
    """ContainerDependentMovable class

    Used for objects that move with a speed dependent on the container level
    compute_v: a function, given the fraction the container is filled (in [0,1]), returns the current speed"""

    def __init__(self, compute_v, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.compute_v = compute_v
        self.wgs84 = pyproj.Geod(ellps='WGS84')

    @property
    def current_speed(self):
        return self.compute_v(self.container.level / self.container.capacity)


class HasResource(SimpyObject):
    """HasProcessingLimit class

    Adds a limited Simpy resource which should be requested before the object is used for processing."""

    def __init__(self, nr_resources=1, priority = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""

        self.resource = simpy.PriorityResource(self.env, capacity=nr_resources) if priority else simpy.Resource(self.env, capacity=nr_resources)


class Log(SimpyObject):
    """Log class

    log: log message [format: 'start activity' or 'stop activity']
    t: timestamp
    value: a value can be logged as well
    geometry: value from locatable (lat, lon)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.log = {"Message": [],
                    "Timestamp": [],
                    "Value": [],
                    "Geometry": []}

    def log_entry(self, log, t, value, geometry_log):
        """Log"""
        self.log["Message"].append(log)
        self.log["Timestamp"].append(datetime.datetime.fromtimestamp(t))
        self.log["Value"].append(value)
        self.log["Geometry"].append(geometry_log)

    def get_log_as_json(self):
        json = []
        for msg, t, value, geometry_log in zip(self.log["Message"], self.log["Timestamp"], self.log["Value"], self.log["Geometry"]):
            json.append(dict(message=msg, time=t, value=value, geometry_log=geometry_log))
        return json


class Processor(SimpyObject):
    """Processor class

    rate: rate with which quantity can be processed [amount/s]"""

    def __init__(self, rate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.rate = rate

    # noinspection PyUnresolvedReferences
    def process(self, origin, destination, amount, origin_resource_request=None, destination_resource_request=None):
        """get amount from origin container, put amount in destination container,
        and yield the time it takes to process it"""
        assert isinstance(origin, HasContainer) and isinstance(destination, HasContainer)
        assert isinstance(origin, HasResource) and isinstance(destination, HasResource)
        assert isinstance(origin, Log) and isinstance(destination, Log)

        assert origin.container.level >= amount
        assert destination.container.capacity - destination.container.level >= amount

        my_origin_turn = origin_resource_request
        if my_origin_turn is None:
            my_origin_turn = origin.resource.request()

        my_dest_turn = destination_resource_request
        if my_dest_turn is None:
            my_dest_turn = destination.resource.request()

        yield my_origin_turn
        yield my_dest_turn
                
        origin.log_entry('unloading start', self.env.now, origin.container.level)
        destination.log_entry('loading start', self.env.now, destination.container.level)

        origin.container.get(amount)
        destination.container.put(amount)
        yield self.env.timeout(amount / self.rate)

        origin.log_entry('unloading stop', self.env.now, origin.container.level)
        destination.log_entry('loading stop', self.env.now, destination.container.level)

        logger.debug('  process:        ' + '%4.2f' % ((amount / self.rate) / 3600) + ' hrs')

        if origin_resource_request is None:
            origin.resource.release(my_origin_turn)
        if destination_resource_request is None:
            destination.resource.release(my_dest_turn)


class DictEncoder(json.JSONEncoder):
    """serialize a simpy digital_twin object to json"""
    def default(self, o):
        result = {}
        for key, val in o.__dict__.items():
            if isinstance(val, simpy.Environment):
                continue
            if isinstance(val, simpy.Container):
                result['capacity'] = val.capacity
                result['level'] = val.level
            elif isinstance(val, simpy.Resource):
                result['nr_resources'] = val.capacity
            else:
                result[key] = val

        return result


def serialize(obj):
    return json.dumps(obj, cls=DictEncoder)


# class Movable(SimpyObject, Locatable, Routeable):
#     """Movable class

#     Used for object that can move with a fixed speed
#     geometry: point used to track its current location
#     v: speed"""

 
#     def __init__(self, v=1, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         """Initialization"""
#         self.v = v
#         self.wgs84 = pyproj.Geod(ellps='WGS84')
#         self.current_index = 0
#         self.path_has_next = True
#         self.distance_convered = 0


#     def do_switch(self, replace, with_this, destination):
#         first_element_to_replace = self.route.index(replace[0])
#         last_element_to_replace = self.route.index(replace[-1])
#         new_route = self.route[:first_element_to_replace] + list(with_this) + self.route[last_element_to_replace + 1:]
#         self.route = new_route

#     def check_switch(self, destination):
#         path_options = self.env.crossover_points[destination]
#         # assume that bi directional
#         edge = None
#         edge_opposite = None
#         for i in range(0, len(path_options[0]) - 1):
#             if self.env.FG.edges[path_options[0][i], path_options[0][i + 1]]["Object"] == "Lock":
#                 edge = self.env.FG.edges[path_options[0][i], path_options[0][i + 1]]
#             if self.env.FG.edges[path_options[1][i], path_options[1][i + 1]]["Object"] == "Lock":
#                 edge_opposite = self.env.FG.edges[path_options[1][i], path_options[1][i + 1]]
#         if (edge == None and edge_opposite == None):
#             # need two locks to work
#             return
         
#         queue_one = len(edge["Resources"].queue)
#         queue_two = len(edge_opposite["Resources"].queue)
#         # print("Queues: ",edge_opposite["attribute"].lock_name, queue_one, queue_two, self.env.now / (60 * 60))
#         if ( queue_one < queue_two and path_options[0][i] not in self.route):
#             # replace all values in path and in path_options[1] in favor of path_options[0]
#             self.do_switch(path_options[1], path_options[0], destination)
#         if (queue_one >= queue_two and  path_options[1][i] not in self.route):
#             # put the alternative path on vessel path
#             self.do_switch(path_options[0], path_options[1], destination)

#     def move(self):
#         """determine distance between origin and destination, and
#         yield the time it takes to travel it
        
#         Assumption is that self.path is in the right order - vessel moves from route[0] to route[-1].
#         """
#         self.distance = 0

#         # Check if vessel is at correct location - if note, move to location
#         if self.geometry != nx.get_node_attributes(self.env.FG, "geometry")[self.route[0]]:
#             orig = self.geometry
#             dest = nx.get_node_attributes(self.env.FG, "geometry")[self.route[0]]
            
#             self.distance += self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
#                                             shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]
    
#             yield self.env.timeout(self.distance / self.current_speed)
#             self.log_entry("Sailing to start", self.env.now, self.distance, dest)

#         # update position while we have a new node on the path
#         while self.path_has_next:
#             if (self.route[self.current_index + 1] == self.route[-1]):
#                 self.path_has_next = False
            
#             origin = self.route[self.current_index]
#             destination = self.route[self.current_index + 1]
#             current_node = self.env.FG.nodes[origin]
#             edge = self.env.FG.edges[origin, destination]
#             self.geometry = current_node["geometry"]
#             # wait for bridges
#             if (current_node["bridge"] == True):
#                 if (self.height >= 9.1):
#                     self.log_entry("waiting to pass bridge start", self.env.now, 0, self.geometry)
#                     yield self.env.timeout(10*60)
#                     self.log_entry("waiting to pass bridge stop", self.env.now, 0, self.geometry)

#             # update current index
#             self.current_index += 1

#             # if encountering a crossover point we check if we are goining into the lock
#             if (destination in self.env.crossover_points):
#                 # check if goining into lock
#                 if (origin not in self.env.crossover_points[destination][0] \
#                     and origin not in self.env.crossover_points[destination][1]):
#                     self.check_switch(destination)

#             if "Object" in edge.keys():
#                 if edge["Object"] == "Lock":
#                     yield from self.pass_lock(origin, destination)
#                 elif edge["Object"] == "Waiting Area":
#                     yield from self.pass_waiting_area(origin, destination, self.route[self.current_index + 1])
#                 else:
#                     yield from self.pass_edge(origin, destination)
#             else:
#                 yield from self.pass_edge(origin, destination)



#         # check for sufficient fuel
#         if isinstance(self, HasFuel):
#             fuel_consumed = self.fuel_use_sailing(self.distance, self.current_speed)
#             self.check_fuel(fuel_consumed)

#         self.geometry = nx.get_node_attributes(self.env.FG, "geometry")[destination]
#         logger.debug('  distance: ' + '%4.2f' % self.distance + ' m')
#         logger.debug('  sailing:  ' + '%4.2f' % self.current_speed + ' m/s')
#         logger.debug('  duration: ' + '%4.2f' % ((self.distance / self.current_speed) / 3600) + ' hrs')

#         # lower the fuel
#         if isinstance(self, HasFuel):
#             # remove seconds of fuel
#             self.consume(fuel_consumed)
    
#     def pass_edge(self, origin, destination):
#         edge = self.env.FG.edges[origin, destination]
#         orig = nx.get_node_attributes(self.env.FG, "geometry")[origin]
#         dest = nx.get_node_attributes(self.env.FG, "geometry")[destination]

#         #next_node = self.env.FG.nodes[self.route[self.current_index + 1]]

#         distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
#                                   shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]

#         self.distance += distance
#         arrival = self.env.now
        
#         # Act based on resources
#         if "Resources" in edge.keys():
#             with self.env.FG.edges[origin, destination]["Resources"].request() as request:
#                 yield request

#                 if arrival != self.env.now:
#                     self.log_entry("waiting to pass edge {} - {} start".format(origin, destination), arrival, 0, orig)
#                     self.log_entry("waiting to pass edge {} - {} stop".format(origin, destination), self.env.now, 0, orig)  

#                 self.log_entry("Sailing from node {} to node {} start".format(origin, destination), self.env.now, 0, orig)

#                 #if (next_node["slow_down"]):
#                 #    yield self.env.timeout((distance - self.length * 7) / self.current_speed)
#                 #else:
#                 yield self.env.timeout((distance) / self.current_speed)

#                 self.log_entry("Sailing from node {} to node {} stop".format(origin, destination), self.env.now, 0, dest)
        
#         else:
#             self.log_entry("Sailing from node {} to node {} start".format(origin, destination), self.env.now, 0, orig)
#             yield self.env.timeout(distance / self.current_speed)
#             self.log_entry("Sailing from node {} to node {} start".format(origin, destination), self.env.now, 0, dest)
        

#     def pass_lock(self, origin, destination):
#         edge = self.env.FG.edges[origin, destination]
#         lock = edge['attribute']

#         orig = nx.get_node_attributes(self.env.FG, "geometry")[origin]
#         dest = nx.get_node_attributes(self.env.FG, "geometry")[destination]
#         water_level = origin

#         distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
#                                   shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]

#         self.distance += distance
#         arrival = self.env.now
        
#         if "Water level" in edge.keys():
#             if edge["Water level"] == water_level:
#                 priority = 0
#             else:
#                 priority = 1
#         else:
#             priority = 0

#         with self.env.FG.edges[origin, destination]["Resources"].request(priority = priority) as request:
#             yield request

#             if arrival != self.env.now:

#                 self.log_entry("waiting to pass lock start".format(origin, destination), arrival, 0, orig)
#                 self.log_entry("waiting to pass lock stop".format(origin, destination), self.env.now, 0, orig)

#             # Check direction (for now do not use this)
#             if "Water level" in edge.keys():
                
#                 # If water level at origin is not similar to lock-water level --> change water level and wait
#                 if water_level != edge["Water level"]:
                    
#                     # Doors closing
#                     self.log_entry("Doors closing start", self.env.now, 0, orig)
#                     yield self.env.timeout(1 * 60)
#                     self.log_entry("Doors closing stop", self.env.now, 0, orig)

#                     # Converting chamber
#                     self.log_entry("Converting chamber start", self.env.now, 0, orig)
#                     yield self.env.timeout(14 * 60)
#                     self.log_entry("Converting chamber stop", self.env.now, 0, orig)

#                     # Doors opening
#                     self.log_entry("Doors opening start", self.env.now, 0, orig)
#                     yield self.env.timeout(1 * 60)
#                     self.log_entry("Doors opening start", self.env.now, 0, orig)

#                     # Change edge water level
#                     self.env.FG.edges[origin, destination]["Water level"] = water_level

#             # If direction is similar to lock-water level --> pass the lock
#             if not "Water level" in edge.keys() or edge["Water level"] == water_level:
#                 chamber = shapely.geometry.Point((orig.x + dest.x) / 2, (orig.y + dest.y) / 2)
#                 lock.log_entry("Ship in lock", self.env.now, self.name, chamber)
#                 # Sailing in
#                 self.log_entry("Sailing into lock start", self.env.now, 0, orig)
#                 yield self.env.timeout(5 * 60)
#                 self.log_entry("Sailing into lock stop", self.env.now, 0, chamber)

#                 # Doors closing
#                 self.log_entry("Doors closing start", self.env.now, 0, chamber)
#                 yield self.env.timeout(lock.doors_close)
#                 self.log_entry("Doors closing stop", self.env.now, 0, chamber)

#                 # Converting chamber
#                 chamber = shapely.geometry.Point((orig.x + dest.x) / 2, (orig.y + dest.y) / 2)
#                 self.log_entry("Converting chamber start", self.env.now, 0, chamber)
#                 yield self.env.timeout(lock.operating_time)
#                 self.log_entry("Converting chamber stop", self.env.now, 0, chamber)

#                 # Doors opening
#                 self.log_entry("Doors opening start", self.env.now, 0, chamber)
#                 yield self.env.timeout(lock.doors_open)
#                 self.log_entry("Doors opening stop", self.env.now, 0, chamber)

#                 # Sailing out
#                 self.log_entry("Sailing out of lock start", self.env.now, 0, chamber)
#                 yield self.env.timeout(5 * 60)
#                 self.log_entry("Sailing out of lock stop", self.env.now, 0, dest)
                
#                 lock.log_entry("Ship out lock", self.env.now, self.name, chamber)

#                 # Change edge water level
#                 self.env.FG.edges[origin, destination]["Water level"] = destination
        
#             # Change edge water level
#             self.env.FG.edges[origin, destination]["Water level"] = destination
    
#     def pass_waiting_area(self, origin, destination, lock):
#         edge = self.env.FG.edges[origin, destination]
#         edge_lock = self.env.FG.edges[destination, lock]
#         orig = nx.get_node_attributes(self.env.FG, "geometry")[origin]
#         dest = nx.get_node_attributes(self.env.FG, "geometry")[destination]
#         water_level = destination

#         distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, 
#                                   shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]

#         self.distance += distance
#         arrival = self.env.now
        
#         # Act based on resources
#         if "Resources" in edge.keys():
#             with self.env.FG.edges[origin, destination]["Resources"].request() as request:
#                 yield request

#                 if arrival != self.env.now:
#                     self.log_entry("waiting to pass edge {} - {} start".format(origin, destination), arrival, 0, orig)
#                     self.log_entry("waiting to pass edge {} - {} stop".format(origin, destination), self.env.now, 0, orig)  

#                 if "Water level" in edge_lock.keys():
#                     if edge_lock["Water level"] != water_level:
#                         self.log_entry("waiting to pass lock start".format(origin, destination), self.env.now, 0, orig)

#                         while edge_lock["Water level"] != water_level:
#                             yield self.env.timeout(60)
                        
#                         self.log_entry("waiting to pass lock stop".format(origin, destination), self.env.now, 0, dest)
                    
#                     else:
#                         self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
#                         yield self.env.timeout(distance / self.current_speed)
#                         self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
                    
#                 else:
#                     self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
#                     yield self.env.timeout(distance / self.current_speed)
#                     self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)
        
#         else:
#             yield self.env.timeout(distance / self.current_speed)
#             self.log_entry("Sailing from node {} to node {}".format(origin, destination), self.env.now, 0, dest)


#     def is_at(self, locatable, tolerance=100):
#         current_location = shapely.geometry.asShape(self.geometry)
#         other_location = shapely.geometry.asShape(locatable.geometry)
#         _, _, distance = self.wgs84.inv(current_location.x, current_location.y,
#                                         other_location.x, other_location.y)
#         return distance < tolerance

#     @property
#     def current_speed(self):
#         return self.v