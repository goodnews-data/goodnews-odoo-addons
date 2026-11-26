# GoodNews · Entregas parciales (`gn_entregas_parciales`)

Algunos **proveedores entregan un pedido en varias veces**. Este desarrollo:

1. **Marca sus pedidos de compra** como «Partial delivery». La Store App lo lee en Recepciones para dejar recibir en varias entregas.
2. **Cancela los pendientes que crea la Store App** a los 10 minutos cuando el proveedor **no** acepta entregas parciales. La Store App escribe en la nota «Store App-Creado parcial» al crear el pendiente de una recepción a medias. Antes de cancelar deja una nota en el chatter.

**Autora:** Isabella Maffi · Odoo 17.0 · sustituye a las automatizaciones de Studio 21 y 22.

## Configuración

| Dónde | Qué |
|---|---|
| Proveedor → «Partial delivery», «Number deliveries», «Delivery 1/2/3» | Si acepta parciales y en cuántas entregas suele mandar (lo usa la Store App) |
| Ajustes → Técnico → Parámetros del sistema → `gn_entregas_parciales.tipos_sin_parcial` | Tipos de operación cuyos pedidos **nunca** se marcan, separados por comas (en GoodNews: las recepciones de las tiendas de Barcelona) |
| `gn_entregas_parciales.categorias_sin_cancelar` | Categorías cuyos pendientes **nunca** se cancelan (en GoodNews: 93 «Sweets & Pastries») |

## Mejoras respecto a Studio

- **Sin ids fijos en las reglas:** los tipos de operación y la categoría pasan a dos parámetros que se cambian sin tocar código y que sirven en cualquier base.
- **La marca del pedido** solo se recalcula al crear el pedido o al cambiar de proveedor o de tipo de operación, y nunca se reescribe si ya estaba puesta. Antes corría en cualquier cambio del pedido.
- **Categorías protegidas:** un pendiente no se cancela si tiene **algún** producto de esas categorías. Antes solo miraba el primer producto.
- **La nota de cancelación** dice el motivo completo: el proveedor no acepta entregas parciales.

## Instalar

| Base de datos | Qué hacer |
|---|---|
| **GoodNews 2026** (los campos ya existen) | Importar `gn_entregas_parciales.zip` y luego `python tools/retirar_studio_entregas_parciales.py prod apply`: apaga las automatizaciones 21 y 22 de Studio y pasa sus ids a los parámetros. Guarda copia y se deshace con `undo`. |
| **Base nueva o migrada** | `gn_entregas_parciales_base.zip` (campos y vistas) y después este. Rellenar los dos parámetros con los ids de esa base. |
