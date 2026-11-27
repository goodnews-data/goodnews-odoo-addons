# GoodNews · Configuración de TPV y accesos de tienda

Campos propios en la configuración del TPV y los accesos de menú a Store Operations y Store Tools.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `gn_pos_config_base`, `gn_studio_grupos`, `pos_preparation_display`, `website`.

## Qué contiene

**Enlaces (acciones URL)** (1)

- Tools → https://goodnews.tools/

**Menús** (2)

- Store Operations
- Store Tools

**Reglas de registro** (1)

- Restrict Preparation Display by Owner
