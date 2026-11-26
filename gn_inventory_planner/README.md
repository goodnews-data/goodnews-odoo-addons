# GoodNews · Planificador de inventario (`gn_inventory_planner`)

Inventarios cíclicos de las tiendas. Un **planificador** dice qué grupos de productos se cuentan, en qué ubicaciones, cada cuántos días y quién los cuenta. Cada noche pide los recuentos que tocan, y el **historial** sigue si están pendientes, en curso o hechos.

Es el desarrollo de Studio de enero de 2026 (Inventory Planner, Inventory History e Inventory Groups) empaquetado como app para las **migraciones**.

**Autora:** Isabella Maffi · Odoo 17.0 · depende de [`gn_base`](../gn_base/)

## Dos módulos: la lógica y los modelos

| Módulo | Qué lleva | Dónde se instala |
|---|---|---|
| **`gn_inventory_planner`** (este) | Botones, acciones planificadas, vistas, menús, permisos y reglas | **En cualquier base**, también en la de GoodNews de 2026: busca los modelos por su nombre |
| [`gn_inventory_planner_base`](../gn_inventory_planner_base/) | Los 3 modelos, sus campos y el campo «Grupo de inventarios» del producto | **Solo en una base nueva o migrada** (donde no existe el desarrollo de Studio) |

**En producción desde el 23/11/2026** (instalado encima del desarrollo de Studio). Las piezas de Studio que sustituye se retiraron con `tools/retirar_studio_planificador_inventario.py`: menús archivados, botones desvinculados, acciones planificadas 163 y 199 y reglas 536-538 apagadas. No se borró nada, y la copia de seguridad permite deshacerlo.

### Actualizar (mejoras futuras)

1. Cambiar el código aquí y subir la versión en `__manifest__.py` (17.0.1.0.0 → 17.0.1.1.0).
2. `python tools/empaquetar.py gn_inventory_planner --out dist`.
3. En Odoo: Aplicaciones → **Importar módulo** → el zip nuevo. Odoo actualiza el módulo instalado.

Ojo: las **acciones planificadas** están en `noupdate`, así que una actualización no les cambia ni el horario ni el código. Si cambias su código, cámbialo también a mano en Ajustes → Técnico → Acciones planificadas, o súbelo con un script.

### Base nueva (migración)

Instalar en orden: `gn_base` → `gn_inventory_planner_base` → `gn_inventory_planner`. Después hay que pasar los datos: grupos con sus productos, planificadores y, si interesa, el historial. Se exportan de la base vieja y se importan con los mismos nombres de campo.

Los nombres técnicos son **los mismos que en Studio**. La GN Tools los lee por nombre: el dashboard de la Store App, las etiquetas, Desechos y el «Grupo de inventario» de Alta de Productos. **No cambiarlos.**

## Qué incluye

| Pieza | Detalle |
|---|---|
| Modelos | `x_product_tags` (grupos de inventario), `x_inventory_planner` (planificador), `x_inventory_history` (historial) |
| Campo en productos | `product.template.x_studio_inventory_group_tag`, en la pestaña Inventario de la ficha |
| Menús | Inventario → Configuración → Gestión de almacenes → Inventory Planner · Informes → Inventory History · Configuración → Productos → Inventory Groups |
| Botones del planificador | **Asignar inventario** (pide ya los recuentos, sin mover el calendario) · **Cancelar inventario** (cancela los recuentos abiertos y archiva el planificador) · **Etiquetas de producto** |
| Botón del historial | **Cancelar inventario** (cancela esa solicitud y libera sus recuentos) |
| Acción planificada diaria | **Ejecutar recuentos programados** (00:35 UTC): pide los recuentos de los planificadores con fecha de hoy o atrasada y calcula las fechas siguientes |
| Acción planificada cada 15 min | **Actualizar inventory history**: recalcula cuántos productos faltan por contar, marca Hecho al terminar y borra el historial cerrado de más de 3 meses |
| Permisos | Usuarios internos: planificador e historial (sin borrar), grupos solo lectura · Supply: planificador, historial lectura, grupos todo · Data: grupos todo · Ajustes: todo |
| Reglas | Cada usuario ve solo los registros de sus compañías (o sin compañía) |

## Cómo funciona

1. **Grupos de inventario**: cada grupo agrupa productos que se cuentan juntos. Un producto puede estar en varios.
2. **Planificador**: grupos, ubicaciones internas, frecuencia en días (0 = una sola vez), día de la semana opcional, fecha del próximo recuento, compañía y persona opcional.
3. **Cada noche** se piden los recuentos de cada ubicación (Inventario → Recuento físico, asignado a la persona). La persona es la del planificador o, si no hay, el usuario que tiene esa ubicación como **Almacén asignado** (`gn_base`).
4. **Cada 15 minutos** el historial mira cuántos productos siguen asignados: Pending → In progress → Completed.

## Mejoras respecto al desarrollo de Studio

- **Asignar inventario** usa la misma lógica que la acción nocturna. El código viejo estaba pegado dos veces y tenía topes silenciosos (800 productos, 1.500 líneas) que dejaban recuentos incompletos. Tampoco filtraba ubicaciones internas.
- Si falta un usuario, **Asignar inventario** dice todo lo que falta **antes de crear nada**. Antes fallaba a mitad y deshacía lo hecho sin decir qué planificador.
- **Cancelar** solo libera los recuentos asignados **a la persona de ese inventario**. Antes liberaba todos los de esos productos en esa tienda, aunque fueran de otro recuento.
- **Cancelar inventario ahora archiva el planificador**, así de verdad no se vuelve a ejecutar. La nota de Studio decía «this scheduler will not be executed again», pero no lo paraba. Para volver a usarlo: desarchivarlo y poner la próxima fecha.
- Con varias compañías en el planificador, el historial toma la primera. Antes fallaba con «Expected singleton».
- Los filtros **Pendiente / En proceso / Completado** del historial funcionan. Los de Studio comparaban con la etiqueta y nunca encontraban nada. Además se añade **Cancelado**.
- Las vistas ya no llevan **ids fijos** de ubicaciones ni de compañías, que en otra base no existen. Ubicaciones: solo internas. Compañías: las del usuario.
- No incluye lo que ya no se usa: el modelo `x_etiquetas` (0 registros), la automatización 7 y la acción planificada 189 (ambas apagadas y sustituidas por «Actualizar inventory history»).
- Las acciones planificadas corren como `__system__`, no como un usuario de una persona concreta.

## Para revisar después de instalar

- Que los usuarios de tienda tengan su **Almacén asignado** (Ajustes → Usuarios → Permisos de acceso → GoodNews).
- Que Supply y Data tengan a sus personas (`gn_base`).
- La hora de la acción planificada diaria (00:35 UTC por defecto).

## Probarlo sin tocar el desarrollo real

`tools/variante_prueba.py` genera una copia de los tres módulos con todos los nombres técnicos cambiados (`x_t_…`, módulos `*_t`). Se instala en test, se prueba y se desinstala sin tocar el desarrollo de Studio ni la GN Tools. Se probó así el 23/11/2026: Asignar, no duplicar, progreso cada 15 min, filtros, Cancelar + archivar, cron nocturno con día de la semana y vistas.
