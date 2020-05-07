#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_pool.py
Grupo: 23
Números de aluno: 53746, 51153, 51220
"""
# Zona para fazer importação

import time

###############################################################################

class resource_lock:
    def __init__(self, rId):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.id = rId
        self.lockTime = 0
        self.nTimesLocked = 0
        self.isInactive = False
        self.isLocked = False
        self.lockStartTime = 0

    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        if self.isInactive == False:
            if self.isLocked == False:
                self.isLocked = True
                self.lockTime = time_limit
                self.client_id = client_id
                self.lockStartTime = time.time()
                self.nTimesLocked += 1
                return True
            elif self.isLocked == True:
                if self.client_id == client_id:
                    self.lockTime = time_limit
                    self.lockStartTime = time.time()
                    self.nTimesLocked += 1
                    return True
        return False

    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.isLocked = False

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """
        if int(self.client_id) == int(client_id):
            self.isLocked = False
            return True
        else:
            return False

    def status(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se 
        encontre inativo.
        """
        return [self.isLocked, self.isInactive]
    
    def stats(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado em k.
        """
        return self.getNtimesLocked()

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.isInactive = True

    def getNtimesLocked(self):
        """
        Devolve o numero de vezes que o recurso foi blockeado
        """
        return self.nTimesLocked

    def calcRemainingTime(self, timeNow):
        """
        Calcula o tempo que resta de bloqueio
        Retorna True se o tempo de bloqueio terminou e False se ainda nao
        """
        t = timeNow - self.lockStartTime
        timeLeft = self.lockTime - t
        return timeLeft

###############################################################################

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao 
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado 
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um 
        recurso seja libertado.
		Define T, o tempo máximo de concessão de bloqueio.
        """
        self.resources = []
        self.K = K
        self.Y = Y
        self.N = N
        self.T = T
        self.locksAllowed = True
        for i in range(0, N):
            self.resources.append(resource_lock(i))
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for resource in self.resources:
            if resource.status()[0] == True and resource.status()[1] == False:
                if resource.calcRemainingTime(time.time()) <= 0:
                    resource.urelease()

    def check_resources_K_stats(self):
        """
        Verifica se existem recursos que já atingiram os K bloqueios permitidos, e desativa 
        estes recursos;
        """
        for resource in self.resources:
            if resource.stats() >= self.K:
                resource.disable()

    def check_resources_Y_stats(self):
        """
        Verifica se o número de recursos bloqueados num dado momento já atingiu Y, e não
        permite bloqueios a novos recursos;
        """
        if self.ystats()[0] >= self.Y:
            self.locksAllowed = False
        else:
            self.locksAllowed = True

    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não 
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi 
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """
        if self.validade_resource_id(resource_id):
            if self.locksAllowed == True and time_limit <= self.T:
                return self.resources[resource_id].lock(client_id, time_limit)
            else:
                return False
        else:
            return None

    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """
        if self.validade_resource_id(resource_id):
            return self.resources[resource_id].release(client_id)
        else:
            return None

    def status(self,resource_id):
        """
        Retorna o estado do recurso numa lista [isBlocked, isDisabled]
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se
        encontre inativo.
        """
        if self.validade_resource_id(resource_id):
            status = self.resources[resource_id].status()
            if status[1] == True:
                return "disabled"
            else:
                return status[0]
        else: 
            return None

    def stats(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos 
        K bloqueios permitidos.
        """
        if self.validade_resource_id(resource_id):
            return [self.resources[resource_id].stats(), self.K]
        else:
            return None

    def ystats(self):
        """
        Retorna o número de recursos bloqueados num dado momento do Y permitidos.
        """
        nRecLock = 0
        for resource in self.resources:
            if resource.status()[0] == True:
                nRecLock += 1
        return [nRecLock, self.Y] 

    def validade_resource_id(self, resource_id):
        """
        Valida o id do recurso
        """
        return resource_id <= len(self.resources) - 1 and resource_id >= 0

    def nstats(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        recDisp = 0
        for resource in self.resources:
            if resource.status()[1] == False and resource.status()[0] == False:
                recDisp += 1
        return recDisp
		
    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output = ""
        #
        # Acrescentar na output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        # Caso o recurso não esteja inativo a linha é simplesmente da forma:
        # recurso <número do recurso> inativo
        #
        for resource in self.resources:
            if resource.status()[1] == True:
                output += "Recurso " + str(resource.id) + " inativo" + "\n"
            if resource.status()[1] == False and resource.status()[0] == True:
                output += "Recurso " + str(resource.id) + " bloqueado pelo cliente " + str(resource.client_id) + " até " + str(resource.calcRemainingTime(time.time())) + "\n"
            else:
                output += "Recurso " + str(resource.id) + " desbloqueado" + "\n"
        output += "--------------------------------"
        return output