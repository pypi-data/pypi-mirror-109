import numpy as np
import csv


class Firm:
    def __init__(self, industry, idx, path, startup_length, burn_in, industry_shocks):
        self.name = 'F'+str(idx)
        self.industry = industry
        self.wallet = None
        self.private_key = None
        self.address = None
        self.contract = None
        self.size = 1
        self.delinquent = False
        self.ma_params = [np.random.uniform(-80, 80)/100 for i in range(np.random.randint(2, 6))]
        self.mu = np.random.uniform()*4
        self.sigma = np.random.uniform()

        cf_series = [np.random.normal(self.mu, self.sigma)]
        for i in range(1, len(self.ma_params) + startup_length):
            cf_series.append(np.random.normal(self.mu, self.sigma) +
                             sum([cf_series[j]*self.ma_params[j] for j in range(min(i, len(self.ma_params)))]) +
                             industry_shocks[self.industry][i])
        cf_series = cf_series[burn_in:]
        with open(path + '/cash_flows/' + self.name + '.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['period', 'cash_flow'])
            for i in range(len(cf_series)):
                w.writerow([i - len(cf_series), cf_series[i]])

        self.prior_cf = cf_series[-len(self.ma_params):]

    def name_firm(self, rw, name_list):
        while self.name is None or self.name in name_list:
            self.name = ' '.join([rw.word(include_parts_of_speech=["adjectives"]).capitalize(),
                                  rw.word(include_parts_of_speech=["nouns"]).capitalize(),
                                  np.random.choice(['Co.', 'Inc.', 'Ltd.', 'LLC',
                                                    'Company', 'Incorporated', 'Stores', ''])]
                                 ).strip()

    def change_address(self, building_address):
        self.address = building_address

    def get_stats(self):
        return [self.name, self.industry]

    def increment_cash(self, industry_shocks):
        cf = np.random.normal(self.mu, self.sigma) + sum([self.prior_cf[j]*self.ma_params[j]
                                                          for j in range(len(self.ma_params))] +
                                                         industry_shocks[self.industry])
        self.prior_cf.pop(0)
        self.prior_cf.append(cf)
        return cf

    @staticmethod
    def select_winning_bid(bids, discount_rate):
        if len(bids) == 0:
            return None, None
        bid_npv = {}
        max_contract_length = max([contract.periods for contract in bids.values()])
        median_rent = np.median([contract.rent for contract in bids.values()])
        for player, contract in bids.items():
            npv = 0
            for period in range(contract.periods):
                npv += contract.rent / (1 + discount_rate) ** period
            for period in range(contract.periods, max_contract_length):
                npv += median_rent / (1 + discount_rate) ** period  # TODO: smarter expected renewal rent
            bid_npv.update({player: npv})
        # winning bid is the lowest cost
        bid_npv = dict(sorted(bid_npv.items(), key=lambda item: item[1], reverse=True))
        winning_player = [k for k in bid_npv.keys()][0]
        return [winning_player, bids[winning_player]]
