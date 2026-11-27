# GoodNews · Incidencias de tiendas (tickets de asistencia)

Campos de los tickets de asistencia (los que rellena Buddy), colores por prioridad, alertas críticas por ciudad, seguidores, reapertura/cierre por correo y mantenimientos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base_automation`, `gn_helpdesk_base`, `helpdesk`, `mail`.

## Qué contiene

**Automatizaciones** (7)

- Colores tickets (helpdesk.ticket, on_create_or_write)
- Correos de seguimiento alertas crítica (helpdesk.ticket, on_create_or_write)
- Añadir seguidores tickets de asistencia (helpdesk.ticket, on_create_or_write)
- Propagar ticket en factura (helpdesk.ticket, on_create_or_write)
- Reabrir tickets con mensaje entrante (helpdesk.ticket, on_message_received)
- Cerrar tickets con mensaje salida (helpdesk.ticket, on_message_sent)
- Creacion de mantenimientos desde buddy (helpdesk.ticket, on_create_or_write)

**Acciones de servidor** (7)

- Actualizar Índice de Colores (helpdesk.ticket)
- Ejecutar código (helpdesk.ticket)
- Ejecutar código (helpdesk.ticket)
- Ejecutar código (helpdesk.ticket)
- Ejecutar código (helpdesk.ticket)
- Ejecutar código (helpdesk.ticket)
- Ejecutar código (helpdesk.ticket)

**Acciones de ventana** (1)

- Enviar correo electrónico (Incidencias Barcelona (crítica)) (mail.compose.message)
