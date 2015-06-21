'''
Created on 21/06/2015

@author: Isaac
'''
import sys
import random
from sympy.mpmath.calculus.extrapolation import sumap

MINIMIZACION = 1.0
MAXIMIZACION = -1.0
TAMANIO_POBLACION = 100
TAMANIO_INDIVIDUO = 1000
MAX_NUMERO_GENERACIONES = 1000

TIPO_PROBLEMA = MAXIMIZACION

mDistancia = []  # Matriz de flujo
mFlujo = []     # Matriz de distancia
mX = []         # Matriz de permutacion


def verificaArgumentos():
        if len(sys.argv) <= 1:
            nombreImagen = "circulo.png"
        else:
            nombreImagen = sys.argv[1]
            print 'Abriendo <', nombreImagen , '> ...'
        print 'Imagen a imitar: ', nombreImagen


def crearPoblacion(tamanioPoblacion, tamanioIndividuo):
    return [[random.randint(0,1) for i in range(tamanioIndividuo)] for j in range(tamanioPoblacion)]

def imprimirIndividuo(individuo, aptitud):
    print aptitud, individuo

def imprimirPoblacion(poblacion, aptitudes):
    for individuo, aptitud in zip(poblacion, aptitudes):
        imprimirIndividuo(individuo, aptitud)

def calcularAptitud(individuo):
    aptitud = 0.0
    for alelo in individuo:
        if alelo == 0:
            aptitud+=1.0
    return  aptitud*TIPO_PROBLEMA

def calcularAptitudPoblacion(poblacion):
    aptitudes = [0.0 for i in range(TAMANIO_POBLACION)]
    for i, individuo in zip(range(TAMANIO_POBLACION), poblacion):
        aptitudes[i] = calcularAptitud(individuo)
    return aptitudes

#Aptitudes para practica
def calcularAptitudMatrices(individuo):
    lmd = len(mDistancia)
    lmf = len(mFlujo)
    fX = 0  #funcion de aptitud
    for i in range(lmd):
        sumatoriaJ = 0
        for j in range(lmf):
            xi = mX[i]
            xj = mX[j]
            sumatoriaJ +=  mDistancia[i][j] * mFlujo[xi][xj]
        fX += sumatoriaJ



#Calcular tabla total de aptitudes y valores esperados
def preSeleccion(aptitudes):
    totalAptitudes = sum(aptitudes)
    print 'TA: ',totalAptitudes
    valoresEsperados = [aptitud/totalAptitudes for aptitud in aptitudes]
    #print sum(valoresEsperados)
    return valoresEsperados

#Seleccion por ruleta
def seleccion(valoresEsperados):
    r = random.random()
    sve = 0.0
    for i, ve in zip(range(TAMANIO_POBLACION), valoresEsperados):
        sve += ve
        if r < sve:
            return i
    return TAMANIO_POBLACION-1



def cruzar(padre, madre):
    puntoCruza = random.randint(1, TAMANIO_INDIVIDUO-2)
    #print "Punto cruza: ", puntoCruza
    hijo1 = padre[:puntoCruza] + madre[puntoCruza:]
    hijo2 = madre[:puntoCruza] + padre[puntoCruza:]
    return hijo1, hijo2

# Mutacion uniforme
def mutar(individuo):
    pm = 1.0 / TAMANIO_INDIVIDUO
    for i in range(TAMANIO_INDIVIDUO):
        r = random.random()
        if r < pm:
            if individuo[i] == 0:
                individuo[i] = 1
            else:
                individuo[i] = 0
    return individuo

def seleccionarMejores(poblacion):
    poblacionOrdenada = sorted(poblacion, key=calcularAptitud)
    return poblacionOrdenada[:TAMANIO_POBLACION]

def elitismo(elMejor, individuo, aptitud):
    if elMejor is None:
        elMejor = (individuo, aptitud)
    else:
        if aptitud < elMejor[1]:
            elMejor = (individuo, aptitud)
    return elMejor



poblacion = crearPoblacion(TAMANIO_POBLACION, TAMANIO_INDIVIDUO)
aptitudes = calcularAptitudPoblacion(poblacion)
elMejor = elitismo(None, poblacion[0], aptitudes[0])

imprimirPoblacion(poblacion, aptitudes)

for generacion in range(MAX_NUMERO_GENERACIONES):
    valoresEsperados = preSeleccion(aptitudes)
    for i in range(TAMANIO_POBLACION/2):
        pos1 = seleccion(valoresEsperados)
        pos2 = seleccion(valoresEsperados)

        #print "Cruzar: ",pos1, pos2
        hijo1, hijo2 = cruzar(poblacion[pos1], poblacion[pos2])
        #imprimirIndividuo(hijo1, calcularAptitud(hijo1))
        #imprimirIndividuo(hijo2, calcularAptitud(hijo2))
        hijo1 = mutar(hijo1)
        hijo2 = mutar(hijo2)

        poblacion.append(hijo1)
        poblacion.append(hijo2)

    poblacion = seleccionarMejores(poblacion)
    aptitudes = calcularAptitudPoblacion(poblacion)
    print "Generacion ", generacion
    #imprimirPoblacion(poblacion, aptitudes)

    elMejor = elitismo(elMejor, poblacion[0], aptitudes[0])

    print 'El mejor:'
    imprimirIndividuo(elMejor[0], elMejor[1])
    

print 'EL mejor de los mejores del universo:'
imprimirIndividuo(elMejor[0], elMejor[1])


