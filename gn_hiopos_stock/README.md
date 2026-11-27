# GoodNews · HioPoS: stock del TPV durante el día

Actualiza poco a poco el stock de los TPV de HioPoS durante el día.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_hiopos_stock_base`, `point_of_sale`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Acciones de servidor** (1)

- hiopos_daytime_stock_slices (pos.session)

**Acciones planificadas (se instalan apagadas)** (1)

- hiopos_daytime_stock_slices (en prod apagada, cada 2 minutes)
