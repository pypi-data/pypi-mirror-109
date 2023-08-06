import warnings

from Blankly.utils import utils as utils
from Blankly.exchanges.Alpaca.Alpaca_API import API
from Blankly.interface.currency_Interface import CurrencyInterface
import alpaca_trade_api

from Blankly.utils.purchases.limit_order import LimitOrder
from Blankly.utils.purchases.market_order import MarketOrder

class AlpacaInterface(CurrencyInterface):
    def __init__(self, authenticated_API: API, preferences_path: str):
        super().__init__('alpaca', authenticated_API, preferences_path)
        assert isinstance(self.calls, alpaca_trade_api.REST)

    def init_exchange(self):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        account_info = self.calls.get_account()
        try:
            if account_info['account_blocked']:
                warnings.warn('Your alpaca account is indicated as blocked for trading....')
        except KeyError:
            raise LookupError("Alpaca API call failed")

        self.__exchange_properties = {
            "maker_fee_rate": 0,
            "taker_fee_rate": 0
        }

    def get_products(self) -> dict:
        '''
        [
            {
              "id": "904837e3-3b76-47ec-b432-046db621571b",
              "class": "us_equity",
              "exchange": "NASDAQ",
              "symbol": "AAPL",
              "status": "active",
              "tradable": true,
              "marginable": true,
              "shortable": true,
              "easy_to_borrow": true,
              "fractionable": true
            },
            ...
        ]
        '''
        needed = self.needed['get_products']
        assets = self.calls.list_assets(status=None, asset_class=None)

        for asset in assets:
            asset['currency_id'] = asset.pop('id')
            asset['base_currency'] = asset.pop('symbol')
            asset['quote_currency'] = 'usd'
            asset['base_min_size'] = -1
            asset['base_max_size'] = -1
            asset['base_increment'] = -1

        for i in range(len(assets)):
            assets[i] = utils.isolate_specific(needed, assets[i])

        return assets

    def get_account(self, currency=None, override_paper_trading=False):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        needed = self.needed['get_account']

        account_dict = self.calls.get_account()
        account_dict['available'] = account_dict.pop('cash')
        account_dict['hold'] = -1

        positions = self.calls.list_positions()
        for position in positions:
            position['currency'] = position.pop('symbol')
            position['available'] = position.pop('qty')
            position['hold'] = -1

        positions.append(account_dict)

        for i in range(len(positions)):
            positions[i] = utils.isolate_specific(needed, positions[i])

        return positions

    def market_order(self, product_id, side, funds) -> MarketOrder:
        assert isinstance(self.calls, alpaca_trade_api.REST)
        needed = self.needed['market_order']

        order = {
            'funds': funds,
            'side': side,
            'product_id': product_id,
            'type': 'market'
        }
        response = self.calls.submit_order(product_id, side=side, type='market', time_int_force='day', notional=funds)
        response = utils.isolate_specific(needed, response)
        return MarketOrder(order, response, self)

    def limit_order(self, product_id, side, price, size) -> LimitOrder:
        pass

    def cancel_order(self, currency_id, order_id) -> dict:
        assert isinstance(self.calls, alpaca_trade_api.REST)
        self.calls.cancel_order(order_id)

        #TODO: handle the different response codes
        return {'order_id': order_id}

    # TODO: this doesnt exactly fit
    def get_open_orders(self, product_id=None):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        needed = self.needed['get_open_orders']
        orders = self.calls.list_orders()
        renames = [
            ["asset_id", "product_id"],
            ["filled_at", "price"],
            ["qty", "size"],
            ["notional", "funds"]
        ]
        for order in orders:
            order = utils.rename_to(renames, order)
            order = utils.isolate_specific(needed, order)
        return orders

    def get_order(self, currency_id, order_id) -> dict:
        assert isinstance(self.calls, alpaca_trade_api.REST)
        needed = self.needed['get_order']
        order = self.calls.get_order(order_id)
        renames = [
            ["asset_id", "product_id"],
            ["filled_at", "price"],
            ["qty", "size"],
            ["notional", "funds"]
        ]
        order = utils.rename_to(renames, order)
        order = utils.isolate_specific(needed, order)
        return order

    def get_fees(self):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        return {
            'maker_fee_rate': 0,
            'taker_fee_rate': 0
        }

    def get_product_history(self, product_id, epoch_start, epoch_stop, granularity):
        assert isinstance(self.calls, alpaca_trade_api.REST)

        pass

    # TODO: tbh not sure how this one works
    def get_market_limits(self, product_id):
        assert isinstance(self.calls, alpaca_trade_api.REST)
        pass

    def get_price(self, currency_pair) -> float:
        assert isinstance(self.calls, alpaca_trade_api.REST)
        response = self.calls.get_last_trade()
        return float(response['p'])