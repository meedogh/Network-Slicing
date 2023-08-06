from Outlet.Cellular.ICellular import Cellular


class FourG(Cellular):
    """
    outlet from type 4G
    """
    def calculate_coverage_area(self):
        """Returns
            -------
            float
            The coverage area that the tower will response the requests in it."""
        return 1

    def calculate_downlink(self):
        """Returns
            -------
            float
            The downlink that the tower will use it for responsing the requests ."""
        return 2
