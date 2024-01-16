from ...Service.IService import Service
def check_slice_num(service, outlets, slice_num=1):
    for outlet in outlets:
        if slice_num>4:
            return -1
        if outlet.capacity >= service.service_power_allocate:
            return slice_num
        if outlet.capacity < (service.service_power_allocate // slice_num) and slice_num<=4:
            slice_num+=1
            return check_slice_num(service, outlets, slice_num)
        
def request_slicer(service, outlets, slice_num=1):
    services = []
    sub_service = None
    for outlet in outlets:
        slice_num = check_slice_num(service, outlets, slice_num)
        for _ in range(slice_num):
            sub_service = Service(service.bandwidth , 
                                service.criticality , 
                                service.realtime , 
                                service.service_power_allocate , 
                                service.dec_services_types_mapping , 
                                service.id ,
                                service.slice_id , 
                                service.time_out , 
                                service.time_execution , 
                                service.request_failure , 
                                service.cost_in_bit_rate ,
                                service.total_cost_in_dolars,
                                service.remaining_time_out,
                                service.tower_capacity_before_time_out_step,
                                service.risk_flag,)
            sub_service.slice_id += 1
            sub_service.service_power_allocate /= slice_num
            services.append(sub_service)
    service.service_power_allocate=0
    return services
            
        
