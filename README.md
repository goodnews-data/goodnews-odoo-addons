# GoodNews · Odoo addons

Desarrollos de Odoo de GoodNews empaquetados como **apps instalables**.

Todo lo que se hace con Studio, acciones de servidor o vistas se pasa aquí como
módulo, para poder instalarlo en producción y llevarlo de una versión a otra en las
migraciones sin rehacerlo a mano.

**Autora:** Isabella Maffi

## Módulos

| Módulo | Odoo | Qué hace |
|---|---|---|
| [`gn_vendor_transition_uom`](gn_vendor_transition_uom/) | 17.0 | UdM de compra por proveedor y cambio a UdM de transición desde la recepción. |
| [`gn_launch_planner`](gn_launch_planner/) | 17.0 | Lanzamientos programados por fecha y hora (precios, TPV, categorías, combos, tarifas, nombres, archivar), con validación y Deshacer. Sustituye al «Planificador Master Data» de Studio. |

## Convención

- Una carpeta por módulo, prefijo `gn_`.
- Módulos de datos (XML, sin Python) siempre que se pueda: se instalan con
  **Aplicaciones → Importar módulo** sin tocar el servidor.
- Cada módulo lleva un `README.md` que explica qué hace, cómo se configura y qué
  revisar antes de instalarlo.
- El `.zip` instalable de cada módulo se publica en *Releases*.
