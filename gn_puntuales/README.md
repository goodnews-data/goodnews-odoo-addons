# GoodNews · Acciones puntuales y pruebas

Acciones de un solo uso o de prueba sobre productos, compras y diarios.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `account`, `product`, `purchase`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Acciones de servidor** (9)

- Cancelar Sdp (purchase.order)
- Desactivar cookies holy (product.template)
- Activar Oysho (product.template)
- Asignar cuentas (product.template)
- [PRUEBA] Confirmar pedido con reintentos (purchase.order)
- Prueba califrais 2-3 min (purchase.order)
- Deliverect API snooze (product.product)
- Deliverect API unsnooze (product.product)
- accounr.journal (account.journal)

**Acciones planificadas (se instalan apagadas)** (1)

- Prueba califrais 2-3 min (en prod apagada, cada 2 minutes)
