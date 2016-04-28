class Component(object):
    def __init__(self, component_type, name, stats=None):
        self.name = name
        self.component_type = component_type
        self.stats = stats or {}

    def component_dict(self):
        return {"NAME": self.name, "TYPE": self.component_type, "STATS": self.stats}
