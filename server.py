import grpc
from concurrent import futures
import order_management_pb2_grpc
import order_management_pb2
import uuid

class OrderManagementServicer(order_management_pb2_grpc.OrderManagementServicer):

    def __init__(self, dict_order={}):
        self.dict_order = dict_order

    def addOrder(self, request, context):

        order_id = str(uuid.uuid1().hex)

        print("[SERVER] Ordine ricevuto", request)

        request.id = order_id

        print("[SERVER] Generato id", order_id)

        self.dict_order[order_id] = request 

        return order_management_pb2.StringMessage(value=order_id)
    

    def getOrder(self, request, context):

        order_id = request.value

        order = self.dict_order.get(order_id)
        

        if order is not None:   # se l'ordine esiste, restituisci l'ordine corrispondente al client

            print("[SERVER] invio Ordine ", order)
            return order
        
        else: #ritorno un ordine vuoto e quindi lo istanzio vuoto

            context.set_code(grpc.StatusCode.NOT_FOUND)         #eventualmente lato cliente potrebbe rice
            context.set_details('Order id '+str(order_id)+' not found') #eventualmente lato cliente potrebbe ricevere questo messaggio di errore

            print("[SERVER] Ordine non trovato con id ", order)

            return order_management_pb2.Order()
        


    def searchOrders(self, request, context):

        item_to_find = request.value

        orders = [] # lista degli ordini che contengono l'item richiesto

    
        # per ogni ordine presente nel dizionario degli ordini, controlliamo se l'item richiesto è presente nella lista degli item dell'ordine
        for order in self.dict_order.values(): 

            #if item in order.items: 

            for item in order.items:    

                if item_to_find in item:

                    orders.append(order) # se l'item è presente, aggiungiamo l'ordine alla lista degli ordini da restituire al client

                    break # se abbiamo trovato l'item in questo ordine, non ha senso continuare a cercare negli altri item di questo ordine, quindi usciamo dal ciclo interno
        
        print("[SERVER] ritorno ordine ", len(orders))
            

        for order in orders: 

                yield order 







                
    def processOrders(self, request_iterator, context):
        
        orders = [] # lista degli ordini da processare
        destination_dict = {} # dizionario che associa ad ogni destinazione la lista degli ordini da spedire a quella destinazione

        for order in request_iterator: # per ogni ordine ricevuto dal client, lo aggiungiamo alla lista degli ordini da processare


            orders.append(order)

            if order.destination in destination_dict.keys(): # se la destinazione dell'ordine è già presente nel dizionario, aggiungiamo l'ordine alla lista degli ordini da spedire a quella destinazione

                destination_dict[order.destination].append(order)

            else: # altrimenti, creiamo una nuova voce nel dizionario per quella destinazione e aggiungiamo l'ordine alla lista degli ordini da spedire a quella destinazione

                destination_dict[order.destination] = [order]

        for order_list in destination_dict.values(): # per ogni lista di ordini da spedire a una destinazione, creiamo un oggetto CombinedShipment e lo restituiamo al client


            

            yield order_management_pb2.CombinedShipment(id=str(uuid.uuid1().hex),status="PROCESSED", orders=order_list)










if __name__ == '__main__':
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) 
    # stiamo creando un server gRPC con un pool di thread per gestire le richieste in modo concorrente

    #quando andiamo ad inserie una porta con add_insecure_port, 
    # stiamo dicendo al server di ascoltare su tutte le interfacce di rete (indicato da '[::]') 
    # e di assegnare una porta dinamica (indicato da '0').
    port = server.add_insecure_port('[::]:0')

    print("[SERVER] Running on port", port)

    order_management_pb2_grpc.add_OrderManagementServicer_to_server(OrderManagementServicer(), server)
    # stiamo registrando il nostro servizio effettivo OrderManagementServicer al server gRPC,
    # in modo che possa gestire le richieste in arrivo.

    server.start() # avviamo il server gRPC, rendendolo pronto a ricevere richieste dai client.
    server.wait_for_termination() # mettiamo il server in attesa di terminazioneß