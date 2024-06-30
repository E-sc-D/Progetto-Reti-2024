<Center><sup><h1>Progetto Programmazione di Reti<br>Chat Server - Client</h1></sup></Center>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<Center><h3>Edoardo Scorza<br>Matricola : 0001077424 </h3></Center>
<Center><h4>24 giugno 2024</h4></Center>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

## Indice
1. [<h3>Istruzioni d'uso</h3>](#istruzioni-duso)
   
2. [<h3>Server.py</h3>](#serverpy)
   
3. [<h3>Client.py</h3>](#capitolo-3---sviluppo)
   

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

## Istruzioni d'uso
La Chat Client-Server <br>
è strutturata in 2 file il Client e il Server.<br>
é possibile eseguirli attraverso il file.bat passandogli<br> come 
argomento il numero di client che si vogliono eseguire
es:



``
./run 2 
``

Una volta eseguito il comando verranno generati n + 1 terminali,<br>
con n client e 1 server, l'indirizzo ip e porta del server sono fissati<br> e verranno mostrati a seguito dell'avvio.

Una volta impostato l'ip e la porta del server nel client<br> verrà
richiesto il nome utente, a quel punto è possibile iniziare la conversazione<br> con i client gia connessi.
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

## Server.py
Il server per il suo funzionamento fa leva
su due principali componenti:

I socket, in questo caso lo stream socket<br>
usato per la comunicazione di tipo TCP, ovvero connection oriented<br>
affidabile e sicuro per la trasmissione di dati.

I thread invece permettono al server di gestire piu client in contemporanea<br> e di separare le sue funzioni, tra cui troviamo:

- listen_to_connections()<br>
la quale si occupa di ricevere le richieste sulla porta comune<br> e stabilire una nuova porta per la comunicazione fra quel client e il server

- Handle_client(socket)<br>
listen_to_connection creerà un nuovo tread con la funzione
Handle_client<br> che si occuperà di gestire la comunicazione fra il server e il client specifico

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

## Client.py
Il client come il server usa i socket per 
stabilire la comunicazione con il server,<br> a differenza di esso però, non ha bisogno di molti thread,<br> in quanto la sua comunicazione è di tipo 1-1, solo con il server insomma,
per questo è anche piu semplice:

- Script principale:<br>
Il condice fondamentale che inizializza la GUI e la connessione<br>
viene eseguito fuori da una funzione, Non deve essere chiamato ma eseguito come prima cosa,<br>in quanto fondamentale per il client

- send_messages():<br>
Questa funzione potremmo dire che è la parte operativa del programma,<br>
si occupa di gestire l'input dell'utente, che siano comandi (!exit)
oppure messaggi,<br> è situato in un altro thread per non causare 
rallentamenti alla Gui
    
