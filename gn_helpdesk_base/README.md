# GoodNews · Incidencias de tiendas (tickets de asistencia) (modelos)

Campos de los tickets de asistencia (los que rellena Buddy), colores por prioridad, alertas críticas por ciudad, seguidores, reapertura/cierre por correo y mantenimientos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `account`, `helpdesk`, `maintenance`.

Va antes que `gn_helpdesk` (la lógica).

## Qué contiene

**Campos** (30)

- helpdesk.ticket.x_studio_barista_id (Barista Id, char)
- helpdesk.ticket.x_studio_barista_name (Barista Name, char)
- helpdesk.ticket.x_studio_city (City, selection)
- helpdesk.ticket.x_studio_comentario_valoracion (Feedback comments, text)
- helpdesk.ticket.x_studio_confirmed_date (Fecha confirmada intervención, text)
- helpdesk.ticket.x_studio_email_enviado (Sent email to supplier, boolean)
- helpdesk.ticket.x_studio_fecha_email (Sent Date and Time, datetime)
- helpdesk.ticket.x_studio_incidencia_catalogo (Notion Incidence, char)
- helpdesk.ticket.x_studio_incidencia_detectada (Incidence, text)
- helpdesk.ticket.x_studio_intervention_date (Intervention date, datetime)
- helpdesk.ticket.x_studio_notas (Call summary, text)
- helpdesk.ticket.x_studio_priority (Priority, selection)
- helpdesk.ticket.x_studio_recursos_visuales_mov (Videos, text)
- helpdesk.ticket.x_studio_reopened (Reopened, boolean)
- helpdesk.ticket.x_studio_resumen_problema (Problem summary, text)
- helpdesk.ticket.x_studio_status (Estado, selection)
- helpdesk.ticket.x_studio_valoracion (Feedback rating, selection)
- helpdesk.ticket.x_studio_visual_elements (Images, text)
- account.move.x_studio_many2many_field_4rv_1jpl3q5vt (Nuevo Many2Many, many2many)
- account.move.x_studio_many2many_field_75_1jpl3s1cq (Nuevo Many2Many, many2many)
- account.move.x_studio_tickets (Tickets, many2many)
- helpdesk.ticket.x_studio_invoice (Invoice, many2one)
- helpdesk.ticket.x_studio_maintenance_request_id (Solicitud de mantenimiento, many2many)
- helpdesk.ticket.x_studio_pdv (Store, many2one)
- helpdesk.ticket.x_studio_reopened_tickets (Reopened tickets, many2many)
- helpdesk.ticket.x_studio_responsable (responsable, many2one)
- helpdesk.ticket.x_studio_supplier (Supplier, many2one)
- maintenance.request.x_studio_pdv (Pdv, many2one)
- maintenance.request.x_studio_survey (Survey, many2one)
- maintenance.request.x_studio_ticket_origin (ticket origin, many2one)
