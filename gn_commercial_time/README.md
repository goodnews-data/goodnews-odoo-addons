# GoodNews · Horario comercial de tiendas

Horarios de apertura y cierre por tienda y tolerancia para abrir la sesión del TPV (lo usa el widget de sesiones).

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_commercial_time_base`, `sale_timesheet_enterprise`.

## Qué contiene

**Acciones de servidor** (1)

- Get Commercial Times (POS Sessions Widget) (x_commercial_time)

**Acciones de ventana** (1)

- Commercial time (x_commercial_time)

**Vistas** (6)

- Default list view for x_commercial_time (x_commercial_time)
- Default form view for x_commercial_time (x_commercial_time)
- Default search view for x_commercial_time (x_commercial_time)
- Odoo Studio: Default form view for x_commercial_time customization (x_commercial_time)
- Odoo Studio: Default list view for x_commercial_time customization (x_commercial_time)
- Odoo Studio: Default search view for x_commercial_time customization (x_commercial_time)

**Menús** (1)

- Timesheets/Configuration/Commercial time
