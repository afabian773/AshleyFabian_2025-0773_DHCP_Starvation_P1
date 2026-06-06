# AshleyFabian_2025-0773_DHCP_Starvation_P1

## Ataque DHCP Starvation — Agotamiento del Pool
**Estudiante:** Ashley Fabian  
**Matrícula:** 2025-0773  
**Práctica:** P1  
**Asignatura:** Seguridad en Redes  
**Plataforma:** GNS3 — Kali Linux  

---

## Descripción

Este repositorio contiene el script y la documentación técnica del ataque DHCP Starvation. El atacante envía múltiples solicitudes DHCPDISCOVER con MACs aleatorias, agotando el pool de direcciones IP del servidor DHCP legítimo e impidiendo que nuevos hosts obtengan configuración de red.

---

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `AshleyFabian_2025-0773_DHCP_Starvation_P1.py` | Script del ataque |
| `AshleyFabian_2025-0773_Informe_DHCP_Starvation_P1.pdf` | Documentación técnica profesional |

---

## Topología de red

| Dispositivo | IP | Puerto |
|---|---|---|
| R1 (CSR1000v) | 25.7.73.1/24 | Gi1 → SW1 Gi0/0 |
| SW1 (vIOS L2) | 25.7.73.2/24 | Gi0/1→VPCS, Gi0/2→Kali |
| Kali Linux | 25.7.73.50/24 | eth0 → SW1 Gi0/2 |
| VPCS (PC1) | 25.7.73.20/24 | eth0 → SW1 Gi0/1 |

**Red:** 25.7.73.0/24 (basada en matrícula 2025-0773)

---

## Uso del script

```bash
# Ejecutar el ataque enviando 254 solicitudes
sudo python3 AshleyFabian_2025-0773_DHCP_Starvation_P1.py -i eth0 -c 254

# Verificar en R1
R1# show ip dhcp binding
R1# show ip dhcp pool

# Intentar obtener IP desde la VPCS (fallará)
dhcp

# Parámetros disponibles
# -i  Interfaz de red
# -c  Cantidad de DISCOVER (0=infinito)
# -d  Delay entre paquetes en segundos (default: 0)
```

---

## Evidencia del ataque

- Pool DHCP de R1 casi agotado tras el ataque
- Entradas en estado `Selecting` (sin completar handshake)
- VPCS no puede obtener IP: `Can't find dhcp server`
- R1 reporta `PING_CONFLICT` al verificar IPs del pool

---

## Contra-medida

```
SW1(config)# ip dhcp snooping
SW1(config)# ip dhcp snooping vlan 1
SW1(config-if)# ip dhcp snooping limit rate 15  ← en puerto de Kali (Gi0/2)
```

---

## Video de demostración

🎬 [Ver video en YouTube](https://youtu.be/NE6pmPOR9w0?si=LM-RCcJfXIXznT0N)

> El video muestra el ataque en funcionamiento y la aplicación de la contra-medida.

---

## Requisitos

- Kali Linux
- Python 3.6+
- Scapy: `sudo apt install python3-scapy`
- GNS3 con CSR1000v y vIOS L2
- Ejecutar como root
