from omniORB import CORBA
import Example

class Greetings_i(Example.Greetings):
    def __init__(self, client_id):
        self.client_id = client_id
        self.client_name = None

    def sayHello(self):
        return f"Bom dia, Cliente {self.client_id}!"

    def sendMessage(self, message):
        print(f"Cliente {self.client_name}: {message}")

    def setClientName(self, client_name):
        self.client_name = client_name

# Inicializa o ORB
orb = CORBA.ORB_init([], CORBA.ORB_ID)

# Solicita o IOR do servidor
ior = input("Insira o IOR fornecido pelo servidor: ")

# Conecta ao objeto Greetings no servidor
obj = orb.string_to_object(ior)
greetings = obj._narrow(Example.Greetings)

# Verifica se a referência do objeto é válida
if greetings is None:
    print("A referência do objeto não é um Greetings válido")
else:
    try:
        # Solicita um nome para o cliente
        client_name = input("Insira seu nome: ")
        
        # Cria uma instância Greetings_i para o cliente
        client = Greetings_i("client")
        client.setClientName(client_name)

        while True:
            # Solicita uma mensagem para enviar ao servidor
            message_to_send = input(f"Cliente {client.client_name}, envie uma mensagem para o servidor (digite 'exit' para sair): ")

            # Verifica se o usuário quer sair
            if message_to_send.lower() == 'exit':
                break

            # Chama o método sendMessage no servidor
            greetings.sendMessage(f"{client.client_name}: {message_to_send}")

    except KeyboardInterrupt:
        print("Cliente encerrado.")

# Encerra o ORB
orb.destroy()

