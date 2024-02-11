
from Environment.utils.imports import *
from Environment.utils.period import Period
from Greedy.greedy import Greedy
from GridCell.GridCell import GridCell



class Environment:
    Grids = {}

    size = 0
    data = {}
    Grids = {}
    steps = 0
    average_qvalue_centralize = []
    # Initialize previous_steps variable
    previous_steps = 0
    frame_rate_for_sending_requests = 1
    previous_steps_sending = 0
    previous_period = 0
    snapshot_time = 5
    previous_steps_centralize = 0
    previous_steps_centralize_action = 0
    previouse_steps_reseting = 0
    prev = 0
    memory_threshold = 1500  # 3.5GB
    temp_outlets = []
    gridcells_dqn = []
    flag_processing_old_requests = [False] * 3
    reset_decentralize = False
    previouse_steps_reward32 = 0

    def __init__(self, period: str):
        Period(period)
        self.polygon = traci.polygon
        self.route = traci.route
        self.vehicle = traci.vehicle
        self.poi = traci.poi
        self.gui = traci.gui
        self.simulation = traci.simulation

    def get_polygons(self):
        all_polygon_ = self.polygon.getIDList()
        return all_polygon_

    def get_buildings(self):
        all_builds_ = []
        for id_poly in self.get_polygons():
            if self.polygon.getType(id_poly) == "building":
                all_builds_.append(id_poly)
        return all_builds_

    def prepare_route(self):
        """
        add routes to env_variables
        where the routes generated by randomTrips and store in random_routes_path
        """
        tree = ET.parse(env_variables.random_routes_path)
        root = tree.getroot()
        for child_root in root:
            id_ = child_root.attrib["id"]
            for child in child_root:
                # print(child.tag, child.attrib)
                # if child_root.tag == 'route':
                edges_ = list((child.attrib["edges"]).split(" "))
                # print('the id: {}  , edges: {}'.format(id_, edges_))
                self.route.add(id_, edges_)
                env_variables.all_routes.append(id_)
        del tree
        del root

    def update_outlet_color(self, id_, value):
        color_mapping = {
            (9, 10): (64, 64, 64, 255),  # dark grey
            (6, 9): (255, 0, 0, 255),  # red
            (3, 6): (0, 255, 0, 255),  # green
            (1, 3): (255, 255, 0, 255),  # yellow
        }

        for val_range, color in color_mapping.items():
            if value >= val_range[0] and value <= val_range[1]:
                traci.poi.setColor(id_, color)
        del color_mapping

    def get_all_outlets(self, performancelogger):
        """
        get all outlets and add id with position to env variables
        """
        outlets = []
        poi_ids = traci.poi.getIDList()

        def append_outlets(id_):
            type_poi = traci.poi.getType(id_)

            if type_poi in env_variables.types_outlets:
                print(" type_poi : ", type_poi)
                position_ = traci.poi.getPosition(id_)
                env_variables.outlets[type_poi].append((id_, position_))
                val = 0
                if type_poi == "3G":
                    val = 850
                elif type_poi == "4G":
                    val = 1250
                elif type_poi == "5G":
                    val = 10000
                elif type_poi == "wifi":
                    val = 150
                factory = FactoryCellular(
                    outlet_types[str(type_poi)],
                    1,
                    1,
                    [1, 1, 0],
                    id_,
                    [position_[0], position_[1]],
                    10000,
                    [],
                    [10, 10, 10],
                )

                outlet = factory.produce_cellular_outlet(str(type_poi))
                outlet.outlet_id = id_
                outlet.radius = val
                performancelogger.set_outlet_services_power_allocation(outlet, [0, 0, 0])
                performancelogger.set_queue_requested_buffer(outlet, deque([]))
                performancelogger.set_queue_ensured_buffer(outlet, deque([]))
                performancelogger.set_queue_power_for_requested_in_buffer(outlet, deque([]))
                performancelogger.set_outlet_services_requested_number_all_periods(outlet, [0, 0, 0])
                # performancelogger.set_outlet_services_requested_number(outlet, [0, 0, 0])
                performancelogger.set_outlet_services_ensured_number(outlet, [0, 0, 0])
                # performancelogger.set_outlet_services_power_allocation_10_TimeStep(outlet, [0, 0, 0])

                outlets.append(outlet)

        list(map(lambda x: append_outlets(x), poi_ids))

        # satellite = Satellite(1, [1, 1, 0], 0, [0, 0],
        #                       100000, [],
        #                       [10, 10, 10])
        # outlets.append(satellite)

        del poi_ids

        return outlets

    def distance(self, outlet1, outlet2):
        """Returns the Euclidean distance between two outlets"""
        return math.sqrt(
            (outlet1.position[0] - outlet2.position[0]) ** 2
            + (outlet1.position[1] - outlet2.position[1]) ** 2
        )

    def fill_grids_with_the_nearest(self, outlets):
        sub_dis = []
        for j in outlets:
            dis = []
            for i in outlets:
                dis.append(self.distance(j, i))
            if len(dis) >= 3:
                sorted_dis = sorted(dis)
                min_indices = [dis.index(sorted_dis[i]) for i in range(3)]
                elements = [outlets[i] for i in min_indices]
                outlets = [
                    element
                    for index, element in enumerate(outlets)
                    if index not in min_indices
                ]
                sub_dis.append(elements)
        return sub_dis

    @staticmethod
    def fill_grids(grids):
        Grids = {
            "grid1": [],
            "grid2": [],
            "grid3": [],
            "grid4": [],
            "grid5": [],
            "grid6": [],
            "grid7": [],
        }

        def grid_namer(i, grid):
            name = "grid" + str(i + 1)
            Grids[name] = grid

        list(map(lambda x: grid_namer(x[0], x[1]), enumerate(grids)))
        return Grids

    def select_outlets_to_show_in_gui(self):
        """
        select outlets in .network to display type of each outlet
        """
        # for key in env_variables.outlets.keys():
        #     for _id,_ in env_variables.outlets[key]:
        #         self.gui.toggleSelection(_id, 'poi')
        from itertools import chain

        array = list(
            map(
                lambda x: x,
                chain(*list(map(lambda x: x[1], env_variables.outlets.items()))),
            )
        )
        list(
            map(
                lambda x: self.gui.toggleSelection(x[0], "poi"), map(lambda x: x, array)
            )
        )
        del array

    def get_positions_of_outlets(self, outlets):
        positions_of_outlets = []

        list(map(lambda x: positions_of_outlets.append(x.position), outlets))
        return positions_of_outlets

    def generate_vehicles(self, number_vehicles):
        """
        It generates vehicles and adds it to the simulation
        and get random route for each vehicle from routes in env_variables.py
        :param number_vehicles: number of vehicles to be generated
        """

        all_routes = env_variables.all_routes

        def add_vehicle(id_route_):
            uid = str(uuid4())
            self.vehicle.add(vehID=uid, routeID=id_route_)

            env_variables.vehicles[uid] = Car(uid, 0.0, 0.0)

        list(map(add_vehicle, ra.choices(all_routes, k=number_vehicles)))
        del all_routes

    def starting(self):
        """
        The function starts the simulation by calling the sumoBinary, which is the sumo-gui or sumo
        depending on the nogui option
        """

        os.environ["SUMO_NUM_THREADS"] = "8"
        # show gui
        # sumo_cmd = ["sumo-gui", "-c", env_variables.network_path]
        # dont show gui
        sumo_cmd = ["sumo", "-c", env_variables.network_path]
        traci.start(sumo_cmd)

        # end the simulation and d

        self.prepare_route()

    def remove_vehicles_arrived(self):
        """
        Remove vehicles which removed from the road network ((have reached their destination) in this time step
        the add to env_variables.vehicles (dictionary)
        """
        ids_arrived = self.simulation.getArrivedIDList()

        def remove_vehicle(id_):
            # print("del car object ")
            del env_variables.vehicles[id_]

        if len(ids_arrived) != 0:
            list(map(remove_vehicle, ids_arrived))

    def add_new_vehicles(self):
        """
        Add vehicles which inserted into the road network in this time step.
        the add to env_variables.vehicles (dictionary)
        """
        ids_new_vehicles = traci.vehicle.getIDList()

        def create_vehicle(id_):
            env_variables.vehicles[id_] = Car(id_, 0, 0)

        list(map(create_vehicle, ids_new_vehicles))

    def car_distribution(self, step):
        if step == 0:
            number_cars = int(
                nump_rand.normal(
                    loc=env_variables.number_cars_mean_std["mean"],
                    scale=env_variables.number_cars_mean_std["std"],
                )
            )
            self.generate_vehicles(number_cars)

        if traci.vehicle.getIDCount() <= env_variables.threashold_number_veh:
            number_cars = int(
                nump_rand.normal(
                    loc=env_variables.number_cars_mean_std["mean"],
                    scale=env_variables.number_cars_mean_std["std"],
                )
            )
            self.generate_vehicles(number_cars)

    def decentralize_reset(self,outlets, performance_logger):
        for i, outlet in enumerate(outlets):
            performance_logger.set_outlet_services_power_allocation_10_TimeStep(outlet, [0, 0, 0])
            # print("befor resetting : ")
            # print("requested buffer  : ", len(performance_logger.queue_requested_buffer[outlet]))
            # print("ensured buffer  : ", len(performance_logger.queue_ensured_buffer[outlet]))

            for j in range(len(performance_logger.queue_ensured_buffer[outlet])):
                performance_logger.queue_requested_buffer[outlet].popleft()
                service = performance_logger.queue_power_for_requested_in_buffer[outlet].popleft()
                performance_logger.queue_provisioning_time_buffer.pop(service)
            performance_logger.queue_ensured_buffer[outlet].clear()
            # print("after resetting : ")
            # print("requested buffer  after : ", len(performance_logger.queue_requested_buffer[outlet]))
            # print("ensured buffer  after : ", len(performance_logger.queue_ensured_buffer[outlet]))

    def provisioning_time_services(self,outlets, performance_logger, time_step_simulation):
        for i, outlet in enumerate(outlets):
            for service in performance_logger.queue_power_for_requested_in_buffer[outlet]:
                start_time = performance_logger.queue_provisioning_time_buffer[service][0]
                period_of_termination = performance_logger.queue_provisioning_time_buffer[service][1]
                if start_time + period_of_termination == time_step_simulation:
                    outlet.current_capacity = outlet.current_capacity + service.service_power_allocate

    def enable_sending_requests(self,greedy,car, observer, performance_logger, start_time):

        # car.attach(observer)
        car.set_state(
            float(round(traci.vehicle.getPosition(car.id)[0], 4)),
            float(round(traci.vehicle.getPosition(car.id)[1], 4)),
        )

        # car.add_satellite(outlets[-1])
        info = car.send_request()
        if info != None:
            service = info[1][2]
            outlet = info[0]
            service_index = service._dec_services_types_mapping[service.__class__.__name__]
            outlet.supported_services = greedy._supported_services

            if outlet.supported_services[service_index] == 1:
                # print(action,"  ",service.request_supported(outlet)," ",outlet.current_capacity)
                performance_logger.queue_requested_buffer[outlet].appendleft(1)
                performance_logger.set_queue_provisioning_time_buffer(service, [0, 0])
                performance_logger.queue_provisioning_time_buffer[service] = [start_time,
                                                                              service.calcualate_processing_time()]
                request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
                request_cost = RequestCost(request_bandwidth, service.realtime)
                request_cost.cost_setter(service.realtime)
                service.service_power_allocate = request_bandwidth.allocated
                # print("service.service_power_allocate : ",service.service_power_allocate)
                power_aggregation(
                    performance_logger.outlet_services_power_allocation,
                    outlet,
                    service.__class__.__name__,
                    service,
                    1,
                )

                services_aggregation(
                    performance_logger.outlet_services_requested_number,
                    outlet,
                    service.__class__.__name__,
                    1,
                )

                services_aggregation(
                    performance_logger.outlet_services_requested_number_all_periods,
                    outlet,
                    service.__class__.__name__,
                    1,
                )

                performance_logger.queue_power_for_requested_in_buffer[outlet].appendleft(service)
                # print("req")
                # print("action : ",outlet.dqn.agents.action.command.action_value_decentralize)
                # print("action[service_index] : ", action[service_index])
                # print("outlet.current_capacity : ",outlet.current_capacity)
                # print("service.service_power_allocate : ",service.service_power_allocate)
                if outlet._max_capacity !=0 and outlet._max_capacity > service.service_power_allocate:
                    # print("ensured ")
                    ensured_service_aggrigation(
                        performance_logger.outlet_services_ensured_number,
                        outlet,
                        service.__class__.__name__,
                        1,

                    )
                    power_aggregation(
                        performance_logger._outlet_services_power_allocation_10_TimeStep,
                        outlet,
                        service.__class__.__name__,
                        service,
                        1,
                    )
                    performance_logger.queue_ensured_buffer[outlet].appendleft(1)
                    outlet._max_capacity = outlet._max_capacity - service.service_power_allocate

    def run(self):

        self.starting()
        performance_logger = PerformanceLogger()
        outlets = self.get_all_outlets(performance_logger)
        self.Grids = self.fill_grids(self.fill_grids_with_the_nearest(outlets[:21]))
        step = 0
        print("\n")
        for i in outlets:
            print("out ", i.__class__.__name__)

        outlets_pos = self.get_positions_of_outlets(outlets)
        observer = Car(outlets_pos, outlets)
        greedy = Greedy()
        # set the maximum amount of memory that the garbage collector is allowed to use to 1 GB
        max_size = 273741824

        gc.set_threshold(700, max_size // gc.get_threshold()[1])
        gc.collect(0)
        build = []
        for i in range(1):
            build.append(RLBuilder())
            self.gridcells_dqn.append(
                build[i]
                .agent.build_agent(ActionAssignment())
                .environment.build_env(CentralizedReward(), CentralizedState())
                .model_.build_model("centralized", 12, 2)
                .build()
            )

            self.gridcells_dqn[i].agents.grid_outlets = self.Grids.get(f"grid{i + 1}")
            self.gridcells_dqn[i].agents.outlets_id = list(
                range(len(self.gridcells_dqn[i].agents.grid_outlets))
            )

        for i in range(1):
            for index, outlet in enumerate(self.gridcells_dqn[i].agents.grid_outlets):
                outlet._max_capacity = outlet.set_max_capacity(outlet.__class__.__name__)

                self.temp_outlets.append(outlet)
        print("self.temp_outlets.append(outlet): ", self.temp_outlets)

        number_of_decentralize_periods = 0
        while step < env_variables.TIME:
            process = psutil.Process()
            memory_usage = process.memory_info().rss / 1024.0 / 1024.0  # Convert to MB
            if memory_usage > self.memory_threshold:
                gc.collect(0)

            gc.collect(0)

            traci.simulationStep()
            self.car_distribution(step)
            self.remove_vehicles_arrived()
            print("step is ....................................... ", step)

            # if self.steps - previous_steps_sending == frame_rate_for_sending_requests:
            #     previous_steps_sending = self.steps

            number_of_cars_will_send_requests = round(
                len(list(env_variables.vehicles.values())) * 0.01
            )
            vehicles = ra.sample(
                list(env_variables.vehicles.values()), number_of_cars_will_send_requests
            )
            # list(map(lambda veh: requests_buffering(veh, observer, performance_logger), vehicles, ))
            # for index, outlet in enumerate(self.temp_outlets):

            list(map(lambda veh:self.enable_sending_requests(veh, observer , performance_logger,self.steps,greedy),vehicles))

            update_figures(self.steps / 10, self.temp_outlets, self.gridcells_dqn)

            if self.steps - self.prev == self.snapshot_time:
                self.prev = self.steps
                take_snapshot_figures()

            else:
                close_figures()

                step += 1
                self.steps += 1


            self.close()

    def close(self):
        traci.close()
