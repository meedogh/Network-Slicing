from abc import ABC, abstractmethod


class Communications(ABC):

    def __init__(self, frequency: float, bandwidth: float, data_rate: float,
                 radius: float, interference: float):
        """
            Project a point on the surface of a sphere

            Parameters
            ----------
            frequency : float
                The number of cycles of a waveform that occur in one second, and it is typically measured in hertz (Hz)
            bandwidth : Tuple[float,float,float]
                Determines the maximum amount of data that can be transmitted over a channel,
            data_rate : float
                Refers to the amount of data that can be transmitted per second, typically measured in bits per second (bps)
            radius : float
                Coverage Range of the outlet.
            interference : float
                The amount of attenuation emitted from the environment.

            """
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.data_rate = data_rate
        self.radius = radius
        self.interference = interference

    @abstractmethod
    def propagation_range(self):
        """ calculate wave propagation """
        pass

    def calculate_data_rate(self):
        """ calculate downlink and uplink"""
        pass
