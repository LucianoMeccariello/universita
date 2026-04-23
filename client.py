import grpc
import sys
import order_management_pb2
import order_management_pb2_grpc
N_REQS = 5

def generate_orders(orders):
    
    for order in orders:

        yield order 
        #yield essendo uno stream, inoltre possiamo ritornare direttamente order, essendo order un oggetto di tipo Order, 
        # che è il tipo di dato che il metodo processOrders restituisce al client


if __name__ == '__main__':
    
    try:

        port = sys.argv[1]
        
    except IndexError:
        print("[CLIENT] Specificare porta del server")
        sys.exit(-1)

destination = ["Tecchio", "San Giovanni", "Via Claudio ", "Agnano"]
orders = []

with grpc.insecure_channel('localhost:' + port) as channel:

    stub = order_management_pb2_grpc.OrderManagementStub(channel)

    for i in range (N_REQS):

        order_id = stub.addOrder(order_management_pb2.Order(items=["item" + str(i), "item"+ str(i+1)],description="description"+str(i),price=100 *(i+1 ),destination=destination[i%len(destination)] ))

        print("[CLIENT] Ordine ricevuto", order_id)

        order = stub.getOrder(order_id) #possiamo passare direttamente l'id dell'ordine, 
        # perché il metodo getOrder accetta come input un messaggio di tipo StringMessage, che contiene una stringa, 
        # e l'id dell'ordine è una stringa

        orders.append(order)

        print("[CLIENT] Ordine ricevuto", order)
    
    for order in stub.searchOrders(order_management_pb2.StringMessage(value="item1")) :
        
        print("[CLIENT] Ordine ricevuto", order)

    for shipment in stub.processOrders(generate_orders(orders)): 
        #possiamo passare direttamente orders, dato che orders è una lista di oggetti di tipo Order

        #non possiamo passare direttamente order all'interno di processOrders, 
        # dato che accetta come input un iteratore di ordini

        print("[CLIENT] Spedizione", shipment)
    
