# GoodNews · Vistas de Studio

Cambios hechos con Studio en vistas estándar de Odoo (formularios, listas, búsquedas). Una misma vista mezcla campos de varios desarrollos, por eso van juntas y se instalan al final.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `account`, `base`, `documents`, `event`, `gn_pos_correcciones`, `gn_roturas_encuestas`, `goodnews`, `helpdesk`, `hr_attendance`, `maintenance`, `point_of_sale`, `pos_custom_discounts`, `pos_preparation_display`, `product`, `purchase`, `quality_control`, `stock`, `survey`.

## Qué contiene

**Vistas** (45)

- Odoo Studio: hr.attendance.form customization (hr.attendance)
- Odoo Studio: survey.user_input.view.form customization (survey.user_input)
- Odoo Studio: account.out.invoice.tree customization (account.move)
- Odoo Studio: stock.location.route.form customization (stock.route)
- Odoo Studio: res.partner.form customization (res.partner)
- Odoo Studio: event.event.form customization (event.event)
- Odoo Studio: pos.session.form.view customization (pos.session)
- Odoo Studio: purchase.order.form customization (purchase.order)
- Odoo Studio: survey.question.answer.view.form customization (survey.question.answer)
- Odoo Studio: Form view for survey question customization (survey.question)
- Odoo Studio: preparation.display.form.view customization (pos_preparation_display.display)
- Odoo Studio: survey.user_input.line.view.tree customization (survey.user_input.line)
- Odoo Studio: survey.user_input.line.view.form customization (survey.user_input.line)
- Odoo Studio: stock.picking.form customization (stock.picking)
- Odoo Studio: product.template.product.form customization (product.template)
- Odoo Studio: pos.custom.discount customization (pos.custom.discount)
- Odoo Studio: survey.user_input.view.tree customization (survey.user_input)
- Odoo Studio: product.category.form customization (product.category)
- Odoo Studio: stock.picking.kanban customization (stock.picking)
- Odoo Studio: pos.config.tree.view customization (pos.config)
- Odoo Studio: helpdesk.ticket.tree customization (helpdesk.ticket)
- Odoo Studio: helpdesk.ticket.form customization (helpdesk.ticket)
- Odoo Studio: quality.check.view.form customization (quality.check)
- Odoo Studio: product.category.list customization (product.category)
- Odoo Studio: Abastecimiento POS Vista Busqueda customization (pos.resupply.order)
- Odoo Studio: helpdesk.ticket.search customization (helpdesk.ticket)
- Odoo Studio: survey.question.answer.view.search customization (survey.question.answer)
- Odoo Studio: pos.order.form customization (pos.order)
- Odoo Studio: equipment.request.form customization (maintenance.request)
- Odoo Studio: helpdesk.ticket.kanban customization (helpdesk.ticket)
- Odoo Studio: account.move.form customization (account.move)
- Odoo Studio: event.event.tree customization (event.event)
- Odoo Studio: documents facet form view with folder customization (documents.facet)
- Odoo Studio: product.pricelist.form customization (product.pricelist)
- pos.config.kanban.view (pos.config)
- Odoo Studio: pos.config.kanban.view customization (pos.config)
- Odoo Studio: Marcas customization (goodnews.supercategory)
- GoodNews: vida útil abierto (form) (product.template)
- GoodNews: vida útil abierto (list) (product.template)
- GoodNews: vida útil abierto (search) (product.template)
- GoodNews: KCAL (form) (product.template)
- GoodNews: KCAL (list) (product.template)
- GoodNews: KCAL (search) (product.template)
- Default search view for ir.model(1462,) (pos.combo)
- Odoo Studio: Default search view for ir.model(1462,) customization (pos.combo)
