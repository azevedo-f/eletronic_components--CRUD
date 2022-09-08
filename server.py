####################################################################################################################################
#                                             CRUD - Estoque de componentes eletrônicos                                            #
#                                           Alunas: Eduarda S. Gavião e Fernanda Azevedo                                           #
#                                                          SERVER                                                                  #
####################################################################################################################################
#                                             DISCIPLINA :  SISTEMAS DISTRIBUÍDOS                                                  #
####################################################################################################################################
## BIBLIOTECAS ##
import socket
from random import randint

####################################################################################################################################
## VARIAVÉIS ##
components_list={}
id=0

####################################################################################################################################
# Gera um id aleatório
def id():
    
    id = randint(0,500)
    id = id +1
    return id

# Definição da classe dos componentes eletronicos
class EletronicComponent:
    def __init__(self, name, price,quantity):
        global id
        self.id= id()
        self.name=name
        self.price=price  
        self.quantity=quantity              
               
                
    # Realiza a atualização dos componentes  
    def update_component(self,name, value, quantity):
        self.name=name
        self.value=value  
        self.quantity=quantity             
    
    def show_component(self):
         return f"ID: {self.id} | Nome: {self.name}| Valor: {self.price} | Quantidade: {self.quantity}"        
        
####################################################################################################################################
## FUNÇÕES ##

# Decodifica as mensagens enviadas pelo cliente
def decode_message(socket_dados):
    
    # Decodifica o tamanho do nome e o nome do componente
    tam_name=int.from_bytes(socket_dados.recv(1),'big')
    name=socket_dados.recv(tam_name).decode('utf-8')
      
    # Decodifica o valor do componente
    price=int.from_bytes(socket_dados.recv(1),'big')
    
    # Decodifica a quantidade de componentes
    quantity=int.from_bytes(socket_dados.recv(1),'big')

    return name,price,quantity

def error_message(id_component,option):
    if  option==2:
        option_message = " Não foi possível realizar a busca "
    elif option==3: 
        option_message= " Não foi possível atualizar os dados "
    elif option==4:
        option_message= " Não foi possível excluir os dados "
    
    info_message= f" !!! Componente com o id {id_component} não encontrado !!!" + option_message
    tam_info_message=len(info_message.encode())                
    pacote_message=tam_info_message.to_bytes(1,'big') + info_message.encode()
                
    # Monta o pacote de resposta para o cliente
    pacote_resposta=len(pacote_message).to_bytes(1,'big')+ pacote_message
    socket_dados.send(pacote_resposta)
                                
    
####################################################################################################################################
# Criação e configuração do socket
socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Definição IP e porta
ip='127.0.0.1'
port=50000
origin=(ip,port)

# Conexão do socket 
socket_server.bind(origin)

print('Aguardando inicio da conexão ...')

# Aguarda a conexão do usuário
socket_server.listen(1)

# Aceitação da conexão
[socket_dados,info_cliente]=socket_server.accept()

####################################################################################################################################

# Cria uma flag para verificar se o cliente ainda está ativo
client_session = True

# Verifica os envios de mensagem do cliente
while client_session:
    
    # Recebe o tamanho da mensagem do cliente
    tam_mensagem = socket_dados.recv(2)
    
    # Verifica se o cliente enviou alguma mensagem caso não, encerra a conexão
    if not tam_mensagem:
        print("Cliente desconectado")
        client_session=False
    else:
        # Decodifica a opção escolhida pelo cliente
        option=int.from_bytes(socket_dados.recv(1),'big')
        
        ####### VERIFICAÇÃO DAS OPERAÇÕES ####### 
        # REALIZA A ADIÇÃO DE UM NOVO COMPONENTE #
        if(option==1):
            # Decodifica a mensagem do cliente e as atribui as suas respectivas variaveis
            name,price, quantity=decode_message(socket_dados)
            
            # Cria um novo componente
            component=EletronicComponent(name,price,quantity)
            component.show_component() # Imprime dados do componente
            
            # Adiciona o componente a uma lista
            components_list[component.id]=component
            
            # Envio de mensagem de confirmação para o cliente
            conf_message=f"!!!! Componente {component.name} foi inserido com o id: {component.id} !!!"
            tam_conf_message=len(conf_message.encode())
            pacote_message=tam_conf_message.to_bytes(1,'big')+conf_message.encode()
            
            # Monta o pacote para enviar ao cliente
            pacote_resposta=len(pacote_message).to_bytes(1,'big')+pacote_message
            
            # Envia mensagem para o cliente
            
            socket_dados.send(pacote_resposta)
        
        # REALIZA A LEITURA DO COMPONENTE #    
        elif(option==2):
            
            # Decodifica o id do componente
            id_component=int.from_bytes(socket_dados.recv(2),'big')
            
            # Verifica se o componente existe na lista de componentes
            # Se existir monta uma mensagem para enviar ao cliente com as infos
            if id_component in components_list:                
                info_message= "Componente encontrado -> " + components_list[id_component].show_component() + "| ID: " + str(id_component)
                tam_info_message=len(info_message.encode())                
                pacote_message=tam_info_message.to_bytes(1,'big') + info_message.encode()
                
                # Monte o pacote de resposta para o cliente
                pacote_resposta=len(pacote_message).to_bytes(1,'big')+ pacote_message
                                
                socket_dados.send(pacote_resposta)
            
            # Se não existir monta um pacote com uma mensagem de erro
            else: 
                
                error_message(id_component,option)
                        
        # REALIZA A ATUALIZAÇÃO DO COMPONENTE #
        elif(option==3):
            
            # Decodifica o id do componente
            id_component=int.from_bytes(socket_dados.recv(2),'big')
            
             # Verifica se o componente existe na lista de componentes
            # Se existir atualiza e monta uma mensagem para enviar ao cliente com as infos
            if id_component in components_list:             
                # Decodifica a mensagem do cliente e as atribui as suas respectivas variaveis
                name,price, quantity=decode_message(socket_dados)   
                
                # Atualiza os atributos do componente
                components_list[id_component].update_component(name,price,quantity)
                components_list[id_component].show_component()                
                
                # Envia mensagem de confirmação para o cliente
                update_message=  f"Componente Atualizado -> {components_list[id_component].show_component()} "
                tam_update_message=len(update_message.encode())                
                pacote_message=tam_update_message.to_bytes(1,'big') + update_message.encode()
                
                # Monte o pacote de resposta para o cliente
                pacote_resposta=len(pacote_message).to_bytes(1,'big')+ pacote_message
                                
                socket_dados.send(pacote_resposta)
            
            # Se não existir monta um pacote com uma mensagem de erro
            else: 
                
                error_message(id_component,option)            
                    
         # REALIZA A EXCLUSÃO DO COMPONENTE #
        elif option==4:
            
         # Decodifica o id do componente
            id_component=int.from_bytes(socket_dados.recv(2),'big')        
         # Verifica se o componente existe na lista de componentes
         # Se existir exclui e monta uma mensagem para enviar ao cliente com as infos
            if id_component in components_list:    
                components_list.pop(id_component)        
                         
                info_message= f"!!! Componente com o id {id_component} excluido com sucesso !!!" 
                tam_info_message=len(info_message.encode())                
                pacote_message=tam_info_message.to_bytes(1,'big') + info_message.encode()
                
                # Monte o pacote de resposta para o cliente
                pacote_resposta=len(pacote_message).to_bytes(1,'big')+ pacote_message
                                
                socket_dados.send(pacote_resposta)
            
            # Se não existir monta um pacote com uma mensagem de erro
            else: 
                
                error_message(id_component,option)
            
####################################################################################################################################

# Encerramento do socket de dados e do socket de conexão
socket_dados.close()
socket_server.close()

input('\n\tDigite enter para encerrar ...')