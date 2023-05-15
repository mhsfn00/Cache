import random
import os
import time

class Acesso :
    def __init__ (self, endereco, nome, dadosArmazenados):
        self.endereco = endereco
        self.nome = nome
        self.dadosArmazenados = dadosArmazenados

acessosPossiveis = [] 
historico = []
cache = []
tamanhoCache = 5
acompanhamentoFIFO = 0

def LerDadosTxt (): #Coloca os dados do txt em acessosPossiveis
    arquivo = open("cacheData10.txt")
    linhas = len(arquivo.readlines())
    arquivo.seek(0)
    for _ in range (linhas):
        tmpEndereco, nome, dadosArmazenados = arquivo.readline().split(", ")
        endereco = float(tmpEndereco)
        acessosPossiveis.append(Acesso(endereco, nome, dadosArmazenados))
    arquivo.close()

def MostrarAcessosInteiro (acessos): #Mostra os acessos (acessosPossiveis, historico, cache) completos.
    for _ in range (0, len(acessos)):
        print (acessos[_].endereco)
        print (acessos[_].nome)
        print (acessos[_].dadosArmazenados)

def MostrarAcessosResumido (acessos):
    for _ in range (0, len(acessos)):
        msgResumida  = str((_, acessos[_].endereco))
        print (msgResumida, end="")
    print()

def MostrarAcessosResumidoComparativo (historico, acessosCache):
    historicoTam = len(historico)
    i = 0

    for _ in range (0, historicoTam):
        if (i < tamanhoCache):                #|(index do elemento atual)|
            print (_, ",", historico[_].endereco, "  |", acessosCache.index(acessosCache[i]), ",", acessosCache[i].endereco)
            i+=1
        else:
            print (_, ",", historico[_].endereco)

def GerarAcesso (acessosPossiveis): #Gera e retorna UM acesso
    novoAcesso = (acessosPossiveis[random.randrange(len(acessosPossiveis))])    
    return novoAcesso

def EncherCache (cache, acessosPossiveis, historico):
    print()

    confirmacaoCache = True
    while (confirmacaoCache):
        novoAcesso = GerarAcesso (acessosPossiveis)
        confirmacaoCache, mensagemSobreCache = TentarSalvarAcessoNoCache (novoAcesso)

        if (len(cache) == tamanhoCache):
            historico.append(novoAcesso)
            break

        if (confirmacaoCache is True):
            #print (mensagemSobreCache)
            pass
            historico.append(novoAcesso)
        else:
            #print (mensagemSobreCache)
            break
        #time.sleep(1)

    return (cache)

def TentarSalvarAcessoNoCache (acesso): #Caso True salva acesso no cache, pula se o acesso já está inserido.Caso False retorna False.
    if (SeAcessoEstaNoCache (acesso) == True):
        return (True, "Acesso repetido")
    else:    
        if len(cache) < tamanhoCache:                         
            cache.append(acesso)
            return (True, "Acesso inserido")
        else: #É 5 O_O
            return (False, "Acesso esperando para ser inserido, chamar substituição")

def SeAcessoEstaNoCache (acesso): #Checa se o cache está vazio ou se o novo acesso já está inserido
    if (len(cache) == 0):
        return False
    for _ in range (len(cache)):
        if (acesso == cache[_]):
            return True
    return False

def LFU (acessosCache, novoAcesso): #Menos frequente
    auxiliar = [0 for _ in range (tamanhoCache)]

    for i in range (len(acessosCache)):
        for j in range (len(historico)):
            if (acessosCache[i].endereco == historico[j].endereco):
                auxiliar[i] += 1 

    minimo = min(auxiliar)
    indiceDoMinimo = auxiliar.index(minimo)

    print ("Cache [", indiceDoMinimo,"] *", auxiliar[indiceDoMinimo])
    '''
    for aux in range (len(auxiliar)):
        print (auxiliar[aux], "|", end=" ")
    '''
    entradaDoUsuario = input("Pressione enter para substituir (LFU)")
    
    acessosCache[indiceDoMinimo] = novoAcesso

def LRU (acessosCache, novoAcesso): #Mais antigo do historico
    auxiliar = [0 for _ in range (tamanhoCache)]

    for i in range (len (acessosCache)):
        for j in range (len(historico)-1, -1, -1):
            if (acessosCache[i].endereco == historico[j].endereco):
                auxiliar[i] = j
                break
            else:
                pass
    
    maisAntigo = min(auxiliar)
    indiceDoMaisAntigo = auxiliar.index(maisAntigo)

    print ("Cache [", indiceDoMaisAntigo, "] -> Histórico [", auxiliar[indiceDoMaisAntigo], "]")
    '''
    for aux in range (len(auxiliar)):
        print (auxiliar[aux], "|", end=" ")
    '''
    entradaDoUsuario = input("Pressione enter para substituir (LRU)")

    acessosCache[indiceDoMaisAntigo] = novoAcesso

    return acessosCache

def FIFO (acessosCache, novoAcesso, acompanhamentoFIFO):
    print (acompanhamentoFIFO, "será substituido")
    msg = input()
    if (acompanhamentoFIFO == 4):
        acessosCache[acompanhamentoFIFO] = novoAcesso
        acompanhamentoFIFO = 0
    else:
        acessosCache[acompanhamentoFIFO] = novoAcesso
        acompanhamentoFIFO+=1
    
    return (acessosCache, acompanhamentoFIFO)

def InsercaoRandomica (acessosCache, novoAcesso):
    indice = random.randrange(tamanhoCache)
    print (indice, "será substituido")
    msg = input()

    acessosCache[indice] = novoAcesso
 
def EscolherMetodoDeSubstituicao (cache, novoAcesso, acompanhamentoFIFO):
    print ("Acesso pendente:",novoAcesso.endereco)
    entradaDoUsuario = None
    while (entradaDoUsuario == None):
        print ("1 | LFU (Least Frequently Used)\n2 | LRU (Least Recently Used)\n3 | FIFO (First In First Out)\n4 | Random Cache Insert")
        print ("'q' para sair.")
        entradaDoUsuario = input()

        match entradaDoUsuario:
            case "1":
                cache = LFU (cache, novoAcesso)
                return acompanhamentoFIFO
            case "2":
                cache = LRU (cache, novoAcesso)
                return acompanhamentoFIFO
            case "3":
                cache, acompanhamentoFIFO = FIFO (cache, novoAcesso, acompanhamentoFIFO)
                return acompanhamentoFIFO
            case "4":
                cache = InsercaoRandomica (cache, novoAcesso)
                return acompanhamentoFIFO
            case "":
                pass
                return acompanhamentoFIFO
            case "q":
                raise SystemExit
            case "Q":
                raise SystemExit

def GerarEInserirNovoAcesso (cache, acessosPossiveis, historico, acompanhamentoFIFO):
    novoAcesso = GerarAcesso (acessosPossiveis)
    historico.append(novoAcesso)
    confirmacao, msgCache = TentarSalvarAcessoNoCache (novoAcesso)

    if (confirmacao == False):
       acompanhamentoFIFO = EscolherMetodoDeSubstituicao (cache, novoAcesso, acompanhamentoFIFO)

    return acompanhamentoFIFO
       

LerDadosTxt () 
cache = EncherCache (cache, acessosPossiveis, historico)

while (True):
    os.system("cls")
    MostrarAcessosResumidoComparativo(historico, cache)
    acompanhamentoFIFO = GerarEInserirNovoAcesso (cache, acessosPossiveis, historico, acompanhamentoFIFO)



