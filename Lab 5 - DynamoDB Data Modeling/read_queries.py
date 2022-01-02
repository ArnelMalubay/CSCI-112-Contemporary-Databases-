import user_ops as user
import order_ops as order_ops   
from pprint import pprint
from decimal import Decimal

if __name__ == '__main__':
    
    print('Access Pattern 1: Get User Profile\n')
    print('User Profile of tgrimes1\n')
    pprint(user.query_user_profile('tgrimes1'))
    
    print('\n-------\n')
    
    print('Access Pattern 2: Get Orders for User\n')
    print('Orders of tgrimes1\n')
    orders = order_ops.query_user_orders('tgrimes1')
    for order in orders:
        pprint(order)
        print('\n')
        
    print('-------\n')
    
    print('Access Pattern 3: Get Single Order and Order Items\n')
    order_id = orders[0]['sk'][7:]
    print('Items for Order {0}\n'.format(order_id))
    items = order_ops.query_order_items(order_id)
    for item in items:
        pprint(item)
        print('\n')
        
    print('-------\n')
    
    print('Access Pattern 4: Orders for User by Status and Date\n')
    
    print('Placed Orders of aarchamb\n')
    placed_orders = user.query_user_status('aarchamb','Placed')
    for placed_order in placed_orders:
        pprint(placed_order)
        print('\n')
    print('-------')
    print('Orders of aarchamb on 11/18/21\n')
    orders_on_date = user.query_user_date('aarchamb','11/18/21')
    for order_on_date in orders_on_date:
        pprint(order_on_date)
        print('\n')
    print('-------')
    print('Placed Orders of tgrimes1 on 11/20/21\n')
    placed_orders_on_date = user.query_user_status_date('tgrimes1', 'Placed', '11/20/21')
    for placed_order_on_date in placed_orders_on_date:
        pprint(placed_order_on_date)
        print('\n')
    
    print('-------\n')
    
    print('Access Pattern 5: Get All Pending Orders\n')
    print('All Pending Orders\n')
    pending_orders = order_ops.query_status_orders('Pending')
    for pending_order in pending_orders:
        pprint(pending_order)
        print('\n')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    