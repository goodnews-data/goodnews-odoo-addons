# GoodNews · Alérgenos (modelos)

Lista de alérgenos y trazas por producto, y el texto que se imprime.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `mail`, `product`.

Va antes que `gn_alergenos` (la lógica).

## Qué contiene

**Modelos** (1)

- Allergens (x_allergens)

**Campos** (6)

- product.template.x_studio_allergens_text (allergens text, html)
- x_allergens.x_active (Activo, boolean)
- x_allergens.x_name (Descripción, char)
- x_allergens.x_studio_sequence (Secuencia, integer)
- product.template.x_studio_allergens (Allergens, many2many)
- product.template.x_studio_allergy_traces (allergy traces, many2many)
