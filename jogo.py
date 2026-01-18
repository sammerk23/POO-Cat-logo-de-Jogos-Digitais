# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from config import obter_limite_jogos_simultaneos, atualizar_configuracao

# Classe gerenciadora de coleção de jogos
class GerenciadorJogos:
    _instancia = None
    _limite_jogos_simultaneos = 3
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GerenciadorJogos, cls).__new__(cls)
            cls._instancia._carregar_configuracoes()
        return cls._instancia
    
    def _carregar_configuracoes(self):
        """Carrega as configurações do arquivo settings.json"""
        self._limite_jogos_simultaneos = obter_limite_jogos_simultaneos()
    
    def atualizar_limite(self, novo_limite: int):
        """Atualiza o limite de jogos simultâneos"""
        if novo_limite <= 0:
            raise ValueError("O limite deve ser maior que 0")
        self._limite_jogos_simultaneos = novo_limite
        self._salvar_configuracoes()
    
    def obter_limite(self):
        """Retorna o limite configurado"""
        return self._limite_jogos_simultaneos
    
    def _salvar_configuracoes(self):
        """Salva as configurações no arquivo settings.json"""
        atualizar_configuracao('limite_jogos_simultaneos', self._limite_jogos_simultaneos)
    
    @staticmethod
    def validar_limite(lista_jogos, novo_status: str, jogo_atual=None):
        """
        Valida se é possível alterar um jogo para o status "jogando".
        
        Args:
            lista_jogos: Lista de todos os jogos
            novo_status: O novo status que se quer atribuir
            jogo_atual: O jogo que está sendo modificado (para não contar ele mesmo)
        
        Returns:
            bool: True se é permitido, False caso contrário
            
        Raises:
            Exception: Se o limite for excedido
        """
        if novo_status.lower() == "jogando":
            jogos_jogando = 0
            for jogo in lista_jogos:
                if jogo is not jogo_atual and jogo.status.lower() == "jogando":
                    jogos_jogando += 1
            
            if jogos_jogando >= GerenciadorJogos().obter_limite():
                limite = GerenciadorJogos().obter_limite()
                raise Exception(f"Limite de {limite} jogos simultâneos atingido. Finalize um jogo antes de iniciar outro.")
        
        return True

class Jogo(ABC):
    # Atributo de classe para rastrear a lista de jogos (será definido por setjogos_lista)
    _lista_jogos_global = None
    
    def __init__(self, titulo: str, nota: int, horasJogadas: int, genero: str, dataInicio: str, dataTermino: str, anoLancamento: int):
        self.__titulo = titulo
        self.__nota = nota
        self.__horasJogadas = horasJogadas
        self.__genero = genero
        self.__dataInicio = dataInicio
        self.__dataTermino = dataTermino
        self.__anoLancamento = anoLancamento
        if self.__horasJogadas > 0:
            self.__status = "jogando"
        else:
            self.__status = "não iniciado"
    
    @classmethod
    def definir_lista_jogos(cls, lista_jogos):
        """Define a lista global de jogos para validação de limite"""
        cls._lista_jogos_global = lista_jogos
    
    @classmethod
    def validar_duplicata(cls, titulo: str, plataforma: str, lista_jogos=None):
        # atribui a lista de jogos, caso ela não esteja vazia, caso esteja usará a lista global
        lista = lista_jogos if lista_jogos is not None else cls._lista_jogos_global
        
        if lista is None:
            return True
        # Verifica se já existe um jogo com o mesmo título e plataforma
        for jogo in lista:
            if jogo.titulo.lower() == titulo.lower() and hasattr(jogo, 'plataforma') and jogo.plataforma.lower() == plataforma.lower():
                return False
        return True

    def __str__(self):
        return f"Jogo: {self.__titulo} | Nota: {self.__nota} | {self.__status}"

    @abstractmethod
    def __repr__(self):
        pass

    def __eq__(self, outro_jogo):
        # Verifica se o outro_jogo é uma instância de Jogo
        if not isinstance(outro_jogo, Jogo):
            return False
        
        # Compara título (minúsculo)
        mesmo_titulo = self.titulo.lower() == outro_jogo.titulo.lower()
        
        # Compara plataforma
        # Truque: Como JogoPC tem .plataforma e JogoConsole tem .console,
        # normalizamos a comparação:
        minha_plat = getattr(self, 'plataforma', '').lower()
        if hasattr(self, 'console'): 
            minha_plat = self.console.lower()
            
        outra_plat = getattr(outro_jogo, 'plataforma', '').lower()
        if hasattr(outro_jogo, 'console'):
            outra_plat = outro_jogo.console.lower()

        return mesmo_titulo and (minha_plat == outra_plat)

    def __lt__(self, outro_jogo):
        # Verifica se o outro_jogo é uma instância de Jogo
        if not isinstance(outro_jogo, Jogo):
            return NotImplemented
        # Compara as horas jogadas de um jogo com o outro
        return self.horasJogadas < outro_jogo.horasJogadas

    @property
    def titulo(self):
        return self.__titulo

    @property
    def nota(self):
        return self.__nota

    @property
    def horasJogadas(self):
        return self.__horasJogadas

    @property
    def status(self):
        return self.__status

    @property
    def genero(self):
        return self.__genero

    @property
    def dataInicio(self):
        return self.__dataInicio

    @property
    def dataTermino(self):
        return self.__dataTermino

    @property
    def anoLancamento(self):
        return self.__anoLancamento

    @titulo.setter
    def titulo (self, novoNome):
        self.__titulo = novoNome

    @nota.setter
    def nota (self, novaNota):
        if novaNota < 0 or novaNota > 10:
          raise Exception("Nota inválida")
        if self.__status != "finalizado":
          raise Exception("Jogo deve estar FINALIZADO para receber avaliação")
        self.__nota = novaNota

    @horasJogadas.setter
    def horasJogadas (self, novaHora):
        if novaHora < 0:
          raise Exception("Horas jogadas não pode ser negativo")
        if novaHora < self.__horasJogadas:
          raise Exception("Horas jogadas só podem ser atualizadas progressivamente (não pode diminuir)")
        self.__horasJogadas = novaHora

    @status.setter
    def status (self, novoStatus):
      if novoStatus == "finalizado":
        if self.__horasJogadas >= 1:
          self.__status = novoStatus
        else:
          raise Exception("Horas jogadas insuficientes")
      elif novoStatus == "jogando":
        # Valida o limite de jogos simultâneos
        if Jogo._lista_jogos_global is not None:
          GerenciadorJogos.validar_limite(Jogo._lista_jogos_global, novoStatus, self)
        self.__status = novoStatus
      elif novoStatus == "não iniciado":
        if self.__horasJogadas == 0:
          self.__status = novoStatus
        else:
          raise Exception("Você já registrou tempo de jogo nesse jogo")
      else:
        raise Exception("Status inválido")

    @genero.setter
    def genero (self, novoGenero):
        self.__genero = novoGenero

    @dataInicio.setter
    def dataInicio (self, novaDataInicio):
        self.__dataInicio = novaDataInicio

    @dataTermino.setter
    def dataTermino (self, novaDataTermino):
        self.__dataTermino = novaDataTermino

    @anoLancamento.setter
    def anoLancamento (self, novoAno):
        self.__anoLancamento = novoAno


class MixinExportacao:
    # Cria um dicionário base com os dados comuns a todos os jogos
    def exportar_dados(self):
        dados = {
            "titulo": self.titulo,
            "nota": self.nota,
            "horasJogadas": self.horasJogadas,
            "status": self.status,
            "genero": self.genero,
            "dataInicio": self.dataInicio,
            "dataTermino": self.dataTermino,
            "anoLancamento": self.anoLancamento,
            "tipo_classe": self.__class__.__name__ # Imperativo para sabermos qual classe recriar ao carregar o JSON
        }
        return dados

class JogoPc(Jogo, MixinExportacao):
    def __init__(self, titulo: str, nota: float, horasJogadas: int, genero: str, dataInicio: str, dataTermino: str, anoLancamento: int):
        super().__init__(titulo, nota, horasJogadas, genero, dataInicio, dataTermino, anoLancamento)
        self.__plataforma = "Computador"

    def __repr__(self):
        return f"Título: {self.titulo} Nota: {self.nota} Horas Jogadas: {self.horasJogadas} Status: {self.status} Gênero: {self.genero} Data Início: {self.dataInicio} Data Término: {self.dataTermino} Ano Lançamento: {self.anoLancamento}"

    def __str__(self):
        return super().__str__() + f" | Plataforma: {self.__plataforma}"

    @property
    def plataforma(self):
        return self.__plataforma
    
    def exportar_dados(self):
        dados = super().exportar_dados()
        dados["plataforma"] = self.plataforma
        return dados

class JogoMobile(Jogo, MixinExportacao):
    def __init__(self, titulo: str, nota: float, horasJogadas: int, genero: str, dataInicio: str, dataTermino: str, anoLancamento: int):
        super().__init__(titulo, nota, horasJogadas, genero, dataInicio, dataTermino, anoLancamento)
        self.__plataforma = "Mobile"

    def __repr__(self):
        return f"Título: {self.titulo} Nota: {self.nota} Horas Jogadas: {self.horasJogadas} Status: {self.status} Gênero: {self.genero} Data Início: {self.dataInicio} Data Término: {self.dataTermino} Ano Lançamento: {self.anoLancamento}"

    def __str__(self):
        return super().__str__() + f" | Plataforma: {self.__plataforma}"

    @property
    def plataforma(self):
        return self.__plataforma
    
    def exportar_dados(self):
        dados = super().exportar_dados()
        dados["plataforma"] = self.plataforma
        return dados

class JogoConsole(Jogo, MixinExportacao):
    def __init__(self, titulo: str, nota: float, horasJogadas: int, genero: str, dataInicio: str, dataTermino: str, anoLancamento: int, console: str):
        super().__init__(titulo, nota, horasJogadas, genero, dataInicio, dataTermino, anoLancamento)
        self.__plataforma = "Console"
        self.__console = console

    def __repr__(self):
        return f"Título: {self.titulo} Nota: {self.nota} Horas Jogadas: {self.horasJogadas} Status: {self.status} Gênero: {self.genero} Data Início: {self.dataInicio} Data Término: {self.dataTermino} Ano Lançamento: {self.anoLancamento}"

    def __str__(self):
        return super().__str__() + f" | Console: {self.__console}"

    @property
    def plataforma(self):
        return self.__plataforma
    
    @property
    def console(self):
        return self.__console
    
    def exportar_dados(self):
        dados = super().exportar_dados()
        dados["plataforma"] = self.plataforma
        dados["console"] = self.console
        return dados
