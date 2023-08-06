def power_aggregation(
		outlet_services_power_allocation, outlet, service_type, service, flag
):
	if outlet not in outlet_services_power_allocation:
		outlet_services_power_allocation[outlet] = [0.0, 0.0, 0.0]

	if str(service_type) == "FactorySafety":
		x = outlet_services_power_allocation[outlet][0]
		# if action_value == 1:
		if flag == 1:
			outlet_services_power_allocation[outlet][0] = float(x) + float(
				service.service_power_allocate
			)
		elif flag == -1 and x != 0:
			outlet_services_power_allocation[outlet][0] = float(x) - float(
				service.service_power_allocate
			)

	elif str(service_type) == "FactoryEntertainment":
		x = outlet_services_power_allocation[outlet][1]
		# if action_value == 1:
		if flag == 1:
			outlet_services_power_allocation[outlet][1] = float(x) + float(
				service.service_power_allocate
			)
		elif flag == -1 and x != 0:
			outlet_services_power_allocation[outlet][1] = float(x) - float(
				service.service_power_allocate
			)

	elif str(service_type) == "FactoryAutonomous":
		x = outlet_services_power_allocation[outlet][2]
		# if action_value == 1:
		if flag == 1:
			outlet_services_power_allocation[outlet][2] = float(x) + float(
				service.service_power_allocate
			)
		elif flag == -1 and x != 0:
			outlet_services_power_allocation[outlet][2] = float(x) - float(
				service.service_power_allocate
			)


def services_aggregation(
		outlet_services_requested_number, outlet, service_type, flag
):
	# print("outlet_services_requested_number: ... ", outlet_services_requested_number[outlet])
	if outlet not in outlet_services_requested_number:
		outlet_services_requested_number[outlet] = [0.0, 0.0, 0.0]

	if str(service_type) == "FactorySafety":
		num = outlet_services_requested_number[outlet][0]
		if flag == -1 and num != 0:
			outlet_services_requested_number[outlet][0] = int(num) + flag
		elif flag == 1:
			outlet_services_requested_number[outlet][0] = int(num) + flag

	elif str(service_type) == "FactoryEntertainment":
		num = outlet_services_requested_number[outlet][1]
		if flag == -1 and num != 0:
			outlet_services_requested_number[outlet][1] = int(num) + flag
		if flag == 1:
			outlet_services_requested_number[outlet][1] = int(num) + flag
	elif str(service_type) == "FactoryAutonomous":
		num = outlet_services_requested_number[outlet][2]
		if flag == -1 and num != 0:
			outlet_services_requested_number[outlet][2] = int(num) + flag
		if flag == 1:
			outlet_services_requested_number[outlet][2] = int(num) + flag


def ensured_service_aggrigation(
		outlet_services_ensured_number, outlet, service_type, flag) :
	if outlet not in outlet_services_ensured_number:
		outlet_services_ensured_number[outlet] = [0.0, 0.0, 0.0]

	if str(service_type) == "FactorySafety":
		service_ensured_value = outlet_services_ensured_number[outlet][0]
		# if action_value == 1:
		if flag == -1 and service_ensured_value != 0:
			outlet_services_ensured_number[outlet][0] = (
					int(service_ensured_value) + flag
			)
		if flag == 1:
			outlet_services_ensured_number[outlet][0] = (
					int(service_ensured_value) + flag
			)

	elif str(service_type) == "FactoryEntertainment":
		service_ensured_value = outlet_services_ensured_number[outlet][1]
		# if action_value == 1:
		if flag == -1 and service_ensured_value != 0:
			outlet_services_ensured_number[outlet][1] = (
					int(service_ensured_value) + flag
			)
		if flag == 1:
			outlet_services_ensured_number[outlet][1] = (
					int(service_ensured_value) + flag
			)

	elif str(service_type) == "FactoryAutonomous":
		service_ensured_value = outlet_services_ensured_number[outlet][2]
		# if action_value == 1:
		if flag == -1 and service_ensured_value != 0:
			outlet_services_ensured_number[outlet][2] = (
					int(service_ensured_value) + flag
			)
		if flag == 1:
			outlet_services_ensured_number[outlet][2] = (
					int(service_ensured_value) + flag
			)

