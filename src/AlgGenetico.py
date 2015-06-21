'''
Created on 21/06/2015

@author: Isaac
'''
import sys

def verificaArgumentos():
        if len(sys.argv) <= 1:
            nombreImagen = "circulo.png"
        else:
            nombreImagen = sys.argv[1]
            print 'Abriendo <', nombreImagen , '> ...'
        print 'Imagen a imitar: ', nombreImagen

