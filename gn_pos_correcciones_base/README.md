# GoodNews · Correcciones de pedidos del TPV (IVA, coste, errores) (modelos)

Acciones para corregir pedidos del TPV marcados con error: impuestos, coste/margen y ajustes de inventario.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `point_of_sale`.

Va antes que `gn_pos_correcciones` (la lógica).

## Qué contiene

**Campos** (2)

- pos.order.line.x_studio_ticket_error (Ticket error, boolean)
- pos.order.x_studio_product (Product, many2many)
