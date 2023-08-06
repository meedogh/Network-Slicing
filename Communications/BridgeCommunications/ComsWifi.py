from Communications.IComs import Communications


class ComsWifi(Communications):
    def propagation_range(self):
        return 1

    def calculate_data_rate(self):
        return 2
