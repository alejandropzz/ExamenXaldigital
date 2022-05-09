import requests

#Funcion para obtener los datos
def obtenerDatos():
    liga="https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow"
    datos = requests.get(url=liga, params={}).json()

    items={}
    if("items" in datos):
        items=datos["items"]
    return items

#Funcion para obtener los valores (contestadas, no contestadas, etc)
def procesarDatos(datos):
    contestadas=0
    noContestadas=0
    incompleto = 0
    
    menosVistas={}
    respuestaU= {}
    respuestaA={}
    popular={}
    

    for i in range(len(datos)):
        item=datos[i]
        itemIncompleto=False


        #En esta parte se hace las validaciones y los calculos
        if("is_answered" in item):
            if(item["is_answered"]==True):
                contestadas=contestadas+1
            elif(item["is_answered"] == False):
                noContestadas=noContestadas+1
        else:
            itemIncompleto=True

        if ("creation_date" in item):
            if (respuestaU == {}):
                respuestaU = item
            elif (respuestaU["creation_date"] > item["creation_date"]):
                respuestaU = item

            if (respuestaA == {}):
                respuestaA = item
            elif (respuestaA["creation_date"] < item["creation_date"]):
                respuestaA = item
        else:
            itemIncompleto=True

        if("view_count" in item):

            if (menosVistas == {}):
                menosVistas = item
            elif (menosVistas["view_count"] > item["view_count"]):
                menosVistas = item
        else:
            itemIncompleto=True

        if ("owner" in item):
            if("reputation" in item["owner"]):
                if(popular=={}):
                    popular=item
                elif(popular["owner"]["reputation"]<item["owner"]["reputation"]):
                    popular=item
        else:
            itemIncompleto=True

        if(itemIncompleto==True):
            incompleto=incompleto+1

    respuesta={}
    respuesta["contestadas"]=contestadas
    respuesta["no_contestadas"] = noContestadas
    respuesta["menos_vistas"] = menosVistas
    respuesta["respuesta_vieja"] = respuestaU
    respuesta["respuesta_reciente"] = respuestaA
    respuesta["mayor_reputacion"]=popular
    respuesta["items_incompletos"] = incompleto

    return respuesta

#Funcion para imprimir las respuestas
def imprimirRespuesta(respuesta):
    llaves = respuesta.keys()
    for k in llaves:
        print(k, ":", respuesta[k],"\n")


#Funcion principal
def main():
    datos=obtenerDatos()
    respuesta=procesarDatos(datos)
    imprimirRespuesta(respuesta)


main()
