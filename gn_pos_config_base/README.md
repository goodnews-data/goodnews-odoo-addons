# GoodNews · Configuración de TPV y accesos de tienda (modelos)

Campos propios en la configuración del TPV y los accesos de menú a Store Operations y Store Tools.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `point_of_sale`, `pos_preparation_display`, `stock`.

Va antes que `gn_pos_config` (la lógica).

## Qué contiene

**Campos** (6)

- pos.config.x_studio_division (Division, selection)
- pos.config.x_studio_open (Active, boolean)
- stock.location.x_color (Color, integer)
- pos.config.x_studio_combo_tax_categ_ids (Tax Combo Category, many2many)
- pos_preparation_display.display.x_studio_owner_id (Owner id, many2one)
- res.users.x_studio_assigned_central (Assigned central, many2one)
