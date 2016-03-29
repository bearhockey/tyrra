class Component(object):
    def __init__(self, component_type, name, stats=None):
        self.name = name
        self.component_type = component_type
        self.stats = stats or {}
