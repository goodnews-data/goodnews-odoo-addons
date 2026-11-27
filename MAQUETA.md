# Maqueta de migración: todos los desarrollos como zips

Generado con `tools/maqueta_leer.py` (lee Odoo prod, solo lectura) y `tools/maqueta_generar.py`.

Orden de instalación en una base nueva (Aplicaciones → Importar módulo, uno a uno):

1. `gn_base`
2. Los módulos ya migrados a mano: `gn_inventory_planner_base`, `gn_inventory_planner`, `gn_valijas_base`, `gn_valijas`, `gn_entregas_parciales_base`, `gn_entregas_parciales`, `gn_purchase_account_rules`, `gn_vendor_transition_uom`, `gn_launch_planner`.
3. Los de la maqueta, en este orden:

   1. `gn_alergenos_base`: Alérgenos
   2. `gn_app_tour_base`: App Tour de Store Operations
   3. `gn_commercial_time_base`: Horario comercial de tiendas
   4. `gn_control_desecho_base`: Control de desecho y fabricación
   5. `gn_descuentos_base`: Descuentos programados del TPV
   6. `gn_eventos_base`: Eventos
   7. `gn_helpdesk_base`: Incidencias de tiendas (tickets de asistencia)
   8. `gn_hiopos_stock_base`: HioPoS: stock del TPV durante el día
   9. `gn_link_controller_base`: Gestión de enlaces (Link controller: Califrais y Amazon)
   10. `gn_otros_base`: Otros (sin desarrollo claro)
   11. `gn_pos_config_base`: Configuración de TPV y accesos de tienda
   12. `gn_pos_correcciones_base`: Correcciones de pedidos del TPV (IVA, coste, errores)
   13. `gn_product_cycle_base`: Product cycle
   14. `gn_producto_campos_base`: Campos de producto
   15. `gn_recepcion_calidad_base`: Recepciones: hoja de control de calidad
   16. `gn_roturas_encuestas_base`: Formulario de roturas de stock y compras Amazon
   17. `gn_studio_modelos_base`: Modelos sueltos de Studio
   18. `gn_studio_campos_base`: Campos sueltos de Studio
   19. `gn_studio_grupos`: Grupos propios
   20. `gn_alergenos`: Alérgenos
   21. `gn_app_tour`: App Tour de Store Operations
   22. `gn_b2b`: B2B: almacén, posición fiscal y pedidos recurrentes
   23. `gn_commercial_time`: Horario comercial de tiendas
   24. `gn_control_desecho`: Control de desecho y fabricación
   25. `gn_descuentos`: Descuentos programados del TPV
   26. `gn_goodcard`: GoodCard y GoodCrew
   27. `gn_helpdesk`: Incidencias de tiendas (tickets de asistencia)
   28. `gn_hiopos_stock`: HioPoS: stock del TPV durante el día
   29. `gn_link_controller`: Gestión de enlaces (Link controller: Califrais y Amazon)
   30. `gn_nude`: Nude Project: acceso restringido
   31. `gn_otros`: Otros (sin desarrollo claro)
   32. `gn_pos_config`: Configuración de TPV y accesos de tienda
   33. `gn_pos_correcciones`: Correcciones de pedidos del TPV (IVA, coste, errores)
   34. `gn_product_cycle`: Product cycle
   35. `gn_puntuales`: Acciones puntuales y pruebas
   36. `gn_recepcion_calidad`: Recepciones: hoja de control de calidad
   37. `gn_roturas_encuestas`: Formulario de roturas de stock y compras Amazon
   38. `gn_shopify`: Shopify: validación automática de entregas
   39. `gn_studio_modelos`: Modelos sueltos de Studio
   40. `gn_studio_vistas`: Vistas de Studio

Después: pasar los datos de cada modelo (exportar de la base vieja e importar con los mismos nombres de campo), encender las acciones planificadas y revisar `maqueta_avisos.txt`.
