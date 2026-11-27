# GoodNews · B2B: almacén, posición fiscal y pedidos recurrentes

Contactos B2B con su almacén y posición fiscal, el pedido de venta que hereda el almacén, y los pedidos recurrentes.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `account`, `base`, `base_automation`, `gn_otros_base`, `sale`, `stock`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Automatizaciones** (1)

- Warehouse b2b (sale.order, on_create_or_write)

**Acciones de servidor** (8)

- Ejecutar el código Python (sale.order)
- Recurring purchases (sale.order)
- Recurring purchases 90 days (sale.order)
- Recurring purchases 15 days (sale.order)
- Recurring sales confirmed sales, draft invoice (sale.order)
- ES: Asignar almacén B2B (res.partner)
- ES: Asignar posicion fiscal B2B (res.partner)
- Limpieza res.partner posición fiscal (res.partner)

**Acciones planificadas (se instalan apagadas)** (4)

- Recurring purchases (en prod activa, cada 1 days)
- Recurring purchases 90 days (en prod apagada, cada 90 days)
- Recurring purchases 15 days (en prod apagada, cada 15 days)
- Recurring sales confirmed sales, draft invoice (en prod apagada, cada 1 months)
