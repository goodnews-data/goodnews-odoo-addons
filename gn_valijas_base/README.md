# GoodNews · Valijas, campos (`gn_valijas_base`)

Los 3 campos de las valijas en las transferencias, con los nombres de Studio:
- `x_studio_scheduled`: programada, sin entrega parcial;
- `x_studio_locked`: bloqueada;
- `x_studio_validation_date`: fecha de autovalidación.

**Solo para una base nueva o migrada.** En la de GoodNews de 2026 ya existen. Allí basta con [`gn_valijas`](../gn_valijas/).

El campo viejo `x_studio_scheduled_backorder` («con entrega parcial») no se incluye, porque nunca se usó.

**Autora:** Isabella Maffi · Odoo 17.0
