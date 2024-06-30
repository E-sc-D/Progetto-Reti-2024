# -*- coding: utf-8 -*-
"""
Created on Tue June 20 11:19:24 2024

@author: edoardo
"""
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import tkinter as tk

BUFFSIZE=1024

#questa funzione è la connessione diretta con il server, 
#ascoltarà per messaggi in arrivo
def get_messages():
    while True:
        try:
            message=client_socket.recv(BUFFSIZE).decode("utf8")#viene attesa la ricezione di un messaggio
            messages_list.insert(tk.END, message)#che viene poi inserito nella lista 
            
        # Se ci sono eccezioni dovute all'abbandono della chat non si attendono più nuovi messaggi
        except Exception as e:
            print(f"Errore durante la ricezione di messaggi: {e}")
            break
        

# Funzione per inviare messaggi, chiamata al momento della pressione del pulsante invio
def send_messages():
    # Lettura del messaggio da inviare dalla casella di invio e liberazione della casella
    message=my_msg.get()
    my_msg.set("")
    # Invio del messaggio sul socket
    client_socket.send(bytes(message, "utf8"))
    # Se il messaggio è quello con cui si termina la connessione si attende l'ultimo messaggio mandato dal server
    # e si chiudono il socket e la finestra
    if message == "!exit":
        client_socket.recv(BUFFSIZE)
        client_socket.close()
        window.destroy()
        
#Questa funzione viene chiamata alla chiusura della applicazione
def end(event = None):
    my_msg.set("!exit")
    send_messages()

#Creazione della finestra 
window = tk.Tk()
window.title("Centralized Chat")

#Questo frame è cio che mostrerà i messaggi
messages_frame = tk.Frame(window)
#Qua vengono salvati i messaggi da inviare
my_msg = tk.StringVar()
my_msg.set("Scrivi qui")
scrollbar = tk.Scrollbar(messages_frame)

#Questa è la lista che contiene i messaggi in arrivo
messages_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
messages_list.pack(side=tk.LEFT, fill=tk.BOTH)
messages_list.pack()
messages_frame.pack()

# Creazione del campo di input e associazione alla variabile stringa
entry_field = tk.Entry(window, textvariable=my_msg)
# Collegamento della funzione invio al tasto Return
entry_field.bind("<Return>", send_messages)

entry_field.pack()
# Creazione del pulsante invio e associazione alla funzione invio
send_button = tk.Button(window, text="Invio", command=send_messages)
# Integrazione del tasto nel pacchetto
send_button.pack()

# Associazione della funzione chiusura alla chiusura della finestra
window.protocol("WM_DELETE_WINDOW", end)


# Richiesta di inserimento della coppia indirizzo-porta del server
# se non viene specificato uno dei due vengono chiesti nuovamente
while True: 
    INDIRIZZO_SERVER=input("Inserire l'indirizzo IP del server host: ")
    PORTA_SERVER=input("Inserire la porta del server host: ")
    if not INDIRIZZO_SERVER or not PORTA_SERVER:
        print("Indirizzo non valido, inserire nuovamente")
    else:
        break

PORTA_SERVER=int(PORTA_SERVER)
SERVER = (INDIRIZZO_SERVER, PORTA_SERVER)

# Creazione del socket e collegamento al server
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(SERVER)
# Creazione e avvio del thread che si occuperà di ricevere i messaggi
thread_ric = Thread(target=get_messages)
thread_ric.start()
tk.mainloop()
