from Environment.env_variables import outlet_radius


class Observer:
    def update(self, subject):
        pass


class ConcreteObserver(Observer):
    def __init__(self, outlet_pos, outlets):
        self.outlet_radius = outlet_radius
        self.outlet_pos = outlet_pos
        self.outlets = outlets



    def check(self, subject):
        def check_radius(outlet):



            if (outlet.position[0] - outlet.radius) <= subject.x <= (
                    outlet.position[0] + outlet.radius
            ) and (outlet.position[1] - outlet.radius) <= subject.y <= (
                    outlet.position[1] + outlet.radius
            ):
                return outlet


        subject.outlets_serve = list(map(lambda outlet: check_radius(outlet), self.outlets))
        subject.outlets_serve = list(filter(lambda x: x is not None, subject.outlets_serve))


    def update(self, subject):
        self.check(subject)
