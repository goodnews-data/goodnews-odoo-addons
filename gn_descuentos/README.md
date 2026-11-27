# GoodNews · Descuentos programados del TPV

Botones de descuento del TPV que se encienden y apagan solos por fechas (cron 166). Es el «botón de descuento» de Product Collabs.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_descuentos_base`, `pos_custom_discounts`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Acciones de servidor** (1)

- POS Discount – Auto Activate & Discontinue (pos.custom.discount)

**Acciones planificadas (se instalan apagadas)** (1)

- POS Discount – Auto Activate & Discontinue (en prod activa, cada 1 days)
