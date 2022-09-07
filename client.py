####################################################################################################################################
#                                             CRUD - Estoque de componentes eletrônicos                                            #
#                                           Alunas: Eduarda S. Gavião e Fernanda Azevedo                                           #
#                                                          CLIENT                                                                  #
####################################################################################################################################
#                                             DISCIPLINA :  SISTEMAS DISTRIBUÍDOS                                                  #
####################################################################################################################################
# Bibliotecas
from email import message
from operator import le
import socket
####################################################################################################################################
# Funções

# Menu de opções do CRUD
def menu():
    menu_options = """
     ************************************************************
     ***** MENU - CRUD - ESTOQUE DE COMPONENTES ELETRÔNICOS *****
     ************************************************************
     Escolha uma das opções:
     [1] Adicionar um componente eletrônico
     [2] Buscar um componente eletrônico
     [3] Atualizar um componente eletrônico 
     [4] Deletar um componente eletrônico
     [5] Sair
     ************************************************************
    """
    
    print(menu_options)

# Menu para adicionar o  componente eletrônico
def add_component():
    
    name= input("\tInsira o nome do componente eletrônico: ")    
    price=input("\tInsira o valor do componente eletrônico: ")
    quantity = input("\tInsira a quantidade dos componentes eletrônicos: ")
        
    return name, price, quantity

# Realiza a conversão das informações 
def convert_bytes_add(option,name,price,quantity):
    
    # Converte as opções para bytes
    option_bytes =option.to_bytes(1,'big')
       
    # Codifica e converte o nome para bytes
    name_bytes = name.encode('utf-8')
    tam_name_bytes = len(name_bytes).to_bytes(1, 'big')    
       
    # Converte o preço para bytes
    price_bytes =price.to_bytes(1,'big')    
    
    # Converte a quantidade para bytes
    quantity_bytes =quantity.to_bytes(1,'big')
        
    # MONTAGEM DOS PACOTES
    pacote = option_bytes + tam_name_bytes + name_bytes + price_bytes + quantity_bytes
    tam_pacote=len(pacote).to_bytes(2,'big')
    
    return pacote, tam_pacote
    
# Menu para atualizar o  componente eletrônico
def update_component():
    
    id_component = input("\t Insira o id do componente eletrônico que deseja atualizar: ")
    name= input("\t Insira o nome do componente eletrônico: ")    
    price=input("\t Insira o valor do componente eletrônico: ")
    quantity = input("\t Insira a quantidade dos componentes eletrônicos: ")
    
    return id_component, name, price, quantity

def convert_bytes_update(option,id_component,name,price,quantity):
    
    # Converte as opções para bytes
    option_bytes =option.to_bytes(1,'big')
    
    # Converte o id dos componentes para bytes
    id_component_bytes = id_component.to_bytes(2,'big')
        
    # Codifica e converte o nome para bytes
    name_bytes = name.encode('utf-8')
    tam_name_bytes = len(name_bytes).to_bytes(1, 'big')    
       
    # Converte o preço para bytes
    price_bytes =price.to_bytes(1,'big')    
    
    # Converte a quantidade para bytes
    quantity_bytes =quantity.to_bytes(1,'big')
    
    # MONTAGEM DOS PACOTES
    pacote = option_bytes + id_component_bytes + tam_name_bytes + name_bytes + price_bytes+quantity_bytes
    tam_pacote=len(pacote).to_bytes(2,'big')
    
    return pacote, tam_pacote
# Recebe e imprime a mensagem do servidor
def server_message():
    
    # Recebe o pacote do servidor
    socket_client.recv(1)
    
    #Decodficação da mensagem do servidor
    tam_mensagem = int.from_bytes(socket_client.recv(1),'big')
    mensagem = socket_client.recv(tam_mensagem).decode()
    
    # Imprime a mensagem do servidor
    print(f"\nMensagem do servidor: \n\t{mensagem}")

# Verifica se a operação pode ser convertida para inteiro
def convert_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False
    
####################################################################################################################################
# Criação e configuração do socket
socket_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Definição IP e porta
ip='127.0.0.1'
port=50000
dest=(ip,port)

# Conexão ao servidor, permanece bloqueado até ser aceito
socket_client.connect(dest)

####################################################################################################################################
# Aplicação

option = 0

while option!=5:
    
    # Imprime o menu de opções
    menu()
    
    # Seleciona a operação a ser realizada
    option = input ("Insira a operação:")
    
    # Verifica se a operação inserida é valida
    if option:
        if convert_int(option):
            option=int(option)
        else:
           print("\n\t !!! Operação inválida inserida  - Tente novamente !!!")
           continue
    else:
      print("\n\t!!! Operação não inserida - Tente novamente !!!")   
      continue
    
    ####### VERIFICAÇÃO DAS OPERAÇÕES ####### 
    
    if option>= 1 and option<=4:
    # OPERAÇÃO DE ADIÇÃO DE COMPONENTES #
      if option ==1:
         name,price,quantity= add_component()
       
        # Verifica se é possível inserir os preços e quantidades
         if convert_int(price):
             price = int(price)
          
         else:
             print("\n\t !!! Preço inserido é inválido !!! ")
             continue

         if convert_int(quantity):
             quantity = int(quantity)
         else:
             print("\n\t !!! Quantidade inserida é inválida - Tente novamente !!!")
             continue
        
        # Formatação do pacote
         pacote, tam_pacote= convert_bytes_add(option,name,price,quantity)
       
        # Envia pacote para o servidor  
         socket_client.send(tam_pacote+pacote)
       
        # Verifica o recebimento da mensagem do servidor
         server_message()
        
    # OPERAÇÃO DE LEITURA #
      elif option==2:
        # Informa o id a ser lido
         id_component= input("\tInsira o nome do componente eletrônico: ")    
        
        # Verifica se é possível realizar a conversão do id desejado
         if convert_int(id_component):
             id_component = int(id_component)
         else:
             print("\n\t !!! ID inválido inserido - Tente novamente !!!")
             continue
        
        # Realiza a montagem do pacote para busca
         busca_mensagem = option.to_bytes(1,'big') + id_component.to_bytes(2,'big')
         pacote = len(busca_mensagem).to_bytes(2,'big') + busca_mensagem
        
        # Realiza o envio do pacote
         socket_client.send(pacote)
        
        # Verifica o recebimento da mensagem do servidor
         server_message()
    
    # OPERAÇÃO DE ATUALIZAÇÃO #
      elif option ==3:
        # Chama a função para atualizar os valores
         id_component, name,price,quantity= update_component()
        
        # Verifica se é possível realizar a conversão do id desejado
         if convert_int(id_component):
             id_component = int(id_component)
         else:
             print("\n\t !!! ID inválido inserido - Tente novamente !!!")
             continue
       
        # Verifica se é possível inserir os preços 
         if convert_int(price):
             price = int(price)
          
         else:
             print("\n\t !!! Preço inserido é inválido !!! ")
             continue
        
        # Verifica se é possível inserir as quantidades
         if convert_int(quantity):
             quantity = int(quantity)
         else:
             print("\n\t !!! Quantidade inserida é inválida - Tente novamente !!!")
             continue
       
       # Formatação do pacote
         pacote, tam_pacote= convert_bytes_update(option,id_component,name,price,quantity)
       
       # Envia pacote para o servidor  
         socket_client.send(tam_pacote+pacote)
       
       # Verifica o recebimento da mensagem do servidor
         server_message()
     
      # DELETAR COMPONENTE #
      elif option==4:
          # Informa o id a ser excluido
         id_component= input("\tInsira o nome do componente eletrônico que deseja excluir: ")  
         # Verifica se é possível realizar a conversão do id desejado
         if convert_int(id_component):
             id_component = int(id_component)
         else:
             print("\n\t !!! ID inválido inserido - Tente novamente !!!")
             continue
          
        # Realiza a montagem do pacote para excluir
         busca_mensagem = option.to_bytes(1,'big') + id_component.to_bytes(2,'big')
         pacote = len(busca_mensagem).to_bytes(2,'big') + busca_mensagem
        
        # Realiza o envio do pacote
         socket_client.send(pacote)
        
        # Verifica o recebimento da mensagem do servidor
         server_message()
        
    elif option==5:
        socket_client.close()
        
    