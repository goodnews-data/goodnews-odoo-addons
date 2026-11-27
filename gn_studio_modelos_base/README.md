# GoodNews · Modelos sueltos de Studio (modelos)

Modelos creados con Studio que el mapa del Manual no asigna a ningún desarrollo.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `mail`.

Va antes que `gn_studio_modelos` (la lógica).

## Qué contiene

**Modelos** (5)

- Factura de Proveedor (x_factura_de_proveedor)
- (BPP) - Banco Prevsion de Pago (x_bpp_banco_prevsion_d)
- (BPP) - Banco Prevsion de Pago Tags (x_bpp_banco_prevsion_d_tag)
- survey_user_input_line (x_survey_user_input_line_93926)
- facgur (x_facgur)

**Campos** (12)

- x_bpp_banco_prevsion_d.x_active (Activo, boolean)
- x_bpp_banco_prevsion_d.x_name (Banco de Previsión de Pago, char)
- x_bpp_banco_prevsion_d.x_studio_notes (Notas, html)
- x_bpp_banco_prevsion_d.x_studio_sequence (Secuencia, integer)
- x_bpp_banco_prevsion_d_tag.x_color (Color, integer)
- x_bpp_banco_prevsion_d_tag.x_name (Nombre, char)
- x_facgur.x_name (Name, char)
- x_factura_de_proveedor.x_name (Name, char)
- x_survey_user_input_line_93926.x_name (Descripción, char)
- x_survey_user_input_line_93926.x_studio_sequence (Secuencia, integer)
- x_bpp_banco_prevsion_d.x_studio_tag_ids (Etiquetas, many2many)
- x_survey_user_input_line_93926.x_survey_user_input_id (X Survey User Input, many2one)
