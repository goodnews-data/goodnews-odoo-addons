# GoodNews · Otros (sin desarrollo claro) (modelos)

Piezas que no se han podido relacionar con ningún desarrollo: revisar una a una.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`.

Va antes que `gn_otros` (la lógica).

## Qué contiene

**Campos** (1)

- res.partner.x_studio_warehouse_id (Almacén, many2one)
