# GoodNews · HioPoS: stock del TPV durante el día (modelos)

Actualiza poco a poco el stock de los TPV de HioPoS durante el día.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `point_of_sale`.

Va antes que `gn_hiopos_stock` (la lógica).

## Qué contiene

**Campos** (1)

- pos.order.x_studio_stockpicking (Recogida, many2one)
