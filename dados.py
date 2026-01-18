import json
import os
from jogo import Jogo, JogoPc, JogoMobile, JogoConsole
from colecoes import Colecao
import config

ARQUIVO_JOGOS = config.ARQUIVO_JOGOS

def salvar_tudo(dicionario_colecoes):
    dados_para_salvar = {}

    # Itera sobre cada coleção e exporta seus jogos
    for nome_colecao, objeto_colecao in dicionario_colecoes.items():
        lista_exportada = []
        for jogo in objeto_colecao.jogos:
            if hasattr(jogo, 'exportar_dados'):
                lista_exportada.append(jogo.exportar_dados())
        
        # Salva a lista de jogos dentro da chave com o nome da coleção
        dados_para_salvar[nome_colecao] = lista_exportada

    try:
        with open(ARQUIVO_JOGOS, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
        print("✅ Todas as coleções foram salvas.")
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")

def carregar_tudo():
    # Se não existe arquivo, retorna um dicionário com a coleção padrão vazia
    if not os.path.exists(ARQUIVO_JOGOS):
        col_default = Colecao("Minha coleção")
        return {"Minha coleção": col_default}

    try:
        with open(ARQUIVO_JOGOS, 'r', encoding='utf-8') as f:
            dados_brutos = json.load(f)

        dicionario_final = {}

        # Itera sobre cada coleção no JSON (ex: "Minha coleção", "Favoritos")
        for nome_colecao, lista_jogos_json in dados_brutos.items():
            nova_colecao = Colecao(nome_colecao)
            
            # Recria os jogos desta coleção
            for item in lista_jogos_json:
                tipo = item.pop("tipo_classe", None)
                status_salvo = item.pop("status", None)
                item.pop("plataforma", None)
                item.pop("console", None) 

                novo_jogo = None
                try:
                    if tipo == "JogoPc":
                        novo_jogo = JogoPc(**item)
                    elif tipo == "JogoMobile":
                        novo_jogo = JogoMobile(**item)
                    elif tipo == "JogoConsole":
                        novo_jogo = JogoConsole(**item)
                    else:
                        print(f"Tipo desconhecido: {tipo}")
                        continue
                    
                    # Restaura o status
                    if novo_jogo and status_salvo:
                        try:
                            # Tenta forçar o status salvo
                            novo_jogo.status = status_salvo
                        except:
                            pass
                    
                    if novo_jogo:
                        # Registra o jogo na coleção
                        nova_colecao.jogos.append(novo_jogo) 
                
                except Exception as e:
                    print(f"Erro ao carregar jogo: {e}")
            
            # Guarda a coleção pronta no dicionário
            dicionario_final[nome_colecao] = nova_colecao

        return dicionario_final

    except Exception as e:
        print(f"Erro crítico ao carregar: {e}")
        return {"Minha coleção": Colecao("Minha coleção")}