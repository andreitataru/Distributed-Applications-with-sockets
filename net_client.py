#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - net_client.py
Grupo: 23
Números de aluno: 53746, 51153, 51220
"""

# zona para fazer importação

import sock_utils
import pickle, struct
import time

###############################################################################
# definição da classe server 

class server:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.socket = None
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização do
        objeto.
        """
        self.socket = sock_utils.create_tcp_client_socket(self.address, self.port)

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna a
        resposta recebida pela mesma socket.
        """
        try:
            data_bytes = pickle.dumps(data, -1)
            data_size_bytes = struct.pack('!i', len(data_bytes))
            self.socket.sendall(data_size_bytes)
            self.socket.sendall(data_bytes)

            response = ""
            response_size_bytes = self.socket.recv(4)
            response_bytes = sock_utils.receive_all(self.socket, struct.unpack('!i', response_size_bytes)[0])
            response = pickle.loads(response_bytes)
        except:
            print("Connection lost, server disconnected")
            self.socket.close()
            exit()
        return response 
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.socket.close()
