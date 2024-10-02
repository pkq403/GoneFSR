#!/bin/bash
echo "[*] Copiando dependencias a /usr/local/bin"
cp dependencies/coder_nlfsr /usr/local/bin 2> /dev/null
cp dependencies/decoder_nlfsr /usr/local/bin 2> /dev/null
if [ $? -ne 0 ]; then
    echo "[x] Error: no se han podido instalar las dependencias correctamente"
    echo "[!] Recuerda: debes ejecutar el instalador como administrador"
    exit 1
else 
    echo "[*] instalación terminada"
fi
