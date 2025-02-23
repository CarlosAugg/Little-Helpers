import os

def listar_nomes_dos_arquivos(pasta):
    itens = os.listdir(pasta)
    nomes = []

    for item in itens:
        caminho_completo = os.path.join(pasta, item)
        if os.path.isfile(caminho_completo):
           
            nome_sem_extensao = os.path.splitext(item)[0]
            nomes.append(nome_sem_extensao)
        else:
         
            nomes.append(item)

    return nomes

def salvar_em_texto(nomes, caminho_arquivo_texto):
   
    with open(caminho_arquivo_texto, 'w') as f:
        for nome in nomes:
            f.write(f"{nome}\n")

def main():
    pasta = input("Digite o caminho da pasta: ")
    nome_arquivo = input("Digite o nome do arquivo (sem extensão, ex: arquivos): ")
    
  
    nome_arquivo_com_extensao = f"{nome_arquivo}.txt"
    

    if not os.path.isdir(pasta):
        print("A pasta especificada não existe.")
        return
    
    nomes = listar_nomes_dos_arquivos(pasta)
    
 
    caminho_arquivo = os.path.join(pasta, nome_arquivo_com_extensao)
    
    salvar_em_texto(nomes, caminho_arquivo)

    print(f"Os nomes dos arquivos e pastas foram salvos em {caminho_arquivo}")

if __name__ == "__main__":
    main()