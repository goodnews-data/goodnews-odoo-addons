# GoodNews · Base (`gn_base`)

Las piezas que **comparten varios desarrollos** de GoodNews. Se instala la primera en una base nueva o migrada, antes del resto de módulos `gn_*` que dependen de ella.

**Autora:** Isabella Maffi · Odoo 17.0

## Qué incluye

| Pieza | Para qué |
|---|---|
| Grupo **Inventory / Supply** | El equipo de Supply. Lo usan el planificador de inventario y otros desarrollos. |
| Grupo **Dashboard / Data** | El equipo de Data. |
| Campo **Almacén asignado** (`res.users.x_studio_assigned_warehouse`) | La ubicación de la tienda de cada usuario. El planificador de inventario le asigna ahí los recuentos y la Store App la usa como su almacén. |
| Campo **Assigned central** (`res.users.x_studio_assigned_central`) | El almacén central que abastece a esa tienda. |
| Vista | Los dos campos en la ficha del usuario, pestaña Permisos de acceso, bloque «GoodNews». |

Los nombres técnicos de los campos son **los de Studio**, porque la GN Tools los lee por nombre. No cambiarlos.

## Cuándo se instala

- **Base nueva o migrada:** instalar el zip (Aplicaciones → Importar módulo) antes que los demás `gn_*`. Después hay que poner a las personas en Supply y Data y rellenar el almacén de cada usuario de tienda.
- **Base de GoodNews de 2026 (producción y test): no instalar.** Los grupos y los campos ya existen (creados a mano y con Studio) y se duplicarían.
