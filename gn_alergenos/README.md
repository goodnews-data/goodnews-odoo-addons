# GoodNews · Alérgenos

Lista de alérgenos y trazas por producto, y el texto que se imprime.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_alergenos_base`, `point_of_sale`.

## Qué contiene

**Acciones de ventana** (1)

- Allergens (x_allergens)

**Vistas** (4)

- Default list view for x_allergens (x_allergens)
- Default form view for x_allergens (x_allergens)
- Default search view for x_allergens (x_allergens)
- Odoo Studio: Default form view for x_allergens customization (x_allergens)

**Menús** (1)

- Point of Sale/Configuration/Products/Allergens
