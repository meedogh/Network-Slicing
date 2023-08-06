from Outlet.Cellular.ICellular import Cellular


class ThreeG(Cellular):
    """
    outlet from type 3G
    """

    def calculate_coverage_area(self):
        """Returns
            -------
            float
            The coverage area that the tower will response the requests in it."""
        print(",,,,,,,,,,,,",self.coms.calculate_data_rate())

    def calculate_downlink(self):
        """Returns
            -------
            float
            The downlink that the tower will use it for responsing the requests ."""
        return 2


