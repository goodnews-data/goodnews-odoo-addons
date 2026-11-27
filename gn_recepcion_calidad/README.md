# GoodNews · Recepciones: hoja de control de calidad

Hoja «Recepción» del control de calidad con fotos de incidencias, y qué recepciones ve cada usuario.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base_automation`, `gn_recepcion_calidad_base`, `gn_studio_grupos`, `quality`, `stock`.

## Qué contiene

**Automatizaciones** (2)

- Alerta recepciones con diferencia (quality.check, on_create_or_write)
- Attach reception picture for quality checks (x_quality_check_worksheet_template_1, on_create_or_write)

**Acciones de servidor** (2)

- Ejecutar código (x_quality_check_worksheet_template_1)
- Ejecutar código (quality.check)

**Acciones de ventana** (1)

- Worksheets (x_quality_check_worksheet_template_1)

**Vistas** (4)

- template_view_Recepción (x_quality_check_worksheet_template_1)
- tree_view_Recepción (x_quality_check_worksheet_template_1)
- search_view_Recepción (x_quality_check_worksheet_template_1)
- Odoo Studio: template_view_Recepción customization (x_quality_check_worksheet_template_1)

**Reglas de registro** (3)

- Recepciones solo del almacén asignado al usuario
- x_quality_check_worksheet_template_1_own
- x_quality_check_worksheet_template_1_all

## Hoja de control de calidad

Este modelo es una **hoja de control de calidad** («Recepción»). En Odoo la crea la plantilla de hojas (Calidad → Configuración → Plantillas de hojas). Aquí se crea como modelo normal con sus vistas; en la base nueva hay que crear la plantilla «Recepción» y enlazarla a este modelo, y asignarla al punto de control QCP00001.
