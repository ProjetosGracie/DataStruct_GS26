# Citizen Assist AI

Assistente de terminal que organiza **serviços de apoio ao cidadão** (documentos, trabalho, assistência social, capacitação etc.), desenvolvido em Python para a **Global Solution 2026.2 – Data Structures & Algorithms (DSA)**.

O diferencial técnico do projeto é que os dados ficam armazenados em uma **lista encadeada simples implementada do zero**, sem usar `list` ou `deque` do Python como estrutura principal.

---

## Sumário

- [Requisitos](#requisitos)
- [Como executar](#como-executar)
- [Funcionalidades](#funcionalidades)
- [Estrutura de dados](#estrutura-de-dados)
- [Complexidade das operações](#complexidade-das-operações)
- [Organização do código](#organização-do-código)
- [Validações e regras de negócio](#validações-e-regras-de-negócio)
- [Exemplo de uso](#exemplo-de-uso)
- [Limitações](#limitações)

---

## Requisitos

- Python **3.8 ou superior**
- Nenhuma biblioteca externa (apenas recursos nativos da linguagem)

## Como executar

```bash
python citizen_assist_ai.py
```

Para testar rapidamente, escolha a opção **8 – Carregar dados de exemplo** no menu principal.

Para encerrar, use a opção **0** ou `Ctrl + C`.

---

## Funcionalidades

| Opção | Função | Descrição |
|-------|--------|-----------|
| 1 | Inserir informações | Cadastra um novo serviço (permite cadastrar vários em sequência). |
| 2 | Consultar informações | Consulta por ID ou lista todos os serviços. |
| 3 | Editar informações | Atualiza ou exclui um serviço pelo ID. |
| 4 | Buscar informações | Busca por título (nome completo ou parte) ou por categoria. |
| 5 | Organizar informações | Ordena a lista por título, categoria ou ID. |
| 6 | Análise de dados | Total de serviços, quantidade por categoria, percentuais e categoria mais frequente. |
| 7 | Mostrar todas | Exibe todos os serviços cadastrados. |
| 8 | Carregar dados de exemplo | Insere 6 serviços ilustrativos, sem duplicar títulos já existentes. |
| 0 | Sair | Encerra o programa. |

### Dados de cada serviço

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | int | Identificador único, gerado automaticamente. |
| `titulo` | str | Nome do serviço. |
| `categoria` | str | Agrupamento do serviço. |
| `descricao` | str | Explicação resumida. |
| `requisitos` | list[str] | Documentos ou condições necessárias. |
| `local` | str | Onde o serviço é prestado. |

---

## Estrutura de dados

A aplicação usa uma **lista simplesmente encadeada** com ponteiros de início e fim:

```
inicio                                             fim
  │                                                 │
  ▼                                                 ▼
[Servico 1 | •]──►[Servico 2 | •]──►[Servico 3 | •]──► None
```

- **`No`**: guarda um objeto `Servico` e a referência para o próximo nó.
- **`ListaEncadeada`**: mantém `inicio`, `fim`, `quantidade` e um contador de IDs (`proximo_id`).
- O ponteiro `fim` permite **inserir no final em O(1)**.
- Os IDs **nunca são reaproveitados**, mesmo após exclusões.

### Ordenação

A ordenação usa **Insertion Sort estável**, aplicado diretamente sobre os nós (religando ponteiros, sem copiar dados). O método `ordenar(chave)` recebe uma função que define o critério de comparação, por exemplo `lambda s: s.titulo.casefold()`.

---

## Complexidade das operações

| Operação | Complexidade |
|----------|--------------|
| Inserir no final | O(1) |
| Percorrer a lista | O(n) |
| Buscar por ID, título ou categoria | O(n) |
| Remover por ID | O(n) |
| Ordenar (Insertion Sort) | Melhor caso O(n) · Médio e pior caso O(n²) · Espaço extra O(1) |

---

## Organização do código

```
citizen_assist_ai.py
├── 1. Servico              → registro de um serviço
├── 2. No                   → nó da lista encadeada
├── 3. ListaEncadeada       → inserir, percorrer, buscar, remover, ordenar
├── 4. Instância global     → `informacoes` + dados de exemplo (EXEMPLOS)
├── 5. Entrada e validação  → ler_texto, ler_inteiro, ler_id, ler_requisitos, ler_sim_nao, ler_titulo_novo
├── 6. Cadastro             → inserir_informacoes, carregar_exemplos
├── 7. Mostrar tudo         → mostrar_informacoes
├── 8. Consultar            → consultar_informacoes, consultar_id
├── 9. Buscar               → buscar_informacoes, buscar_titulo, buscar_categoria
├── 10. Excluir             → excluir_info
├── 11. Atualizar           → atualizar_info, editar_informacoes
├── 12. Análise de dados    → analise_dados
├── 13. Organizar           → organizar_informacoes
├── 14. Menu principal      → menu
└── 15. Execução            → ponto de entrada (`__main__`)
```

### Recursos de Python utilizados

- Classes e métodos especiais (`__init__`, `__str__`, `__len__`, `__iter__`)
- Geradores (`yield`) para percorrer a lista
- Funções como argumento (ordenação por chave)
- List comprehension, dicionários e f-strings
- Tratamento de exceções (`try/except`)

---

## Validações e regras de negócio

- Campos de texto **não podem ficar vazios**.
- **Não é permitido cadastrar dois serviços com o mesmo título** (comparação sem diferenciar maiúsculas/minúsculas).
- Títulos, categorias e locais são padronizados com a primeira letra de cada palavra em maiúscula.
- Requisitos são digitados separados por vírgula, com **no mínimo um**.
- IDs devem ser **inteiros maiores que zero**; entradas inválidas exibem aviso em vez de quebrar o programa.
- A **exclusão exige confirmação** (`s/n`).
- Na **atualização**, deixar um campo vazio mantém o valor atual.
- As buscas ignoram maiúsculas, minúsculas e acentuação de caixa (`casefold`).
- `Ctrl + C` e `Ctrl + D` encerram o programa de forma limpa.

---

## Exemplo de uso

```
================================
        CITIZEN ASSIST AI
================================
1 - Inserir informações
2 - Consultar informações
3 - Editar informações
4 - Buscar informações
5 - Organizar informações
6 - Análise de dados
7 - Mostrar todas as informações
8 - Carregar dados de exemplo
0 - Sair
================================
Digite sua opção: 8

6 serviço(s) de exemplo carregado(s).
```

Análise de dados após carregar os exemplos:

```
================================
     ANÁLISE DE DADOS
================================
Total de serviços: 6
Total de categorias: 4
--------------------------------
Trabalho: 2 serviço(s) (33.3%)
Documentos: 2 serviço(s) (33.3%)
Assistência Social: 1 serviço(s) (16.7%)
Capacitação: 1 serviço(s) (16.7%)
--------------------------------
Categoria com mais serviços: Trabalho
```

---

## Limitações

- Os dados ficam **apenas em memória**: ao encerrar o programa, tudo é perdido.
- As buscas são lineares, adequadas para volumes pequenos de dados.
- O Insertion Sort é simples e didático, mas não é o mais eficiente para listas muito grandes.