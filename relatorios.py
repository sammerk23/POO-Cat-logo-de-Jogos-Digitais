from typing import List, Dict
from jogo import Jogo
from config import obter_meta_anual

def calcular_total_horas(lista_jogos: List['Jogo']) -> float:
    # Calcula o total de horas jogadas somando as horas de cada jogo na lista
    total = sum(jogo.horasJogadas for jogo in lista_jogos)
    return total

def calcular_media_avaliacoes(lista_jogos: List['Jogo']) -> float:
    # Percorre a lista de jogos e filtra apenas os com status "finalizado", e o armazena em uma nova lista
    finalizados = [j for j in lista_jogos if j.status.lower() == "finalizado"]
    
    if not finalizados:
        return 0.0
    
    # Calcula a soma das notas dos jogos finalizados
    soma_notas = sum(j.nota for j in finalizados)
    media = soma_notas / len(finalizados)
    return round(media, 2) # arredonda para 2 casas decimais

def gerar_estatisticas_status(lista_jogos: List['Jogo']) -> Dict[str, str]: # Retorna um dicionário com a porcentagem de jogos em cada status
    total_jogos = len(lista_jogos)
    if total_jogos == 0:
        return {"aviso": "Nenhum jogo cadastrado."}
    
    contagem = {}
    
    # Conta quantos jogos tem em cada status
    for jogo in lista_jogos:
        status = jogo.status.lower()
        contagem[status] = contagem.get(status, 0) + 1
        
    # Calcula a porcentagem
    resultado = {}
    for status, qtd in contagem.items():
        percentual = (qtd / total_jogos) * 100
        resultado[status] = f"{percentual:.1f}%"
        
    return resultado

def listar_top_jogos(lista_jogos: List['Jogo'], top_n=5) -> List['Jogo']:
    # Ordena a lista do maior para o menor.
    lista_ordenada = sorted(lista_jogos, key=lambda x: x.horasJogadas, reverse=True)
    
    # Retorna apenas os primeiros 5 jogos (top_n = 5)
    return lista_ordenada[:top_n]

def verificar_meta_anual(lista_jogos: List['Jogo']):
    meta = obter_meta_anual()
    finalizados = [j for j in lista_jogos if j.status.lower() == "finalizado"]
    qtd_finalizados = len(finalizados)
    
    print("\n📅 META ANUAL:")
    print(f"   Meta: {meta} jogos | Finalizados: {qtd_finalizados}")
    
    if qtd_finalizados < meta:
        faltam = meta - qtd_finalizados
        print(f"   ⚠️  AVISO: Faltam {faltam} jogo(s) para atingir a meta anual!")
    else:
        print(f"   ✅ Meta atingida! ({qtd_finalizados}/{meta})")
    
    print("="*40)

def exibir_relatorio_geral(lista_jogos: List['Jogo']):
    print("="*40)
    print("       RELATÓRIO DO CATÁLOGO DE JOGOS       ")
    print("="*40)
    
    # Total de Horas
    total_horas = calcular_total_horas(lista_jogos)
    print(f"⏱️  Tempo total de horas jogadas: {total_horas:.2f} horas")
    
    # Média de Notas
    media = calcular_media_avaliacoes(lista_jogos)
    print(f"⭐ Média de notas: {media}/10")
    
    print("-" * 40)
    
    # Status
    print("📊 Distribuição por status:")
    stats = gerar_estatisticas_status(lista_jogos)
    for status, porc in stats.items():
        print(f"   • {status.capitalize()}: {porc}")
        
    print("-" * 40)

    # Top 5
    print("🏆 Top 5 mais jogados:")
    top5 = listar_top_jogos(lista_jogos)
    if not top5:
        print("   (Nenhum jogo registrado)")
    else:
        for i, jogo in enumerate(top5, 1):
            print(f"   {i}. {jogo.titulo} - {jogo.horasJogadas}h")
    
    print("-" * 40)
    
    # Aviso de Meta Anual
    verificar_meta_anual(lista_jogos)