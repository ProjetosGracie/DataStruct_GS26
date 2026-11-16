"""
==========================================================================
CITIZEN ASSIST AI
Global Solution 2026.2 - Data Structures & Algorithms (DSA)
==========================================================================
Assistente de terminal que organiza serviços de apoio ao cidadão usando
uma LISTA ENCADEADA implementada do zero (sem usar list/deque do Python
como estrutura principal).

Como executar:
    python citizen_assist_ai.py        (Python 3.8 ou superior)

Recursos da linguagem Python utilizados:
    - Classes e métodos especiais (__init__, __str__, __len__, __iter__)
    - Geradores (yield) para percorrer a lista
    - Funções como argumento (ordenação por chave)
    - List comprehension, dicionários e f-strings
    - Tratamento de exceções (try/except)
"""


# ==========================================================================
# 1. REGISTRO: SERVIÇO
# ==========================================================================

# Registro de um serviço de apoio ao cidadão.
class Servico:
    

    def __init__(self, id, titulo, categoria, descricao, requisitos, local):
        self.id = id                    # int  - identificador único
        self.titulo = titulo            # str  - nome do serviço
        self.categoria = categoria      # str  - agrupamento do serviço
        self.descricao = descricao      # str  - explicação resumida
        self.requisitos = requisitos    # list - lista de strings
        self.local = local              # str  - onde o serviço é prestado

    def __str__(self):
        return (
            f"\nID: {self.id}"
            f"\nTítulo: {self.titulo}"
            f"\nCategoria: {self.categoria}"
            f"\nDescrição: {self.descricao}"
            f"\nRequisitos: {', '.join(self.requisitos)}"
            f"\nLocal: {self.local}"
        )


# ==========================================================================
# 2. NÓ DA LISTA
# ==========================================================================

# Cada nó guarda um Servico e aponta para o próximo nó
class No:

    def __init__(self, servico):
        self.servico = servico
        self.proximo = None


# ==========================================================================
# 3. LISTA ENCADEADA SIMPLES (com ponteiros de início e fim)
# ==========================================================================
# Lista simplesmente encadeada de objetos Servico
class ListaEncadeada:

    def __init__(self):
        self.inicio = None      # primeiro nó
        self.fim = None         # último nó (permite inserir em O(1))
        self.quantidade = 0     # tamanho atual da lista
        self.proximo_id = 1     # contador de IDs (nunca reaproveita IDs)

    # ---------- métodos especiais ----------

    def __len__(self):
        return self.quantidade

    def __iter__(self):
        return self.percorrer()

    # ---------- utilitários ----------

    def esta_vazia(self):
        return self.inicio is None

    # Entrega o próximo ID disponível e avança o contador
    def gerar_id(self):
        novo_id = self.proximo_id
        self.proximo_id += 1
        return novo_id

    # ---------- INSERÇÃO NO FINAL - O(1) ----------

    def inserir(self, servico):
        novo_no = No(servico)

        if self.inicio is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

        self.quantidade += 1

    # ---------- PERCORRER (gerador) - O(n) ----------

    def percorrer(self):
        atual = self.inicio

        while atual is not None:
            yield atual.servico
            atual = atual.proximo

    # ---------- BUSCAS (todas lineares - O(n)) ----------
    # Retorna o Servico com o ID informado ou None.
    def buscar_id(self, id):
        atual = self.inicio

        while atual is not None:
            if atual.servico.id == id:
                return atual.servico
            atual = atual.proximo

        return None
    # Retorna lista de serviços cujo título CONTÉM o termo (case insensitive).
    def buscar_titulo(self, termo):
        
        termo = termo.casefold()
        resultados = []
        atual = self.inicio

        while atual is not None:
            if termo in atual.servico.titulo.casefold():
                resultados.append(atual.servico)
            atual = atual.proximo

        return resultados

    # Verifica se já existe um serviço com o título informado (ignorando o ID).
    def existe_titulo(self, titulo, ignorar_id=None):
        for servico in self.percorrer():
            if servico.id != ignorar_id and \
               servico.titulo.casefold() == titulo.casefold():
                return True
        return False
    # Retorna lista de serviços da categoria informada.
    def buscar_categoria(self, categoria):
        
        categoria = categoria.casefold()
        return [
            servico for servico in self.percorrer()
            if servico.categoria.casefold() == categoria
        ]

    # ---------- REMOÇÃO POR ID - O(n) ----------

    # Remove o serviço com o ID informado e o retorna (ou None).
    def remover(self, id):
        atual = self.inicio
        anterior = None

        while atual is not None:

            if atual.servico.id == id:

                if anterior is None:                # remoção no início
                    self.inicio = atual.proximo
                else:                               # meio ou fim
                    anterior.proximo = atual.proximo

                if atual == self.fim:               # removeu o último nó
                    self.fim = anterior

                self.quantidade -= 1
                return atual.servico

            anterior = atual
            atual = atual.proximo

        return None

    # ---------- ORDENAÇÃO: INSERTION SORT (estável) ----------
    # Melhor caso O(n) | Pior e caso médio O(n²) | Espaço extra O(1)

    # Ordena a lista religando os nós (sem copiar dados).'chave' é uma função que recebe um Servico e devolve o valor usado na comparação (ex.: lambda s: s.titulo.casefold()).
    def ordenar(self, chave):
        ordenada = None     # início da lista já ordenada
        ultimo = None       # último nó da lista já ordenada
        atual = self.inicio

        while atual is not None:
            proximo = atual.proximo
            valor = chave(atual.servico)

            if ordenada is None:                        # primeiro nó
                atual.proximo = None
                ordenada = ultimo = atual

            elif valor >= chave(ultimo.servico):        # vai para o fim
                atual.proximo = None
                ultimo.proximo = atual
                ultimo = atual

            elif valor < chave(ordenada.servico):       # vai para o início
                atual.proximo = ordenada
                ordenada = atual

            else:                                       # procura posição
                posicao = ordenada
                while chave(posicao.proximo.servico) <= valor:
                    posicao = posicao.proximo
                atual.proximo = posicao.proximo
                posicao.proximo = atual

            atual = proximo

        self.inicio = ordenada
        self.fim = ultimo

    def ordenar_por_titulo(self):
        self.ordenar(lambda s: s.titulo.casefold())

    def ordenar_por_categoria(self):
        self.ordenar(lambda s: s.categoria.casefold())

    def ordenar_por_id(self):
        self.ordenar(lambda s: s.id)


# ==========================================================================
# 4. INSTÂNCIA GLOBAL DA LISTA
# ==========================================================================

informacoes = ListaEncadeada()


# Dados ilustrativos usados na opção "Carregar dados de exemplo".
EXEMPLOS = [
    ("Carteira De Trabalho Digital", "Trabalho",
     "Emissão e consulta da CTPS pelo aplicativo ou portal oficial.",
     ["CPF", "Conta gov.br"], "Online"),
    ("Emissão De CPF", "Documentos",
     "Inscrição ou regularização do CPF, exigido na admissão.",
     ["Documento de identificação", "Data de nascimento"],
     "Online Ou Posto De Atendimento"),
    ("Título De Eleitor", "Documentos",
     "Emissão do título eleitoral e regularização da situação.",
     ["Documento com foto", "Comprovante de residência"],
     "Cartório Eleitoral"),
    ("Cadastro Único", "Assistência Social",
     "Cadastro de famílias de baixa renda para programas sociais.",
     ["Documento com foto", "CPF", "Comprovante de residência"], "CRAS"),
    ("Consulta Ao FGTS", "Trabalho",
     "Consulta de saldo e depósitos feitos pelo empregador.",
     ["CPF", "Aplicativo do FGTS"], "Online"),
    ("Programa Jovem Aprendiz", "Capacitação",
     "Orientação sobre contratação de aprendizes e qualificação.",
     ["Idade entre 14 e 24 anos", "Ensino em andamento ou concluído"],
     "Escolas Técnicas E Empresas Parceiras"),
]


# ==========================================================================
# 5. FUNÇÕES DE ENTRADA E VALIDAÇÃO
# ==========================================================================

# Repete a pergunta até receber um texto não vazio
def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor:
            return valor

        print("Este campo não pode ficar vazio.")

# Retorna um inteiro digitado ou None (com aviso) se for inválido
def ler_inteiro(mensagem):
    try:
        return int(input(mensagem).strip())
    except ValueError:
        print("Digite um número inteiro válido.")
        return None

# Lê um ID (inteiro positivo). Retorna None se for inválido
def ler_id(mensagem):
    valor = ler_inteiro(mensagem)

    if valor is None:
        return None

    if valor < 1:
        print("O ID deve ser um número maior que zero.")
        return None

    return valor

# Lê requisitos separados por vírgula (mínimo de um)
def ler_requisitos(mensagem="Digite os requisitos separados por vírgula: "):
    while True:
        entrada = input(mensagem)

        requisitos = [
            item.strip()
            for item in entrada.split(",")
            if item.strip()
        ]

        if requisitos:
            return requisitos

        print("Digite pelo menos um requisito.")

# "Retorna True para 's' e False para 'n'; repete se for inválido
def ler_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()

        if resposta in ("s", "sim"):
            return True

        if resposta in ("n", "nao", "não"):
            return False

        print("Responda apenas com 's' ou 'n'.")

# Lê um título que ainda não exista na lista
def ler_titulo_novo():

    while True:
        titulo = ler_texto("Digite o nome do serviço: ").title()

        if not informacoes.existe_titulo(titulo):
            return titulo

        print("Já existe um serviço com esse título. Escolha outro.")


# ==========================================================================
# 6. CADASTRO (CREATE)
# ==========================================================================

def inserir_informacoes():

    while True:

        print("\n================================")
        print("     INSERIR INFORMAÇÕES")
        print("================================")

        titulo = ler_titulo_novo()
        categoria = ler_texto("Digite a categoria do serviço: ").title()
        descricao = ler_texto("Digite a descrição do serviço: ")
        requisitos = ler_requisitos()
        local = ler_texto("Digite o local do serviço: ").title()

        novo_id = informacoes.gerar_id()
        informacoes.inserir(
            Servico(novo_id, titulo, categoria, descricao, requisitos, local)
        )

        print("\nInformação adicionada com sucesso!")
        print(f"ID gerado: {novo_id}")

        if not ler_sim_nao("Deseja adicionar outra informação? (s/n): "):
            break


def carregar_exemplos():
    adicionados = 0

    for titulo, categoria, descricao, requisitos, local in EXEMPLOS:
        if not informacoes.existe_titulo(titulo):
            informacoes.inserir(Servico(
                informacoes.gerar_id(), titulo, categoria,
                descricao, requisitos, local
            ))
            adicionados += 1

    print(f"\n{adicionados} serviço(s) de exemplo carregado(s).")


# ==========================================================================
# 7. MOSTRAR TUDO (READ)
# ==========================================================================

def mostrar_informacoes():

    if informacoes.esta_vazia():
        print("Nenhuma informação cadastrada.")
        return

    print("\n================================")
    print("     INFORMAÇÕES CADASTRADAS")
    print("================================")

    for info in informacoes:
        print(info)
        print("--------------------------------")

    print(f"Total: {len(informacoes)} serviço(s).")


# ==========================================================================
# 8. CONSULTAR (READ)
# ==========================================================================

def consultar_informacoes():

    if informacoes.esta_vazia():
        print("Nenhuma informação cadastrada.")
        return

    while True:

        print("\n================================")
        print("     CONSULTAR INFORMAÇÕES")
        print("================================")
        print("1 - Consultar por ID")
        print("2 - Consultar todas as informações")
        print("3 - Voltar ao menu principal")

        opcao = ler_inteiro("Digite sua opção: ")

        if opcao is None:
            continue

        if opcao == 1:
            consultar_id()

        elif opcao == 2:
            mostrar_informacoes()

        elif opcao == 3:
            break

        else:
            print("Opção inválida.")


def consultar_id():

    id_consulta = ler_id("Digite o ID do serviço: ")

    if id_consulta is None:
        return

    resultado = informacoes.buscar_id(id_consulta)

    if resultado is not None:
        print("\nServiço encontrado!")
        print(resultado)
    else:
        print("Informação não encontrada.")


# ==========================================================================
# 9. BUSCAR
# ==========================================================================

def buscar_informacoes():

    if informacoes.esta_vazia():
        print("Nenhuma informação cadastrada.")
        return

    while True:

        print("\n================================")
        print("     BUSCAR INFORMAÇÕES")
        print("================================")
        print("1 - Buscar por título (nome completo ou parte)")
        print("2 - Buscar por categoria")
        print("3 - Voltar ao menu principal")

        opcao = ler_inteiro("Digite sua opção: ")

        if opcao is None:
            continue

        if opcao == 1:
            buscar_titulo()

        elif opcao == 2:
            buscar_categoria()

        elif opcao == 3:
            break

        else:
            print("Opção inválida.")


def exibir_resultados(resultados, mensagem_vazia):
    if not resultados:
        print(mensagem_vazia)
        return

    print(f"\n{len(resultados)} serviço(s) encontrado(s):")

    for resultado in resultados:
        print(resultado)
        print("--------------------------------")


def buscar_titulo():
    termo = ler_texto("Digite o título (ou parte dele): ")
    exibir_resultados(
        informacoes.buscar_titulo(termo),
        "Nenhum serviço encontrado com esse título."
    )


def buscar_categoria():
    categoria = ler_texto("Digite a categoria do serviço: ")
    exibir_resultados(
        informacoes.buscar_categoria(categoria),
        "Nenhuma informação encontrada para essa categoria."
    )


# ==========================================================================
# 10. EXCLUIR (DELETE)
# ==========================================================================

def excluir_info():

    id_excluir = ler_id("Digite o ID do serviço que deseja excluir: ")

    if id_excluir is None:
        return

    info = informacoes.buscar_id(id_excluir)

    if info is None:
        print("Informação não encontrada.")
        return

    print(info)

    if not ler_sim_nao("Confirma a exclusão deste serviço? (s/n): "):
        print("Exclusão cancelada.")
        return

    informacoes.remover(id_excluir)
    print("Informação excluída com sucesso!")


# ==========================================================================
# 11. ATUALIZAR (UPDATE)
# ==========================================================================

def atualizar_info():

    id_atualizar = ler_id("Digite o ID do serviço que deseja atualizar: ")

    if id_atualizar is None:
        return

    info = informacoes.buscar_id(id_atualizar)

    if info is None:
        print("Informação não encontrada.")
        return

    print("\nServiço encontrado!")
    print("Deixe o campo vazio para manter o valor atual.")

    titulo = input(f"Título atual ({info.titulo}): ").strip()
    categoria = input(f"Categoria atual ({info.categoria}): ").strip()
    descricao = input(f"Descrição atual ({info.descricao}): ").strip()
    requisitos = input(
        f"Requisitos atuais ({', '.join(info.requisitos)}): "
    ).strip()
    local = input(f"Local atual ({info.local}): ").strip()

    if titulo:
        titulo = titulo.title()

        if informacoes.existe_titulo(titulo, ignorar_id=info.id):
            print("Já existe outro serviço com esse título. Título mantido.")
        else:
            info.titulo = titulo

    if categoria:
        info.categoria = categoria.title()

    if descricao:
        info.descricao = descricao

    if requisitos:
        novos = [item.strip() for item in requisitos.split(",") if item.strip()]

        if novos:
            info.requisitos = novos

    if local:
        info.local = local.title()

    print("Informação atualizada com sucesso!")


def editar_informacoes():

    if informacoes.esta_vazia():
        print("Nenhuma informação cadastrada.")
        return

    while True:

        print("\n================================")
        print("     EDITAR INFORMAÇÕES")
        print("================================")
        print("1 - Excluir informação")
        print("2 - Atualizar informação")
        print("3 - Voltar ao menu principal")

        opcao = ler_inteiro("Digite sua opção: ")

        if opcao is None:
            continue

        if opcao == 1:
            excluir_info()

        elif opcao == 2:
            atualizar_info()

        elif opcao == 3:
            break

        else:
            print("Opção inválida.")

        # a lista pode ter ficado vazia após uma exclusão
        if informacoes.esta_vazia():
            print("A lista ficou vazia.")
            break


# ==========================================================================
# 12. ANÁLISE DE DADOS
# ==========================================================================

def analise_dados():

    if informacoes.esta_vazia():
        print("Nenhuma informação cadastrada.")
        return

    categorias = {}

    for info in informacoes:
        categorias[info.categoria] = categorias.get(info.categoria, 0) + 1

    total = len(informacoes)

    print("\n================================")
    print("     ANÁLISE DE DADOS")
    print("================================")
    print(f"Total de serviços: {total}")
    print(f"Total de categorias: {len(categorias)}")
    print("--------------------------------")

    for categoria, quantidade in categorias.items():
        percentual = quantidade / total * 100
        print(f"{categoria}: {quantidade} serviço(s) ({percentual:.1f}%)")

    mais_comum = max(categorias, key=categorias.get)
    print("--------------------------------")
    print(f"Categoria com mais serviços: {mais_comum}")


# ==========================================================================
# 13. ORGANIZAR (ORDENAÇÃO)
# ==========================================================================

def organizar_informacoes():

    if informacoes.esta_vazia():
        print("Nenhuma informação cadastrada.")
        return

    print("\n================================")
    print("     ORGANIZAR INFORMAÇÕES")
    print("================================")
    print("1 - Ordenar por título (A-Z)")
    print("2 - Ordenar por categoria (A-Z)")
    print("3 - Ordenar por ID (ordem de cadastro)")
    print("4 - Cancelar")

    opcao = ler_inteiro("Digite sua opção: ")

    if opcao == 1:
        informacoes.ordenar_por_titulo()
        print("\nInformações organizadas por título com sucesso!")

    elif opcao == 2:
        informacoes.ordenar_por_categoria()
        print("\nInformações organizadas por categoria com sucesso!")

    elif opcao == 3:
        informacoes.ordenar_por_id()
        print("\nInformações organizadas por ID com sucesso!")

    elif opcao == 4:
        print("Organização cancelada.")
        return

    elif opcao is not None:
        print("Opção inválida.")
        return

    else:
        return

    mostrar_informacoes()


# ==========================================================================
# 14. MENU PRINCIPAL
# ==========================================================================

def menu():

    while True:

        print("\n================================")
        print("        CITIZEN ASSIST AI")
        print("================================")
        print("1 - Inserir informações")
        print("2 - Consultar informações")
        print("3 - Editar informações")
        print("4 - Buscar informações")
        print("5 - Organizar informações")
        print("6 - Análise de dados")
        print("7 - Mostrar todas as informações")
        print("8 - Carregar dados de exemplo")
        print("0 - Sair")
        print("================================")

        opcao = ler_inteiro("Digite sua opção: ")

        if opcao is None:
            continue

        if opcao == 1:
            inserir_informacoes()

        elif opcao == 2:
            consultar_informacoes()

        elif opcao == 3:
            editar_informacoes()

        elif opcao == 4:
            buscar_informacoes()

        elif opcao == 5:
            organizar_informacoes()

        elif opcao == 6:
            analise_dados()

        elif opcao == 7:
            mostrar_informacoes()

        elif opcao == 8:
            carregar_exemplos()

        elif opcao == 0:
            print("Encerrando o Citizen Assist AI. Até logo!")
            break

        else:
            print("Opção inválida. Escolha uma opção disponível.")


# ==========================================================================
# 15. EXECUÇÃO DO PROGRAMA
# ==========================================================================

if __name__ == "__main__":
    try:
        menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma encerrado pelo usuário.")