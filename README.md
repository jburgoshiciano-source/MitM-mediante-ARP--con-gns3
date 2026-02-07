# MitM-mediante-ARP--con-gns3

**Estudiante:** Juan Francisco burgos hiciano 
**Matrícula:** 2023-1981 
**Asignatura:** Seguridad en Redes  
**Fecha:** 06 Febrero 2026 

**Link del video**: [https://youtu.be/s6Emg7BInSg](https://www.youtube.com/watch?v=DgTl9wyqAUs)
 
 ## 1. Descripción y Topología del Escenario

El laboratorio se ha desplegado en un entorno virtualizado utilizando **GNS3**, simulando una infraestructura de red corporativa vulnerada desde el interior.

### Detalles de la Topología
* **Segmentación de Red:** Se ha configurado basada en los últimos 4 dígitos de la matrícula.
* **Direccionamiento IP:** Subred `198.1.98.0\24`.
* **Infraestructura:**
    * **Gateway Router Cisco IOU L3
    * **Switch Cisco IOU L2
* **Actores:**
    * **Atacante:** Kali Linux (IP asignada : `198.1.98.60`).
    * **Víctima:** PC1 / VPCS (IP asignada : `198.1.98.10`).
      
 
  <img width="888" height="650" alt="Image" src="https://github.com/user-attachments/assets/d3be5c83-f0de-4a50-a954-edcb1d3cc823" />


  ### Tabla de Direccionamiento

| Dispositivo | Dirección IP | Máscara de Subred | Gateway Predeterminado |
| :--- | :--- | :--- | :--- |
| **Router Gateway** | 198.1.98.1 | 255.255.255.0 (/24) | N/A |
| **Kali Linux (Atacante)** | 198.1.98.60 | 255.255.255.0 (/24) | 198.1.98.1 |
| **PC1 (Víctima)** | 198.1.98.10 | 255.255.255.0 (/24) | 198.1.98.1 |
---

## 2. Requisitos Previos y Herramientas

Para la ejecución exitosa de estos scripts, se requiere el siguiente entorno:

* **Sistema Operativo:** Kali Linux 
* **Lenguaje:** Python 3.x.
* **Librerías:** `Scapy` (Instalación: `sudo apt install python3-scapy`).
* **Privilegios:** Acceso **Root**

---
 Man-in-the-Middle (ARP Spoofing)

### Objetivo del Script
El script `ataque_arp.py` El objetivo del script es ejecutar un ataque Man-in-the-Middle (MitM) mediante ARP Spoofing, permitiendo al atacante interceptar y manipular el tráfico de red entre un equipo víctima y el gateway, demostrando cómo la falta de mecanismos de autenticación en ARP puede comprometer la confidencialidad y la integridad de la comunicación en un entorno de laboratorio controlado.

### Parámetros Usados
* **Interfaz:** `eth0`
* **IP DE VICTIMA:** 198.1.98.10
    * *IP DEL GATEWAY:* 198.1.98.1
    * *MAC DEL ATACANTE:* 00:0C:29:CA:4E:91
    * *TIPO DE ATAQUE:* ARP Spoofing (envenenamiento de tablas ARP).
 
## 5. Medidas de Mitigación
ARP Inspection (DAI):
Habilitar Dynamic ARP Inspection en switches para validar paquetes ARP y evitar suplantación.

DHCP Snooping:
Activar DHCP Snooping para crear una base de datos confiable usada por DAI.

Entradas ARP Estáticas:
Configurar tablas ARP estáticas en equipos críticos como servidores y gateways.

Segmentación de Red:
Implementar VLANs y limitar el acceso entre segmentos para reducir el alcance del ataque.

Monitoreo de Red:
Utilizar herramientas de detección de anomalías ARP para identificar ataques MitM.
