# GoodNews · App Tour de Store Operations

Tours guiados de la web de Store Operations: tours y pasos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `gn_app_tour_base`, `website_slides`.

## Qué contiene

**Acciones de ventana** (2)

- App Tour (x_app_tour)
- Tour step (x_tour_step)

**Vistas** (11)

- Default list view for x_app_tour (x_app_tour)
- Default form view for x_app_tour (x_app_tour)
- Default search view for x_app_tour (x_app_tour)
- Odoo Studio: Default form view for x_app_tour customization (x_app_tour)
- Default list view for x_tour_step (x_tour_step)
- Default form view for x_tour_step (x_tour_step)
- Default search view for x_tour_step (x_tour_step)
- Odoo Studio: Default form view for x_tour_step customization (x_tour_step)
- Default kanban view for ir.model(3281,) (x_app_tour)
- Odoo Studio: Default kanban view for ir.model(3281,) customization (x_app_tour)
- Odoo Studio: Default search view for x_tour_step customization (x_tour_step)

**Menús** (3)

- eLearning/Configuration/Store Operations
- eLearning/Configuration/Store Operations/App Tour
- eLearning/Configuration/Store Operations/Tour step
