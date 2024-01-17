import Service
def check_slice_num(service_list, outlets, slice_num=1):
    for outlet in outlets:
        service = service_list[2]
        # print(service)
        if slice_num>4:
            return -1
        if outlet.current_capacity >= service.service_power_allocate:
            return slice_num
        if outlet.current_capacity < (service.service_power_allocate // slice_num) and slice_num<=4:
            slice_num+=1
            return check_slice_num(service, outlets, slice_num)
        
def request_slicer(performance_logger, service_list, outlets, slice_num=1):
    services = []
    
    sub_service = None
    for outlet in outlets:
        slice_num = check_slice_num(service_list, outlets, slice_num)
        for i in range(slice_num):
            service = service_list[2]
            sub_service = service
            sub_service.slice_id = i + 1
            sub_service.service_power_allocate /= slice_num
            services.append(sub_service)
    performance_logger.slice_num_dic = (service._id, slice_num)
    service.service_power_allocate=0
    return services
            
        
