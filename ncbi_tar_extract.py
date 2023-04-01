#!/usr/bin/env python3
# coding: utf-8

import os
import shutil
import argparse

parser = argparse.ArgumentParser(
    description='Welcome')
parser.add_argument('-i', '--input', metavar='', type=str, required=True,
                    help='Valid directory with the files')
args = parser.parse_args()

folder_input = os.path.expanduser(f'{args.input}')

os.chdir(folder_input)


def descompactar_arquivos_targz(folder_input):
    os.chdir(folder_input)
    for arquivo in os.listdir():
        if arquivo.endswith('.tar'):
            os.system('tar -xf ' + str(arquivo))

def gunzip_arquivos(folder_input):
    os.chdir(folder_input)
    for pasta in os.listdir():
        if os.path.isdir(os.path.join(pasta)):
            os.chdir(os.path.abspath(pasta))
            for arquivos_gz in os.listdir():
                if arquivos_gz.endswith('.gz'):
                    os.system("gunzip " + str(arquivos_gz)) 

extensoes = ['.fna', '.faa', '.fasta']
def mover_arquivos_para_pasta_anterior(folder_input):              
        
        for file in os.listdir():
            for extensao in extensoes:
                if file.endswith(extensao):   
                    caminho_do_file = (os.path.join(os.getcwd(), file))
                    novo_caminho = os.path.join(folder_input , file)
                    shutil.move(caminho_do_file, novo_caminho)

def renomear_arquivos(folder_input):
    os.chdir(folder_input)
    for arquivos in os.listdir():
        for extensao in extensoes:
            if arquivos.endswith(extensao): 
                with open(arquivos, "r") as file:
                    first_line = file.readline().split()
                    if len(first_line) > 2:
                        sp_name = first_line[1][0] + first_line[2]
                        if 'strain' in first_line:
                            strain = first_line[4]
                        else:
                            strain = first_line[0].replace(">","")
                            print(f"Could not rename {arquivos} properly, changed to NCBI'ID")
                        strain_final = strain.replace(" ", "_").replace("(", "").replace(")", "").replace(";","").replace(",","").replace("/","").replace("|","").replace("\\","").replace("[","").replace("]","")
                        caminho_inicial = (os.path.join(os.getcwd(), arquivos))
                        caminho_final = (os.path.join(os.getcwd(), strain_final) + extensao)
                        os.rename(caminho_inicial, caminho_final)
                    else: 
                                  
                        print(f"Could not rename {arquivos} properly, please rename it manually.")
                        
def deletar_arquivos_desnecessarios(folder_input):
    os.chdir(folder_input)
    for arquivos_para_deletar in os.listdir():
        caminho_completo_do_arquivo = os.path.join(os.getcwd(), arquivos_para_deletar)
        if os.path.isdir(caminho_completo_do_arquivo) and "ncbi-genomes" in arquivos_para_deletar:
            shutil.rmtree(caminho_completo_do_arquivo)
        elif os.path.isfile(caminho_completo_do_arquivo) and arquivos_para_deletar == 'report.txt':
            os.remove(caminho_completo_do_arquivo)
    
def processar_arquivos(folder_input):
    descompactar_arquivos_targz(folder_input)
    gunzip_arquivos(folder_input)
    mover_arquivos_para_pasta_anterior(folder_input)
    renomear_arquivos(folder_input)
    deletar_arquivos_desnecessarios(folder_input)
        

if __name__ == '__main__':
    processar_arquivos(folder_input)

    """ O if __name__ == '__main__': é uma verificação comum que se faz em Python para checar 
se o script está sendo executado diretamente ou se está sendo importado como um módulo 
em outro script. Se ele estiver sendo executado diretamente, ou seja, se o módulo for
o programa principal, então a função processar_arquivos() será chamada. """