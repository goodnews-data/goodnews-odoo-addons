# GoodNews · Nude Project: acceso restringido

Reglas para que el usuario de Nude Project solo vea sus pedidos, sesiones, pagos e informes del día.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_studio_grupos`, `point_of_sale`.

## Qué contiene

**Reglas de registro** (4)

- NUDE Pedidos
- NUDE Sesiones
- NUDE pagos
- NUDE informes
