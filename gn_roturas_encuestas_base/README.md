# GoodNews · Formulario de roturas de stock y compras Amazon (modelos)

Encuestas «Out of Stock» por país y «Compras Amazon»: estado de la incidencia, botones para ver stock/movimientos/compras y pedidos de compra automáticos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `survey`.

Va antes que `gn_roturas_encuestas` (la lógica).

## Qué contiene

**Campos** (22)

- survey.question.x_studio_binary_field_112_1j0mkrkq1 (Nuevo Archivo, binary)
- survey.question.x_studio_binary_field_112_1j0mkrkq1_filename (Filename for x_studio_binary_field_112_1j0mkrkq1, char)
- survey.question.x_studio_binary_field_4gs_1j0mkvuf8 (Nuevo Archivo, binary)
- survey.question.x_studio_binary_field_4gs_1j0mkvuf8_filename (Filename for x_studio_binary_field_4gs_1j0mkvuf8, char)
- survey.question.x_studio_binary_field_8th_1j0mkn3n3 (Nuevo Archivo, binary)
- survey.question.x_studio_binary_field_8th_1j0mkn3n3_filename (Filename for x_studio_binary_field_8th_1j0mkn3n3, char)
- survey.question.x_studio_binary_field_bj_1j0mkppdb (Nuevo Archivo, binary)
- survey.question.x_studio_binary_field_bj_1j0mkppdb_filename (Filename for x_studio_binary_field_bj_1j0mkppdb, char)
- survey.question.answer.x_studio_idproduct (ID, integer)
- survey.question.answer.x_studio_producto_data_id (Product ID, char)
- survey.survey.x_studio_binary_field_5an_1j0mjidjl (Nuevo Archivo, binary)
- survey.survey.x_studio_binary_field_5an_1j0mjidjl_filename (Filename for x_studio_binary_field_5an_1j0mjidjl, char)
- survey.survey.x_studio_binary_field_9lj_1j0mkkdlo (Nuevo Archivo, binary)
- survey.survey.x_studio_binary_field_9lj_1j0mkkdlo_filename (Filename for x_studio_binary_field_9lj_1j0mkkdlo, char)
- survey.user_input.x_studio_managed (Done, boolean)
- survey.user_input.x_studio_read (Read, boolean)
- survey.user_input.line.x_studio_fake (, boolean)
- survey.user_input.line.x_studio_handled (Handled, boolean)
- survey.question.answer.x_studio_delivery_address (Entrega, many2one)
- survey.question.answer.x_studio_product_product_id (Producto, many2one)
- survey.user_input.x_studio_purchase_order (Purchase order, many2one)
- survey.user_input.x_studio_out_of_stock (Out of stock, one2many)
