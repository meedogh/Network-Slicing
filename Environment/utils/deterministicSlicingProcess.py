import Service
def check_slice_num(service_list, outlets, slice_num=1):


    for outlet in outlets:
        service = service_list[2]
        print('check_slice_num outlet.current_capacity', outlet.current_capacity)
        print('check_slice_num service.service_power_allocate', service.service_power_allocate)
        print('check_slice_num (service.service_power_allocate // slice_num)', (service.service_power_allocate // slice_num))
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
    # print('number of outlets', len(outlets))
    for outlet in outlets:
        # print('service either list or one', service_list[2])
        # # print('service len', len(service_list[2]))

        # print('service id', service_list[2]._id)
        # print('service id get id', service_list[2].get_id())



        slice_num = check_slice_num(service_list, outlets, slice_num)
        # print('slice number', slice_num)

        if slice_num > 1:
            performance_logger.slice_num_dic = (service, slice_num)
            for i in range(slice_num):
                service = service_list[2]
                sub_service = service
                sub_service.slice_id = i + 1
                sub_service.parent_service = service
                sub_service.service_power_allocate /= slice_num
                services.append(sub_service)
            service.service_power_allocate=0
        else:
            services = service_list
    return services
            
        
