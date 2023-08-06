import os
import csv
import numpy as np
import pandas as pd
from datetime import datetime
import secrets
import pickle
from eth_utils import to_wei, from_wei
from ether_real_estate.building import Building
from ether_real_estate.firm import Firm
from ether_real_estate.player import Player
from ether_real_estate.bank import Bank
from ether_real_estate.contract import Contract


class Game:
    def __init__(self, num_industry=5, num_players=5, num_ai=0, verbose=False, game_path='', reload=False
                 # building_min_size=5, building_max_size=20,
                 ):

        if reload:
            with open(game_path + '/game.pkl', 'rb') as f:
                game_data = pickle.load(f)
                self.period = game_data[0]
                self.verbose = game_data[1]
                self.discount_rate = game_data[2]
                self.tax_rate = game_data[3]
                self.property_tax_rate = game_data[4]
                self.buildings = game_data[5]
                self.building_names = game_data[6]
                self.occupancy = game_data[7]
                self.firms = game_data[8]
                self.firm_names = game_data[9]
                self.players = game_data[10]
                self.player_names = game_data[11]
                self.ai = game_data[12]
                self.money_supply = game_data[13]
                self.banker_private_key = game_data[14]
                receipts = game_data[15]
                self.path = game_data[16]
                self.size_increment = game_data[17]
                self.num_industry = game_data[18]
            self.bank = Bank(wallet_amount=1000000)
            self.bank.add_account(self.banker_private_key)
            self.banker_wallet = self.bank.get_accounts()[1]
            self.send_transaction(self.bank.get_accounts()[0], self.banker_wallet, self.money_supply,
                                  collect_receipt=False)
            for player in self.players:
                self.bank.add_account(player.private_key)
            for firm in self.firms:
                self.bank.add_account(firm.private_key)
            self.receipts = []
            for head, tail, amount in receipts:
                self.send_transaction(head, tail, amount)

        else:
            if game_path == '':
                print('No path for game data has been specified.')
                game_path = input('Please specify path for save data now, or leave blank for the default: ')
                while game_path != '' and not os.path.exists(game_path):
                    game_path = input('Path specified does not exist.  Please specify path for save data now, or leave '
                                      'blank for the default: ')
                if game_path == '':
                    game_path = os.path.dirname(os.getcwd())\
                                + '/'\
                                + str(datetime.now().year) + '-'\
                                + str(datetime.now().month) + '-'\
                                + str(datetime.now().day) + '_'\
                                + str(datetime.now().hour) + ':'\
                                + str(datetime.now().minute)
                    print('Using the default game path:', game_path)

            building_n = (num_players+num_ai) * 3
            os.mkdir(game_path)
            os.mkdir(game_path + '/building_bids')
            os.mkdir(game_path + '/firm_bids')
            os.mkdir(game_path + '/building_bids/0')
            os.mkdir(game_path + '/firm_bids/0')
            os.mkdir(game_path + '/stats')
            os.mkdir(game_path + '/stats/0')
            os.mkdir(game_path + '/blocks/')
            os.mkdir(game_path + '/blocks/0')
            os.mkdir(game_path + '/cash_flows/')
            self.period = 0
            self.path = game_path
            self.verbose = verbose
            self.discount_rate = 0.02
            self.tax_rate = 0.4
            self.property_tax_rate = 0.08
            self.buildings = [Building(address=i,
                                       size=20, # np.random.randint(building_min_size, building_max_size),
                                       idx=i)
                              for i in range(building_n)]
            self.building_names = {b.name: b for b in self.buildings}
            self.occupancy = sum([b.size for b in self.buildings])
            # create firms
            self.num_industry = num_industry
            startup_length = 150
            burn_in = 50
            industry_shocks = [np.random.normal(0, 1, startup_length+burn_in) for _ in range(self.num_industry)]
            self.firms = [Firm(industry=(i % self.num_industry),
                               idx=i,
                               path=self.path,
                               startup_length=startup_length,
                               burn_in=burn_in,
                               industry_shocks=industry_shocks)
                          for i in range(int(self.occupancy * 1.2))]
            self.firm_names = {f.name: f for f in self.firms}
            # populate all buildings to ~90% occupancy
            firm_idx = 0
            for building in self.buildings:
                while building.get_size() < 0.9 * building.size:
                    firm = self.firms[firm_idx]
                    if firm.size < building.size - building.get_size():
                        firm.change_address(building_address=building.address)
                        building.firms.append(firm)
                        firm_idx += 1
                    else:
                        break
            del firm_idx
            # create contracts for occupied firms
            for firm in self.firms:
                if firm.address is None:
                    continue
                firm.contract = Contract(rent=np.random.randint(3, 6), periods=np.random.randint(2, 4))
            median_building_value = np.median([building.get_discounted_value(self.discount_rate)
                                               for building in self.buildings])
            # every unit of size_increment cash holdings, firm size goes up
            self.size_increment = 5
            # create players
            self.players = [Player(str(i)) for i in range(num_players+num_ai)]
            self.player_names = {p.name: p for p in self.players}  # if names later set by players, ensure unique
            # instantiate blockchain
            self.money_supply = 1000000
            self.bank = Bank(wallet_amount=self.money_supply)
            private_keys = [secrets.token_hex(32)]
            self.banker_private_key = private_keys[0]
            self.bank.add_account(self.banker_private_key)
            self.banker_wallet = self.bank.get_accounts()[1]
            self.send_transaction(self.bank.get_accounts()[0], self.banker_wallet, self.money_supply,
                                  collect_receipt=False)
            self.receipts = []
            filter_id = self.bank.create_block_filter()
            for i in range(len(self.players) + len(self.firms)):
                private_key = secrets.token_hex(32)
                while private_key in private_keys:  # shouldn't really need to worry about this
                    private_key = secrets.token_hex(32)
                private_keys.append(private_key)
                account = self.bank.add_account(private_key)  # this is slow
                if i < len(self.players):
                    player = self.players[i]
                    player.wallet = account
                    player.private_key = private_key
                    starting_balance = median_building_value * 3
                else:
                    firm = self.firms[i - len(self.players)]
                    firm.wallet = account
                    firm.private_key = private_key
                    # give an initial amount of cash to each firm
                    if firm.address is None:
                        starting_balance = np.random.randint(2, 6)
                    else:
                        starting_balance = np.random.randint(firm.contract.rent, firm.contract.rent + 1)
                self.send_transaction(self.banker_wallet, account, starting_balance)
            if self.verbose:
                print('Starting deposit transactions:', self.bank.get_all_filter_logs(filter_id))
            self.bank.delete_filter(filter_id)
            self.ai = [i for i in range(num_players,num_players+num_ai)]
            # flag whether to run the game on autopilot
            self.save_game()

    def get_balance(self, account):
        return float(from_wei(self.bank.get_balance(account), 'ether'))

    def send_transaction(self, head, tail, amount, collect_receipt=True):
        try:
            transaction = {'from': head,
                           'to': tail,
                           'gas': 4500000,
                           'gas_price': 0,
                           'value': to_wei(amount, 'ether')}
            self.bank.call(transaction)
            _transaction_hash = self.bank.send_transaction(transaction)
            if collect_receipt:
                self.receipts.append([head, tail, amount])
        except Exception as e:
            print(e,
                  '\n\t head balance:', self.get_balance(head),
                  '\n\t tail balance:', self.get_balance(tail),
                  '\n\t transaction amount:', amount)
            raise Exception('Send Transaction Error')
        # gas_used = self.bank.estimate_gas(transaction)
        # print(self.bank.get_block_by_hash(self.bank.get_transaction_receipt(transaction_hash)['block_hash']))

    def get_building_stats(self):
        stats = {building: building.get_stats() for building in self.buildings}
        df = pd.DataFrame(columns=['building', 'size', 'firm', 'industry', 'rent', 'maturity', 'cash_holdings'])
        for building, data in stats.items():
            for firm_data in data:
                wallet = firm_data.pop()
                df.loc[len(df.index)] = [building.name, building.size] + firm_data + [self.get_balance(wallet)]
        df.to_csv(self.path + '/stats/' + str(self.period) + '/buildings.csv', index=False)

    def get_unassigned_firm_stats(self):
        df = pd.DataFrame(columns=['firm', 'industry', 'cash_holdings'])
        for firm in self.firms:
            if firm.address is not None:
                continue
            df.loc[len(df.index)] = firm.get_stats() + [self.get_balance(firm.wallet)]
        df.to_csv(self.path + '/stats/' + str(self.period) + '/unassigned_firms.csv', index=False)

    def get_stats(self):
        self.get_building_stats()
        self.get_unassigned_firm_stats()

    def get_building_bids_ai(self, buildings):
        bids = {building: {} for building in buildings}  # <building> : { <player>: <bid amount> }
        ecf = {building: building.get_discounted_value(self.discount_rate) for building in buildings}
        for player in [self.players[i] for i in self.ai]:
            if len(buildings) == 1:
                building_choices = [0]
            else:
                building_choices = np.random.choice(len(buildings), size=len(buildings), replace=False)
            cash = self.get_balance(player.wallet)
            for building_index in building_choices:
                building = buildings[building_index]
                bid = ecf[building] * (1 + np.random.normal(0, 0.05))
                if bid >= cash:
                    continue
                bids[building].update({player: bid})
                cash -= bid
        # write to csv
        for player in self.players:
            df = pd.DataFrame(columns=['id', 'bid'])
            for building in buildings:
                if player in bids[building].keys():
                    df.loc[len(df.index)] = [building.name, bids[building][player]]
            if len(df.index) == 0:
                continue
            df.to_csv(self.path + '/building_bids/' + str(self.period) + '/' + str(player.name) + '.csv',
                      index=False, header=False)

    def get_building_bids(self):
        buildings = [b for b in self.buildings if b.player is None]
        if len(buildings) == 0:
            return
        if self.ai:
            self.get_building_bids_ai(buildings=buildings)
        # read bids from csv
        bids = {building: {} for building in buildings}  # <building> : { <player>: <bid amount> }
        for name in os.listdir(self.path + '/building_bids/' + str(self.period)):
            # CSV file expects: filename = player ID, columns = [building ID, bid params]
            df = pd.read_csv(self.path + '/building_bids/' + str(self.period) + '/' + name, header=None)
            player_id = name[:name.find('.csv')].strip().lower()
            if player_id in self.player_names.keys():
                player = self.player_names[player_id]
                for i in range(len(df.index)):
                    building_name, bid = df.iloc[i]
                    building_name = building_name.strip().upper()
                    if building_name in self.building_names.keys():
                        bids[self.building_names[building_name]].update({player: bid})
        # submit each bid to each firm
        for building in buildings:
            player, winning_bid = building.select_winning_bid(bids=bids[building])
            if player is None:
                continue
            building.player = player
            player.properties.append(building)
            self.send_transaction(player.wallet, self.banker_wallet, winning_bid)
        if self.verbose:
            print('\t Property acquisition completed:')
            for player in self.players:
                print('\t player:', player.name,
                      'eth:', self.get_balance(player.wallet),
                      'properties:', [b.name for b in player.properties])

    def increment_cash(self):
        industry_shocks = np.random.normal(0, 1, self.num_industry)
        for firm in self.firms:
            cash_flow = firm.increment_cash(industry_shocks=industry_shocks)
            with open(self.path + '/cash_flows/' + firm.name + '.csv', 'a', newline='') as f:
                w = csv.writer(f)
                w.writerow([self.period, cash_flow])
            if cash_flow < 0:
                if self.get_balance(firm.wallet) > 1e-5:
                    self.send_transaction(firm.wallet, self.banker_wallet,
                                          amount=min(cash_flow*-1, self.get_balance(firm.wallet)-1e-5))
            else:
                self.send_transaction(self.banker_wallet, firm.wallet, amount=cash_flow)

    def pay_rent(self):
        # self.get_balance(account)
        for building in self.buildings:
            player = building.player
            if player is None:
                continue
            for firm in building.firms:
                firm.contract.periods -= 1
                rent = firm.contract.rent
                if self.get_balance(firm.wallet) >= rent:
                    self.send_transaction(firm.wallet, player.wallet, rent)
                else:
                    firm.delinquent = True
        if self.verbose:
            print('\t Collected rent:')
            for player in self.players:
                print('\t player:', player.name, 'eth:', self.get_balance(player.wallet))

    def evict(self):
        for building in self.buildings:
            for firm in building.firms:
                if firm.delinquent or (firm.contract is not None and firm.contract.periods == 0):
                    firm.delinquent = False
                    firm.address = None
                    firm.contract = None
                    building.firms = [f for f in building.firms if f.name != firm.name]

    def get_firm_bids_ai(self, firms):
        bids = {firm: {} for firm in firms}  # <firm> : { <player>: Contract }
        for player in [self.players[i] for i in self.ai]:
            for firm in np.random.choice(firms, len(firms), replace=False):
                bids[firm].update({player: Contract(rent=np.random.randint(3, 6),
                                                    periods=np.random.randint(2, 4))})
        # write to csv
        for player in self.players:
            df = pd.DataFrame(columns=['id', 'rent', 'periods'])
            for firm in firms:
                if player in bids[firm].keys():
                    df.loc[len(df.index)] = [firm.name, bids[firm][player].rent, bids[firm][player].periods]
            if len(df.index) == 0:
                continue
            df.to_csv(self.path + '/firm_bids/' + str(self.period) + '/' + str(player.name) + '.csv',
                      index=False, header=False)
        return None

    def get_firm_bids(self):
        firms = [f for f in self.firms if f.address is None]
        if self.ai:
            self.get_firm_bids_ai(firms=firms)
        # get bids from csv
        bids = {firm: {} for firm in firms}  # <firm> : { <player>: Contract }
        for name in os.listdir(self.path + '/firm_bids/' + str(self.period)):
            # CSV file expects: filename = player ID, columns = [firm ID, bid params]
            df = pd.read_csv(self.path + '/firm_bids/' + str(self.period) + '/' + name, header=None)
            player_id = name[:name.find('.csv')].strip().lower()
            if player_id in self.player_names.keys():
                player = self.player_names[player_id]
                for i in range(len(df.index)):
                    firm_name, rent, periods = df.iloc[i]
                    firm_name = firm_name.strip().upper()
                    if firm_name in self.firm_names.keys():
                        bids[self.firm_names[firm_name]].update({player: Contract(rent=float(rent),
                                                                                  periods=int(periods))})
        # assign wining bids
        for firm in firms:
            players_with_space = [p for p in self.players if
                                  max([b.size >= b.get_size() + firm.size for b in p.properties] + [False])]
            remove_players = [p for p in self.players if p not in players_with_space]
            for player in remove_players:
                del bids[firm][player]
            player, contract = firm.select_winning_bid(bids[firm], self.discount_rate)
            if player is None:
                continue
            building_list = [b for b in player.properties if b.size >= b.get_size() + firm.size]
            building = building_list[np.random.choice(len(building_list))]
            firm.contract = contract
            firm.address = building.address
            building.firms.append(firm)

    def update_firm_sizes(self):
        firms_grew = []
        for firm in self.firms:
            old_size = firm.size
            new_size = int(self.get_balance(firm.wallet)/self.size_increment)+1
            if new_size > old_size:
                firms_grew.append(firm)
            firm.size = new_size
        for building in self.buildings:
            while sum([firm.size for firm in building.firms]) > building.size:
                # randomly remove a grown firm until building occupancy is within its limit
                firm = np.random.choice([firm for firm in building.firms if firm in firms_grew])
                firm.address = None
                firm.contract = None
                building.firms = [f for f in building.firms if f.name != firm.name]

    def fill_unowned_buildings(self):
        buildings = [b for b in self.buildings if b.player is None]
        firms = [f for f in self.firms if f.address is None]
        for building in buildings:
            if self.verbose:
                print('filling building', building.name)
            while building.get_size() / building.size < 0.9:
                firm_choice = np.random.choice(len(firms))
                firm = firms[firm_choice]
                if self.verbose:
                    print(building.get_size(), building.size, len(firms))
                    print(firm_choice, firm, firm.size)
                if firm.size <= building.size - building.get_size():
                    firm.address = building
                    firm.contract = Contract(rent=np.random.randint(3, 6),
                                             periods=np.random.randint(2, 4))
                    building.firms.append(firm)

    def pay_taxes(self, taxable_transactions):
        # get taxable income from rent
        blocks = self.bank.get_all_filter_logs(taxable_transactions)
        tax_base = {player: 0 for player in self.players}
        player_lookup = {player.wallet: player for player in self.players}
        for block in blocks:
            transactions = self.bank.get_block_by_hash(block)['transactions']
            for transaction in transactions:
                txn = self.bank.get_transaction_by_hash(transaction)
                txn_from = txn['from']
                txn_to = txn['to']
                txn_value = txn['value']
                if txn_from in player_lookup.keys():
                    tax_base[player_lookup[txn_from]] -= txn_value
                elif txn_to in player_lookup.keys():
                    tax_base[player_lookup[txn_to]] += txn_value
        # each player pays tax on rental profit (net of building acquisitions) and real estate
        for player in self.players:
            rental_income_tax = tax_base[player] * self.property_tax_rate
            if 0 < rental_income_tax <= self.get_balance(player.wallet):
                self.send_transaction(player.wallet, self.banker_wallet, rental_income_tax)
            properties = {building: building.get_discounted_value(self.discount_rate) for building in player.properties}
            properties = dict(sorted(properties.items(), key=lambda item: item[1], reverse=True))
            for building, property_value in properties.items():
                property_tax = property_value * self.property_tax_rate
                if property_tax > self.get_balance(player.wallet):
                    building.player = None
                    player.properties = [p for p in player.properties if p != building]
                    continue
                self.send_transaction(player.wallet, self.banker_wallet, property_tax)
        if self.verbose:
            print('\t End of stage:')
            for player in self.players:
                print('\t player:', player.name, 'eth:', self.get_balance(player.wallet))
                for building in player.properties:
                    print('\t\t', building.name, [f.name for f in building.firms],
                          building.get_size(), building.size)

    def write_blocks(self, blocks):
        df = pd.DataFrame(columns=['block', 'from', 'to', 'value'])
        for block in self.bank.get_all_filter_logs(blocks):
            transactions = self.bank.get_block_by_hash(block)['transactions']
            for transaction in transactions:
                txn = self.bank.get_transaction_by_hash(transaction)
                block = txn['block_number']
                txn_from = txn['from']
                txn_to = txn['to']
                txn_value = from_wei(txn['value'], 'ether')
                df.loc[len(df.index)] = [block, txn_from, txn_to, txn_value]
        df.to_csv(self.path + '/blocks/' + str(self.period) + '/blocks.csv', index=False)

    def increment_game(self, last_period=False):
        blocks = self.bank.create_block_filter()
        self.increment_cash()
        taxable_transactions = self.bank.create_block_filter()
        self.pay_rent()
        self.pay_taxes(taxable_transactions)
        self.write_blocks(blocks)
        if not last_period:
            self.evict()
            self.update_firm_sizes()
            self.fill_unowned_buildings()
            self.period += 1
            os.mkdir(self.path + '/building_bids/' + str(self.period))
            os.mkdir(self.path + '/firm_bids/' + str(self.period))
            os.mkdir(self.path + '/stats/' + str(self.period))
            os.mkdir(self.path + '/blocks/' + str(self.period))

    def save_game(self):
        if self.verbose:
            print('Saving the game')
        with open(self.path + '/game.pkl', 'wb') as f:
            pickle.dump([self.period,
                         self.verbose,
                         self.discount_rate,
                         self.tax_rate,
                         self.property_tax_rate,
                         self.buildings,
                         self.building_names,
                         self.occupancy,
                         self.firms,
                         self.firm_names,
                         self.players,
                         self.player_names,
                         self.ai,
                         self.money_supply,
                         self.banker_private_key,
                         self.receipts,  # this is a bit of a hack, but we can't pickle the Bank object directly
                         self.path,
                         self.size_increment,
                         self.num_industry]
                        , f)


def load_game(game_path=''):
    if game_path == '':
        print('No path for game data has been specified.')
        game_path = input('Please specify path to the save data now.')
        pos = game_path.rfind('game.pkl')
        if pos > -1:
            game_path = game_path[:pos]
        while game_path != '' and not os.path.exists(game_path):
            game_path = input('Path specified does not exist.  Please specify path to the save data now.')
    print('Loading the game at path', game_path)
    g = Game(game_path=game_path, reload=True)
    return g


def sample_ai_game(n=5, num_periods=10):
    print('Running the game with', n, 'ai players for', num_periods, 'periods')
    g = Game(num_players=0, num_ai=n, verbose=True)

    print('Initial building allocation to players')
    g.get_stats()
    g.get_building_bids()
    g.get_firm_bids()

    print('Incrementing game')
    g.save_game()
    path = g.path
    del g
    g = load_game(path)
    for t in range(num_periods):
        print('... period', t)
        last_period = t == num_periods - 1
        g.increment_game(last_period=last_period)
        if not last_period:
            g.get_stats()
            g.get_building_bids()
            g.get_firm_bids()
