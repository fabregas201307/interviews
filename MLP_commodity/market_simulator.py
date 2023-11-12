#!/bin/python3

import json
import math
import os
import random
import re
import sys


import heapq
#
# Complete the 'simulate_orders' function below.
#
# The function is expected to return a STRING.
# The function accepts DICT_ARRAY orders as parameter.
#

    
def simulate_orders(orders: list) -> str:
    result = list()
    limit_orders = dict()
    order_number = 0

    for order in orders:
        order_number += 1
        if order.get("type") == "limit":
            # order is limit
            cur_key = (order.get("symbol"), order.get("action"))
            if (order.get("action") == "buy") and ((order.get("symbol"), "sell") in limit_orders):
                _ = fill_order(order=order, cur_heap=limit_orders.get((order.get("symbol"), "sell")), cache_list=result)
            elif (order.get("action") == "sell") and ((order.get("symbol"), "buy") in limit_orders):
                _ = fill_order(order=order, cur_heap=limit_orders.get((order.get("symbol"), "buy")), cache_list=result)
            else:
                # can't fill this limit order
                pass

            # after fill this limit order, we may still need to push it into heapq

            if cur_key in limit_orders:
                if cur_key[1] == "buy":
                    # kept in maximum heap
                    cur_heap = limit_orders.get(cur_key)
                    heapq.heappush(cur_heap, ((-1) * order.get("price"), order_number, order))
                else:
                    # must be sell limit order, kept in minimum heap,  and cur_key[1] == "sell"
                    cur_heap = limit_orders.get(cur_key)
                    heapq.heappush(cur_heap, (order.get("price"), order_number, order))
            else:
                # current key never seen, keep one empty heap
                this_heap = []
                if cur_key[1] == "buy":
                    heapq.heappush(this_heap, ((-1) * order.get("price"), order_number, order))
                    limit_orders[cur_key] = this_heap
                    print("kai debug 1:")
                    print(this_heap)
                    print(limit_orders)
                else:
                    heapq.heappush(this_heap, (order.get("price"), order_number, order))
                    limit_orders[cur_key] = this_heap

        else:
            # order is "market", expire if not filled
            # cur_key = (order.get("symbol"), order.get("action"))
            if (order.get("action") == "buy") and ((order.get("symbol"), "sell") in limit_orders):
                # top_item = heapq.heappop(limit_orders.get((cur_key[0]), "sell"))
                _ = fill_order(order=order, cur_heap=limit_orders.get((order.get("symbol"), "sell")), cache_list=result)
            elif (order.get("action") == "sell") and ((order.get("symbol"), "buy") in limit_orders):
                print("kai debug 2")
                print(order)
                _ = fill_order(order=order, cur_heap=limit_orders.get((order.get("symbol"), "buy")), cache_list=result)
            else:
                # market order expires
                pass

    result = sort_results(result)
    return result

def fill_order(order, cur_heap, cache_list):
    if len(cur_heap) < 1:
        return None
    top_item = heapq.heappop(cur_heap)
    if order.get("type") == "limit":
        # to fill limit order
        if order.get("action") == "buy" and top_item[2].get("action") == "sell":
            if (order.get("price")>=top_item[2].get("price")) and (order.get("quantity") <= top_item[2].get("quantity")):
                top_item[2]["quantity"] = top_item[2].get("quantity") - order.get("quantity")
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:{order.get("quantity")} USD:-{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{(-1) * order.get("quantity")} USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                if top_item[2]["quantity"] > 0:
                    heapq.heappush(cur_heap, top_item)
            elif order.get("price")>=top_item[2].get("price"):
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:{top_item[2].get("quantity")} USD:-{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{(-1) * top_item[2].get("quantity")} USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                order["quantity"] = order["quantity"] - top_item[2].get("quantity")
                fill_order(order, cur_heap, cache_list)
            else:
                # market_order expired
                return None
            
        elif order.get("action") == "sell" and top_item[2].get("action") == "buy":
            if (order.get("price")<=top_item[2].get("price")) and (order.get("quantity") <= top_item[2].get("quantity")):
                top_item[2]["quantity"] = top_item[2].get("quantity") - order.get("quantity")
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:-{order.get("quantity")} USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{order.get("quantity")} USD:-{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                if top_item[2]["quantity"] > 0:
                    heapq.heappush(cur_heap, top_item)
            elif order.get("price")<=top_item[2].get("price"):
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:-{top_item[2].get("quantity")} USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{top_item[2].get("quantity")} USD:-{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                order["quantity"] = order["quantity"] - top_item[2].get("quantity")
                fill_order(order, cur_heap, cache_list)
            else:
                # market_order expired
                return None
        else:
            return None
    else:
        # to fill market order
        if order.get("action") == "buy" and top_item[2].get("action") == "sell":
            if (order.get("quantity") <= top_item[2].get("quantity")):
                top_item[2]["quantity"] = top_item[2].get("quantity") - order.get("quantity")
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:{order.get("quantity")} USD:-{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{(-1) * order.get("quantity")} USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                if top_item[2]["quantity"] > 0:
                    heapq.heappush(cur_heap, top_item)
            else:
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:{top_item[2].get("quantity")} USD:-{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{(-1) * top_item[2].get("quantity")} USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                order["quantity"] = order["quantity"] - top_item[2].get("quantity")
                fill_order(order, cur_heap, cache_list)
        elif order.get("action") == "sell" and top_item[2].get("action") == "buy":
            if (order.get("quantity") <= top_item[2].get("quantity")):
                top_item[2]["quantity"] = top_item[2].get("quantity") - order.get("quantity")
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:-{order.get("quantity")} USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{order.get("quantity")} USD:-{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                if top_item[2]["quantity"] > 0:
                    heapq.heappush(cur_heap, top_item)
            else:
                trade_record_str_1 = f"""{order.get("user")}: {order.get("symbol")}:-{top_item[2].get("quantity")} USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}: {top_item[2].get("symbol")}:{top_item[2].get("quantity")} USD:-{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                order["quantity"] = order["quantity"] - top_item[2].get("quantity")
                fill_order(order, cur_heap, cache_list)
        else:
            return None

def sort_results(records) -> str:
    print("kai debug:")
    print(records)
    tuples = [(j.split(":")[0], j) for j in records]
    sorted_list = sorted(tuples, key=lambda x: x[0])
    
    # fix 
    ans = dict()
    
    for i in sorted_list:
        username = i[0]
        quantity = int(i[1].split()[1].split(":")[1])
        dollar = int(i[1].split()[2].split(":")[1])
        if quantity < 0:
            money = abs(quantity) * dollar
        elif quantity > 0:
            money = quantity * dollar
        else:
            # should not have quantity equals 0
            pass
            
        if username not in ans:
            ans[username] = dict()
            ans[username]["USD"] = money
            ans[username]["trades"] = i[1].split()[1]
        else:
            ans.get(username)["USD"] = ans.get(username)["USD"] + money
            ans.get(username)["trades"] = ans.get(username)["trades"] + " " + i[1].split()[1]
    
    result = list()
    for username in ans:
        cur_str = username + ": " + ans.get(username).get("trades") + " USD:" + str(ans.get(username).get("USD"))
        if ans.get(username).get("USD") != 0:
            result.append(cur_str)
        else:
            # if this username trades ends up zero dollars, pass
            pass

    # end of fix
    
    # result = [i[1] for i in sorted_list]
    
    
    ans = "\n".join(result)
    return ans
    
    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    orders_count = int(input().strip())

    orders = []

    for _ in range(orders_count):
        orders_item = json.loads(input())
        orders.append(orders_item)

    result = simulate_orders(orders)

    fptr.write(result + '\n')

    fptr.close()
