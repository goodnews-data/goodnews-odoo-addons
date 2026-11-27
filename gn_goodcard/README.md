# GoodNews · GoodCard y GoodCrew

Tarifas y contactos de la GoodCard de empleados: limpieza al archivar un empleado, saldo de GoodCrew y excepciones.

> **Maqueta de migración.** Generado automáticamente con `tools/maqueta_generar.py` a partir de Odoo producción (solo lectura). Copia exacta de lo hecho con Studio, con los mismos nombres técnicos.

## Cuándo se instala

Solo en una base **sin** este desarrollo (nueva o migrada). En las bases actuales de GoodNews (test y producción) ya existe con Studio y la instalación fallaría por nombres duplicados.

Depende de: `base`, `base_automation`, `hr`, `loyalty`.

**Las acciones planificadas se instalan apagadas**: encenderlas a mano (Ajustes → Técnico → Acciones planificadas) cuando la base tenga ya los datos. Su usuario será el que instale el módulo; en producción eran de GoodNews Buddy.

## Qué contiene

**Automatizaciones** (1)

- Employee Archive → Update Partner Pricelist + Log M (hr.employee, on_archive)

**Acciones de servidor** (4)

- Ejecutar código (hr.employee)
- Limpiar Saldo GoodCrew (loyalty.card)
- Limpiar Saldo GoodCrew (loyalty.card)
- Limpieza res.partner (res.partner)

**Acciones planificadas (se instalan apagadas)** (2)

- Limpiar Saldo GoodCrew (en prod activa, cada 8 hours)
- Limpieza res.partner (en prod apagada, cada 2 minutes)
