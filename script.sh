#!/bin/bash

ROJO ='\033[0;31m'
VERDE ='\033[0;32m'
AMARILLO ='\033[1;33m'
REINICIAR ='\033[0m'

if [ "$#" -ne 2]; then
    echo -e "${ROJO}Uso incorrectto. Debes proporcionar la url CON XAVIER y el diccionario${REINICIAR}"
    echo -e "EJEMPLO : $0 'http://example.com/page?id=XAVIER' 'diccionario.txt'"
    exit 1
fi

URL = $1
DICCIONARIO = $2

if [ ! -f "$DICCIONARIO"];then
    echo -e "${ROJO}El diccionario no existe${REINICIAR}"
    exit 1
fi

PETICION_FILTRADA = $(curl -s -o /dev/null -w "%{http_code}" $URL)

TOTAL_LINEAS = $(wc -l < $DICCIONARIO)
LINEA_ACTUAL = 0

mostrar_progreso(){
    local progreso = $1
    local total = $2
    local porcentaje = $(($progreso * 100 ) / $total)
    local llenado = $((porcentaje * 40) / 100)
    local vacio = $((40 - $llenado))
    printf "\r["
    printf "%0.s${VERDE}#${REINICIAR}" $(seq 1 $llenado)
    printf "%0.s${AMARILLO}-${REINICIAR}" $(seq 1 $vacio)
    printf "] %d%%" "$porcentaje"
}
echo -e "${AMARILLO}Iniciando ataque de fuerza bruta${REINICIAR}"

while IFS = read -r PAYLOAD; do 
    URL_FUZZED = ${URL//XAVIER//$PAYLOAD}
    RESULTADO_CURL = $(curl -s -o /dev/null -w "%{http_code}" $URL_FUZZED)
    CODIGO_ESTADO = $(echo $RESULTADO_CURL | cut -d " " -f 1)
    TAMANIO = $(echo $RESULTADO_CURL | cut -d " " -f 2)
    if [ "$CODIGO_ESTADO" -ne 404 ] && [ "$TAMANIO" -ne "$PETICION_FILTRADA" ]; then
        echo -e "${VERDE}Encontrado: $URL_FUZZED${REINICIAR}"
        exit 0
    fi

    LINEA_ACTUAL = $(($LINEA_ACTUAL + 1))
    mostrar_progreso $LINEA_ACTUAL $TOTAL_LINEAS

done < $DICCIONARIO

echo -e "\n${AMARILLO} completado.${REINICIAR}"

