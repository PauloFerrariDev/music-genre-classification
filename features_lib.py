# -*- coding: utf-8 -*-
"""
Created on Sat May 25 20:21:30 2024

@author: aiurkiv
"""
import os
import librosa
import numpy as np
#import sounddevice as sd

# Retorna um vetor com a média dos valores das linhas de uma matriz
def media_linhas(matriz):
    medias = [sum(linha) / len(linha) for linha in matriz]
    return medias

# Recebe o endereço de um diretório como parâmetro e retorna o nome dos arquivos
# .wav do diretório.
def listar_nomes_de_arquivos(diretorio):
    nome_arquivo = []
    for nome_arq in os.listdir(diretorio):
        if nome_arq.endswith('.wav'):
            nome_arquivo.append(nome_arq)
    return nome_arquivo

# Retorna um vetor com as subpastas do diretório informado
def listar_subpastas(diretorio):
    subpastas = [nome for nome in os.listdir(diretorio) if os.path.isdir(os.path.join(diretorio, nome))]
    return subpastas

# Aqui insiro o cabeçalho
def cabecalho():
    cabec = []
    cabec.append('Nome do arquivo')
    for i in range (0, 20):
        cabec.append('mfcc' + '{:02d}'.format(i))
    return cabec

def extrair_vetor_features(data, sr):
    return media_linhas(librosa.feature.mfcc(y=data, sr=sr))

# Definição dos diretórios principais
diretorio_audios = './audios'
diretorio_features = './features'

matriz_banco = []
matriz_banco.insert(0, cabecalho())


# cria o diretório principal das features
if not os.path.exists(diretorio_features):
    os.makedirs(diretorio_features)

diretorios_musicas = listar_subpastas(diretorio_audios) # Carrega nome das pastas com as músicas

for nome_diretorio in diretorios_musicas:               # Loop para ler todos as pastas
    i = 0;
    nome_diretorio_full = diretorio_audios + '/' + nome_diretorio
    nomes_arquivos = listar_nomes_de_arquivos(nome_diretorio_full)  # Carrega nome das músicas da pasta
    for nome_arquivo in nomes_arquivos:
        contador = '{:02d}'.format(i)
        nome_audio_full = os.path.join(nome_diretorio_full, nome_arquivo)
        data, sr = librosa.load(nome_audio_full)
        matriz_banco.append([nome_diretorio + contador] + extrair_vetor_features(data, sr))
        i+=1
np.savetxt(os.path.join(diretorio_features, "xxx.csv"), matriz_banco, delimiter=';')
        
        
        


    
    