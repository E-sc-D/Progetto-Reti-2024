# -*- coding: utf-8 -*-
"""
Created on Tue June 20 10:21:32 2024

@author: edoardo
"""
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM



# Configurazione del server
BUFFSIZE = 1024
serverAddress = ('127.0.0.1', 52090)

# Dizionari per tenere traccia dei client e dei loro indirizzi
clients = {}
addresses = {}

# Creazione del socket del server
# Crea un socket IPv4 (AF_INET) di tipo stream (SOCK_STREAM).
server = socket(AF_INET, SOCK_STREAM)
# associa il socket all'indirizzo IP e alla porta specificati.
server.bind(serverAddress)

# Accetta nuove connessioni in un ciclo continuo.
# Usa un try-except per catturare e gestire eventuali eccezioni durante l'accettazione delle connessioni.
# Avvia un nuovo thread per ogni client connesso per gestire la comunicazione.


def listen_to_connections():
    while True:
        try:
            client, client_address = server.accept()
            print("{}:{} è entrato nella chat.".format(client_address[0],client_address[1]))
            client.send(bytes("Username:", "utf8"))
            addresses[client] = client_address
            # Avvia un nuovo thread per gestire il client
            Thread(target=handle_client, args=(client,)).start()
        except Exception as e:
            print(f"errore nel accettare la connesione: {e}")

# Riceve il nome del client e invia un messaggio di benvenuto.
# Gestisce i messaggi del client in un ciclo continuo.
# Rimuove il client dalla lista quando questo si disconnette (inviando {quit}).
# Usa un try-except per catturare e gestire eventuali eccezioni durante la gestione del client.
#Questo thread è la connessione del client con il server
#si occupa di inviare i messaggi del client, interpretare comandi(!exit)
#e logga eventuali stati sulla console (si è scollegato dalla chat)
def handle_client(client):
    try:
        name = client.recv(BUFFSIZE).decode("utf8")
        client.send(bytes("Benvenuto! {}\r\n usa !exit per uscire.".format(name) , "utf8"))
         
        broadcast(bytes("{} è entrato nella chat".format(name), "utf8"))
        clients[client] = name
        
        while True:
            msg = client.recv(BUFFSIZE)
            if msg != bytes("!exit", "utf8"):
                broadcast(msg,"{}:".format(name))
            else:
                client.send(bytes("uscendo...", "utf8"))
                client.close()
                client.pop(client,None)
                broadcast(bytes("{} ha lasciato la chat".format(name), "utf8"))
                print("{} si è scollegato.".format(addresses[client]))
                break
    except Exception as e:
        print(f"Errore nella gestione del client: {e}")
        client.close()
        if client in clients:
            clients.pop(client,None)
            broadcast(bytes("{} ha forzatamente lasciato la chat".format(clients[client]), "utf8"))
            print(addresses[client], " si è scollegato forzatamente.")

#Invia un messaggio in broadcast aggiungendo il prefisso in string
#al msg in byte, viene usato un trycath per gestire eventuali errori
#permettendo al server di continuare a operare
#se un client causa un errore viene rimosso dalla lista
def broadcast(msg, prefisso=""):
    for user in clients:
        try:
            user.send(bytes(prefisso, "utf8") + msg)
        except Exception as e:
            print(f"Errore nell'invio del messaggio: {e}")
            user.close()
            clients.pop(user,None)


if __name__ == "__main__":
    
    server.listen(5)# Il server aspetta richieste di connessione in modo asyncrono
    print("Server Pronto\r\n Indirizzo: {} Porta: {}".format(serverAddress[0],serverAddress[1]))
    
    
    introducer = Thread(target=listen_to_connections)#Questo thread accetterà le richieste di connessione
    introducer.start()
    introducer.join()
    #usando il join su introducer rendiamo introducer bloccante sul programma
    #quindi server.close() verrà chiamato non appena introducer sarà chiuso.
    server.close()
