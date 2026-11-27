# GoodNews · Shopify: validación automática de entregas

Valida cada día las entregas de pedidos de Shopify del almacén externo.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `stock`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Acciones de servidor** (1)

- Validar ordenes de entrega shopify barcelona (stock.picking)

**Acciones planificadas (se instalan apagadas)** (1)

- Validar ordenes de entrega shopify barcelona (en prod activa, cada 1 days)
