# GoodNews · Lanzamientos programados

**Autora:** Isabella Maffi · **Odoo:** 17.0 (Enterprise) · **Licencia:** LGPL-3

Módulo de datos (sin Python, se instala con **Importar módulo**) que sustituye al
planificador de Studio «Planificador Master Data» (`x_planificador_master_` + cron 168).

## Por qué

El planificador de Studio tenía estos problemas (revisados en producción el 17/11/2026):

- **Solo fecha, sin hora**, y un cron diario a las 00:55 UTC. Los lanzamientos de
  «11am» o «6pm» había que ejecutarlos a mano.
- **Combinaciones + Desactivar** y **Categorías TPV + Actualizar** fallaban siempre.
- **Un error a mitad dejaba cambios a medias** y podía parar los lanzamientos
  siguientes del día.
- **El precio de proveedor nunca funcionó** (usaba un campo que no existe).
- **La compañía se ignoraba** (el coste se habría escrito siempre en Barcelona).
- **UK no tenía valores por defecto**, así que sus lanzamientos no se habrían ejecutado nunca.
- Solo 6 campos posibles y un único valor numérico.

## Qué se puede cambiar

| Cambio | Cómo | Se aplica a |
|---|---|---|
| Disponible en TPV | Activar / Desactivar | Productos |
| Precio de venta | Importe | Productos |
| Coste | Importe (en la compañía del lanzamiento, todas las variantes) | Productos |
| Nombre del producto | Texto, en un idioma o en todos | Productos |
| Categoría del TPV del producto | Añadir / Quitar / Sustituir por | Productos |
| Combinaciones del producto | Añadir / Quitar / Sustituir por | Productos |
| Precio en tarifa | Poner precio / Quitar (una o varias tarifas) | Productos |
| Precio de proveedor | Importe, para uno o varios proveedores | Productos |
| Archivar productos / Recuperar archivados | — | Productos |
| Categorías visibles en el punto de venta | Añadir / Quitar / Sustituir por | Puntos de venta |

Un lanzamiento puede llevar **varios cambios** a la vez (pestaña «Cambios»), sobre los
mismos productos y puntos de venta (pestaña «Productos y tiendas»).

## Cómo se usa

**Punto de venta → Productos → Lanzamientos programados** (lista, calendario y ficha).

1. **Nuevo**: nombre, compañía y **fecha y hora**.
2. **Productos y tiendas**: los productos (también se pueden elegir archivados, para
   recuperarlos) y, si hace falta, los puntos de venta.
3. **Cambios**: una línea por cambio. La ficha de la línea muestra solo lo que pide ese
   tipo de cambio.
4. **Programar**: revisa el lanzamiento y enseña de una vez todo lo que falta (sin
   productos, importe a 0 sin marcar «Importe 0 a propósito», tarifas o puntos de venta
   de otra compañía…). Si está bien, pasa a **Programado**.
5. El cron **«Lanzamientos programados: aplicar»** pasa **cada 5 minutos** y aplica los
   programados cuya hora ha llegado. **Lanzar ya** lo aplica en el próximo minuto.
6. Resultado:
   - **Hecho**: la pestaña «Resultado» dice qué ha cambiado en cada línea.
   - **Error**: **no se ha aplicado nada** de ese lanzamiento y el motivo está en «Resultado».
     Se corrige y se vuelve a programar.
7. **Deshacer** (en Hecho): restaura los valores guardados en «Valores anteriores».
   Si alguien cambió esos mismos campos después, sus cambios se pierden. El botón lo avisa.
8. **Duplicar** copia los cambios y los productos en un borrador nuevo. Es útil para
   repetir el lanzamiento en otra compañía o fecha.

### A tener en cuenta

- **El TPV**: una caja abierta ve los cambios de producto y de categorías al recargar el TPV.
- **El coste** es por compañía. En productos con valoración automática, Odoo puede
  generar el asiento de revalorización, igual que si se cambia a mano.
- **Las tarifas**: solo se tocan precios **fijos por producto, sin fechas y sin cantidad
  mínima**. Las reglas por categoría, por variante, con fechas o con fórmula no se tocan.
- **El nombre** sin idioma se escribe en todos los idiomas instalados.
- **La hora** se ve en la zona horaria de quien mira (Madrid, París, Ámsterdam o Londres)
  y se guarda en UTC.

## Piezas que instala

| Pieza | Nombre técnico |
|---|---|
| Modelos | `x_gn_launch`, `x_gn_launch_line`, `x_gn_launch_snapshot` |
| Motor (validar, aplicar, deshacer) | acción de servidor `gn_launch_planner.action_engine` |
| Botones | `action_schedule`, `action_launch_now`, `action_to_draft`, `action_undo` |
| Cron cada 5 min | `gn_launch_planner.cron_launches` (usuario `__system__`, con `sudo()` + `with_company()`) |
| Regla multicompañía | cada usuario ve los lanzamientos de sus compañías activas |
| Permisos | usuarios internos crean y editan; gestor de TPV y administradores borran |

### Detalles técnicos (por si hay que tocarlo)

- El código de las acciones de Odoo no admite `with` ni `lambda` que usen variables de la
  función. Por eso el aislamiento es **`commit` / `rollback` por lanzamiento**, y los
  filtros usan `filtered_domain`.
- Cada campo manual recarga todos los modelos al crearse (~3 s en GoodNews). Por eso los
  campos se crean **en bloque** dentro del `ir.model`. Así la instalación tarda ~20 s y no
  se pasa del límite de tiempo del servidor.
- Esos bloques van con `noupdate="1"`. Para añadir un campo en una versión futura,
  créalo como un registro `ir.model.fields` aparte, **no** editando los bloques.

## Instalación en producción

1. Activa el modo desarrollador.
2. **Aplicaciones → Importar módulo** → sube `gn_launch_planner.zip` (tarda ~20 s).
3. Requiere `point_of_sale`, `product` y `mail` (ya instalados).

Probado en `goodnews-test` el 17/11/2026: instalación, actualización encima (no
duplica campos ni pierde datos), los 11 tipos de cambio, Deshacer, un lanzamiento con
error que no deja nada a medias, «Lanzar ya» y Duplicar.

## Retirar el planificador viejo (Studio) sin romper Odoo

No hay que tocar nada del módulo nuevo: los dos conviven sin problema.

**Fase 1, el día de la instalación (reversible).**

1. Comprueba que en el viejo no queden fichas *Pending* activas. En prod, el 17/11 solo
   había la #93, que está archivada.
2. Desactiva el cron viejo: **Ajustes → Técnico → Acciones planificadas → «Planificador
   Master Data»** → desmarca *Activo*. Desde ese momento el viejo ya no hace nada, pero
   todo sigue ahí por si hace falta volver atrás.
3. Usa el módulo nuevo una o dos semanas.

**Fase 2, borrar el viejo.**

El historial (206 lanzamientos) está exportado en `planificador_master_historial_prod.xlsx`.

Se hace con `tools/retirar_planificador_studio.py`, que borra en el orden seguro:
cron → menú → acción → filtros guardados → vistas (primero las heredadas) → regla de
compañía → acción de servidor → campo calculado `x_studio_seller_1` (bloquea el borrado
del modelo) → modelo (Odoo borra sus campos, valores por defecto, permisos y tabla) →
referencias de Studio a esos registros.

```bash
python -I tools/retirar_planificador_studio.py ../visualstudio/.env prod dry    # solo lista
python -I tools/retirar_planificador_studio.py ../visualstudio/.env prod apply  # borra
```

Ensayado en `goodnews-test` el 17/11/2026: ~70 s. Después, 756 menús cargan bien, las
vistas de producto, TPV y proyecto abren y el cron nuevo funciona.

> Borrar a mano desde **Ajustes → Técnico → Modelos** también vale, pero en ese orden.
> Si intentas borrar el modelo primero, Odoo lo impide por el campo calculado.
