import grpc
import user_pb2
import user_pb2_grpc

def register_user(stub):
    email = input("Inserisci l'email per la registrazione: ")
    ticker = input("Inserisci il ticker: ")

    response = stub.RegisterUser(user_pb2.RegisterUserRequest(
        email=email,
        ticker=ticker
    ))
    print(f"Risultato della registrazione: Successo={response.success}, Messaggio={response.message}")

def update_user_ticker(stub):
    email = input("Inserisci l'email dell'utente da aggiornare: ")
    new_ticker = input("Inserisci il nuovo ticker: ")

    response = stub.UpdateUserTicker(user_pb2.UserRequest(
        email=email,
        ticker=new_ticker
    ))
    print(f"Risultato dell'aggiornamento: Successo={response.success}, Messaggio={response.message}")

def delete_user(stub):
    email = input("Inserisci l'email dell'utente da cancellare: ")

    response = stub.DeleteUser(user_pb2.DeleteUserRequest(
        email=email
    ))
    print(f"Risultato della cancellazione: Successo={response.success}, Messaggio={response.message}")


# Funzione per ottenere l'ultimo valore del ticker
def get_latest_value(stub):
    email = input("Inserisci l'email dell'utente per recuperare l'ultimo valore del ticker: ")

    # Crea la richiesta per ottenere l'ultimo valore del ticker
    request = user_pb2.EmailRequest(email=email)


    try:
        # Invia la richiesta al server
        response = stub.GetLatestValue(request)
        
        
        print(f"[DEBUG] Risposta dal server: {response}")


        # Gestisce la risposta del server
        if response.success:
            print(f"Ultimo valore per {email}: {response.message}")
            print(f"Valore: {response.value}, Timestamp: {response.timestamp}")
        else:
            print(f"Errore: {response.message}")
    except grpc.RpcError as e:
        # Qui possiamo aggiungere un controllo per i dettagli specifici dell'errore
        print(f"[ERROR] Si è verificato un errore gRPC: {e.code()} - {e.details()}")        
    except Exception as e:
        print(f"[ERROR] Si è verificato un errore generico: {str(e)}")


def calculate_average(stub):
    email = input("Inserisci l'email dell'utente: ")
    count = int(input("Inserisci il numero di ultimi valori da considerare per la media: "))

    # Crea la richiesta al server
    request = user_pb2.AverageRequest(
        email=email,
        count=count
    )
    
    try:
        # Invia la richiesta al server
        response = stub.CalculateAverage(request)
        
        if response.success:
            print(f"Media calcolata: {response.average}")
            print(f"Risposta dal server:{response.message}")
        else:
            print(f"Errore: {response.message}")
    except grpc.RpcError as e:
        print(f"Errore gRPC: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"Errore generale: {str(e)}")




def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        while True:
            print("\n Funzionalità di gestione degli utenti")
            print("1: Registrare un nuovo utente")
            print("2: Aggiornare il ticker di un utente")
            print("3: Cancellare un utente")
            print("4: Recuperare l'ultimo valore del ticker")
            print("5: Calcolare la media degli ultimi X valori")
            print("6: Esci")
            choice = input("Scegli un'opzione: ")

            if choice == "1":
                register_user(stub)
            elif choice == "2":
                update_user_ticker(stub)
            elif choice == "3":
                delete_user(stub)
            elif choice == "4":
                get_latest_value(stub)
            elif choice == "5":
                calculate_average(stub)
            elif choice == "6":
                print("Uscita dal client...")
                break
            else:
                print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    run()