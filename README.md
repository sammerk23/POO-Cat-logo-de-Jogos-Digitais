# POO-Catálogo-de-Jogos-Digitais
Projeto da cadeira de POO do curso de ADS da UFCA.

## Integrantes
- Kelvin Sammer Gonçalves Marques: Arquivos/Classes jogo.py (contendo Jogo, JogoPC, JogoConsole, JogoMobile e JogoMultiplataforma).
- Jonathan Oliveira Silva: Arquivos dados.py (módulo), settings.json, jogos.json.
- Ryan Keven Alves: Arquivos/Classes usuario.py (classe Usuario), colecao.py (classe Colecao).
- José Wellington Rodrigues da Silva: Interface e Interação (Frontend/CLI)
- Rafael Herbert de Menezes Paixão: Arquivos relatorios.py, test_sistema.py (pytest).

## Principais Classes
### Jogo (JogoPC, JogoMobile, JogoConsole, JogoMultiplataforma)
- Atributos: titulo, nota, horasJogadas, status, genero, dataInicio, dataTermino, anoLancamento
- Métodos: __str__, __repr__, __eq__, __lt__, cadastrarJogos, atualizarJogos, relatorioJogos

### Coleção
- Atributos: nome, listaJogos
- Métodos: __str__, __len__, adicionarJogo, removerJogo, listarJogos

### Usuário
- Atributos: nome, colecoes, 
- Métodos: __str__, adicionarJogoBiblioteca, removerJogoBiblioteca, adicionarColecao, encontrarJogo

## Rodando o código

1. Para rodar o código é necessário a instalação do pytest, para isso basta executar o comando "**pip install pytest**" no terminal.
2. Para executar o catálogo, execute o arquivo "interface.py"

## Decisões de design
### Abstração e Herança (jogo.py)
Utilizamos a classe abstrata Jogo (herdando de ABC) como base para garantir que todos os tipos de jogos compartilhem atributos essenciais (título, nota, status) e comportamentos.
- Classes Concretas: As classes JogoPc, JogoConsole e JogoMobile herdam de Jogo, especializando-se conforme a plataforma.
- Métodos Abstratos: O uso de @abstractmethod (como no __repr__) obriga as subclasses a implementarem sua própria representação textual, garantindo polimorfismo.

### Encapsulamento e Regras de Negócio
Para proteger a integridade dos dados, todos os atributos da classe Jogo são privados (ex: __nota, __status). O acesso e modificação ocorrem exclusivamente através de Properties e Setters (@property), onde implementamos as regras de negócio críticas:
- Validação de Nota: Garante que a nota esteja entre 0 e 10 e só possa ser atribuída a jogos finalizados.
- Consistência de Status: Impede que um jogo seja marcado como "finalizado" se tiver 0 horas jogadas.
- Progressão de Tempo: Impede que as horas jogadas sejam reduzidas (apenas aumentadas).

### Padrão Mixin para Exportação de Dados
Em vez de duplicar a lógica de criação de dicionários (para salvar em JSON) em cada classe, criamos a classe MixinExportacao.
- As classes de jogos herdam tanto de Jogo quanto de MixinExportacao (Herança Múltipla).
- Isso permite separar a responsabilidade de "ser um jogo" da responsabilidade de "ser serializável", facilitando a manutenção do método exportar_dados.

### Padrão Singleton (GerenciadorJogos)
Implementamos a classe GerenciadorJogos seguindo o padrão Singleton (sobrescrevendo o método __new__).
- Objetivo: Garantir que exista apenas uma instância controlando as configurações globais do sistema, como o limite de jogos simultâneos ("jogando") e a meta anual.
- Isso centraliza o carregamento e salvamento das configurações do arquivo settings.json.

### Associação e Composição (colecoes.py e usuario.py)
- Coleção: A classe Colecao atua como um container que gerencia uma lista de objetos Jogo. Ela abstrai a complexidade de listas do Python, oferecendo métodos de alto nível como buscar_por_status ou listar_ordenado.
- Relacionamento: Um Usuario possui um dicionário de coleções, demonstrando uma relação de composição onde o usuário gerencia múltiplos grupos de jogos (ex: "Favoritos", "Backlog").

### Persistência de Dados (dados.py)
A persistência foi separada da lógica de negócio. O módulo dados.py é responsável por converter os objetos em JSON e vice-versa.
- Implementamos um mecanismo de reconstrução de objetos que lê a string tipo_classe do JSON e instancia a classe correta (JogoPc, JogoConsole, etc.) dinamicamente ao carregar o sistema.
