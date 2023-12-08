# server.py

from omniORB import CORBA
import Example, Example__POA
import datetime

class Greetings_i(Example__POA.Greetings):
    def __init__(self, client_id):
        Example__POA.Greetings.__init__(self)
        self.client_id = client_id
        self.log_file_path = f"log_cliente_{client_id}.txt"
        self.log_file = open(self.log_file_path, "a")
        self.log_file.write(f"=== Log Iniciado em {datetime.datetime.now()} ===\n")
        self.log_file.flush()

    def sayHello(self):
        return f"Bom dia, Cliente {self.client_id}!"

    def sendMessage(self, message):
        timestamp = datetime.datetime.now()
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{formatted_timestamp} - Cliente {self.client_id}: {message}\n"
        print(log_message)
        self.log_file.write(log_message)
        self.log_file.flush()

    def _release(self):
        # Este método é chamado quando a instância é liberada.
        # Certifica-se de fechar o arquivo de log corretamente.
        self.log_file.write(f"=== Log Encerrado em {datetime.datetime.now()} ===\n")
        self.log_file.close()

# Dicionário para armazenar instâncias de Greetings_i para cada cliente
clients = {}

# Inicializa o ORB
orb = CORBA.ORB_init([], CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")
poaManager = poa._get_the_POAManager()
poaManager.activate()

# Cria uma instância Greetings_i para fornecer o IOR
greetings = Greetings_i("server")
obj = greetings._this()

# Obtém o IOR da instância do objeto e exibe
ior = orb.object_to_string(obj)
print(f"IOR do Servidor: {ior}")

# Aguarda a conexão de clientes
try:
    orb.run()

except KeyboardInterrupt:
    print("Servidor encerrado.")

# Encerra o ORB
orb.destroy()
