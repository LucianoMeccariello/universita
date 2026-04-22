import grpc
import sys
import order_management_pb2
import order_management_pb2_grpc
N_REQS = 5


if __name__ == '__main__':
    
    try:

        port = sys.argv[1]
        
    except IndexError:
        print("[CLIENT] Specificare porta del server")
        sys.exit(-1)

destination = ["TECCHIO, Montesantangelo, sangiovanni"]
orders = []

with grpc.insecure_channel('localhost:' + port) as channel:

    stub = order_management_pb2_grpc.OrderManagementStub(channel)



    for i in range (N_REQS):

        order_id = stub.addOrder(order_management_pb2.Order(items=["item" + str(i), "item"+ str(i)],description="description",price=100 +(i+1 ),destination=destination[i%len(destination)] ))

        print("[CLIENT] Id ordine ricevuto", order_id)


        order = stub.getOrder(order_id)
        orders.append(order)

        print("[CLIENT] Ordine ricevuto", order)
    
    for order in stub.searchOrders(order_management_pb2.StringMessage(value="item1")) :
        
        print("[CLIENT] Ordine ricevuto????????", order)

    
