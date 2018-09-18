#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Kened Wanderson Cruz OLiveira
Engenharia de Computação
2016.2 - Sistemas Operacionais

Os algoritmos de substituição de páginas implementados:
¤ FIFO (First In, First Out)
¤ OTM: Algoritmo Ótimo
¤ LRU: (Least Recently Used o u Menos Recentemente Utilizado)
'''

'''
Programa deve ser intepretado em Python3
Entrada via terminal do arquivo de entrada e o de saida, como descrito a baixo:

# python3 paginação.py entrada.txt saida.txt 

'''

import sys

def main():
	entrada = sys.argv[1]
	saida = sys.argv[2]
	arq = open(entrada, 'r')
	log = open(saida, 'a')
	
	date = arq.readlines()
	
	log.write("FIFO ")	
	log.write(str(FIFO(date[:])))	

	log.write("\nOTM ")	
	log.write(str(OTM(date[:])))	

	log.write("\nLRU ")	
	log.write(str(LRU(date[:])))	

	arq.close()
	log.close()

def FIFO(data):
	faltas = j = 0
	Mram = []
	quadros = int(data[0])
	del data[0]
	[Mram.append("kened") for k in range(quadros)] #preenchendo os espaços da RAM com um valor vazio
	
	for i in range(len(data)): #enquanto tiver o que ser precessado
		if(j == quadros): #deixar a ram circular
			j=0
		if(Mram.count(data[i]) == 0): # se não tiver a pagina na RAM
			Mram[j] = data[i]
			faltas+=1
			j+=1
		#print("RAM:",Mram,"\tf:",faltas,"\tj",j)#DEBUG
	return faltas

def OTM(data):
	faltas = j = 0
	Mram = []
	menor = []

	quadros = int(data[0]) # captura o tamanho da ram
	del data[0] #deleta o tamanho da ram da nossa lista
	[Mram.append(data[k]) for k in range(quadros)] #carrega a ram
	faltas = quadros #como a ram foi preenchida, o valor foi atribuido ao numero de faltas de paginas
	data = data[quadros:] #apaga o que foi consumido
	[menor.append(0) for k in range(quadros)] #preenchendo os espaços do menor com distancia 0
	
	for i in range(len(data)): #enquanto estiver o que processar
		#print("Ram:",Mram,"\tf:",faltas,"\tmenor:",menor,"\tdata:",data[i],"\nDATA:",data) #DEBUG
		if(j == quadros): #deixar a ram circular
			j=0
		if(Mram.count(data[i]) == 0): # se não tiver a pagina na RAM
			distancia(menor,data[i:],Mram) # calcula a distancia de cada pagina na ram, com a pagina na data
			if(menor.index(max(menor)) == j):
				Mram[j] = data[i]
				j+=1
				faltas+=1
			else:
				Mram[menor.index(max(menor))] = data[i]
				j = menor.index(max(menor))
				faltas+=1
			
	return faltas

def LRU(data):
	Mram = []
	quadros = int(data[0]) # captura o tamanho da ram
	del data[0] #deleta o tamanho da ram da nossa lista
	[Mram.append(data[k]) for k in range(quadros)] #carrega a ram
	data = data[quadros:] #apaga o que foi consumido
	faltas = quadros #como a ram foi preenchida, o valor foi atribuido ao numero de faltas de paginas

	for i in range(len(data)): #enquanto estiver o que processar
		if(Mram.count(data[i]) == 0): # se não tiver a pagina na RAM
			Mram[0] = data[i]
			faltas+=1
			troca(Mram,data,i)# troca a prioridade da pagina para maior
		else:
			troca(Mram,data,i) # troca a prioridade da pagina para maior
		#print("Mram:",Mram,"\tf:",faltas) #DEBUG		
	return faltas

def troca(Mram,data,i):
	aux = Mram[Mram.index(data[i])]
	del Mram[Mram.index(data[i])]
	Mram.append(aux)

def distancia(menor,data,Mram):
	for i in range(len(Mram)):
		for j in range(len(data)):
			if(Mram[i] == data[j]): 
				menor[i] = j+1
				break
			else: # se não tiver proximo, recebe a maior prioridade de escolha
				menor[i] = 999
				
if __name__ == "__main__":
    main()
