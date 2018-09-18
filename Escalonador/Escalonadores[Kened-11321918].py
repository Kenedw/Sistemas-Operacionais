#!/usr/bin/env python
'''
Kened Wanderson Cruz OLiveira
Engenharia de Computação
2016.2 - Sistemas Operacionais

Escalonador FCFS
Escalonador SJF
Escalonador RR

'''
from itertools import cycle
from operator import itemgetter
import copy


def main():
	matInput = [] # minha matriz de entrada
	k=0

	log = open('output.txt', 'a')
	arq = open('input.txt', 'r')

	FilaPronto = list(map(int,arq.read().split( ))) #tranforma minha str em uma lista
	for j in range(2,len(FilaPronto)+2,2): #Transforma a Lista em matrizes 2x2
		matInput.append(FilaPronto[k:j])
		k=j
#-------------FCFS-----------
	log.write("FCFS ")
	log.write(" ".join([str(round(num,1)) for num in FCFS(matInput)])) # Imprime a lista sem o [ , ]
	log.write('\n')
#-------------SJF------------
	log.write("SJF ")
	log.write(" ".join([str(round(num,1)) for num in SJF(copy.deepcopy(matInput))])) # Imprime a lista sem o [ , ]
	log.write('\n')
#-------------RR-------------
	log.write("RR ")
	log.write(" ".join([str(round(num,1)) for num in RR(copy.deepcopy(matInput))])) # Imprime a lista sem o [ , ]
	log.write('\n')

	arq.close()
	log.close()

'''Escalonamento FCFS - o primeiro que chega é o primeiro a sair, ou seja, será executado primeiro '''
def FCFS(matInput):
	tempos = []
	aux=Rtime=0

	#print ("-------------------FCFS-------------------")#Debugg
	for i in range(len(matInput)):
			aux2 = aux
			aux = aux+ matInput[i][1]
			#print ("Rodar processo [",i,"] de [",aux2,"] ate [",aux,"]")#Debugg
			Rtime += aux2
	Rtime -= atraso(matInput) #tira o atraso do total de picos

	
	tempos.append(float((aux+Rtime)/(i+1))) #Tempo de retorno medio (tempo total)
	tempos.append(float(Rtime/(i+1))) #tempo de resposta medio: intervalo entre a chegada ao sistema e inicio de sua execução	
	tempos.append(float(Rtime/(i+1))) #tempo de espera medio: soma dos períodos em que o programa estava no seu estado pronto. (tempo total que passou esperando)	


	return tempos

def SJF(matInput):
	tempos=[]
	aux=Rtime=k=0
	#print ("-------------------SJF-------------------")#Debugg
	Rtime -= atraso(matInput) #tira o atraso do total de picos
	for i in range(len(matInput)):
		matInput=sorted(matInput, key=itemgetter(0,1))# ordena a matriz 2d
		aux2 = aux
		aux = aux + matInput[0][1]		
		#print ("Rodar processo [",i,"] de [",aux2,"] ate [",aux,"]")#Debugg
		Rtime += aux2

		del matInput[0]
		for j in range(len(matInput)): #faz com que o tempo passe(tempo de atraso, o tempo que o processo chega na CPU)
			if(aux > matInput[j][0]):# zera se o atraso for menor que o tempo decorido
				matInput[j][0] = 0
			else:
				matInput[j][0] -= aux# da a diferença de tempo de atraso passado se ainda tiver restado algum

	tempos.append(float((aux+Rtime)/(i+1))) #Tempo de retorno medio (tempo total)
	tempos.append(float(Rtime/(i+1))) #Tempo de Resposta	medio	
	tempos.append(float(Rtime/(i+1))) #Tempo de espera medio (tempo total que 

	return tempos

def RR(matInput):
	tempos = []
	serv = []
	aux=k=Rtempo=Etime=Rtime=chave=i=tempo=0
	quantum = 2
	tam = len(matInput) # tamanho da entrada
	tempEtime = matInput[tam-1][0]
	tempRtime = matInput[0][0]
	
	#print ("-------------------RR-------------------")#Debugg
	while (countM(serv) != tam):
		while (k != (len(matInput))): #quanto o processo chega no sistema ela é mandada pra fila de prontos
			if((matInput[k][0] <= tempo) & (matInput[k][0] != -1)):
				Etime -= matInput[k][1]
				Rtime += 1
				serv.append(matInput[k][:])
				matInput[k][0] = -1
				k = 0
			else:
				k += 1
		k=0
		# .insert(indice, elemento): insere elemento após a posição índice;
		aux = tempo # tempo inicial
		if(len(serv) != 0):# processa os meus dados num intervalo de quantum, de 1 por 1
			if ((serv[i][1] < quantum) & (serv[i][1] != 0)):
		 		serv[i][1] -= 1
		 		tempo += 1
		 		if(serv[i][1] == 0):
		 			Etime += tempo
		 			Rtempo += tempo
			elif(serv[i][1] != 0):
		 		serv[i][1] -= quantum
			 	tempo += quantum
		 		if(serv[i][1] == 0):
		 			Etime += tempo
		 			Rtempo += tempo

		
		if((i+1 == len(matInput)) & (chave == 0)): # captura o tempo decorrido ate a chegada do ultimo processo(tempo de retorno)
			Rtime = tempo
			chave = 1
			
		if (len(serv) != 0): #entra só se tiver elementos a serem servidos
			'''if ((serv[i][1] != 0) | (countM(serv) == len(serv))): # se não for um processo morto, mostre-o
				print ("Rodar processo [",i,"] de [",aux,"] ate [",tempo,"]")'''#Debugg
			if(i >= len(serv)):
				while(serv[i][1] != 0): #pula um processo ja finalizado
					i += 1
			else:
				i += 1
		else:
			tempo += 1
		if(i == tam): # zera o indice para simular uma lista circular
			i=0
	
	Etime -= tempEtime  
	Rtempo -= tempEtime 
	Rtime -= tempRtime	
	
	tempos.append(float(Rtempo/len(serv))) #Tempo de retorno medio (tempo total)
	tempos.append(float(Rtime/len(serv))) #tempo de resposta medio: intervalo entre a chegada ao sistema e inicio de sua execução	
	tempos.append(float(Etime/len(serv))) #tempo de espera medio: soma dos períodos em que o programa estava no seu estado pronto. (tempo total que passou esperando)	'''

	return tempos

def atraso(matriz): # soma das diferenças(somatorio das diferenças, apartir do primeiro tempo)
	resul= 0
	maximo = matriz[0][0] 
	for i in range(1,len(matriz)):
		resul += maximo - matriz[i][0]
	return abs(resul)

def countM(matriz): # conta quantos 0 tem na coluna 1 de uma matriz
	result = 0
	for i in range(len(matriz)):
		if (matriz[i][1] == 0):
			result += 1
	return result

if __name__ == "__main__":
    main()
