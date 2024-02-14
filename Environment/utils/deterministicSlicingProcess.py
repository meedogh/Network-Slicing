from Utils.Bandwidth import Bandwidth
from copy import deepcopy
def check_slice_num(service_list, outlets):
    for outlet in outlets:
        if isinstance(service_list, list):
            service = service_list[2]
        else:
            service = service_list
        for slice_num in range(1, 5):
            bandwidth = Bandwidth(service.bandwidth, service.criticality).allocated
            if outlet.current_capacity >= bandwidth // slice_num:
                return slice_num
    return 1
        


def request_slicer(performance_logger, service_list, outlets, slice_num=1):
    services = []
    
    sub_service = None
    for outlet in outlets:

        slice_num = check_slice_num(service_list, outlets)
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
            
        
