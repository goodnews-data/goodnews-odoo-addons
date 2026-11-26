# GoodNews · Valijas (`gn_valijas`)

Las **valijas** son los envíos fijos de los **almacenes centrales de España** (Central Barcelona y Central Madrid-Velázquez) a las tiendas. **Supply** las programa cuando arma la valija fija, y se **validan solas de noche**.

**Autora:** Isabella Maffi · Odoo 17.0 · sustituye al desarrollo de Studio «Validación diferida» (acciones 1720/1721, cron 167).

## Cómo funciona

1. En la transferencia (o en varias desde la lista, menú Acción), **«Programar valija»**:
   - solo vale en compañías de **España** (se mira el país de la compañía);
   - revisa todas antes de escribir nada: estado, que haya algo preparado y lotes o series;
   - deja cada línea en lo **preparado** y quita las líneas a 0;
   - marca la transferencia como programada y bloqueada y le pone la **fecha de autovalidación**: «ahora» o, **si es viernes, el domingo a las 08:00**, para que se valide el domingo por la noche, antes de la entrega del lunes;
   - deja una nota en el chatter.
2. **Cada noche** (acción planificada «Valijas: validar las programadas», 22:00 UTC) se validan las programadas con la fecha ya pasada, de los últimos 30 días, como mucho 30 por noche:
   - con lo que está **preparado** y **sin crear pendiente**: lo que no está preparado se quita;
   - **cada valija va aparte**: si una falla, se deshace solo esa, deja un **aviso en su chatter** (lo revisa **Data**) y las demás siguen.
3. **«Validar valija ahora»** valida al momento las seleccionadas, con las mismas reglas, y dice cuáles se han validado y cuáles no.
4. Filtro **«Valijas programadas»** en la búsqueda de transferencias.

## Mejoras respecto a Studio

- **Cada valija va aparte** (punto de restauración). Antes, un fallo a mitad de una valija podía dejarla a medias.
- **Aviso en el chatter** cuando no se puede validar. Antes solo quedaba en el registro técnico.
- **Las valijas «en espera»** ahora se validan; antes se podían programar pero el cron nunca las cogía.
- **«Validar ahora»** solo valida las seleccionadas. El botón viejo validaba **todas** las pendientes.
- **Al ajustar a lo preparado se conservan las líneas**, con sus lotes y paquetes. Antes se rehacía el movimiento copiando solo el primer lote.
- **Sin el modo «con entrega parcial»**, que nunca se usó (Isabella, 23/11/2026).
- **«Solo España» por el país de la compañía**, sin ids fijos de compañía en la vista.
- **La nota del viernes** dice «domingo» (antes decía «lunes», que no era verdad).
- La automatización 8 (bloquear cambios) no se incluye: ya estaba apagada porque quedó obsoleta.

## Instalar

| Base de datos | Qué hacer |
|---|---|
| **La de GoodNews de 2026** (los campos ya existen) | Importar `gn_valijas.zip` y luego `python tools/retirar_studio_valijas.py prod apply`. Ese script desvincula los botones de Studio, apaga el cron 167 y quita de la vista de Studio el botón y los campos viejos. Guarda copia y se deshace con `undo`. |
| **Base nueva o migrada** | `gn_valijas_base.zip` (los 3 campos, con los nombres de Studio) y después `gn_valijas.zip`. |

**Actualizar:** cambiar el código, subir la versión en `__manifest__.py`, `python tools/empaquetar.py gn_valijas --out dist` e importar el zip. La acción planificada no se actualiza sola (para no moverle el horario); su código solo llama al motor `gn_valijas.action_validate`, así que normalmente no hace falta tocarla.
