from scapy.all import get_if_list

interfaces = get_if_list()
print("Interfaces disponibles:")
for iface in interfaces:
    print(iface)
