# -*- coding: utf-8 -*-
import os
import sys
import time

# Importações dos módulos do projeto
from jogo import JogoPc, JogoMobile, JogoConsole
from colecoes import Colecao
import dados
import relatorios
import config

# --- Variáveis Globais de Estado ---
CATALOGO = {}     # Dicionário { "Nome": Colecao() }
COLECAO_ATUAL = None # A coleção que o usuário está mexendo agora

def limpar_tela():
    """Limpa a tela do terminal (Windows/Linux/Mac)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione [ENTER] para continuar...")

def ler_inteiro(mensagem):
    """Lê um número inteiro com validação de erro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("❌ Entrada inválida. Digite um número inteiro.")

# --- MENUS AUXILIARES ---

def menu_gerenciar_colecoes():
    """Requisito: Criar listas nomeadas e alternar entre elas"""
    global COLECAO_ATUAL, CATALOGO
    
    while True:
        limpar_tela()
        print("=== 📂 GERENCIAR COLEÇÕES ===")
        print(f"Coleção Ativa: [ {COLECAO_ATUAL.nome} ]")
        print("-" * 30)
        print("Minhas Coleções:")
        for nome in CATALOGO:
            marcador = " (Ativa)" if nome == COLECAO_ATUAL.nome else ""
            qtd = len(CATALOGO[nome].jogos)
            print(f" • {nome} [{qtd} jogos]{marcador}")
        print("-" * 30)
        print("1. Criar Nova Coleção")
        print("2. Mudar Coleção Ativa")
        print("3. Remover Coleção")
        print("0. Voltar")
        
        op = input("Opção: ")
        
        if op == '1':
            nome = input("Nome da nova coleção (ex: Favoritos): ").strip()
            if nome and nome not in CATALOGO:
                CATALOGO[nome] = Colecao(nome)
                print(f"✅ Coleção '{nome}' criada!")
            elif nome in CATALOGO:
                print("❌ Coleção já existe.")
            pausar()
            
        elif op == '2':
            nome = input("Digite o nome da coleção para ativar: ").strip()
            if nome in CATALOGO:
                COLECAO_ATUAL = CATALOGO[nome]
                print(f"✅ Agora você está gerenciando: {nome}")
            else:
                print("❌ Coleção não encontrada.")
            pausar()

        elif op == '3':
            nome = input("Nome da coleção para remover: ").strip()
            if nome == "Minha coleção":
                print("❌ Não é permitido remover a coleção Minha coleção.")
            elif nome in CATALOGO:
                if nome == COLECAO_ATUAL.nome:
                    COLECAO_ATUAL = CATALOGO["Minha coleção"] # Volta pra Minha coleção se deletar a ativa
                del CATALOGO[nome]
                print("✅ Coleção removida.")
            else:
                print("❌ Não encontrada.")
            pausar()

        elif op == '0':
            break

def menu_cadastrar_jogo(colecao_atual):
    limpar_tela()
    print(f"=== 🎮 CADASTRAR NOVO JOGO EM [{colecao_atual.nome}] ===")
    
    titulo = input("Título: ").strip()
    if not titulo:
        print("❌ O título não pode ser vazio.")
        pausar()
        return

    print("\nTipos: [1] PC  [2] Console  [3] Mobile")
    tipo = input("Escolha o tipo: ").strip()

    genero = input("Gênero: ").strip()
    ano = ler_inteiro("Ano de Lançamento: ")
    
    try:
        novo_jogo = None
        
        if tipo == '1': # PC
            novo_jogo = JogoPc(titulo, 0, 0, genero, "", "", ano)
        
        elif tipo == '2': # Console
            console_nome = input("Qual o Console (ex: PS5, Switch)? ").strip()
            novo_jogo = JogoConsole(titulo, 0, 0, genero, "", "", ano, console=console_nome)
        
        elif tipo == '3': # Mobile
            novo_jogo = JogoMobile(titulo, 0, 0, genero, "", "", ano)
        
        else:
            print("❌ Tipo inválido.")
            pausar()
            return

        # Tenta adicionar na coleção (O método adicionar já valida duplicatas e imprime msg)
        colecao_atual.adicionar(novo_jogo)
        
    except Exception as e:
        print(f"❌ Erro ao criar jogo: {e}")
    
    pausar()

def menu_atualizar_progresso(colecao_atual):
    limpar_tela()
    print(f"=== 🔄 ATUALIZAR JOGO EM [{colecao_atual.nome}] ===")
    
    titulo_busca = input("Digite o título do jogo: ").strip()
    jogo = colecao_atual.buscar_por_titulo(titulo_busca)
    
    if not jogo:
        print("❌ Jogo não encontrado.")
        pausar()
        return

    print(f"\nJogo selecionado: {jogo.titulo} ({jogo.status})")
    print(f"Horas atuais: {jogo.horasJogadas}")
    print(f"Nota atual: {jogo.nota}")
    
    print("\nO que deseja fazer?")
    print("1. Adicionar horas jogadas")
    print("2. Finalizar jogo")
    print("3. Avaliar jogo (Dar nota)")
    print("4. Voltar")
    
    opcao = input("Opção: ")
    
    try:
        if opcao == '1':
            horas = float(input("Quantas horas adicionar? "))
            jogo.horasJogadas += horas # Usa o setter do jogo.py
            # Se tiver > 0 horas, o status muda para 'jogando' automaticamente se não estiver finalizado
            if jogo.status == "não iniciado" and jogo.horasJogadas > 0:
                 jogo.status = "jogando"
            print(f"✅ Horas atualizadas! Total: {jogo.horasJogadas}h")

        elif opcao == '2':
            # Tenta mudar status (o setter do jogo valida se tem > 1h)
            jogo.status = "finalizado"
            print("✅ Jogo marcado como FINALIZADO!")

        elif opcao == '3':
            # Tenta dar nota (o setter valida se está finalizado)
            nota = float(input("Nota (0-10): "))
            jogo.nota = nota
            print(f"✅ Nota {nota} registrada!")
                
        elif opcao == '4':
            return
        
    except Exception as e:
        print(f"❌ Calma camarada, {e}")
    
    pausar()

def menu_remover_jogo(colecao_atual):
    limpar_tela()
    print(f"=== 🗑️ REMOVER JOGO DE [{colecao_atual.nome}] ===")
    
    titulo = input("Digite o título do jogo para remover: ").strip()
    if not titulo:
        return

    jogo = colecao_atual.buscar_por_titulo(titulo)
    
    if not jogo:
        print("❌ Jogo não encontrado.")
        pausar()
        return
    
    print(f"\n⚠️  JOGO ENCONTRADO:")
    print(f"   Título: {jogo.titulo}")
    print(f"   Plataforma: {jogo.plataforma}")
    print(f"   Status: {jogo.status}")
    
    confirmacao = input("\nTem certeza que deseja apagar este jogo permanentemente? (S/N): ").lower()
    
    if confirmacao == 's':
        colecao_atual.remover(jogo.titulo, plataforma=jogo.plataforma)
    else:
        print("\n🚫 Operação cancelada.")
    
    pausar()

def menu_filtros(colecao_atual):
    while True:
        limpar_tela()
        print(f"=== 🔍 CONSULTAS E FILTROS [{colecao_atual.nome}] ===")
        print("1. Listar TODOS os jogos")
        print("2. Buscar por parte do título")
        print("3. Filtrar por Status (Jogando/Finalizado...)")
        print("4. Filtro Avançado (Gênero / Plataforma / Nota Mínima)")
        print("5. Ordenar Lista (Tempo / Nota / Ano)")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            colecao_atual.listar()
            pausar()
            
        elif opcao == '2':
            termo = input("Digite parte do título: ")
            resultados = colecao_atual.buscar_por_parte_titulo(termo)
            print(f"\nEncontrados: {len(resultados)}")
            for j in resultados:
                print(f"- {j}") # Usa o __str__ do jogo
            pausar()

        elif opcao == '3':
            print("\nStatus disponíveis: [jogando] [finalizado] [não iniciado]")
            status = input("Qual status deseja ver? ").strip()
            colecao_atual.listar_por_status(status)
            pausar()
            
        elif opcao == '4':
            # Filtro Avançado
            print("\n--- Filtro Avançado (Pressione ENTER para pular um campo) ---")
            genero = input("Gênero específico? ").strip() or None
            plataforma = input("Plataforma específica? ").strip() or None
            
            nota_input = input("Nota mínima (0-10)? ").strip()
            nota_min = float(nota_input) if nota_input else None
            
            print("\nBuscando...")
            resultados = colecao_atual.filtrar_jogos_por(genero=genero, plataforma=plataforma, nota_minima=nota_min)
            
            if resultados:
                print(f"\n✅ Foram encontrados {len(resultados)} jogos:")
                for j in resultados:
                    print(f" • {j}")
            else:
                print("📭 Nenhum jogo atende a esses critérios.")
            pausar()
            
        elif opcao == '5':
            # Ordenação
            print("\nOrdenar por:")
            print("[1] Tempo Jogado")
            print("[2] Avaliação (Nota)")
            print("[3] Ano de Lançamento")
            print("[4] Título (A-Z)")
            
            escolha = input("Escolha: ")
            criterio = 'titulo'
            reverso = True # Padrão: maior para o menor
            
            if escolha == '1': 
                criterio = 'horas'
            elif escolha == '2': 
                criterio = 'nota'
            elif escolha == '3': 
                criterio = 'ano'
            elif escolha == '4': 
                criterio = 'titulo'
                reverso = False # A-Z é crescente
            
            colecao_atual.listar_ordenado(criterio=criterio, reverso=reverso)
            pausar()
            
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")
            time.sleep(1)

# --- MAIN ---

def main():
    global CATALOGO, COLECAO_ATUAL
    
    # 1. Carregar TUDO (Dicionário de Coleções)
    print("Carregando sistema...")
    CATALOGO = dados.carregar_tudo()
    
    # Define a coleção inicial se não existir nenhuma
    if "Minha coleção" not in CATALOGO:
        CATALOGO["Minha coleção"] = Colecao("Minha coleção")
    
    # Define a coleção ativa padrão
    COLECAO_ATUAL = CATALOGO.get("Minha coleção")
    # Caso a Minha coleção tenha sido deletada e recriada com outro nome, pega a primeira disponível
    if not COLECAO_ATUAL and len(CATALOGO) > 0:
        COLECAO_ATUAL = list(CATALOGO.values())[0]
    
    while True:
        limpar_tela()
        print("="*40)
        print(f"   CATÁLOGO DE JOGOS")
        print(f"   📂 Coleção Atual: {COLECAO_ATUAL.nome}")
        print("="*40)
        print("1. Cadastrar novo jogo")
        print("2. Atualizar jogo (status/horas/nota)")
        print("3. Consultar jogos")
        print("4. Remover Jogo") 
        print("5. Relatórios")
        print("6. Configurações (Meta/Limites)")
        print("7. Gerenciar coleções")
        print("0. Sair e Salvar")
        print("="*40)
        
        opcao = input("Opção: ")
        
        if opcao == '1':
            menu_cadastrar_jogo(COLECAO_ATUAL)
            
        elif opcao == '2':
            menu_atualizar_progresso(COLECAO_ATUAL)
            
        elif opcao == '3':
            menu_filtros(COLECAO_ATUAL)

        elif opcao == '4':
            menu_remover_jogo(COLECAO_ATUAL)
            
        elif opcao == '5':
            limpar_tela()
            relatorios.exibir_relatorio_geral(COLECAO_ATUAL.jogos)
            pausar()
            
        elif opcao == '6':
            limpar_tela()
            print("=== CONFIGURAÇÕES ===")
            print(f"Meta Anual Atual: {config.obter_meta_anual()}")
            nm = input("Definir nova meta (Enter para manter): ")
            if nm.isdigit():
                config.atualizar_configuracao("meta_anual_finalizados", int(nm))
                print("✅ Meta atualizada!")
            
            print(f"Limite Simultâneo Atual: {config.obter_limite_jogos_simultaneos()}")
            nl = input("Definir novo limite (Enter para manter): ")
            if nl.isdigit():
                 config.atualizar_configuracao("limite_jogos_simultaneos", int(nl))
                 print("✅ Limite atualizado!")
            pausar()
            
        elif opcao == '7':
            menu_gerenciar_colecoes()
            
        elif opcao == '0':
            print("\nSalvando todas as coleções...")
            dados.salvar_tudo(CATALOGO)
            print("Até logo! 👋")
            break
            
        else:
            print("Opção inválida.")
            time.sleep(1)

if __name__ == "__main__":
    main()