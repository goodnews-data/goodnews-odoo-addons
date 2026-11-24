# GoodNews · Entregas parciales, campos (`gn_entregas_parciales_base`)

Los campos de entregas parciales con sus nombres de Studio, que la Store App lee en Recepciones:
- en el **proveedor**: `x_studio_partial_delivery`, `x_studio_number_deliveries`, `x_studio_delivery_1/2/3`;
- en el **pedido de compra**: `x_studio_partial_delivery`.

También los coloca en las fichas de proveedor y de pedido. En el proveedor van en el bloque de ubicaciones de inventario, que Odoo solo enseña en **modo desarrollador**, igual que en Studio.

**Solo para una base nueva o migrada**: en la de GoodNews de 2026 ya existen. Allí basta con [`gn_entregas_parciales`](../gn_entregas_parciales/).

**Autora:** Isabella Maffi · Odoo 17.0
