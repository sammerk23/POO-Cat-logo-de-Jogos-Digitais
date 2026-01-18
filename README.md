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

- Para rodar o código é necessário a instalação do pytest, para isso basta executar o comando "*pip install pytest*" no terminal.
- Para executar o catálogo, execute o arquivo "interface.py"