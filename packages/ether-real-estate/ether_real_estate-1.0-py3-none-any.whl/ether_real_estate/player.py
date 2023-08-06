class Player:
    def __init__(self, name):
        self.name = 'p' + name
        self.properties = []
        self.discount_rate = 0.02
        self.tax_rate = 0.15
        self.wallet = None
        self.private_key = None
