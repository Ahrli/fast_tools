from .client import Client
from .consts import *


class SwapAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    def get_position(self):
        return self._request_without_params(GET, SWAP_POSITIONS)

    def get_specific_position(self, instrument_id):
        return self._request_without_params(GET, SWAP_POSITION+str(instrument_id) + '/position')

    def get_accounts(self):
        return self._request_without_params(GET, SWAP_ACCOUNTS)

    def get_coin_account(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNT+str(instrument_id)+'/accounts')

    def get_settings(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNTS+'/'+str(instrument_id)+'/settings')

    def set_leverage(self, instrument_id, leverate, side):
        params = {}
        params['leverage'] = leverate
        params['side'] = side
        return self._request_with_params(POST, SWAP_ACCOUNTS+'/'+str(instrument_id)+'/leverage', params)

    def get_ledger(self, instrument_id, froms='', to='', limit=''):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_ACCOUNTS+'/'+str(instrument_id)+'/ledger', params)

    def take_order(self, instrument_id, size, otype, price, client_oid, match_price):
        params = {'instrument_id': instrument_id, 'size': size, 'type': otype, 'price': price}
        if client_oid:
            params['client_oid'] = client_oid
        if match_price:
            params['match_price'] = match_price
        return self._request_with_params(POST, SWAP_ORDER, params)

    def take_orders(self, order_data, instrument_id):
        params = {'instrument_id': instrument_id, 'order_data': order_data}
        return self._request_with_params(POST, SWAP_ORDERS, params)

    def revoke_order(self, order_id='',client_oid='', instrument_id='BTC-USD-SWAP'):
        if(order_id):
            return self._request_without_params(POST, SWAP_CANCEL_ORDER+str(instrument_id)+'/'+str(order_id))
        elif client_oid:
            return self._request_without_params(POST, SWAP_CANCEL_ORDER + str(instrument_id) + '/' + str(client_oid))

    def revoke_orders(self, ids='',client_oids='', instrument_id=''):
        if ids:
            params = {'ids': ids}
        elif client_oids:
            params = {'client_oids':client_oids}
        return self._request_with_params(POST, SWAP_CANCEL_ORDERS+str(instrument_id), params)

    def get_order_list(self, status, instrument_id, froms='', to='', limit=''):
        params = {'status': status}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_ORDERS+'/'+str(instrument_id), params)

    def get_order_info(self, instrument_id='', order_id='',client_oid = ''):
        if order_id:
            return self._request_without_params(GET, SWAP_ORDERS+'/'+str(instrument_id)+'/'+str(order_id))
        elif client_oid:
            return self._request_without_params(GET, SWAP_ORDERS + '/' + str(instrument_id) + '/' + str(client_oid))

    def get_fills(self, order_id='',client_oid='', instrument_id='', froms='', to='', limit=''):
        if order_id:
            params = {'order_id': order_id, 'instrument_id': instrument_id}
        if client_oid:
            params = {'client_oid': client_oid, 'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_FILLS, params)

    def get_instruments(self):
        return self._request_without_params(GET, SWAP_INSTRUMENTS)

    def get_depth(self, instrument_id, size):
        if size:
            params={'size': size}
            return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth', params)
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth')

    def get_ticker(self):
        return self._request_without_params(GET, SWAP_TICKETS)

    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/ticker')

    def get_trades(self, instrument_id, froms='', to='', limit=''):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/trades', params)

    def get_kline(self, instrument_id, granularity, start, end):
        params = {}
        if granularity:
            params['granularity'] = granularity
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/candles', params)

    def get_index(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/index')

    def get_rate(self):
        return self._request_without_params(GET, SWAP_RATE)

    def get_holds(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/open_interest')

    def get_limit(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/price_limit')

    def get_liquidation(self, instrument_id, status, froms='', to='', limit=''):
        params = {'status': status}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/liquidation', params)

    def get_holds_amount(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNTS + '/' + str(instrument_id) + '/holds')

    def get_funding_time(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/funding_time')

    def get_mark_price(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/mark_price')

    def get_historical_funding_rate(self, instrument_id, froms='', to='', limit=''):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/historical_funding_rate', params)
    def order_algo(self,instrument_id='',otype='',order_type='',size='',side='',trigger_price='',algo_price='',callback_rate='',
                   algo_variance='',avg_amount='',limit_price='',sweep_range='',sweep_ratio='',single_limit='',time_interval=''):

        if order_type==1:
            # 止盈止损
            params = {"instrument_id":instrument_id,"type":otype,"order_type":order_type,"size":size, "trigger_price":trigger_price,'algo_price':algo_price,}
        elif order_type==2:
            # 跟踪委托
            params = {"instrument_id":instrument_id,"type":otype,"order_type":order_type,"size":size, "trigger_price":trigger_price,'callback_rate':callback_rate,}
        elif order_type == 3:
        # 跟踪委托
            params = {"instrument_id": instrument_id, "type": otype, "order_type": order_type, "size": size,
                      "algo_variance": algo_variance, 'avg_amount': avg_amount,'limit_price':limit_price }

        elif order_type == 4:
            # 时间加权委托
            params = {"instrument_id": instrument_id, "type": otype, "order_type": order_type, "size": size,
                      "sweep_range": sweep_range, 'sweep_ratio': sweep_ratio, 'single_limit': single_limit,'limit_price':limit_price,'time_interval':time_interval}

        return self._request_with_params(POST, SWAP_ORDER_ALGO, params)

    def cancel_batch_algos(self,instrument_id='',algo_ids='',order_type='',):
        params = {"instrument_id": instrument_id, "algo_ids": algo_ids, "order_type": order_type}
        return self._request_with_params(POST, SWAP_CANCEL_BATCH_ALGOS, params)
    def get_algo(self,
        instrument_id='',
        order_type='',
        status='',
        algo_ids='',
        before='',
        after='',
        limit='',):

        params={
        'order_type':order_type,

        }
        if status:
            params['status']=status
        if status:
            params['status']=status
        if algo_ids:
            params['status']=status
        if before:
            params['status']=status
        if after:
            params['status']=status
        if limit:
            params['status']=status

        return self._request_with_params(GET, SWAP_ALGO+ '/' + str(instrument_id), params)




