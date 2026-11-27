# GoodNews · Campos sueltos de Studio (modelos)

Campos creados con Studio en modelos de Odoo que el mapa del Manual no asigna a ningún desarrollo.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `account`, `base`, `event`, `gn_studio_modelos_base`, `hr_attendance`, `product`, `survey`.

## Qué contiene

**Campos** (33)

- account.move.x_studio_banco_previsin_de_pago (Banco Prevision de Pago, selection)
- event.event.x_studio_additional_event_information (X Studio Additional Event Information, text)
- event.event.x_studio_attachment_1 (Attachment 1, binary)
- event.event.x_studio_attachment_1_filename (Filename for x_studio_binary_field_8e5_1j1ig6n1t, char)
- event.event.x_studio_attatchment_2 (Attatchment 2, binary)
- event.event.x_studio_attatchment_2_filename (Filename for x_studio_binary_field_29k_1j1ig7jfo, char)
- event.event.x_studio_attatchment_3 (Attatchment 3, binary)
- event.event.x_studio_attatchment_3_filename (Filename for x_studio_binary_field_42h_1j1ig88dh, char)
- event.event.x_studio_attendees (Attendees, integer)
- event.event.x_studio_brand_involved (Brand Involved, char)
- event.event.x_studio_event_state (Event State, selection)
- event.event.x_studio_notice_start_date (Notice start Date, date)
- event.event.x_studio_selection_field_8id_1j1if5cco (Barra de estado de flujo, selection)
- event.event.x_studio_type_collab (Type of Collab, selection)
- event.event.x_studio_type_of_event (Type of Event, selection)
- hr.attendance.x_studio_reasons_of_stay (Reasons of stay, char)
- hr.attendance.x_studio_selection_field_5d1_1ir7hsp6o (Working Location, selection)
- product.template.x_studio_kcal (KCAL (whole product), integer)
- product.template.x_studio_vida_util_abierto (Open shelf life (days), integer)
- res.partner.x_studio_portal_duplicate_control (Portal Duplicate Control, char)
- survey.user_input.x_studio_estate_of_request (Estate of request, selection)
- survey.user_input.x_studio_solution_state_1 (Solution state, selection)
- survey.user_input.line.x_studio_solved (Solved, boolean)
- account.analytic.line.x_plan158_id (CASHFLOW NEW, many2one)
- account.analytic.line.x_plan285_id (TEAMS, many2one)
- account.analytic.line.x_plan306_id (TRAVEL RETAIL, many2one)
- event.event.x_studio_discount (Discount, many2one)
- event.event.x_studio_pdv_involved (Stores Involved, many2many)
- event.event.x_studio_products (Products Involved, many2many)
- event.event.x_studio_responsible (Responsible, many2one)
- event.event.x_studio_staff_involved (Staff Involved, many2many)
- res.partner.x_studio_salesperson (Salesperson, many2one)
- survey.user_input.x_studio_one2many_field_882_1j1i873v6 (Nuevas líneas, one2many)
