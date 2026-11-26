# GoodNews · Planificador de inventario, modelos (`gn_inventory_planner_base`)

Los **modelos y campos** del planificador de inventario, con los nombres técnicos de Studio:
- `x_product_tags`: grupos de inventario.
- `x_inventory_planner`: planificador.
- `x_inventory_history`: historial.
- `product.template.x_studio_inventory_group_tag`: el campo del producto y su sitio en la ficha, en la pestaña Inventario.

**Solo para una base nueva o migrada.** En la de GoodNews de 2026 los modelos ya existen (los creó Studio) y la instalación fallaría por duplicados. Allí basta con [`gn_inventory_planner`](../gn_inventory_planner/), que lleva toda la lógica.

Orden en una base nueva: `gn_base` → `gn_inventory_planner_base` → `gn_inventory_planner`.

**Autora:** Isabella Maffi · Odoo 17.0
