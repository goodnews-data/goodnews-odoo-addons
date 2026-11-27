# GoodNews · Eventos (modelos)

Campos propios de los eventos (montaje, logística, uniformes…), que usa el módulo Eventos de la Tools.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `event`.

## Qué contiene

**Campos** (8)

- event.event.x_studio_additional_information (Additional information, text)
- event.event.x_studio_assembly (assembly, char)
- event.event.x_studio_disassembly (disassembly, char)
- event.event.x_studio_dynamic (X Studio Dynamic, text)
- event.event.x_studio_logistics (logistics, text)
- event.event.x_studio_max_qty (max qty, integer)
- event.event.x_studio_sampling (X Studio Sampling, text)
- event.event.x_studio_uniforms (X Studio Uniforms, text)
