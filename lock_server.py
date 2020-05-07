#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_server.py
Grupo: 23
Números de aluno: 53746, 51153, 51220
"""

# Zona para fazer importação

import sys, os, pickle, struct, sock_utils, traceback, select as sel, socket as s
from lock_pool import lock_pool
from lock_skel import lock_skel

###############################################################################

# código do programa principal

HOST = '127.0.0.1'

try:
    PORT = int(sys.argv[1])
    N = int(sys.argv[2])  #Numero de recursos
    K = int(sys.argv[3])  #Numero de bloqueios por cada recurso
    Y = int(sys.argv[4])  #Numero permitido de recursos bloqueados num dado momento
    T = int(sys.argv[5])  #Tempo maximo de concessão de bloqueio
except:
    print("Insert command in format: ./lock_server.py PORT N K Y T")
    exit()

print("Número de recursos: ", N)
print("Número de bloqueio por cada recurso: ", K)
print("Número permitido de recursos bloqueados num dado momento: ", Y)
print("Tempo máximo de concessão de bloqueio: ", T)

skel = lock_skel(N, K, Y, T)
ListenSocket = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
SocketList = [ListenSocket, sys.stdin]

while True:
    try:
        R, W, X = sel.select(SocketList, [], []) # Espera sockets com
        for sckt in R:
            if sckt is ListenSocket: # Se for a socket de escuta...
                conn_sock, addr = ListenSocket.accept()
                addr, port = conn_sock.getpeername()
                print("New connection: ", "Address: ", addr, "Port: ", port)
                SocketList.append(conn_sock) # Adiciona ligação à lista
            elif sckt is sys.stdin:
                command = sys.stdin.readline()
                if command == 'EXIT\n':
                    exit()
            else: # Se for a socket de um cliente...
                #Verificações de locks
                skel.clear_expired_locks()
                skel.check_Y_K()
                msg_size_byte = sckt.recv(4)
                if msg_size_byte: # Se recebeu dados
                    #Receber
                    msg_size = struct.unpack('!i', msg_size_byte)[0]
                    msg = sock_utils.receive_all(sckt, msg_size)
                    #Processar
                    response = skel.process_message(msg)
                    response_size = struct.pack('!i', len(response))
                    #Responder
                    sckt.sendall(response_size)
                    sckt.sendall(response)
                    print(skel.lockpool)
                else: #Se cliente terminou ligação
                    addr, port = sckt.getpeername()
                    print("Connection closed: ", "Address: ", addr, "Port: ", port)
                    sckt.close()
                    SocketList.remove(sckt)

    except Exception as e:
        traceback.print_exc()
            
SocketList.close()

