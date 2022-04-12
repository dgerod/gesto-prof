import os
import yaml
from scripts.common.configuration import Configuration


def generate_m130(file_path):

    configuration = Configuration()    

    if os.path.dirname(file_path) == "":
        abs_file_path = os.path.join(configuration.get_inputs_directory(),
                                     file_path)
    else:
        abs_file_path = os.path.abspath(file_path)
                             
    with open(abs_file_path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            incomes_without_taxes = data['ingresos']
            expenses_without_taxes = data['gastos']
            payed_previous_period = data['pagado_anteriormente']
            negative_results_previous_periods = data['resultados_negativos']

        except yaml.YAMLError as ex:
            raise

    output_file = os.path.join(configuration.get_outputs_directory(), "calculo_modelo_130.txt")

    _generate_m130(incomes_without_taxes, expenses_without_taxes,
                 payed_previous_period, negative_results_previous_periods, output_file)


def _generate_m130(incomes_without_taxes, expenses_without_taxes,
                 payed_previous_period, negative_results_previous_periods, output_file):

    withholding_irpf_previous_periods = 0. # No retenemos IRPF al ser profesor particular
    deduct_due_to_previous_year = 0. # ¿?¿?¿?¿?

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

    C13 = deduct_due_to_previous_year

    C14 = C12 - C13
    
    if C14 > 0.0:
        C15 = negative_results_previous_periods
    else:
        C15 = 0.

    C16 = 0. # Ninguna deducción por vivienda habitual
    C17 = C14 - C15 - C16

    C18 = 0. # Es cero al no ser una liquidación complementaria
    C19 = C17 - C18

    with open(output_file, "w") as f:

        f.write("")
        f.write("I. Actividades económicas en estimación directa...\n")
        f.write("----------------------------------------------------------\n")
        f.write("   - Ingresos computables (01): %f\n" % C01)
        f.write("   - Gastos deducibles (02): %f\n" % C02)
        f.write("   - Rendimiento neto (03): %f\n" % C03)
        f.write("   - 20 porciento del rendimiento neto (04): %f\n" % C04)
        f.write("   - A deducir de  los periodos anteriores:\n")
        f.write("      - Pagado (05): %f\n" % C05)
        f.write("      - Retenciones de IRPF en las facturas (06): %f\n" % withholding_irpf_previous_periods)
        f.write("   - Pago fraccionado previo del trimestre (07): %f\n" % C07)
        f.write("\n")

        f.write("II. Actividades agrícolas, ganaderas, ...\n")
        f.write("----------------------------------------------------------\n")
        f.write("   Todas las casilla a 0 ya que no es aplicable\n")
        f.write("   - Pago fraccionado previo del trimestre (11): %f\n" % C07)
        f.write("\n")

        f.write("III. Total liquidación.\n")
        f.write("----------------------------------------------------------\n")
        f.write("   - Suma de pagos fraccionados prevíos del trimestre (12): %f\n" % C12)
        f.write("   - A deducir: Minoración por aplicación... (13): %f\n" % C13)
        f.write("   - Diferencia (14): %f\n" % C14)
        f.write("   - A deducir de  los periodos anteriores:\n")
        f.write("      - Resultados negativos de los periodos anteriores (15): %f\n" % C15)
        f.write("      - Adquisición o rehabilitación de vivienda habitual (16): %f\n"% C16)
        f.write("   - Total (17): %f\n" % C17)
        f.write("   - A deducir (autoliquidación complementaria)\n")
        f.write("      - Resultado a ingresar anteriores autoliquidaciones (18): %f\n" % C18)
        f.write("   - Resultado de la autoliquidación (19): %f\n" % C19)
        