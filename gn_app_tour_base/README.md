# GoodNews · App Tour de Store Operations (modelos)

Tours guiados de la web de Store Operations: tours y pasos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `mail`.

Va antes que `gn_app_tour` (la lógica).

## Qué contiene

**Modelos** (2)

- App Tour (x_app_tour)
- Tour step (x_tour_step)

**Campos** (21)

- x_app_tour.x_active (Activo, boolean)
- x_app_tour.x_name (Descripción, char)
- x_app_tour.x_studio_active (Active, boolean)
- x_app_tour.x_studio_description (Description, text)
- x_app_tour.x_studio_sequence (Secuencia, integer)
- x_app_tour.x_studio_sequence_1 (sequence, integer)
- x_app_tour.x_studio_title (Title, char)
- x_tour_step.x_active (Activo, boolean)
- x_tour_step.x_name (Descripción, char)
- x_tour_step.x_studio_advance (advance, selection)
- x_tour_step.x_studio_anchor (anchor, text)
- x_tour_step.x_studio_description (Description, text)
- x_tour_step.x_studio_frame (frame, text)
- x_tour_step.x_studio_page_url (page url, text)
- x_tour_step.x_studio_placement (placement, selection)
- x_tour_step.x_studio_sequence (Secuencia, integer)
- x_tour_step.x_studio_sequence_tourstep (sequence, integer)
- x_tour_step.x_studio_step_body (step body, text)
- x_tour_step.x_studio_step_title (step title, text)
- x_tour_step.x_studio_tour_id (tour id, many2one)
- x_app_tour.x_studio_step_ids (step ids, one2many)
