from rdflib.term import _XSD_STRING
import requests
import urllib.request as ur
import json
from bs4 import BeautifulSoup
import extruct
import requests
import pprint
from w3lib.html import get_base_url
import os
from os import path
from os import remove
from rdflib import Graph, Namespace, Literal
import rdflib
from rdflib import URIRef
from rdflib import RDF, XSD
from rdflib import ConjunctiveGraph, URIRef, RDFS, Literal


dataTomatoes = []
autoresTomatoes = []
actoresTomatoes = []
generosTomatoes = []
personajesTomatoes = []
criticasTomatoes = []

dataIMDB = []
actoresIMDB = []
autoresIMDB = []
generosIMDB = []

dataMeta = []
actoresMetacritic = []
autoresMetacritic = []
generosMetacritic = []
directoresMetacritic = []
generoMetacritic = []

dataECarte = []
actoresECartelera = []
directoresECartelera = []
generosECartelera = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

# Se imprime la info de la película en la web de dataRottenTomatoes
def imprimirInformacionTomatoes(dataRottentomatoes):
  
    
    pp = pprint.PrettyPrinter(indent=10)
    
    for key in dataRottentomatoes["json-ld"]:
        print()
        nombre= key["name"]       
        print("------- INFORMACIÓN DE LA PELÍCULA '"+nombre+"' -------")
      
        print()
        
        # Nombre
        print("Nombre completo: "+nombre)
        dataTomatoes.append(nombre)
        print()
        
        # Web de origen
        url=key["url"]
        print("Web de origen: "+url)
        dataTomatoes.append(url)
        print()
        
        # Calificación
        calificacion=key["contentRating"]
        print("Calificación del contenido: "+calificacion)
        dataTomatoes.append(calificacion)
        print()
        
        # Autor        
        for autor in key["author"] :
            print("Autor: "+autor["name"])
            autoresTomatoes.append(autor["name"])
        print()
        
        # Director      
        for direccion in key["director"]:
            print("Director: "+direccion["name"])
            dataTomatoes.append(direccion["name"])
        print()
    
        # Género/s
        print("Género/s al que pertenece la película: ")
        for genero in (key["genre"]):
            print("       -"+genero)
            generosTomatoes.append(key["genre"])
        print()
      
        # Productora
        productora = key["productionCompany"]["name"]
        print("Productora: "+productora)
        dataTomatoes.append(productora)
        print()
        
        # Actores
        print("Actores:")
        for actores in key["actors"]:
            print("       -"+(actores["name"]))
            actoresTomatoes.append(actores["name"])
        print()
        
        # Personajes
        print("Personajes: ")      
        for personaje in (key["character"]):
           print("       -"+str(personaje))
           personajesTomatoes.append(str(personaje))
        print()
        
        # Porcentaje de rating
        porcentajeRating = key["aggregateRating"]["ratingValue"]+ "% (por sobre un total de " +key["aggregateRating"]["ratingCount"] +" criticas"
        print("Porcentaje de rating: "+porcentajeRating)
        dataTomatoes.append(porcentajeRating)
        print()
        
        # Críticas
        print("Criticas:")
        for critica in key["review"]:
            print("       -Fecha: "+str(critica["dateCreated"]))
            print("       -Autor: "+critica["author"]["name"])            
            print("       -Comentario: "+critica["reviewBody"])
            print()
            criticasTomatoes.append(critica)
            
        """    
        print("Info del arreglo:")
        for info in dataTomatoes:
            print(info)
        """        
                 
# Se imprime la info de la película en la web de IMDB           
def imprimirInformacionImdb(dataImdb):
   
    
    for key in dataImdb["json-ld"]:
        print()

        nombre= key["name"]                 
        print("------- INFORMACIÓN DE LA PELÍCULA '"+nombre+"' -------")
        print()
        
        # Nombre
        print("Nombre completo: "+nombre)
        dataIMDB.append(nombre)
        print()
                
        # Web de origen
        url="https://www.imdb.com"+key["url"]
        print("Web de origen: "+url)
        dataIMDB.append(url)
        print()            
    
        # Calificación
        calificacion=key["contentRating"]
        print("Calificación del contenido: "+calificacion)
        dataIMDB.append(calificacion)
        print()      
        
        # Autor
            # Se guarda en una lista hasta el elemento deseado, ya que como no existe el atributo 'name' en todo el dic, falla al querer imprimirlo
        print("Autores:")
        
        i=0
        for creat in key["creator"]:                    
            if (i <= 5):                                
                i = i + 1     
                autoresIMDB.append(creat)    
                     
        for element in autoresIMDB:
            print ("       -"+element["name"])                
        print()
   
        #CREATOR (código de prueba para los creator) (funcionando mejor mas arriba)
        """
        print((key["creator"][0]["name"]))
        print((key["creator"][1]["name"]))
        print((key["creator"][2]["name"]))
        print((key["creator"][3]["name"]))
        print((key["creator"][4]["name"]))
        print((key["creator"][5]["name"]))        
        """
        
        # Director    
        director=key["director"]["name"]                 
        print("Director: "+director)
        dataIMDB.append(director)
        print()
        
        
        # Género/s
        print("Género/s al que pertenece la película: ")
        for genero in (key["genre"]):
            print("       -"+genero)
            generosIMDB.append(genero)
        print()
        
        # Actores
        print("Actores:")
        for actor in key["actor"]:
            print("       -"+(actor["name"]))
            actoresIMDB.append(actor)
        print()
        
        # Porcentaje de rating
        porcentajeRating = str(key["aggregateRating"]["ratingValue"])+ "% (por sobre un total de " +str(key["aggregateRating"]["ratingCount"]) +" criticas)"
        print("Porcentaje de rating: "+porcentajeRating)
        dataIMDB.append(porcentajeRating)
        print()   
        
        # Críticas   
        fecha = "Fecha de creación: "+key["review"]["dateCreated"] 
        autor = "Autor: "+ key["review"]["author"]["name"]
        comentario = "Comentario: "+ key["review"]["reviewBody"]
        print("Críticas:")                
        print("       -Fecha: "+(key["review"]["dateCreated"]))
        print("       -Autor: "+(key["review"]["author"]["name"]))
        print("       -Comentario: "+(key["review"]["reviewBody"]))
        dataIMDB.append(fecha)
        dataIMDB.append(autor)
        dataIMDB.append(comentario)
        print()    
               
        # Descripción
        descripcion=key["description"]
        print("Descripción de la película: "+descripcion)
        dataIMDB.append(descripcion)
        print()        
                         
        # Trailer
        trailer = key["trailer"]["description"]
        print("Descripción del trailer: "+trailer)
        dataIMDB.append(trailer)
        print()        
            
        # Fecha de publicación
        """
        print("Fecha de publicación: "+key["datePublished"])
        print()
        """
                
        # Duración
        duracion=key["duration"]
        print("Duración: "+duracion)
        dataIMDB.append(duracion)
        print()
                       
        # Palabras claves
   #     palabrasClaves = key["keywords"]
   #     print("Palabras claves: "+palabrasClaves)
   #     dataIMDB.append(palabrasClaves)
   #     print()
        
         
# Se imprime la info de la película en la web de MetaCritic           
def imprimirInformacionMetacritic(dataMetacritic):

    
    for key in dataMetacritic["json-ld"]:
        
        print()
               
        print("------- INFORMACIÓN DE LA PELÍCULA '"+key["name"]+"' -------")
        print()
        
        # Nombre
        nombre= key["name"]  
        print("Nombre completo: "+nombre)
        dataMeta.append(nombre)
        print()
                
        # Web de origen
        url= key["url"]  
        print("Web de origen: "+url)
        dataMeta.append(url)
        print()     
        
        # ContentRating
        calificacion=key["contentRating"]
        print("ContentRating: "+calificacion)
        dataMeta.append(calificacion)
        print()       
    
        # Director            
        print("Directores:")        
        for director in key["director"]:
            print("       -"+(director["name"]))
            directoresMetacritic.append(director)
        print()
    
        # Género/s
        print("Género/s al que pertenece la película: ")
        for genero in (key["genre"]):
            print("       -"+genero)
            generoMetacritic.append(genero)
        print()
        
        # Actores
        print("Actores:")
        for actor in key["actor"]:
            print("       -"+(actor["name"]))
            actoresMetacritic.append(actor)
        print()
        
        # Porcentaje de rating
        porcentajeRating = str(key["aggregateRating"]["ratingValue"])+ "% (por sobre un total de " +str(key["aggregateRating"]["ratingCount"]) +" criticas)"
        print(porcentajeRating)
        dataMeta.append(porcentajeRating)
        print()
        
        
        # Descripción
        descripcion = key["description"]
        print("Descripción: "+descripcion)
        dataMeta.append(descripcion)
        print()
        
        # Duración
        duracion = key["duration"]
        print("Duración: "+duracion)
        dataMeta.append(duracion)
        print()
        
                                    
        # Fecha de publicación
        """
        print("Fecha de publicación: "+key["datePublished"])
        print()
        """
     
    
        # Palabras claves
       # print("Palabras claves: "+key["keywords"])
       # print()
        
      
# Se imprime la info de la película en la web de ECartelera    
def imprimirInformacionEcartelera(dataEcartelera):
        
    for key in dataEcartelera["json-ld"]:
        
        print()
        nombre = key["name"]
        print("------- INFORMACIÓN DE LA PELÍCULA '"+nombre+"' -------")   
        print()
        
        # Nombre    
        print("Nombre completo: "+nombre)
        dataECarte.append(nombre)
        print()
                
        # Web de origen
        url = key["@id"]
        print("Web de origen: "+url)
        dataECarte.append(url)
        print()          
                 
        # Director          
        print("Directores:")
        for director in key["director"]:
            print("       -"+(director["name"]))
            directoresECartelera.append(director)
        print()  
        
        # Género/s
        print("Género/s al que pertenece la película: ")
        for genero in (key["genre"]):
            print("       -"+genero)
            generosECartelera.append(genero)            
        print()
            
        # Actores 
        print("Actores:")
        for actor in key["actor"]:
            print("       -"+(actor["name"]))
            actoresECartelera.append(actor)
        print()
        
        # Porcentaje de rating
        porcentajeRating = str(key["aggregateRating"]["ratingValue"])+ "% (por sobre un total de " +str(key["aggregateRating"]["ratingCount"]) +" criticas)"
        print(porcentajeRating)
        dataECarte.append(porcentajeRating)
        print()
            
        # Descripción
        descripcion = key["description"]
        print("Descripción: "+descripcion)
        dataECarte.append(descripcion)        
        print()
                     
        # Duración
        duracion = key["duration"]
        print("Duración: "+duracion)
        dataECarte.append(duracion)
        print()
                        
        #exportarAJson(name, web, description, duracion, porcentajeRating)
        
        
# Método que exporta a JSON el merge recibido        
def  generarJson(arregloWeb, nombre, calificacion, arregloAutores, director, arregloGeneros, productora, arregloActores, arregloPersonajes, porcentajeTomatoes, porcentajeIMDB, porcentajeMetacritic, porcentajeECartelera, arregloCriticas, descripcion, trailer, duracion):
    
     
    g = Graph()
    Mi_ontologia = Namespace("https://raw.githubusercontent.com//twstp3/master/owlgenerado.ttl#")
    Ontología_de_schema = Namespace("https://schema.org/")
    data = {}
    data['movies'] = []
    
    data['movies'].append({
    'arregloWeb': arregloWeb,
    'nombre': nombre,
    'calificacion': calificacion,
    'arregloAutores': arregloAutores,    
    'director': director,
    'arregloGeneros': arregloGeneros,
    'productora': productora,
    'arregloActores': arregloActores,    
    'arregloPersonajes': arregloPersonajes,
    'porcentajeTomatoes': porcentajeTomatoes,
    'porcentajeIMDB': porcentajeIMDB,
    'porcentajeMetacritic': porcentajeMetacritic,
    'porcentajeECartelera': porcentajeECartelera,
    'arregloCriticas': arregloCriticas,
    'descripcion': descripcion,
    'trailer': trailer,
    'duracion': duracion})
    peli =  Mi_ontologia["Wonder_Woman"]
    g.add((peli, RDF.type, Ontología_de_schema["Movie"]))  ## genera la relacion #Literal(nombre,datatype=XSD.int)
    
    peli =  Ontología_de_schema["director"]
    g.add((peli, RDF.type, Mi_ontologia["Person"]))
    g.add((peli,Ontología_de_schema["name"], Literal(director)))   
   
    peli =  Ontología_de_schema["producer"]
    g.add((peli, RDF.type, Ontología_de_schema["Person"]))  
    g.add((peli,Ontología_de_schema["producer"], Literal(productora)))  

    peli =  Ontología_de_schema["trailer"]
    g.add((peli, RDF.type, Ontología_de_schema["VideoObject"]))  
    g.add((peli,Ontología_de_schema["trailer"], Literal(trailer)))


    peli =  Mi_ontologia["duration"]
    g.add((peli, RDF.type, Mi_ontologia["Duration"]))  
    g.add((peli,Ontología_de_schema["duration"], Literal(duracion)))

   
    for autor in arregloAutores:
       nodoautor =  Ontología_de_schema["autor"+autor.replace(' ', '')]
       g.add((nodoautor, RDF.type, Ontología_de_schema["Person"]))  
       g.add((nodoautor,Ontología_de_schema["name"], Literal(autor.replace(' ', ''))))
   

    for actor in arregloPersonajes:
       nodopersonaje =  Ontología_de_schema["actor"]
       g.add((nodopersonaje, RDF.type, Ontología_de_schema["Person"]))  
       g.add((nodopersonaje,Ontología_de_schema["actor"], Literal(actor))) 

   # peli =  Mi_ontologia["palabrasClaves"]
   # g.add((peli, RDF.type, Mi_ontologia["palabrasClaves"]))  
   # g.add((peli,Ontología_de_schema["palabrasClaves"], Literal(palabrasClaves)))

    for web in arregloWeb:
       nodoweb =  Mi_ontologia["web"+web.replace(' ', '')]
       g.add((nodoweb, RDF.type,Ontología_de_schema["Web"]))  
       g.add((nodoweb,Ontología_de_schema["Web"], Literal(web)))
    
   # for genero in arregloGeneros:
   #    nodogenero =  Ontología_de_schema["genre"]
   #    g.add((nodogenero, RDF.type, Ontología_de_schema["Movie"]))  
   #    g.add((nodogenero,Ontología_de_schema["genre"], Literal(genero))) 

   # peli =  Mi_ontologia["calification"]
   # g.add((peli, RDF.type, Mi_ontologia["schema:calification"]))  
   # g.add((peli,Ontología_de_schema["calification"], Literal(calificacion,datatype=XSD.float)))
    
  
         
    
  #  peli =  Mi_ontologia["director"]
  #  g.add((peli, RDF.type, Mi_ontologia["schema:director"]))  
  #  g.add((peli,Ontología_de_schema["director"], Literal(director)))
    
 #   for genero in arregloGeneros:
 #      peli =  Mi_ontologia["genre"]
 #      g.add((peli, RDF.type, Mi_ontologia["schema:genre"]))  
  #     g.add((peli,Ontología_de_schema["Genre"], Literal(genero)))    
    
 #   peli =  Mi_ontologia["producer"]
 #   g.add((peli, RDF.type, Mi_ontologia["schema:producer"]))  
 #   g.add((peli,Ontología_de_schema["producer"], Literal(productora)))

 #   peli =  Mi_ontologia["trailer"]
 #   g.add((peli, RDF.type, Mi_ontologia["schema:trailer"]))  
 #   g.add((peli,Ontología_de_schema["trailer"], Literal(trailer)))



  #  peli =  Mi_ontologia["description"]
  #  g.add((peli, RDF.type, Mi_ontologia["schema:description"]))  
  #  g.add((peli,Ontología_de_schema["description"], Literal(descripcion)))

    peli =  Mi_ontologia["porcentajeTomatoes"]
    g.add((peli, RDF.type, Mi_ontologia["PorcentajeTomatoes"]))  
    g.add((peli,Ontología_de_schema["porcentajeTomatoes"], Literal(porcentajeTomatoes)))

    peli =  Mi_ontologia["porcentajeIMDB"]
    g.add((peli, RDF.type, Mi_ontologia["PorcentajeIMDB"]))  
    g.add((peli,Ontología_de_schema["porcentajeIMDB"], Literal(porcentajeIMDB)))

    peli =  Mi_ontologia["porcentajeMetacritic"]
    g.add((peli, RDF.type, Mi_ontologia["PorcentajeMetacritic"]))  
    g.add((peli,Ontología_de_schema["porcentajeMetacritic"], Literal(porcentajeMetacritic)))

    peli =  Mi_ontologia["porcentajeECartelera"]
    g.add((peli, RDF.type, Mi_ontologia["PorcentajeECartelera"]))  
    g.add((peli,Ontología_de_schema["porcentajeECartelera"], Literal(porcentajeECartelera)))


    g.serialize(destination='final.ttl', format='turtle')
  
   # with open('data.json', 'w', encoding="utf-8") as file:
   # 	json.dump(data, file, indent=18,ensure_ascii=False)

def mergePeliculas(dataTomatoes, autoresTomatoes, actoresTomatoes, generosTomatoes, personajesTomatoes, criticasTomatoes, dataIMDB, actoresIMDB, autoresIMDB, generosIMDB, dataMeta, actoresMetacritic, autoresMetacritic, generosMetacritic, directoresMetacritic, generoMetacritic, dataECarte, actoresECartelera, directoresECartelera, generosECartelera):
    
    arregloWeb = []
    arregloAutores = []
    arregloActores = []
    arregloGeneros = []
    arregloPersonajes = []
    arregloCriticas = []
    
    print("##############  MERGE DE LA PELÍCULA EN LAS DIFERENTES WEBS ##############")
    print()
    print("Información proveniente de las siguientes webs: ")
    print(dataTomatoes[1])
    print(dataIMDB[1])
    print(dataMeta[1])
    print(dataECarte[1])
    arregloWeb.append(dataTomatoes[1])
    arregloWeb.append(dataIMDB[1])
    arregloWeb.append(dataMeta[1])
    arregloWeb.append(dataECarte[1])
    print()
    
    nombre = dataTomatoes[0]
    print("Nombre de la película "+nombre)    
    print()
    
    calificacion = dataTomatoes[2]
    print("La calificación de la película es: "+calificacion)
    print()
    
    print("Los autores de la película son: ")
    if (len(autoresIMDB) >= len(autoresTomatoes)):        
        for autores in autoresIMDB:
            print(autores["name"])
            arregloAutores.append(autores["name"])
          
    else:
        for autores in autoresTomatoes:
            print(autores["name"])
            arregloAutores.append(autores["name"])
    print()
    
    director = dataIMDB[3]
    print("El director de la película es: "+director)
    print()
    
    print("Los géneros de la película son: ")
    for genero in generosIMDB:
        print(genero)
        arregloGeneros.append(genero)
    print()
    
    productora = dataTomatoes[4]
    print("La productora de la película es: "+productora)
    print()
    
    print("Los actores de la película son: ")    
    for actor in actoresMetacritic:
        print(actor["name"])
        arregloActores.append(actor)
    print()
    
    print("Los personajes de la película son: ")   
    for personaje in personajesTomatoes:
        print(personaje)
        arregloPersonajes.append(actor)
    print() 
    
    porcentajeTomatoes= dataTomatoes[5]
    porcentajeIMDB= dataIMDB[4]
    porcentajeMetacritic= dataMeta[3]
    porcentajeECartelera= dataECarte[2]
    print("PORCENTAJE DE RATING POR WEB:")
    print("Tomatoes: "+porcentajeTomatoes)
    print("IMDB: "+porcentajeIMDB)
    print("Metacritic: "+porcentajeMetacritic)
    print("E cartelera: "+porcentajeECartelera)
    print()
    
    print("CRITICAS POR WEB:")
    print("Tomatoes:")
    for critica in criticasTomatoes:
        print("       -Fecha: "+str(critica["dateCreated"]))
        print("       -Autor: "+critica["author"]["name"])            
        print("       -Comentario: "+critica["reviewBody"])
        arregloCriticas.append(critica)
    print() 
    
    print("IMDB:")
    print(dataIMDB[5])
    print(dataIMDB[6])
    print(dataIMDB[7])
    arregloCriticas.append(dataIMDB[5])
    arregloCriticas.append(dataIMDB[6])
    arregloCriticas.append(dataIMDB[7])
    print()
    
    descripcion = dataECarte[3]
    print("Descripción de la película: "+descripcion)
    print()
    
    trailer = dataIMDB[8]
    print("Trailer de la película: "+trailer)
    print()
    
    duracion = dataECarte[4]
    print("Duración de la película: "+duracion)
    print()
    
  #  palabrasClaves= dataIMDB[11]
  #  print("Palabras claves: "+palabrasClaves)
  #  print()    
    
    generarJson(arregloWeb, nombre, calificacion, arregloAutores, director, arregloGeneros, productora, arregloActores, arregloPersonajes, porcentajeTomatoes, porcentajeIMDB, porcentajeMetacritic, porcentajeECartelera, arregloCriticas, descripcion, trailer, duracion)
        
#pp = pprint.PrettyPrinter(indent=2)

# Se obtienen las URI's de cada película
wonderWomanC1 = requests.get('https://www.rottentomatoes.com/m/wonder_woman_1984')
wonderWomanC2 = requests.get('https://www.imdb.com/title/tt7126948')
wonderWomanC3 = requests.get('https://www.metacritic.com/movie/wonder-woman-1984', headers=headers)
wonderWomanC4 = requests.get('https://www.ecartelera.com/peliculas/wonder-woman-1984')
base_url = get_base_url(wonderWomanC1.text, wonderWomanC1.url)
dataRottentomatoes = extruct.extract(wonderWomanC1.text, base_url=base_url, syntaxes=['json-ld'])
dataImdb = extruct.extract(wonderWomanC2.text, base_url=base_url, syntaxes=['json-ld'])
dataMetacritic = extruct.extract(wonderWomanC3.text, base_url=base_url, syntaxes=['json-ld'])
dataEcartelera = extruct.extract(wonderWomanC4.text, base_url=base_url, syntaxes=['json-ld'])
#pp.pprint()
print()
print("##############  A CONTINUACIÓN, SE IMPRIME LA INFORMACIÓN DE LAS DIFERENTES WEBS ##############")
print()
imprimirInformacionTomatoes(dataRottentomatoes)
imprimirInformacionImdb(dataImdb)
imprimirInformacionMetacritic(dataMetacritic)
imprimirInformacionEcartelera(dataEcartelera)
mergePeliculas(dataTomatoes, autoresTomatoes, actoresTomatoes, generosTomatoes, personajesTomatoes, criticasTomatoes, dataIMDB, actoresIMDB, autoresIMDB, generosIMDB, dataMeta, actoresMetacritic, autoresMetacritic, generosMetacritic, directoresMetacritic, generoMetacritic, dataECarte, actoresECartelera, directoresECartelera, generosECartelera)


