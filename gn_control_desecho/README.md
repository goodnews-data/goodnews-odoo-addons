# GoodNews · Control de desecho y fabricación

Jarras (cold foam…): fabricación desde Store Operations, merma nocturna y compensación de negativos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base_automation`, `gn_control_desecho_base`, `mrp`, `stock`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Automatizaciones** (2)

- Confirmar ordenes de fabricación (mrp.production, on_time_created)
- Validar desecho store app (stock.scrap, on_time_updated)

**Acciones de servidor** (4)

- Ejecutar código (mrp.production)
- Crear ordenes de desecho (x_control_de_desecho)
- Crear compensación por negativos (x_control_de_desecho)
- Ejecutar código (stock.scrap)

**Acciones de ventana** (1)

- Control de desecho (x_control_de_desecho)

**Vistas** (4)

- Default list view for x_control_de_desecho (x_control_de_desecho)
- Default form view for x_control_de_desecho (x_control_de_desecho)
- Default search view for x_control_de_desecho (x_control_de_desecho)
- Odoo Studio: Default form view for x_control_de_desecho customization (x_control_de_desecho)

**Menús** (1)

- Manufacturing/Configuration/Control de desecho

**Acciones planificadas (se instalan apagadas)** (2)

- Crear ordenes de desecho (en prod activa, cada 1 days)
- Crear compensación por negativos (en prod activa, cada 1 days)

**Reglas de registro** (1)

- Control de desecho - Company restriction
