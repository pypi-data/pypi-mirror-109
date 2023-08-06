from eth_utils import to_wei, from_wei
from eth_tester import EthereumTester, PyEVMBackend


class Bank(EthereumTester):
    def __init__(self, wallet_amount):
        genesis_overrides = {'gas_limit': 4500000, 'difficulty': 1}
        custom_genesis_params = PyEVMBackend._generate_genesis_params(overrides=genesis_overrides)
        state_overrides = {'balance': to_wei(wallet_amount, 'ether')}
        # 1 account is the default, use line below to instantiate with multiple accounts
        custom_genesis_state = PyEVMBackend._generate_genesis_state(overrides=state_overrides, num_accounts=1)
        backend = PyEVMBackend(genesis_parameters=custom_genesis_params, genesis_state=custom_genesis_state)
        super().__init__(backend=backend, auto_mine_transactions=True)