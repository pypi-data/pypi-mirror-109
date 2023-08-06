"""
    Inherited object to allow library interaction with a Blankly bot
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from multiprocessing import Process, Manager
import Blankly
import copy
import warnings

from Blankly.exchanges.orderbook_manager import OrderbookManger
from Blankly.exchanges.ticker_manager import TickerManager
from Blankly.interface.abc_currency_interface import ICurrencyInterface
from Blankly.exchanges.Coinbase_Pro.Coinbase_Pro_API import API as Coinbase_Pro_API
from binance.client import Client as Binance_API


class BlanklyBot:
    currency_pair: str
    user_preferences: dict
    exchange_type: str
    initial_state: dict
    # Define the given types for the user
    Orderbook_Manager: OrderbookManger
    Ticker_Manager: TickerManager
    Interface: ICurrencyInterface
    coinbase_pro_direct: Coinbase_Pro_API
    binance_direct: Binance_API

    def __init__(self):
        """
        Initialize state variables when the bot is created
        """
        # If the start is called again, this will make sure multiple processes don't start
        self.__state = {}
        self.coin = ""
        self.exchange_type = ""
        self.initial_state = {}
        self.user_preferences = {}
        self.currency_pair = ""
        self.direct_calls = None
        self.process = Process(target=self.setup_process)

    def setup(self, exchange_type, currency_pair, user_preferences, initial_state, interface):
        """
        This function is populated by the exchange.
        Args:
            exchange_type (str): Type of exchange i.e "binance" or "coinbase_pro"
            currency_pair: Identifier for the coin market, i.e "BTC-USD"
            user_preferences: Dictionary with the defined preferences
            initial_state: Information about the account the model is defaulted to running on
            interface: Object for consistent trading on the supported exchanges
        """
        # Shared variables with the processing a manager
        self.initial_state = initial_state
        self.__state = Manager().dict({})
        self.exchange_type = exchange_type
        self.user_preferences = user_preferences
        self.Interface = copy.deepcopy(interface)
        # Coin id is the currency and which market its on
        self.currency_pair = currency_pair
        self.direct_calls = interface.get_calls()
        self.coinbase_pro_direct = self.direct_calls
        self.binance_direct = self.direct_calls

    def is_running(self):
        """
        This function returns the status of the process. This ensures that two processes cannot be started on the same
        account.
        """
        return self.process.is_alive()

    def run(self, args):
        """
        Called when the user starts the model. This is what begins and manages the process.
        """
        # Start the setup process and then call the main
        p = Process(target=self.setup_process, args=(args,))
        self.process = p
        self.process.start()

    def setup_process(self, args):
        """
        Create any objects that need to be process-specific in the other process
        """
        self.Ticker_Manager = Blankly.TickerManager(self.exchange_type, self.currency_pair)
        self.Orderbook_Manager = Blankly.OrderbookManager(self.exchange_type, self.currency_pair)
        self.main(args)

    """
    State getters and setters for external understanding of the operation
    """
    def get_state(self):
        try:
            return self.__state.copy()
        except BrokenPipeError:
            raise BrokenPipeError("Broken Pipe. Is the main process still running?")

    def update_state(self, key, value):
        """
        This function adds or removes state values from the state dictionary
        Args:
            key: The key value to be added/changed
            value: The value the key should be set to
        """
        self.__state[key] = value

    def remove_key(self, key):
        """
        This function removes a key from the state variable
        Args:
            key: This specifies the key value to remove from the state dictionary
        """
        self.__state.pop(key)

    def main(self, args):
        warnings.warn("No user-created main function to run, stopping...")
