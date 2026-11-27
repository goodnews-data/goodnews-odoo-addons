# GoodNews · Gestión de enlaces (Link controller: Califrais y Amazon)

Enlaces de compra por producto y proveedor, con actualización de ID, nombre y precio desde la URL.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_link_controller_base`, `gn_studio_grupos`, `purchase`.

## Qué contiene

**Acciones de servidor** (1)

- Update Links (x_link_controller)

**Acciones de ventana** (1)

- Link controller (x_link_controller)

**Vistas** (5)

- Default list view for x_link_controller (x_link_controller)
- Default form view for x_link_controller (x_link_controller)
- Default search view for x_link_controller (x_link_controller)
- Odoo Studio: Default form view for x_link_controller customization (x_link_controller)
- Odoo Studio: Default list view for x_link_controller customization (x_link_controller)

**Menús** (1)

- Purchase/Configuration/Link controller

**Reglas de registro** (1)

- Gestión de enlaces - Company restriction
