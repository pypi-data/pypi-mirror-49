#!/usr/bin/python3

from .web3 import Web3
from .rpc import Rpc
from .account import Accounts
from brownie._config import CONFIG, modify_network_config

rpc = Rpc()
web3 = Web3()


def connect(network=None):
    '''Connects to the network.

    Args:
        network: string of of the name of the network to connect to

    Network information is retrieved from brownie-config.json'''
    if is_connected():
        raise ConnectionError(f"Already connected to network '{CONFIG['active_network']['name']}'")
    try:
        modify_network_config(network or CONFIG['network_defaults']['name'])
        if 'host' not in CONFIG['active_network']:
            raise KeyError(
                f"No host in brownie-config.json for network '{CONFIG['active_network']['name']}'"
            )
        web3.connect(CONFIG['active_network']['host'])
        if 'test-rpc' in CONFIG['active_network'] and not rpc.is_active():
            if is_connected():
                if web3.eth.blockNumber != 0:
                    raise ValueError("Local RPC Client has a block height > 0")
                rpc.attach(CONFIG['active_network']['host'])
            else:
                rpc.launch(CONFIG['active_network']['test-rpc'])
        else:
            Accounts()._reset()
    except Exception:
        CONFIG['active_network'] = {'name': None}
        web3.disconnect()
        raise


def disconnect():
    '''Disconnects from the network.'''
    if not is_connected():
        raise ConnectionError("Not connected to any network")
    CONFIG['active_network'] = {'name': None}
    web3.disconnect()
    if rpc.is_active():
        if rpc.is_child():
            rpc.kill()
        else:
            rpc.reset()


def show_active():
    '''Returns the name of the currently active network'''
    if not web3.providers:
        return None
    return CONFIG['active_network']['name']


def is_connected():
    '''Returns a bool indicating if the Web3 object is currently connected'''
    return web3.isConnected()


def gas_limit(*args):
    '''Displays or modifies the default gas limit.

    * If no argument is given, the current default is displayed.
    * If an integer value is given, this will be the default gas limit.
    * If set to "auto", None, True or False, the gas limit is determined
    automatically.'''
    if not is_connected():
        raise ConnectionError("Not connected to any network")
    if args:
        if args[0] in ("auto", None, False, True):
            CONFIG['active_network']['gas_limit'] = False
        else:
            try:
                limit = int(args[0])
            except ValueError:
                raise TypeError(f"Invalid gas limit '{args[0]}'")
            if limit < 21000:
                raise ValueError("Minimum gas limit is 21000")
            CONFIG['active_network']['gas_limit'] = limit
    return f"Gas limit is set to {CONFIG['active_network']['gas_limit'] or 'automatic'}"
