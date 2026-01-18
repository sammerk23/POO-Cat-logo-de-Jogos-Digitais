from jogo import Jogo

class Colecao:
    def __init__(self, nome="Minha coleção"):
        self.nome = nome
        self.jogos = []
    
    def adicionar(self, jogo):
        # Usa o __eq__ do jogo.py para verificar duplicata automaticamente.
        if jogo in self.jogos:  
            print(f"⚠️ Já existe: {jogo.titulo} ({jogo.plataforma})")
            return False
        
        # Se percorreu tudo e não encontrou igual, adiciona
        self.jogos.append(jogo)
        print(f"✅ Adicionado: {jogo.titulo} ({jogo.plataforma})")
        return True
    
    def remover(self, titulo, plataforma=None):
        # Remove um jogo da coleção pelo título e plataforma (opcional)
        for i, j in enumerate(self.jogos):
            if j.titulo.lower() == titulo.lower():
                if plataforma is None or j.plataforma.lower() == plataforma.lower():
                    removido = self.jogos.pop(i)
                    print(f"✅ Removido: {removido.titulo} ({removido.plataforma})")
                    return True
        print(f"❌ Não encontrado: {titulo}")
        return False
    
    def buscar_por_titulo(self, titulo):
        # Busca um jogo pelo título exato
        for j in self.jogos:
            if j.titulo.lower() == titulo.lower():
                return j
        return None
    
    def buscar_por_status(self, status):
        # Busca todos os jogos com um status específico
        return [j for j in self.jogos if j.status.lower() == status.lower()]
    
    def buscar_por_genero(self, genero):
        # Busca todos os jogos de um gênero específico
        return [j for j in self.jogos if j.genero.lower() == genero.lower()]
    
    def listar(self):
        # Lista todos os jogos da coleção
        if not self.jogos:
            print("📭 Nenhum jogo na coleção")
            return
        
        print("\n" + "="*40)
        print("📚 COLEÇÃO DE JOGOS")
        print("="*40)
        for i, j in enumerate(self.jogos, 1):
            print(f"{i}. {j.titulo}")
            print(f"   Plataforma: {j.plataforma}")
            print(f"   Status: {j.status}")
            print(f"   Horas: {j.horasJogadas}h | Nota: {j.nota}")
            print()
        print(f"Total: {len(self.jogos)} jogo(s)")
        print("="*40 + "\n")
    
    def listar_por_status(self, status):
        # Lista jogos filtrados por status
        jogos_filtrados = self.buscar_por_status(status)
        
        if not jogos_filtrados:
            print(f"📭 Nenhum jogo com status '{status}'")
            return
        
        print(f"\n{'='*40}")
        print(f"📚 JOGOS COM STATUS: {status.upper()}")
        print(f"{'='*40}")
        for i, j in enumerate(jogos_filtrados, 1):
            print(f"{i}. {j.titulo} ({j.plataforma}) - {j.horasJogadas}h")
        print(f"Total: {len(jogos_filtrados)} jogo(s)")
        print("="*40 + "\n")
    
    def obter_quantidade(self):
        # Retorna a quantidade total de jogos na coleção
        return len(self.jogos)
    
    def obter_quantidade_por_status(self, status):
        # Retorna a quantidade de jogos com um status específico
        return len(self.buscar_por_status(status))
    
    def buscar_por_parte_titulo(self, termo):
        # Busca jogos cujo título contenha parte do titulo
        termo = termo.lower()
        resultados = [j for j in self.jogos if termo in j.titulo.lower()]
        
        if not resultados:
            print(f"📭 Nenhum jogo encontrado com o termo '{termo}'")
            return []
        
        return resultados

    def filtrar_jogos_por(self, genero=None, plataforma=None, nota_minima=None):
        # Filtra jogos por gênero, plataforma ou nota mínima
        filtrados = self.jogos

        if genero:
            filtrados = [j for j in filtrados if j.genero.lower() == genero.lower()]
        
        if plataforma:
            filtrados = [j for j in filtrados if getattr(j, 'plataforma', '').lower() == plataforma.lower()]
        
        if nota_minima is not None:
            filtrados = [j for j in filtrados if j.nota >= nota_minima]

        return filtrados

    def listar_ordenado(self, criterio='titulo', reverso=False):
        # Requisito: Ordenar lista por tempo jogado, avaliação ou ano.

        if not self.jogos:
            print("📭 Coleção vazia.")
            return

        # Dicionário de funções lambda para ordenação dinâmica
        chaves_ordenacao = {
            'titulo': lambda j: j.titulo,
            'horas': lambda j: j.horasJogadas,
            'nota': lambda j: j.nota,
            'ano': lambda j: j.anoLancamento
        }

        if criterio not in chaves_ordenacao:
            print("Critério de ordenação inválido.")
            return

        # Ordena a lista com base no critério escolhido (titulo, horas, nota, ano)
        lista_ordenada = sorted(self.jogos, key=chaves_ordenacao[criterio], reverse=reverso)

        print(f"\n{'='*40}")
        print(f" LISTA ORDENADA POR: {criterio.upper()}")
        print(f"{'='*40}")
        
        for i, j in enumerate(lista_ordenada, 1):
            val = getattr(j, criterio, '') # Pega o valor usado para ordenar (apenas para display)
            if criterio == 'horas': val = f"{j.horasJogadas}h"
            
            print(f"{i}. {j.titulo} - {val}")