import numpy as np


class Building:
    def __init__(self, address, size, idx):
        self.name = 'B'+str(idx)
        self.address = address
        self.size = size
        self.firms = []
        self.player = None

    def name_building(self, rw, name_list):
        while self.name is None or self.name in name_list:
            self.name = ' '.join([rw.word(include_parts_of_speech=["verbs"]).capitalize(),
                                  np.random.choice(['Towers', 'Building', 'Bldg', 'Place', ''])]
                                 ).strip()

    def get_stats(self):
        return [firm.get_stats() + [firm.contract.rent, firm.contract.periods, firm.wallet] for firm in self.firms]

    def get_discounted_value(self, discount_rate):
        ecf = 0
        for firm in self.firms:
            for period in range(firm.contract.periods):
                ecf += firm.contract.rent / (1 + discount_rate) ** period
        return ecf

    def get_size(self):
        return sum([firm.size for firm in self.firms])

    @staticmethod
    def select_winning_bid(bids):
        if len(bids) == 0:
            return None, None
        bids = dict(sorted(bids.items(), key=lambda item: item[1], reverse=True))
        return [[k, v] for k, v in bids.items()][0]
