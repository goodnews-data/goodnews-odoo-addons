# GoodNews · Recepciones: hoja de control de calidad (modelos)

Hoja «Recepción» del control de calidad con fotos de incidencias, y qué recepciones ve cada usuario.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `quality`.

Va antes que `gn_recepcion_calidad` (la lógica).

## Qué contiene

**Modelos** (1)

- Recepción (x_quality_check_worksheet_template_1)

**Campos** (14)

- x_quality_check_worksheet_template_1.x_comments (Comments, html)
- x_quality_check_worksheet_template_1.x_passed (Passed, boolean)
- x_quality_check_worksheet_template_1.x_studio_damaged_product_imagen (Damaged product image, binary)
- x_quality_check_worksheet_template_1.x_studio_delivery_note (Delivery note, binary)
- x_quality_check_worksheet_template_1.x_studio_extra_pic_1 (, binary)
- x_quality_check_worksheet_template_1.x_studio_extra_pic_2 (Add additional photos if necessary., binary)
- x_quality_check_worksheet_template_1.x_studio_extra_picture (Extra picture, binary)
- x_quality_check_worksheet_template_1.x_studio_extra_picture_filename (Filename for x_studio_binary_field_7e8_1jicje4vi, char)
- x_quality_check_worksheet_template_1.x_studio_missing_product_imagen (Missing product image, binary)
- x_quality_check_worksheet_template_1.x_studio_wrong_product_imagen (Wrong product image, binary)
- x_quality_check_worksheet_template_1.x_studio_wrong_quantity_imagen (Wrong quantity image, binary)
- x_quality_check_worksheet_template_1.x_quality_check_id (Quality Check, many2one)
- x_quality_check_worksheet_template_1.x_studio_incidence_type (Incidence type, many2many)
- x_quality_check_worksheet_template_1.x_name (Name, char)

## Hoja de control de calidad

Este modelo es una **hoja de control de calidad** («Recepción»). En Odoo la crea la plantilla de hojas (Calidad → Configuración → Plantillas de hojas). Aquí se crea como modelo normal con sus vistas; en la base nueva hay que crear la plantilla «Recepción» y enlazarla a este modelo, y asignarla al punto de control QCP00001.
