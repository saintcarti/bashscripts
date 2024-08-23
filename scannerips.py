import argparse
from scapy.all import ARP, Ether, srp

def escanear_red(rango_ip):
    # Crear una solicitud ARP
    arp = ARP(pdst=rango_ip)
    # Crear un paquete Ether broadcast (destino a todas las direcciones MAC)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combinar paquetes ARP y Ether
    paquete = ether/arp

    # Enviar paquete y recibir respuesta
    resultado = srp(paquete, timeout=3, verbose=0)[0]

    # Crear una lista para guardar los resultados
    dispositivos = []

    for enviado, recibido in resultado:
        # Almacenar IP y MAC en un diccionario
        dispositivos.append({'ip': recibido.psrc, 'mac': recibido.hwsrc})

    return dispositivos

if __name__ == "__main__":
    # Configurar argparse para obtener los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Escanear red para encontrar dispositivos conectados.")
    parser.add_argument("rango_ip", help="Rango de IPs a escanear (por ejemplo, 192.168.1.1/24) o una sola IP.")
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    # Obtener el rango de IP desde los argumentos
    rango_ip = args.rango_ip
    
    # Ejecutar el escaneo de red
    dispositivos = escanear_red(rango_ip)

    print("Dispositivos encontrados en la red:")
    print("IP" + " "*18 + "MAC")
    for dispositivo in dispositivos:
        print("{:16}    {}".format(dispositivo['ip'], dispositivo['mac']))
