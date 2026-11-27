# GoodNews · Horario comercial de tiendas (modelos)

Horarios de apertura y cierre por tienda y tolerancia para abrir la sesión del TPV (lo usa el widget de sesiones).

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `mail`.

Va antes que `gn_commercial_time` (la lógica).

## Qué contiene

**Modelos** (1)

- Commercial time (x_commercial_time)

**Campos** (10)

- x_commercial_time.x_active (Activo, boolean)
- x_commercial_time.x_name (Descripción, char)
- x_commercial_time.x_studio_closing (Closing time, datetime)
- x_commercial_time.x_studio_day_type (Schedule type, selection)
- x_commercial_time.x_studio_opening (Opening time, datetime)
- x_commercial_time.x_studio_sequence (Secuencia, integer)
- x_commercial_time.x_studio_shift_type (Shift Type, selection)
- x_commercial_time.x_studio_tolerance_min (Minutes of tolerance for opening POS session, integer)
- x_commercial_time.x_studio_city (City, many2many)
- x_commercial_time.x_studio_pdv (Store, many2many)
