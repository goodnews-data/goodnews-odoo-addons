# GoodNews · Correcciones de pedidos del TPV (IVA, coste, errores)

Acciones para corregir pedidos del TPV marcados con error: impuestos, coste/margen y ajustes de inventario.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_pos_correcciones_base`, `point_of_sale`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Acciones de servidor** (5)

- Impuesto pedido valor St. Jordi (código) (pos.order)
- Limpieza error coste (pos.order)
- Errores tickets (pos.order)
- cambiar estado (pos.order)
- IVA corregir (pos.order)

**Acciones planificadas (se instalan apagadas)** (1)

- Limpieza error coste (en prod apagada, cada 5 minutes)
