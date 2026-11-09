# GoodNews · Vendor transition UoM

**Autora:** Isabella Maffi · **Odoo:** 17.0 (Enterprise) · **Licencia:** LGPL-3

Módulo de datos (sin Python) que empaqueta como app instalable un desarrollo hecho
primero con Studio y acciones de servidor en `goodnews-test`. Así sobrevive a las
migraciones de versión y se instala igual en cualquier base.

## Qué problema resuelve

Algunos proveedores venden un producto en una unidad distinta de la unidad de compra
estándar (p. ej. Califrais vende Evian 50 cl por caja y no por unidad). Y a veces un
proveedor cambia temporalmente de formato: un **producto en transición**.

Este módulo hace que los pedidos de compra usen la unidad y el precio correctos del
proveedor sin que nadie tenga que cambiarlos a mano.

## Qué instala

| Pieza | Dónde | Qué hace |
|---|---|---|
| Campo **Transition** (`x_studio_transition`, booleano) | Producto → pestaña Compra (proveedores) | Marca la fila de proveedor que es el formato de transición. |
| Campo **Udm Transición** (`x_studio_vendor_uom`, many2one a `uom.uom`) | Producto → pestaña Compra (proveedores) | Unidad en la que ese proveedor vende. El precio de la fila va en esa unidad. |
| Automatización **Automatizar UdM de compra según proveedor** | Líneas de pedido de compra | Al crear/editar producto, cantidad, UdM o embalaje, aplica la UdM y el precio del proveedor. |
| Acción **Activar producto transición** | Recepción → menú ⚙ Acción | Pasa las líneas del pedido a la UdM de transición del proveedor. |

## Cómo funciona

### 1. Automatización en las líneas de compra

Se ejecuta en pedidos en borrador / enviados (y en confirmados solo para la regla 1).

- **Regla 1, guarda de transición:** si una línea ya está en la UdM de transición, se
  conserva el precio de transición. Odoo lo recalcularía desde la fila estándar al
  cambiar la cantidad.
- **Regla 2, UdM estándar del proveedor** (solo borrador/enviado): si el proveedor tiene
  UdM propia distinta de la de compra, la línea pasa a esa UdM, se quita el embalaje y
  se pone el precio del proveedor tal cual (convertido de moneda si hace falta).
- Si la UdM del proveedor no es de la misma categoría que la del producto, no toca
  nada y lo avisa.
- Deja **una nota interna por pedido** en el chatter con lo que ha cambiado.
- No toca las líneas creadas por la acción de transición (flag de contexto
  `skip_vendor_uom_rule`).

### 2. Acción «Activar producto transición» (desde la recepción)

Busca en el pedido las líneas cuyo producto tenga una fila de proveedor con
**Transition** marcado, UdM de transición y fechas vigentes.

- **Flujo A:** pedido sin nada recibido ni facturado. Cancela la recepción, cancela
  el pedido, lo pasa a borrador, sustituye las líneas (cantidad convertida, precio de
  transición), lo confirma (sin email) y abre la nueva recepción.
- **Flujo B:** pedido recibido en parte o facturado (no se puede cancelar). Quita los
  movimientos pendientes de la línea vieja, la deja en lo ya recibido y añade una línea
  nueva en la UdM de transición; Odoo añade su movimiento a la recepción abierta.
- Todo va dentro de un **savepoint**: si algo falla, no se aplica nada y el error se
  anota en el chatter.

## Cómo configurarlo en un producto

En **Producto → Compra**, por cada proveedor:

1. Fila estándar: proveedor, **Udm Transición** = la unidad en la que vende (si es
   distinta de la de compra), precio en esa unidad.
2. Fila de transición (si la hay): mismo proveedor, **Transition** marcado, **Udm
   Transición** = unidad de transición, precio en esa unidad. **Colócala debajo de la
   fila estándar**: si Odoo la elige como proveedor por defecto, la automatización avisa
   y no aplica nada.

## Instalación

1. Activa el modo desarrollador.
2. **Aplicaciones → Importar módulo** → sube `gn_vendor_transition_uom.zip`.
3. Requiere que estén instalados `purchase_stock` y `base_automation`.

### Antes de instalar, revisa esto

- **Los campos no pueden existir ya.** Si en la base ya están `x_studio_transition` o
  `x_studio_vendor_uom` (creados con Studio, como en `goodnews-test`), la instalación
  falla por nombre duplicado. En test hay que borrar antes los campos, la
  automatización y la acción de Studio, o probar en una copia limpia.
- **Columnas en la ficha de producto.** El módulo añade las columnas a la lista
  estándar de proveedores (`product.product_supplierinfo_tree_view`). Si Studio ha
  metido en la ficha de producto su propia lista de proveedores (en test ocurre), esa
  lista manda y las columnas hay que añadirlas ahí con Studio.
- **Desinstalar borra los campos y sus datos.**

## Origen (test)

| Pieza | Registro en `goodnews-test` |
|---|---|
| Campos | `ir.model.fields` 49330 y 49328 |
| Automatización | `base.automation` 30 (acción 1924) |
| Acción de transición | `ir.actions.server` 1926 |

El código de las acciones es copia exacta de test (verificado).
