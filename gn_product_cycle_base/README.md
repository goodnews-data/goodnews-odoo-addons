# GoodNews · Product cycle (modelos)

Modelo «product cycle» por compañía.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `mail`.

Va antes que `gn_product_cycle` (la lógica).

## Qué contiene

**Modelos** (1)

- product cycle (x_product_cycle)

**Campos** (4)

- x_product_cycle.x_active (Activo, boolean)
- x_product_cycle.x_name (Descripción, char)
- x_product_cycle.x_studio_sequence (Secuencia, integer)
- x_product_cycle.x_studio_company (Company, many2one)
