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
| [`gn_base`](gn_base/) | 17.0 | Lo compartido: grupos Supply y Data, y el almacén asignado de cada usuario. Va antes que el resto. |
| [`gn_inventory_planner`](gn_inventory_planner/) | 17.0 | Planificador de inventario: recuentos cíclicos por tienda y grupo de productos, con historial. Lógica (botones, acciones, vistas, permisos). **En producción desde el 23/11/2026.** |
| [`gn_inventory_planner_base`](gn_inventory_planner_base/) | 17.0 | Modelos y campos del planificador. Solo para una base nueva o migrada. |
| [`gn_valijas`](gn_valijas/) | 17.0 | Valijas de los centrales de España: «Programar valija» y validación sola de noche, sin pendiente. En producción desde el 23/11/2026. |
| [`gn_valijas_base`](gn_valijas_base/) | 17.0 | Campos de las valijas. Solo para una base nueva o migrada. |
| [`gn_entregas_parciales`](gn_entregas_parciales/) | 17.0 | Proveedores con entregas parciales: marca sus pedidos y cancela los pendientes de la Store App de los que no. En producción desde el 24/11/2026 (sustituye a las automatizaciones de Studio 21 y 22). |
| [`gn_entregas_parciales_base`](gn_entregas_parciales_base/) | 17.0 | Campos de entregas parciales. Solo para una base nueva o migrada. |
| [`gn_purchase_account_rules`](gn_purchase_account_rules/) | 17.0 | Reglas contables de compra: cuenta de gasto e IVA por proveedor y producto en pedidos y facturas. En producción desde el 09/11/2026. Sirve igual para una base nueva. |

## Maqueta de migración (27/11/2026)

El resto de desarrollos de Studio están en módulos `gn_<desarrollo>_base` + `gn_<desarrollo>` generados
automáticamente desde producción (solo lectura) con `tools/maqueta_leer.py` y `tools/maqueta_generar.py`,
más `gn_studio_grupos`, `gn_studio_modelos(_base)`, `gn_studio_campos_base` y `gn_studio_vistas`.
Orden de instalación y qué revisar: [`MAQUETA.md`](MAQUETA.md) y [`maqueta_avisos.txt`](maqueta_avisos.txt).
Probados en test con una variante de nombres cambiados (`tools/maqueta_variante.py`, `tools/maqueta_probar.py`):
los 41 se instalan. No es una migración: en las bases actuales no se instalan (ya existe lo de Studio).

## Convención

- Una carpeta por módulo, prefijo `gn_`.
- Módulos de datos (XML, sin Python) siempre que se pueda: se instalan con
  **Aplicaciones → Importar módulo** sin tocar el servidor.
- Cada módulo lleva un `README.md` que explica qué hace, cómo se configura y qué
  revisar antes de instalarlo.
- El `.zip` instalable de cada módulo se publica en *Releases*.

## Migración: todos los desarrollos como apps

Objetivo: que en una migración (base nueva o versión nueva de Odoo) baste con **instalar los zips** en orden, sin rehacer nada con Studio.

1. `gn_base` (siempre la primera).
2. Los módulos de modelos (`*_base`) y después los de lógica.
3. Pasar los datos de cada desarrollo (exportar de la base vieja e importar con los mismos nombres de campo).

Los módulos que reproducen un desarrollo de Studio **conservan sus nombres técnicos** (`x_studio_…`, `x_inventory_planner`…), porque la GN Tools los lee por nombre. Por eso cada desarrollo va en dos módulos:
- El de **modelos** (`*_base`) solo se instala en una base nueva.
- El de **lógica** se instala también en la de 2026, encima de Studio, y desde entonces se **actualiza** importando el zip nuevo. Antes de eso hay que retirar las piezas de Studio que sustituye (`tools/retirar_studio_*.py`, con copia y deshacer).

- Probarlos: `python tools/variante_prueba.py <carpeta>` genera una copia con todos los nombres cambiados que sí se instala en test.
- Empaquetar: `python tools/empaquetar.py <módulo> [<módulo>…] --out dist`.
