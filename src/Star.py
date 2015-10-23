class Star(object):
    def __init__(self, radius=10, luminosity=128, temperature=128):
        self.radius = radius
        self.luminosity = luminosity
        self.temperature = temperature

        self.satellites = []

    def get_color(self):
        r = 255 - self.temperature
        b = self.luminosity
        g = max((self.temperature + self.luminosity) / 2, 128)

        return r, g, b

