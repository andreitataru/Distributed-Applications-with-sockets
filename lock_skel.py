#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_skel.py
Grupo: 23
Números de aluno: 53746, 51153, 51220
"""
# Zona para fazer importação

import pickle, struct
from lock_pool import lock_pool

###############################################################################

class lock_skel:
    def __init__(self, N, K, Y, T):
        self.lockpool = lock_pool(N, K , Y, T)

    def process_message(self, msg_bytes):
        command = self.bytesToList(msg_bytes)
        response = []
        if command[0] == 10:
            response = [11, self.lockpool.lock(int(command[2]), int(command[3]), int(command[1]))]
        if command[0] ==  20:
            response = [21, self.lockpool.release(int(command[1]), command[2])]
        if command[0] == 30:
            response = [31, self.lockpool.status(int(command[1]))]
        if command[0] == 40:     
            response = [41, self.lockpool.stats(int(command[1]))]
        if command[0] == 50:
            response = [51, self.lockpool.ystats()]
        if command[0] == 60:
            response = [61, self.lockpool.nstats()]
        
        return self.listToBytes(response)
    
    def clear_expired_locks(self):
        self.lockpool.clear_expired_locks()

    def check_Y_K(self):
        self.lockpool.check_resources_K_stats()
        self.lockpool.check_resources_Y_stats()

    def bytesToList(self, bytes):
        lista = pickle.loads(bytes)
        return lista

    def listToBytes(self, msg):
        msg_bytes = pickle.dumps([msg], -1)
        return msg_bytes