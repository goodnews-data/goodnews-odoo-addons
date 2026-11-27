# GoodNews · Formulario de roturas de stock y compras Amazon

Encuestas «Out of Stock» por país y «Compras Amazon»: estado de la incidencia, botones para ver stock/movimientos/compras y pedidos de compra automáticos.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base_automation`, `gn_roturas_encuestas_base`, `survey`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Automatizaciones** (1)

- Solution State Survey (survey.user_input, on_create_or_write)

**Acciones de servidor** (7)

- Ejecutar el código Python (survey.user_input)
- Ejecutar el código Python (survey.user_input)
- Ver compras desde encuesta (survey.user_input)
- Ver movimientos stock desde encuesta (survey.user_input)
- Ver stock desde encuesta (survey.user_input)
- Compras Amazon (survey.user_input)
- Generar compras amazon encuestas HQ (survey.user_input)

**Acciones planificadas (se instalan apagadas)** (1)

- Generar compras amazon encuestas HQ (en prod activa, cada 2 days)
