# GoodNews · Descuentos programados del TPV (modelos)

Botones de descuento del TPV que se encienden y apagan solos por fechas (cron 166). Es el «botón de descuento» de Product Collabs.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `pos_custom_discounts`.

Va antes que `gn_descuentos` (la lógica).

## Qué contiene

**Campos** (4)

- pos.custom.discount.x_studio_active_1 (Activo, boolean)
- pos.custom.discount.x_studio_end_date (Fecha fin, date)
- pos.custom.discount.x_studio_start_date (Fecha inicio, date)
- pos.custom.discount.x_studio_available_in_pos (Scheduled in Pos, many2many)
