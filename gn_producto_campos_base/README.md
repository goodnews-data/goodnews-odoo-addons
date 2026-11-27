# GoodNews · Campos de producto (modelos)

Campos propios del producto que usa la Tools (medida, unidad…).

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `product`.

## Qué contiene

**Campos** (2)

- product.template.x_measurement (Medida, float)
- product.template.x_studio_unit_of_measure (Unit of measure, selection)
