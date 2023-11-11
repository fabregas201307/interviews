import heapq


def simulate_orders(orders: list) -> list:
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
                limit_orders[cur_key] = []
                if cur_key[1] == "buy":
                    heapq.heappush(limit_orders.get(cur_key), ((-1) * order.get("price"), order_number, order))
                else:
                    heapq.heappush(limit_orders.get(cur_key), (order.get("price"), order_number, order))

        else:
            # order is "market", expire if not filled
            # cur_key = (order.get("symbol"), order.get("action"))
            if (order.get("action") == "buy") and ((order.get("symbol"), "sell") in limit_orders):
                # top_item = heapq.heappop(limit_orders.get((cur_key[0]), "sell"))
                _ = fill_order(order=order, cur_heap=limit_orders.get((order.get("symbol"), "sell")), cache_list=result)
            elif (order.get("action") == "sell") and ((order.get("symbol"), "buy") in limit_orders):
                # top_item = heapq.heappop(limit_orders.get((cur_key[0]), "buy"))
                _ = fill_order(order=order, cur_heap=limit_orders.get((order.get("symbol"), "buy")), cache_list=result)
            else:
                # market order expires
                pass

    result = sort_results(result)
    return result


def fill_order(order, cur_heap, cache_list):
    ## assume order is buy and cur_heap is sell;  or the other way
    ## essentialy valid order and cur_heap to fill
    if len(cur_heap) < 1:
        return None
    top_item = heapq.heappop(cur_heap)
    if order.get("type") == "limit":
        ## to fill limit order
        if order.get("action") == "buy" and top_item[2].get("action") == "sell":
            if (order.get("price")>=top_item[2].get("price")) and (order.get("quantity") <= top_item[2].get("quantity")):
                top_item[2]["quantity"] = top_item[2].get("quantity") - order.get("quantity")
                trade_record_str_1 = f"""{order.get("user")}:{order.get("symbol")}:{order.get("quantity")}:USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}:{top_item[2].get("symbol")}:{(-1) * order.get("quantity")}:USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                if top_item[2]["quantity"] > 0:
                    heapq.heappush(cur_heap, top_item) # push back modified item
            elif order.get("price")>=top_item[2].get("price"):
                trade_record_str_1 = f"""{order.get("user")}:{order.get("symbol")}:{top_item[2].get("quantity")}:USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}:{top_item[2].get("symbol")}:{(-1) * top_item[2].get("quantity")}:USD:{top_item[2].get("price")}"""
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
                trade_record_str_1 = f"""{order.get("user")}:{order.get("symbol")}:{order.get("quantity")}:USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}:{top_item[2].get("symbol")}:{(-1) * order.get("quantity")}:USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                heapq.heappush(cur_heap, top_item) # push back modified item
            elif order.get("price")<=top_item[2].get("price"):
                trade_record_str_1 = f"""{order.get("user")}:{order.get("symbol")}:{top_item[2].get("quantity")}:USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}:{top_item[2].get("symbol")}:{(-1) * top_item[2].get("quantity")}:USD:{top_item[2].get("price")}"""
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
        ## to fill market order
        if order.get("action") == "buy" and top_item[2].get("action") == "sell":
            if (order.get("quantity") <= top_item[2].get("quantity")):
                top_item[2]["quantity"] = top_item[2].get("quantity") - order.get("quantity")
                trade_record_str_1 = f"""{order.get("user")}:{order.get("symbol")}:{order.get("quantity")}:USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}:{top_item[2].get("symbol")}:{(-1) * order.get("quantity")}:USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                heapq.heappush(cur_heap, top_item) # push back modified item
            else:
                trade_record_str_1 = f"""{order.get("user")}:{order.get("symbol")}:{top_item[2].get("quantity")}:USD:{top_item[2].get("price")}"""
                trade_record_str_2 = f"""{top_item[2].get("user")}:{top_item[2].get("symbol")}:{(-1) * top_item[2].get("quantity")}:USD:{top_item[2].get("price")}"""
                cache_list.append(trade_record_str_1)
                cache_list.append(trade_record_str_2)
                order["quantity"] = order["quantity"] - top_item[2].get("quantity")
                fill_order(order, cur_heap, cache_list)
        else:
            return None
    

def sort_results(records) -> list:
    tuples = [(j.split(":")[0], j) for j in records]
    sorted_list = sorted(tuples, key=lambda x: x[0])
    result = [i[1] for i in sorted_list]
    return result


if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    # orders_count = int(input().strip())

    orders = [
        {"type": "limit", "action": "sell", "quantity": 10, "symbol": "AAPL", "user": "a", "price": 100},
        {"type": "market", "action": "buy", "quantity": 1, "symbol": "AAPL", "user": "b"},
        {"type": "limit", "action": "sell", "quantity": 20, "symbol": "AAPL", "user": "c", "price": 90},
        {"type": "limit", "action": "sell", "quantity": 10, "symbol": "AAPL", "user": "d", "price": 110},
        {"type": "limit", "action": "sell", "quantity": 10, "symbol": "AAPL", "user": "e", "price": 95},
        {"type": "limit", "action": "sell", "quantity": 20, "symbol": "AMZN", "user": "c", "price": 90},
        {"type": "limit", "action": "sell", "quantity": 10, "symbol": "GOOG", "user": "d", "price": 110},
        {"type": "limit", "action": "sell", "quantity": 10, "symbol": "XY", "user": "e", "price": 95},
        {"type": "limit", "action": "sell", "quantity": 10, "symbol": "AAPL", "user": "f", "price": 100},
        {"type": "market", "action": "buy", "quantity": 1, "symbol": "AAPL", "user": "g"},
        {"type": "limit", "action": "buy", "quantity": 10, "symbol": "AAPL", "user": "h", "price": 150},
        {"type": "limit", "action": "buy", "quantity": 20, "symbol": "AMZN", "user": "h", "price": 100},
        {"type": "limit", "action": "buy", "quantity": 30, "symbol": "AMZN", "user": "a", "price": 90},
        {"type": "limit", "action": "buy", "quantity": 10, "symbol": "AMZN", "user": "c", "price": 90},
        {"type": "limit", "action": "buy", "quantity": 60, "symbol": "AAPL", "user": "i", "price": 150},
        {"type": "market", "action": "buy", "quantity": 1, "symbol": "XY", "user": "a"},
    ]

    # orders = [order_1, order_2, order_3, order_4, order_5, order_6]
    # orders = [order_1, order_2]


    # for _ in range(orders_count):
    #     orders_item = json.loads(input())
    #     orders.append(orders_item)

    result = simulate_orders(orders)
    for record in result:
        print(record)
    # fptr.write(result + '\n')
    # fptr.close()

