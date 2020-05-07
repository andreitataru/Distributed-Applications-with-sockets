#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - sock_utils.py
Grupo: 23
Números de aluno: 53746, 51153, 51220
"""
# Zona para fazer importação

import socket as s

###############################################################################

def create_tcp_server_socket(address, port, queue_size):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(queue_size)
    return sock

def create_tcp_client_socket(address, port):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((address, port))
    return sock

def receive_all(socket, length):
    recebido = b""
    while len(recebido) < length:
        message = socket.recv(length - len(recebido))
        recebido += message
        if not message:
            return recebido
    return recebido