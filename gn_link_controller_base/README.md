# GoodNews · Gestión de enlaces (Link controller: Califrais y Amazon) (modelos)

Enlaces de compra por producto y proveedor, con actualización de ID, nombre y precio desde la URL.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `mail`.

Va antes que `gn_link_controller` (la lógica).

## Qué contiene

**Modelos** (1)

- Link controller (x_link_controller)

**Campos** (17)

- x_link_controller.x_active (Activo, boolean)
- x_link_controller.x_name (Descripción, char)
- x_link_controller.x_studio_api (API, boolean)
- x_link_controller.x_studio_califrais_id (Califrais id, char)
- x_link_controller.x_studio_califrais_name (Califrais name, char)
- x_link_controller.x_studio_price (Price, float)
- x_link_controller.x_studio_price_change (Price change, boolean)
- x_link_controller.x_studio_sequence (Secuencia, integer)
- x_link_controller.x_studio_standard_cost (Standard cost, float)
- x_link_controller.x_studio_update_cost (Actualizar coste, boolean)
- x_link_controller.x_studio_url (URL, char)
- x_link_controller.x_studio_company (Company, many2many)
- x_link_controller.x_studio_product (Product, many2one)
- x_link_controller.x_studio_supplier (Supplier, many2one)
- x_link_controller.x_studio_udm_reabastecimiento (udm reabastecimiento, many2one)
- x_link_controller.x_studio_purchase_tax (Purchase tax, many2one)
- x_link_controller.x_studio_udm_compra (Udm compra, many2one)
