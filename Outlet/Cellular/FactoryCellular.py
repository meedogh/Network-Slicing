from Utils.config import outlet_types
from .FiveG import FiveG
from .FourG import FourG
from .SubSixG import SubSixG
from .ThreeG import ThreeG
from .Wifi import Wifi


class FactoryCellular:
    """
        the factory will create objects from different outlet types for the same abstract class at runtime


        """
    def __init__(self, *args):

        """

            Parameters
            ----------
            three_gen : ThreeG
            outlet object from type ThreeG.
            four_gen : FourG(Object)
            outlet object from type FourG.
            five_gen : FiveG(Object)
            outlet object from type FiveG
            sub_six : SubSixG(Object)
            outlet object from type Sub_Six.
            _wifi : Wifi(Object)
            outlet object from type Wifi.
            cellular_dict : dictionary
            dictionary has the types of all outlets as keys and the values are the objects types.

                    """
        self.three_gen = ThreeG(*args)
        self.four_gen = FourG(*args)
        self.five_gen = FiveG(*args)
        self.sub_six = SubSixG(*args)
        self.wifi = Wifi(*args)
        self.cellular_dict = {'3G': self.three_gen,
                              '4G': self.four_gen,
                              '5G': self.five_gen,
                              'Sub6G': self.sub_six,
                              'wifi': self.wifi}

    def produce_cellular_outlet(self, product):
        """Returns
            -------
            object of type outlet
               will compare if the type of outlet is in the dictionary then return the object from this type."""
        if product in self.cellular_dict:
            return self.cellular_dict[product]
        raise Exception(f'{product} factory not available at the moment!')
