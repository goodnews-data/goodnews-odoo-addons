# GoodNews · Reglas contables de compra (`gn_purchase_account_rules`)

Cada regla dice: **cuando el proveedor X factura los productos Y en la compañía Z, usar esta cuenta de gasto y/o este IVA de compra**.

- En las **líneas de pedido de compra** (borrador, enviado, por aprobar) pone el IVA de la regla, para que el pedido cuadre con la factura.
- En las **líneas de factura de proveedor en borrador** pone la cuenta de gasto y el IVA de la regla.
- Solo sustituye lo que Odoo propuso automáticamente: si alguien lo cambió a mano, se respeta.
- Al guardar una regla comprueba que esté bien hecha: con productos, con cuenta o IVA, proveedor principal, cuenta e IVA de la compañía y sin productos repetidos en otra regla.

**Autora:** Isabella Maffi · Odoo 17.0 · módulo solo de datos (se importa en Aplicaciones → Importar módulo).

**En producción desde el 09/11/2026.** No viene de Studio: crea su propio modelo (`x_gn_purchase_account_rule`), así que el mismo zip sirve para la base actual y para una nueva.

## Usar

Contabilidad → Configuración → Contabilidad → **Reglas contables de compra**. También desde la ficha del proveedor, pestaña «Reglas contables de compra».

## Migración

Instalar el zip y volver a crear las reglas a mano. Son datos, no van en el módulo. Hoy hay 4, todas de Califrais / SAS GN FRANCE 2022 → cuenta 624100 + TVA 20 %.
