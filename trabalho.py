from dataclasses import dataclass
import sys

@dataclass
class Time:
    '''classe que representa um time
    nome será str
    pontos será float
    vitórias será int
    saldo_de_gols será int
    gols_marcados será int
    gols_sofridos será int
    '''
    nome: str
    pontos: float
    vitórias: int
    saldo_de_gols: int
    gols_marcados: int
    gols_sofridos: int

# Pergunta 1, com recursividade
#Descobrir os nomes dos times

def separa(texto: str) -> list[str]: #função split que o uber passou
    '''
    percorre a string e se encontrar um espaço, add oq foi encontrado, e "reinicia" a string, no final add a ultima string se tiver
    >>> separa('Sao-Paulo 1 Atletico-MG 2')
    ['Sao-Paulo', '1', 'Atletico-MG', '2']
    >>> separa('Flamengo 2 Palmeiras 1')
    ['Flamengo', '2', 'Palmeiras', '1']
    >>> separa('Palmeiras 0 Flamengo 0')
    ['Palmeiras', '0', 'Flamengo', '0']
    '''
    caracter = '' #armazena os caracteres
    list2 = [] #lista que vai armazenar as partes
    letra = 0 #letra é o índice da string
    while letra < len(texto): #percorre a string, ate o final
        if texto[letra] != ' ': #se o caracter não for um espaço, add ele na string
            caracter += texto[letra] 
        else:
            list2.append(caracter) #se for um espaço, add o caracter na lista
            caracter = ''
        letra += 1 #contadror de letras

    if caracter != '': #se o caracter não for vazio, add ele na lista
        list2.append(caracter)
    return list2

def descobrir_times(linhas: list[str], times: list[str]) -> list[str]: #função que descobre os times a partir das linhas de partidas
    '''Descobre os times a partir das linhas de partidas. Cada linha deve estar no formato: 'Anfitrião Gols Visitante Gols'.
    interage sobre cada linha do código (partidas), usa a função separa para pegar as parte, "reconhece" e add os gols do anfitrião e visitante e o anfitrião e visitante
    >>> descobrir_times(['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1'], [])
    ['Sao-Paulo', 'Atletico-MG', 'Flamengo', 'Palmeiras']
    >>> descobrir_times(['Flamengo 2 Palmeiras 1', 'Sao-Paulo 1 Atletico-MG 2'], [])
    ['Flamengo', 'Palmeiras', 'Sao-Paulo', 'Atletico-MG']
    >>> descobrir_times(['Palmeiras 0 Flamengo 0', 'Palmeiras 0 Flamengo 0'], [])
    ['Palmeiras', 'Flamengo']
    '''
    for linha in linhas:
        partes = separa(linha) #separa a linha em partes
        anfitriao = partes[0] #anfitrião é a primeira parte
        visitante = partes[2] #visitante é a terceira parte, com índice 2
        if anfitriao not in times: #se o anfitrião não estiver na lista de times, add ele só pra ter certeza, pq tme outros jogos, pra n ter 2 times iguais
            times.append(anfitriao)
        if visitante not in times: #se o visitante não estiver na lista de times, add ele só pra ter certeza, pq tem outros jogos, pra n ter 2 times iguais
            times.append(visitante)
    return times


#Calcular os pontos, n ́umero de vit ́orias e saldo de gols de um time por vez

def partidas_do_time(time: str, partidas: list[list]) -> list[int]: #função q pega os jogos do time
    '''
    Retorna uma lista de listas [gols_marcados, gols_sofridos] para o time, a partir da lista de partidas, meio que filtrando elas.
    >>> partidas = [['Sao-Paulo', 1, 'Atletico-MG', 2], ['Flamengo', 2, 'Palmeiras', 1], ['Palmeiras', 0, 'Sao-Paulo', 0], ['Atletico-MG', 1, 'Flamengo', 2]]
    >>> partidas_do_time('Flamengo', partidas)
    [[2, 1], [2, 1]]
    >>> partidas_do_time('Palmeiras', partidas)
    [[1, 2], [0, 0]]
    >>> partidas_do_time('Sao-Paulo', partidas)
    [[1, 2], [0, 0]]
    '''
    resultado = [] #armazena os resultados
    for jogo in partidas:
        anfitriao, gols_casa, visitante, gols_visitante = jogo #pega os valores do jogo da lista
        if time == anfitriao: #se o time for o anfitriao
            resultado.append([gols_casa, gols_visitante]) # adiciona os gols do anfitrião e do visitante, seria o gols que ele marcou e os gols q ele sofreu
        elif time == visitante: #se o time for o visitante
            resultado.append([gols_visitante, gols_casa]) # adiciona os gols do visitante e do anfitrião, seria o gols que ele marcou e os gols q ele sofreu (eu inverti para n precisar criar mais variáveis)
    return resultado

#antes eu tinha apenas uma função, mas por organização criei 3 recursivas (obrigatórias) que no final a recursiva chama elas no desempenho times, elas serão muito parecidas, vai mudar apenas o cálculo (era um exercício do marcoaurélio)
def pontos_time(partidas_time: list[int]) -> int:
    '''
    Calcula os pontos de um time
    >>> pontos_time([[5, 1], [0, 2], [1, 1]])
    4
    >>> pontos_time([])
    0
    '''
    # caso base: senão tem mais partidas, não há mais pontos a adicionar.
    if len(partidas_time) == 0:
        return 0
    else:
        gols_marcados, gols_sofridos = partidas_time[0] #pega os gols marcados e sofridos da primeira partida
        pontos_atual = 0 #começa com 0 pontos
        if gols_marcados > gols_sofridos: # se venceu
            pontos_atual = 3
        elif gols_marcados == gols_sofridos: #se empatou, pois perder n pontua
            pontos_atual = 1

        return pontos_atual + pontos_time(partidas_time[1:]) #pontos atuais + pontos das partidas restantes

def vitorias_time(partidas_time: list[int]) -> int:
    '''
    Calcula o número de vitórias de um time
    >>> vitorias_time([[5, 1], [0, 2], [1, 1]])
    1
    >>> vitorias_time([])
    0
    '''
    # caso base: senão tem mais partidas, não há mais vitórias a adicionar.
    if len(partidas_time) == 0:
            return 0
    else:
        gols_marcados, gols_sofridos = partidas_time[0] #pega os gols marcados e sofridos da primeira partida
        vitoria_atual = 0 #começa com 0 vitórias
        if gols_marcados > gols_sofridos: #se venceu
                vitoria_atual = 1

        return vitoria_atual + vitorias_time(partidas_time[1:]) #vitorias atuais + vitorias das partidas restantes

def saldo_gols_time(partidas_time: list[int]) -> int:
    '''
    Calcula o saldo de gols de um time usando recursão.
    >>> saldo_gols_time([[5, 1], [0, 2], [1, 1]])
    2
    >>> saldo_gols_time([])
    0
    '''
   # caso base: senão tem mais partidas, não há mais salgo de gols a adicionar.
    if len(partidas_time) == 0:
        return 0
    else:
        gols_marcados, gols_sofridos = partidas_time[0] #pega os gols marcados e sofridos da primeira partida
        saldo_atual = gols_marcados - gols_sofridos #calculo básico do saldo de gols 
    
    return saldo_atual + saldo_gols_time(partidas_time[1:]) #saldo de gols atual + saldo de gols das partidas restantes 

def desempenho_time(partidas_time: list[int]) -> list[int]: # função que retorna os pontos, vitórias e saldo de gols de um time, para utilizar em outras partes do código agrupadas
    '''Retorna pontos, vitórias e saldo de gols de um time.'''
    return [pontos_time(partidas_time), vitorias_time(partidas_time), saldo_gols_time(partidas_time)]

#Classificar os times

#ideia de dividir cada comparação em funções específicas, colocando uma espécie de classificação com 1, -1 e 0 e dps chama-las no classificação critério para comparar
def compara_pontos(time1: Time, time2: Time) -> int:
    '''Compara pontos dos times
    Retorna 1 se time1 > time2 
    Retorna -1 se time1 < time2 
    Retorna 0 se for igual
    >>> compara_pontos(Time('A', 10, 0, 0, 0, 0), Time('B', 5, 0, 0, 0, 0))
    1
    '''
    if time1.pontos > time2.pontos: # se o time1 tem mais pontos que o time2
        return 1
    elif time1.pontos < time2.pontos: # se o time1 tem menos pontos que o time2
        return -1
    else: #time1 = time2 se o time1 tem a msm quant de pontos q o time2
        return 0 

def compara_vitorias(time1: Time, time2: Time) -> int:
    '''Compara vitórias dos times
    Retorna 1 se time1 > time2
    Retorna -1 se time1 < time2 
    Retorna 0 se for igual
    >>> compara_vitorias(Time('A', 0, 5, 0, 0, 0), Time('B', 0, 3, 0, 0, 0))
    1
    '''
    if time1.vitórias > time2.vitórias: # se o time1 tem mais vitórias que o time2
        return 1
    elif time1.vitórias < time2.vitórias: # se o time1 tem menos vitórias que o time2
        return -1
    else: # time1 = time2 e o time1 tem a msm quant de vitórias q o time2
        return 0

def compara_saldo(time1: Time, time2: Time) -> int:
    '''Compara saldo de gols dos times
    Retorna 1 se time1 > time2
    Retorna -1 se time1 < time2 
    Retorna 0 se for igual
    >>> compara_saldo(Time('A', 0, 0, 10, 0, 0), Time('B', 0, 0, 5, 0, 0))
    1
    '''
    if time1.saldo_de_gols > time2.saldo_de_gols: # se o time1 tem mais saldo de gols que o time2
        return 1
    elif time1.saldo_de_gols < time2.saldo_de_gols: # se o time1 tem menos saldo de gols que o time2
        return -1
    else: #time1 = time2 se o time1 tem a msm quant de saldo de gols q o time2
        return 0

def compara_nome(time1: Time, time2: Time) -> int:
    '''Compara nomes dos times em ordem alfabética, python já reconhece 
    Retorna 1 se time1 > time2 
    Retorna -1 se time1 < time2 
    Retorna 0 se for igual
    >>> compara_nome(Time('Flamengo', 0, 0, 0, 0, 0), Time('Vasco', 0, 0, 0, 0, 0))
    1
    '''
    if time1.nome < time2.nome: # se o nome do time1 vem antes do nome do time2
        return 1
    elif time1.nome > time2.nome: # se o nome do time1 vem depois do nome do time2
        return -1
    else: #time1 = time2 se o nome do time1 é igual ao nome do time2
        return 0

def classificacao_criterio(time1: Time, time2: Time) -> bool:
    '''
    Compara dois times e retorna True se o primeiro for melhor que o segundo.
    Ordem: pontos, vitórias, saldo de gols e ordem alfabética.
    >>> classificacao_criterio(Time('Flamengo', 10, 3, 5, 15, 10), Time('Vasco', 9, 2, 4, 12, 8))
    True
    >>> classificacao_criterio(Time('Palmeiras', 10, 3, 5, 15, 10), Time('Corinthias', 10, 3, 5, 15, 10))
    False
    '''
    comparar = compara_pontos(time1, time2) # compara os pontos dos times
    if comparar != 0: # se os pontos forem diferentes, tem um melhor e pior
        return comparar == 1 # se o time1 tem mais pontos que o time2, retorna True, senão retorna False (n achei necessáiro usar else, pq se for False, ele vai pro próximo)

    comparar = compara_vitorias(time1, time2) # compara as vitórias dos times
    if comparar != 0: # se as vitórias forem diferentes, tem um melhor e pior
        return comparar == 1 # se o time1 tem mais vitórias que o time2, retorna True, senão retorna False

    comparar = compara_saldo(time1, time2) # compara o saldo de gols dos times
    if comparar != 0: # se o saldo de gols forem diferentes, tem um melhor e pior
        return comparar == 1 # se o time1 tem mais saldo de gols que o time2, retorna True, senão retorna False

    comparar = compara_nome(time1, time2) # compara os nomes dos times
    if comparar != 0: # se os nomes forem diferentes
        return comparar == 1 # se o time1 (ordem alfabética) vem antes do time2 (ordem alfabética), retorna True, senão retorna False

def selectionsort(arranjo: list[Time]) -> list[Time]: #peguei a função da ordenação na sala
    '''Ordena uma lista de inteiros usando a classificação por critério que ja criei, usando o algoritmo Selection Sort já feito em sala de aula.
    seleciona o menor elemento da lista (percorre a lista e compara com os outros valores) e troca com o da primeira posição 
    dps começa a percorrer o menos elemento novamente, a partir da segunda posição
    >>> times = [Time('Vasco', 10, 4, 5, 15, 10), Time('Flamengo', 10, 4, 5, 15, 10), Time('Palmeiras', 12, 3, 4, 14, 10), Time('Santos', 9, 2, 3, 11, 8)]
    >>> selectionsort(times)
    [Time(nome='Palmeiras', pontos=12, vitórias=3, saldo_de_gols=4, gols_marcados=14, gols_sofridos=10), Time(nome='Flamengo', pontos=10, vitórias=4, saldo_de_gols=5, gols_marcados=15, gols_sofridos=10), Time(nome='Vasco', pontos=10, vitórias=4, saldo_de_gols=5, gols_marcados=15, gols_sofridos=10), Time(nome='Santos', pontos=9, vitórias=2, saldo_de_gols=3, gols_marcados=11, gols_sofridos=8)]
    >>> times2 = [Time('C', 5, 1, 1, 0, 0), Time('A', 10, 2, 3, 0, 0), Time('B', 8, 2, 2, 0, 0)]
    >>> selectionsort(times2)
    [Time(nome='A', pontos=10, vitórias=2, saldo_de_gols=3, gols_marcados=0, gols_sofridos=0), Time(nome='B', pontos=8, vitórias=2, saldo_de_gols=2, gols_marcados=0, gols_sofridos=0), Time(nome='C', pontos=5, vitórias=1, saldo_de_gols=1, gols_marcados=0, gols_sofridos=0)]
    '''
    n: int = len(arranjo)
    for i in range(n): #encontra o elemento da posição i
        min: int = i
        for j in range(i + 1, n): #i + 1, vai seguir em frente ate o final da lista
            #aqui inverte a lógica para min virar a classificação de acordo com os critérios
            if classificacao_criterio(arranjo[j], arranjo[min]): #na lógica da ordenação, vai comparar o min com o da frente(j), ai o min passa a valer j, 
                #o arranjo[j] será o time q estammos analizando e o arranjo[min] é o melhor time encontrado até agora, funcionando como controle
                min = j
        aux = arranjo[i]
        arranjo[i] = arranjo[min]
        arranjo[min] = aux
    return arranjo


def print_tabela(times: list[Time]) -> None: #função que imprime a tabela de classificação, mas n retorna nada
    '''Imprime a tabela de classificação dos times.
    >>> times = [Time('Flamengo', 6, 2, 2, 4, 9), Time('Atletico-MG', 3, 1, 0, 9, 2)]
    >>> print_tabela(times)
     1° - Flamengo      6   2   2
     2° - Atletico-MG   3   1   0
    '''
    posicao: int = 1 #n existe 0° no campeonado
    maior_nome = 0
    for time in times: #encontra o maior nome para formatar a tabela corretamente
        if len(time.nome) > maior_nome: # verifica o tamanho do nome do time e atualiza o maior_nome
            maior_nome = len(time.nome)

    for time in times: #imprime a tabela
        if posicao < 10: # a partir do 10, ele começa a alinhar, pq é um numero a mais, ai coloco um espaço a mais
            posicao_certo = " " + str(posicao) + "° - " 
        else:
            posicao_certo = str(posicao) + "° - "

        nome_certo = time.nome + ' ' * (maior_nome - len(time.nome))

        pontos = str(time.pontos) # converte os pontos para string, para alinhar
        if time.pontos < 10 and time.pontos >= 0:  #se os pontos forem menores que 10 e não negativos, coloca um espaço a mais
            pontos = ' ' + pontos

        vitorias = str(time.vitórias)  # converte as vitórias para string, para alinhar
        if time.vitórias < 10 and time.vitórias >= 0: # se as vitórias forem menores que 10 e não negativas, coloca um espaço a mais
            vitorias = ' ' + vitorias

        saldo = str(time.saldo_de_gols) # converte o saldo de gols para string, para alinhar
        if time.saldo_de_gols < 10 and time.saldo_de_gols >= 0: # se o saldo de gols for menor que 10 e não negativo, coloca um espaço a mais
            saldo = ' ' + saldo

        print(posicao_certo + nome_certo + "  " + pontos + "  " + vitorias + "  " + saldo)
        posicao += 1




# Pergunta 2
def jogos_como_anfitriao(time: str, partidas: list) -> list[int]: #função já feita, porém agora utilizo apenas para pegar os jogos onde o time foi anfitrião
    '''Retorna todas as partidas onde o time foi o anfitrião.
    >>> jogos_como_anfitriao('Time A', [['Time A', 3, 'Time B', 1], ['Time C', 2, 'Time A', 2], ['Time A', 1, 'Time D', 0]])
    [[3, 1], [1, 0]]
    >>> jogos_como_anfitriao('Vasco', [['Vasco', 2, 'Flamengo', 1], ['Vasco', 1, 'Fluminense', 1]])
    [[2, 1], [1, 1]]
    '''
    resultado = []
    for jogo in partidas:
        anfitriao, gols_casa, visitante, gols_visitante = jogo
        if time == anfitriao:
            resultado.append([gols_casa, gols_visitante])
    return resultado


#descobrir o maximo de pontos possíveis
#aproveitamento
def aproveitamento_anfitriao(time: str, partidas: list) -> float:
    '''Calcula o aproveitamento do time como anfitrião
    5 jogos como anfitriao -> 15 pontos possíveis, 
    3 vitórias e 1 empate (9 pontos pela vitória 3x3, 1 ponto pelo empate, perdeu um e não pontua) -> 10 pontos
    pontos_possíveis = anfitrião * 3
    proveitamento = (time.pontos / pontos_possíveis) * 100
    >>> aproveitamento_anfitriao('Time A', [['Time A', 3, 'Time B', 1], ['Time C', 2, 'Time A', 2], ['Time A', 1, 'Time D', 0]])
    100.0
    >>> aproveitamento_anfitriao('Time B', [['Time A', 3, 'Time B', 1], ['Time C', 2, 'Time A', 2], ['Time A', 1, 'Time D', 0]])
    0.0
    >>> aproveitamento_anfitriao('Vasco', [['Vasco', 2, 'Flamengo', 1], ['Vasco', 1, 'Fluminense', 1]])
    66.66666666666666
    '''
    jogos = jogos_como_anfitriao(time, partidas) # pega o time e as partidas onde ele foi anfitrião
    pontos = desempenho_time(jogos)[0] # pega os pontos do time, indice 0 é o retorno dos pontos
    pontos_possiveis = len(jogos) * 3 #3 por vitória -> calculo dos pontos possíveis
    if pontos_possiveis == 0: #aq é pra n dar divisão por zero, se o time não jogou como anfitrião, erro no doctest (mas o cálculo já faria isso)
        return 0.0
    aproveitamento = (pontos / pontos_possiveis) * 100 # calcula o aproveitamento
    return aproveitamento

# Descobrir o time com maior aproveitamento
def time_maior_aproveitamento(times: list[str], aproveitamentos: list[float]) -> str:
    '''Retorna o time com maior aproveitamento, função que fica comparando
    >>> time_maior_aproveitamento(['Gremio', 'Inter'], [80.0, 80.0])
    'Gremio'
    >>> time_maior_aproveitamento(['Santos', 'Palmeiras', 'Sao-Paulo'], [90.0, 85.0, 95.0])
    'Sao-Paulo'
    '''
    maior = aproveitamentos[0] # pega o primeiro aproveitamento como maior
    indice_maior = 0  
    for i in range(1, len(aproveitamentos)): # percorre os aproveitamentos a partir do segundo indice
        if aproveitamentos[i] > maior: # se o aproveitamento for maior que o atual
            maior = aproveitamentos[i] # atualiza
            indice_maior = i 
    return times[indice_maior] #retorna o time com maior aproveitamento, q é o indice do maior aproveitamento na lista de times

def print_aproveitamento(times: list[str], partidas: list) -> None: 
    '''Imprime apenas o time com maior aproveitamento como anfitrião.
    >>> print_aproveitamento(['Vasco', 'Flamengo'], [['Vasco', 2, 'Fluminense', 1], ['Flamengo', 1, 'Vasco', 1], ['Vasco', 0, 'Botafogo', 0]])
    O time com o melhor aproveitamento jogando como anfitrião é Vasco com 66.66666666666666 %
    >>> print_aproveitamento(['Santos', 'Corinthians'], [['Santos', 1, 'Corinthians', 1], ['Corinthians', 0, 'Santos', 2]])
    O time com o melhor aproveitamento jogando como anfitrião é Santos com 33.33333333333333 %
    '''
    maior_aproveitamento = 0 #começa com 0
    time_maior = "" #começa com vazio pra guardar o nome
    for time in range(len(times)):
        aproveitamento = aproveitamento_anfitriao(times[time], partidas) # calcula o aproveitamento do time como anfitrião, com o time especificado e as partidas dele
        if aproveitamento > maior_aproveitamento: #se o aproveitamento for maior que o atual
            maior_aproveitamento = aproveitamento #atualiza o maior aproveitamento
            time_maior = times[time] # atualiza o time com maior aproveitamento arual
    print('O time com o melhor aproveitamento jogando como anfitrião é', time_maior, 'com', maior_aproveitamento, '%')



# Pergunta 3, com recursividade
def encontrar_time_menos_vazado(times: list[Time]) -> Time:
    '''Encontra o time menos vazado, ou seja, aquele que sofreu menos gols.
    Se houver empate, retorna o primeiro encontrado.
    >>> times = [Time('Flamengo', 10, 3, 5, 15, 10), Time('Vasco', 9, 2, 4, 12, 8)]
    >>> encontrar_time_menos_vazado(times)
    Time(nome='Vasco', pontos=9, vitórias=2, saldo_de_gols=4, gols_marcados=12, gols_sofridos=8)
    >>> times2 = [Time('a', 0,0,0,0,5), Time('b', 0,0,0,0,3), Time('c', 0,0,0,0,5)]
    >>> encontrar_time_menos_vazado(times2)
    Time(nome='b', pontos=0, vitórias=0, saldo_de_gols=0, gols_marcados=0, gols_sofridos=3)
    '''
    # caso base: se a lista de times estiver vazia
    if len(times) == 0:
        return None
    # caso base: se a lista tem apenas um time, retorna esse time
    if len(times) == 1:
        return times[0]
    else:
        time_atual = times[0] #pega o primeiro time da lista
        melhor_do_resto = encontrar_time_menos_vazado(times[1:]) #pega o resto da lista, times

        if time_atual.gols_sofridos <= melhor_do_resto.gols_sofridos: #se o primeiro time tem menos gols sofridos q o melhor do resto de times
            return time_atual #retorna o primeiro time
        else:
            return melhor_do_resto #retorna o melhor do resto, que é o time com menos gols sofridos

def print_defesa_menos_vazada(times: list[Time]) -> None:
    '''Imprime o time menos vazado.
    >>> print_defesa_menos_vazada([Time('Flamengo', 10, 3, 5, 15, 10), Time('Vasco', 9, 2, 4, 12, 8)])
    O time com a defesa menos vazada é Vasco com 8 gols sofridos no total de todas as partidas jogadas.
    '''
    time_menos_vazado = encontrar_time_menos_vazado(times) # encontra o time menos vazado, chamando a função para dps printar
    print('O time com a defesa menos vazada é', time_menos_vazado.nome, 'com', time_menos_vazado.gols_sofridos, 'gols sofridos no total de todas as partidas jogadas.')




# vou criar funções apenas para organizar a pergunta 1, para montar a tabela de classificação, e dps vou chamar elas na main
# preparar os dados lidos do arquivo para serem processados pelas funções de cálculo e classificação.
def monta_partidas(jogos: list[str]) -> list:
    '''Recebe a lista de linhas e retorna a lista de partidas formatadas,
    removendo a quebra de linha manualmente.
    >>> monta_partidas(['Sao-Paulo 1 Atletico-MG 2\\n', 'Flamengo 2 Palmeiras 1\\n'])
    [['Sao-Paulo', 1, 'Atletico-MG', 2], ['Flamengo', 2, 'Palmeiras', 1]]
    '''
    partidas_formatadas = [] # lista que vai armazenar as partidas formatadas
    for linha in jogos: #quebra linha, uber pediu
        linha_limpa = "" # string que vai armazenar a linha limpa, sem quebras de linha
        for caractere in linha:
            if caractere != '\n': #se n for uma quebra de linha, add o caractere na str
                linha_limpa += caractere
        
        if linha_limpa: # Garante que a linha não está vazia após a limpeza
            partes = separa(linha_limpa)
            partidas_formatadas.append([partes[0], int(partes[1]), partes[2], int(partes[3])]) #adiciona a partida formatada na lista de partidas
    return partidas_formatadas

def monta_lista_nomes_times(partidas_formatadas: list) -> list[str]:
    '''Retorna a lista de nomes de times sem duplicados.
    >>> monta_lista_nomes_times([['Sao-Paulo', 1, 'Atletico-MG', 2], ['Flamengo', 2, 'Palmeiras', 1]])
    ['Sao-Paulo', 'Atletico-MG', 'Flamengo', 'Palmeiras']
    '''
    nomes = []
    for partida in partidas_formatadas: 
        if partida[0] not in nomes: # se o nome do time anfitrião não estiver na lista de nomes, add ele
            nomes.append(partida[0])
        if partida[2] not in nomes: # se o nome do time visitante não estiver na lista de nomes, add ele
            nomes.append(partida[2])
    return nomes

def monta_lista_times(lista_nomes_times: list[str], partidas_formatadas: list) -> list[Time]: 
    '''Retorna a lista com todosos dados para formatar bonitinho, recursividade.
    Itera sobre cada nome de time único. Para cada um, obtém suas partidas, calcula o desempenho usando desempenho_time e acumula os gols marcados e sofridos.
    Finalmente, cria uma instância da classe Time com todas essas informações.'''
    lista_times = []
    for nome_time in lista_nomes_times:
        jogos_do_time = partidas_do_time(nome_time, partidas_formatadas) # pega os jogos do time, chamando a função que já fiz
        pontos, vitorias, saldo = desempenho_time(jogos_do_time) # pega os pontos, vitórias e saldo de gols do time, chamando a função que já fiz

        gols_marcados = 0
        gols_sofridos = 0
        for jogo in jogos_do_time:
            gols_marcados += jogo[0] # soma os gols marcados do time
            gols_sofridos += jogo[1] # soma os gols sofridos do time
        novo_time = Time(nome_time, pontos, vitorias, saldo, gols_marcados, gols_sofridos) # "cria" um novo time com os dados do time
        lista_times.append(novo_time)
    return lista_times


def main(): 
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)
    if len(sys.argv) > 2:
        print('Muitos parâmetros. Informe apenas um nome de arquivo.')
        sys.exit(1)

    jogos = le_arquivo(sys.argv[1]) 

# TODO: solu ̧c~ao da pergunta 1

    # aq eu chamo as funções que eu criei para montar a tabela de classificação
    partidas_formatadas = monta_partidas(jogos)
    lista_nomes_times = monta_lista_nomes_times(partidas_formatadas)
    lista_times = monta_lista_times(lista_nomes_times, partidas_formatadas)

    # ordena a lista de times usando o selectionsort e imprime a tabela de classificação
    times_ordenados = selectionsort(lista_times)
    print_tabela(times_ordenados)

# TODO: solu ̧c~ao da pergunta 2

    print_aproveitamento(lista_nomes_times, partidas_formatadas)

# TODO: solu ̧c~ao da pergunta 3

    print_defesa_menos_vazada(lista_times)

def le_arquivo(nome: str) -> list[str]: 
    '''
    L^e o conte ́udo do arquivo *nome* e devolve uma lista onde cada elemento
    representa uma linha.
    Por exemplo, se o conte ́udo do arquivo for
    Sao-Paulo 1 Atletico-MG 2
    Flamengo 2 Palmeiras 1
    a resposta produzida  ́e
    [‘Sao-Paulo 1 Atletico-MG 2’, ‘Flamengo 2 Palmeiras 1’]
    '''
    try:
        with open(nome) as f:
            return f.readlines()
    except IOError as e:
        print(f'Erro na leitura do arquivo "{nome}": {e.errno} - {e.strerror}.')
        sys.exit(1)
        
if __name__ == '__main__': 
    main()