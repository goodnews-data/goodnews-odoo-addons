# GoodNews · Grupos propios

Grupos de permisos creados a mano en Odoo (Supply y Data van en gn_base).

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `account`, `base`, `stock`.

## Qué contiene

**Grupos** (7)

- Point of Sale / Preparation Display
- Inventory / Administrador Pro
- Inventory / Puntos de venta
- Inventory / Puntos de venta (nude)
- Point Of Sale / Usuario (nude)
- Point Of Sale / Tools
- Point Of Sale / Store app
