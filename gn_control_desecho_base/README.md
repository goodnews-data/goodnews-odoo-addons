# GoodNews · Control de desecho y fabricación (modelos)

Jarras (cold foam…): fabricación desde Store Operations, merma nocturna y compensación de negativos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `mail`, `product`.

Va antes que `gn_control_desecho` (la lógica).

## Qué contiene

**Modelos** (1)

- Control de desecho (x_control_de_desecho)

**Campos** (13)

- product.template.x_studio_production (Producto a fabricar, boolean)
- x_control_de_desecho.x_active (Activo, boolean)
- x_control_de_desecho.x_name (Descripción, char)
- x_control_de_desecho.x_studio_active (Active, boolean)
- x_control_de_desecho.x_studio_frequency (Frequency, integer)
- x_control_de_desecho.x_studio_last_date (Last date, datetime)
- x_control_de_desecho.x_studio_next_date (Next date, datetime)
- x_control_de_desecho.x_studio_sequence (Secuencia, integer)
- x_control_de_desecho.x_studio_weekday (Weekday, selection)
- x_control_de_desecho.x_studio_company (Company, many2one)
- x_control_de_desecho.x_studio_product_product (X Studio Product Product, many2one)
- x_control_de_desecho.x_studio_warehouse (X Studio Warehouse, many2many)
- x_control_de_desecho.x_studio_scrap (Scrap, many2many)
