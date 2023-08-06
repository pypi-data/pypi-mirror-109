# -*- coding: utf-8 -*-

import sys, json, time
from os.path import dirname, abspath

project_path = dirname(dirname(abspath(__file__)))
projec_full_path = project_path + r'\py_protoc'
sys.path.append(projec_full_path)
import socket
from com import *
############################旧版################################
# from py_protoc import msg_stock_pb2 as msg_stock
# from py_protoc import msg_stock_pb2 as msg_stock
# from py_protoc import msg_stock_common_pb2 as msg_stock_common
############################旧版################################

from py_protoc import msg_comm_request_pb2 as msg_stock_common
from py_protoc import msg_comm_cust_pb2 as cust_pb
from py_protoc import msg_comm_response_pb2 as reponse_pb
from py_protoc import stock_comm_pb2 as comm_pb
from py_protoc import stock_real_pb2 as msg_stock    # real_pb

class KaisaProtoc(object):

    def __init__(self):
        pass

    @staticmethod
    def get_ping_bstring(reqId=1):

        pb_reqhead = msg_stock_common.ReqHead()
        pb_reqhead.reqId = reqId
        pb_reqhead.mod = 3
        # pb_reqhead.len = 0
        # pb_reqhead.data = ""
        #pb_reqhead.reqType = 3
        pb_string = pb_reqhead.SerializeToString()
        return pb_string

    @staticmethod
    def get_subscribe_bstring(symbollist, reqId=1):
        '''
        订阅行情
        SUB_TYPE_NONE = 0;
        QUOTE = 1;
        TICK = 2;
        BROKER = 3;
        ORDER = 4;
        '''

        pb_rule = msg_stock.Rule()
        #pb_stockcode = msg_stock.StockCode()
        for secucode_dict in symbollist:
            pb_stockcode_one = pb_rule.stockCodes.add()
            pb_stockcode_one.code = secucode_dict['code']
            market = secucode_dict['market']
            pb_stockcode_one.market = market
            pb_stockcode_one.language = 0
            pb_stockcode_one.types.append(secucode_dict['sub_type'])
        #pb_rule.types.append(1)
        #pb_rule.types.append(2)
        ps = pb_rule.SerializeToString()
        pb_reqhead = msg_stock_common.ReqHead()
        pb_reqhead.reqId = reqId
        pb_reqhead.mod = 1
        pb_reqhead.cmd = 10   # SubQuote
        pb_reqhead.len = len(ps)
        pb_reqhead.data = ps
        pb_string = pb_reqhead.SerializeToString()

        return pb_string

    @staticmethod
    def get_unsubscribe_bstring(symbollist, reqId=1):
        '''
        退订行情
        SUB_TYPE_NONE = 0;
        QUOTE = 1;
        TICK = 2;
        BROKER = 3;
        ORDER = 4;
        '''
        pb_rule = msg_stock.Rule()
        pb_stockcode = msg_stock.StockCode()
        for secucode_dict in symbollist:
            pb_stockcode_one = pb_rule.stockCodes.add()
            pb_stockcode_one.code = secucode_dict['code']
            market = secucode_dict['market']
            pb_stockcode_one.market = market
            pb_stockcode_one.language = 0
            pb_stockcode_one.types.append(secucode_dict['sub_type'])
        # pb_rule.types.append(1)
        # pb_rule.types.append(2)
        ps = pb_rule.SerializeToString()
        pb_reqhead = msg_stock_common.ReqHead()
        pb_reqhead.reqId = reqId
        pb_reqhead.mod = 1
        pb_reqhead.cmd = 11  # UnSubQuote
        pb_reqhead.len = len(ps)
        pb_reqhead.data = ps
        pb_string = pb_reqhead.SerializeToString()
        return pb_string

    @staticmethod
    def rec_bstring_to_json(bstring):
        '''
        uint32 cmd = 4; //对应模块编号下的指令 2位
        {QUOTE = 1;
        TICK = 2;
        }

        bytes data = 7; //二进制数据 4位
        '''

        data_type = 0
        try:
            pb_reshead = reponse_pb.ResHead()
            pb_reshead.ParseFromString(bstring)
            if pb_reshead.cmd not in ALLDATAIDLIST:
                pass
            else:
                data_type, res_data = KaisaProtoc.handle_any_data_cls(pb_reshead.cmd, pb_reshead.data)

                return {'type': data_type, 'data': res_data}
        except Exception as exp:
            res_data = exp
            return {'type': data_type, 'data': res_data}


    @staticmethod
    def quote_bstring_to_json(quote):
        ## 解析quote-data
        sec = quote.quote_time.seconds
        nano = quote.quote_time.nanos
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sec + nano / 1000000000.0))

        return {'market': quote.market,
                'code': quote.code,
                'now': quote.now,
                'high': quote.high,
                'low': quote.low,
                'volume': quote.volume,
                'amount': quote.amount,
                'quote_time': update_time,
                }

    @staticmethod
    def broker_list_bstring_to_json(broker_list):
        # broker-list data to json

        return {'market': broker_list.market,
                'code': broker_list.code,
                'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    broker_list.time.seconds+broker_list.time.nanos/1000000000.0)),
                'brokerSell': [KaisaProtoc.broker_bstring_to_json(bs) for bs in broker_list.brokerSell],
                'brokerBuy': [KaisaProtoc.broker_bstring_to_json(bb) for bb in broker_list.brokerBuy]
                }

    @staticmethod
    def broker_bstring_to_json(broker):
        ## broker data to json
        return {'broker_level': broker.broker_level,
                'broker_id': [KaisaProtoc.broker_id_bstring_to_json(_id_) for _id_ in broker.broker_id]
                }

    @staticmethod
    def broker_id_bstring_to_json(broker):
        # broker-is data to json
        return {'broker_id': broker}

    @staticmethod
    def ticklist_bstring_to_json(ticklist):

        return {'market': ticklist.market,
                'code': ticklist.code,
                'tick': [KaisaProtoc.tick_bstring_to_json(item) for item in ticklist.tick]
                }

    @staticmethod
    def tick_bstring_to_json(tick):

        return {'now': tick.now,
                'cur_volume': tick.cur_volume,
                'tick_flag': tick.tick_flag,
                'tick_vi': tick.tick_vi,
                'tick_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    tick.tick_time.seconds+tick.tick_time.nanos/1000000000.0))
                }

    @staticmethod
    def level_order_list_string_to_json(order_list):
        # level_order list data
        return {'market': order_list.market,
                'code': order_list.code,
                'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    order_list.time.seconds+order_list.time.nanos/1000000000.0)),
                'orderSell': [KaisaProtoc.level_order_bsstring_to_json(bs) for bs in order_list.orderSell],
                'orderBuy': [KaisaProtoc.level_order_bsstring_to_json(bb) for bb in order_list.orderBuy]
                }
    @staticmethod
    def level_order_bsstring_to_json(order_bs):
        # 转换order中的bs数据
        return {'level': order_bs.level,
                'price': order_bs.price,
                'volume': order_bs.volume,
                'broker_count': order_bs.broker_count
                }

    @staticmethod
    def handle_any_data_cls(DATATYPE, data):
        # total-handle-data
        try:
            THISDATATYPE = PROTODATADIC[DATATYPE]
            if THISDATATYPE == 'QUOTE':
                return KaisaProtoc._get_quote_data(data)
            elif THISDATATYPE == 'TICK':
                return KaisaProtoc._get_tick_data(data)
            elif THISDATATYPE == 'BROKER':
                return KaisaProtoc._get_broker_data(data)
            elif THISDATATYPE == 'ORDER':
                return KaisaProtoc._get_level_order_data(data)
            else:
                pass
        except Exception as exp:
            print('get-quote-data-_dic_ error:{}'.format(exp))
            return None

    @staticmethod
    def _get_tick_data(data):
        #### cmd=2
        #### 逐笔数据 tick
        ticklist = msg_stock.TickList()
        ticklist.ParseFromString(data)
        body_json = KaisaProtoc.ticklist_bstring_to_json(ticklist)
        return PROTODATADIC[TICK], body_json

    @staticmethod
    def _get_quote_data(data):
        #### cmd=1
        #### 盘口数据 quote
        quote = msg_stock.Quote()
        quote.ParseFromString(data)
        try:
            ## 判断该条行情是否有效
            if quote.update_flag != [1, 4, 8, 16, 32, 2048, 32768]:
                return QUOTE, None
            else:
                body_json = KaisaProtoc.quote_bstring_to_json(quote)
                return PROTODATADIC[QUOTE], body_json
        except Exception as exp:
            print('get-quote-data-error:{}'.format(exp))

    @staticmethod
    def _get_broker_data(data):
        #### cmd=3
        #### 经纪商数据 broker-list
        broker_list = msg_stock.BrokerList()
        broker_list.ParseFromString(data)
        body_json = KaisaProtoc.broker_list_bstring_to_json(broker_list)
        return PROTODATADIC[BROKERS], body_json

    @staticmethod
    def _get_level_order_data(data):
        ### cmd=4
        ### level-10 order data
        order_list = msg_stock.OrderStallsList()
        order_list.ParseFromString(data)
        body_json = KaisaProtoc.level_order_list_string_to_json(order_list)
        return PROTODATADIC[LEVEL_ORDER], body_json

if __name__=='__main__':
    print('start.')

