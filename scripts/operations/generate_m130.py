# Modelo 130 de Agencia Tributaria de España

incomes_without_taxes = 1146.45
expenses_without_taxes = 2164.73
withholding_irpf_previous_periods = 0. # No retenemos IRPF al ser profesor particular

payed_previous_period = 20.28
negative_results_previous_periods = 296.07

# P1. Estimación directa
# ------------------------

C01 = incomes_without_taxes # ingresos
C02 = expenses_without_taxes # gastos
C03 = C01 - C02 # rendimiento neto

if C03 > 0.:
    C04 = 0.2* C03
else:
    C04 = 0.

# Esta casilla es donde informaremos de los importes que ya hayamos ingresado en
# los anteriores modelos presentados.
C05 = payed_previous_period

# La casilla 06 corresponde a “Retenciones e ingresos a cuenta soportados por
# las actividades incluidas en este apartado y correspondientes al período
# comprendido entre el primer día del año y el último día del trimestre”. Es decir,
# si eres profesional, en tus facturas aplicas retención. El importe total de
# todas estas retenciones de las facturas emitidas desde el primer día del año hasta
# el trimestre en que estás operando es lo que deberás poner.
C06 = withholding_irpf_previous_periods

C07 = C04 - C05 - C06

# P2. Actividades agrarias y demás
# ------------------------
# Todos las casillas a 0 ya que no es aplicable a un profesor particular

C11 = C07

# P3. Liquidacion total
# ------------------------

if C11 > 0.:
    C12 = C11
else:
    C12 = 0.

C13 = 0. # No aplicable

C14 = C12 - C13
C15 = negative_results_previous_periods
C16 = 0. # Ninguna deducción por vivienda habitual
C17 = C14 - C15 - C16

C18 = 0. # Es cero al no ser una liquidación complementaria
C19 = C17 - C18

print("I. Actividades económicas en estimación directa...")
print("----------------------------------------------------------")
print("   - Ingresos computables (01): ", C01)
print("   - Gastos deducibles (02): ", C02)
print("   - Rendimiento neto (03): ", C03)
print("   - 20% del rendimiento neto (04): ", C04)
print("   - A deducir de  los periodos anteriores:")
print("      - Pagado (05): ", C05)
print("      - Retenciones de IRPF en las facturas (06): ", withholding_irpf_previous_periods)
print("   - Pago fraccionado previo del trimestre (07): ", C07)
print("")

print("II. Actividades agrícolas, ganaderas, ...")
print("----------------------------------------------------------")
print("   Todas las casilla a 0 ya que no es aplicable")
print("   - Pago fraccionad previo del trimestre (11):", C07)
print("")

print("III. Total liquidación.")
print("----------------------------------------------------------")
print("   - Suma de pagos fraccionados del primer trimestre (12):", C12)
print("   - A deducir: Minoración por aplicación... (13):", C13)
print("   - Diferencia (14):", C14)
print("   - A deducir de  los periodos anteriores:")
print("      - Resultados negativos de los periodos anteriores (15):", C15)
print("      - Adquisicón o rehabilitación de vivienda habitual (16):", C16)
print("   - Total (17):", C17)
print("   - A deducir (autoliquidación complementaria)")
print("      - Resultado a ingresar anteriores autoliquidaciones (18) :", C18)
print("   - Resultado de la autoliquidación (19):", C19)
print("")