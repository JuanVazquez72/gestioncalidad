import csv
from passlib.hash import sha256_crypt
from Levenshtein import distance



def lee_archivo_csv(archivo:str)->list:
    '''Lee un archivo CSV y regresa una lista de registros
    '''
    lista = []
    try:
        with open(archivo,'r',encoding='utf-8') as fh:
            csv_reader = csv.reader(fh)
            for renglon in csv_reader:
                lista.append(renglon)
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return lista

def lee_diccionario_csv(archivo:str)->list:
    '''Lee un archivo CSV y regresa un diccionario de diccionarios
    '''
    diccionario = {}
    try:
        with open(archivo,'r',encoding='UTF-8') as fh:
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['usuario']
                diccionario[llave]=renglon
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return diccionario

def lee_diccionario_csv_id(archivo:str)->list:
    '''Lee un archivo CSV y regresa un diccionario de diccionarios
    '''
    diccionario = {}
    try:
        with open(archivo,'r',encoding='UTF-8') as fh:
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['id']
                diccionario[llave]=renglon
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return diccionario

def lee_diccionario_csv_bicicleta(archivo:str)->list:
    '''Lee un archivo CSV y regresa un diccionario de diccionarios
    '''
    diccionario = {}
    try:
        with open(archivo,'r',encoding='UTF-8') as fh:
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['tipo_bicicleta']
                diccionario[llave]=renglon
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return diccionario




def lee_diccionario_csv_admin(archivo:str)->list:
    '''Lee un archivo CSV y regresa un diccionario de diccionarios
    '''
    diccionario = {}
    try:
        with open(archivo,'r',encoding='UTF-8') as fh:
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['admin']
                diccionario[llave]=renglon
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return diccionario

def lee_diccionario_csv_trabajadores(archivo:str)->list:
    '''Lee un archivo CSV y regresa un diccionario de diccionarios
    '''
    diccionario = {}
    try:
        with open(archivo,'r',encoding='UTF-8') as fh:
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['trabajador']
                diccionario[llave]=renglon
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return diccionario


def crea_diccionario(diccionario_peliculas:dict,llave_ext:str)->dict:
    diccionario = {}
    for id,pelicula in diccionario_peliculas.items():
        llave = pelicula[llave_ext]
        if llave not in diccionario:
            diccionario[llave] = [pelicula]
        else:
            diccionario[llave].append(pelicula)
    return diccionario



def sacar_usuarios(dicc:dict)->list:
    lista_usuarios = []
    for usuario,diccionario in dicc.items():
        lista_usuarios.append(usuario)
    return lista_usuarios

def graba_diccionario(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh: #fh = file handle
        lista_campos = obten_campos(diccionario, llave_dict)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        renglones = []
        for llave, valor_d in diccionario.items():
            d = { 'usuario':llave}
            for key, value  in valor_d.items():
                d[key] = value
            renglones.append(d)
        dw.writerows(renglones)


def graba_diccionario_admin(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh: #fh = file handle
        lista_campos = obten_campos(diccionario, llave_dict)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        renglones = []
        for llave, valor_d in diccionario.items():
            d = { 'admin':llave}
            for key, value  in valor_d.items():
                d[key] = value
            renglones.append(d)
        dw.writerows(renglones)

def graba_diccionario_trabajador(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh: #fh = file handle
        lista_campos = obten_campos(diccionario, llave_dict)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        renglones = []
        for llave, valor_d in diccionario.items():
            d = { 'trabajador':llave}
            for key, value  in valor_d.items():
                d[key] = value
            renglones.append(d)
        dw.writerows(renglones)

def graba_diccionario_id(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh: #fh = file handle
        lista_campos = obten_campos(diccionario, llave_dict)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        renglones = []
        for llave, valor_d in diccionario.items():
            d = { 'id':llave}
            for key, value  in valor_d.items():
                d[key] = value
            renglones.append(d)
        dw.writerows(renglones)


def graba_diccionario_nombre_mascota(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh: #fh = file handle
        lista_campos = obten_campos(diccionario, llave_dict)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        renglones = []
        for llave, valor_d in diccionario.items():
            d = { 'nombre_mascota':llave}
            for key, value  in valor_d.items():
                d[key] = value
            renglones.append(d)
        dw.writerows(renglones)


def obten_campos(diccionario:dict,llave_d:str)->list:
    lista = [llave_d]
    llaves = list(diccionario.keys())
    k = llaves[0]
    nuevo_diccionario = diccionario[k]
    lista_campos = list(nuevo_diccionario.keys())
    lista.extend(lista_campos)
    return lista

def limpia_texto(texto:str)->str:
    lista_simbolos = [',',';','.','-','_',':','¿','?','¡','!']
    for simbolo in lista_simbolos:
        texto = texto.replace(simbolo,'')
    return texto
        
def agrega_palabras(diccionario:dict, cadena:str, diccionario_pelicula):
    minusculas = cadena.lower()
    cadena_limpia = limpia_texto(minusculas)
    palabras = cadena_limpia.split(" ")
    for palabra in palabras:
        if palabra not in diccionario:
            diccionario[palabra] = [ diccionario_pelicula ]
        else:
            diccionario[palabra].append(diccionario_pelicula)






def compara_distancia(diccionario:dict,frase:str)->dict:
    diccionario_resultados = {}
    lista_tuplas = []
    for llave, lista in diccionario.items():
        L = distance(frase, llave) 
        tupla = (llave, L)
        lista_tuplas.append(tupla)
    #ordenar lista
    sorted_t = sorted(lista_tuplas, key=lambda tup:tup[1])
    # [ ("memory",15),("memory",2),("memory",3)]
    for t in sorted_t[0:6]:
        llave = t[0]
        distancia = t[1]
        peliculas = diccionario[llave] #lista peliculas asociadas con la llave
        for pelicula in peliculas: #extraemos peliculas de la lista
            id = pelicula['id']
            pelicula['distancia'] = distancia #agregamos distancia de la frase original
            pelicula['frase'] = llave #agregamos la frase con la que la encontramos
            diccionario_resultados[id] = pelicula
    return diccionario_resultados


#if __name__ == "__main__":
   
