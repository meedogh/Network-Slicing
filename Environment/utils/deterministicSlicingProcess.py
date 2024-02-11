from Utils.Bandwidth import Bandwidth
from copy import deepcopy
def check_slice_num(service_list, outlets, slice_num=1):
    
    # bandwidth_demand = SERVICES_TYPES[request.type]["BANDWIDTH"]
    # critical_demand = SERVICES_TYPES[request.type]["CRITICAL"]
    # allocated_bandwidth = Bandwidth(bandwidth_demand, request.power).allocated()
    # if allocated_bandwidth <= tower.capacity:
    for outlet in outlets:
        if isinstance(service_list, list):
            service = service_list[2]
        else:
            service = service_list
        # print("BANDWIDTH", service.bandwidth)
        # print("CRITICALITY", service.criticality)
        # print('check_slice_num outlet.current_capacity', outlet.current_capacity)
        # print('check_slice_num service.service_power_allocate', service.service_power_allocate)
        # print('check_slice_num (service.service_power_allocate // slice_num)', (service.service_power_allocate // slice_num))

        bandwidth = Bandwidth(service.bandwidth, service.criticality)
        allocated_bandwidth = bandwidth.allocated
        # print(service)
        
        if outlet.current_capacity >= allocated_bandwidth:
            return slice_num
        
        elif outlet.current_capacity < (allocated_bandwidth // slice_num) and slice_num<=4:
            slice_num+=1
            return check_slice_num(service, outlets, slice_num)
        
        if slice_num > 4 or slice_num is None:
            return -1
        


def request_slicer(performance_logger, service_list, outlets, slice_num=1):
    services = []
    
    sub_service = None
    for outlet in outlets:
        slice_num = check_slice_num(service_list, outlets, slice_num)
        # print(f"SLICE NUM {slice_num}")
        if slice_num > 1:
            for i in range(slice_num):
                service = service_list[2]
                sub_service = deepcopy(service)
                sub_service.slice_id = i + 1
                sub_service.parent_service = service
                # print("PARENT", sub_service.parent_service)
                sub_service.service_power_allocate /= slice_num
                services.append(sub_service)
            # print("NUM SLICES", slice_num)
            performance_logger.slice_num_dic = (service, slice_num)
            
            service.service_power_allocate=0
        else:
            services = service_list
            performance_logger.slice_num_dic = (services[2], slice_num)
    # print("SLICE NUM DIC", performance_logger.slice_num_dic)
    return services
            
        
