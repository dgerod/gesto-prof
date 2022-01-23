import os
import pandas as pd
from scripts.common.configuration import Configuration
from scripts.common.db import DataBase
from scripts.common import periods as taxes_periods


def generate_report_periods():

    configuration = Configuration()
    db = DataBase(configuration.get_db_directory())
    expenses = db.retrieve_expenses()
    incomes = db.retrieve_incomes()

    periods = taxes_periods.generate_periods()
    summary = []

    for d in periods:
    
        start_date = pd.to_datetime(d[0])
        end_date = pd.to_datetime(d[1])
        mask = (expenses["FECHA OPERACIÓN"] > start_date) & (expenses["FECHA OPERACIÓN"] <= end_date)
        period_expenses = expenses.loc[mask]
    
        mask = (incomes["FECHA FACTURA"] > start_date) & (incomes["FECHA FACTURA"] <= end_date)
        period_incomes = incomes.loc[mask]
    
        if len(period_expenses) > 0:
            total_base = period_expenses["IMPORTE BASE"].sum()
            total_taxes = period_expenses["IMPORTE IVA"].sum()
            total_amount = period_expenses["IMPORTE TOTAL"].sum()
        else:
            total_base = total_taxes = total_amount = 0.0
    
        gastos = (total_base, total_taxes, total_amount)
    
        if len(period_incomes) > 0:
            total_base = period_incomes["IMPORTE BASE"].sum()
            total_taxes = period_incomes["IMPORTE IVA"].sum()
            total_amount = period_incomes["IMPORTE TOTAL"].sum()
        else:
            total_base = total_taxes = total_amount = 0.0
    
        ingresos = (total_base, total_taxes, total_amount)
        summary.append((ingresos, gastos, ingresos[2] - gastos[2]))
        
    output_file = os.path.join(configuration.get_outputs_directory(), "informe_periodos.txt")
    with open(output_file, "w") as f:
        
        total_expenses = 0.
        total_incomes = 0.
        total_difference = 0.

        for t, s in zip(periods, summary):
        
            start_date, end_date = t
            ingresos = s[0]
            gastos = s[1]
            difference = s[2]
        
            total_expenses += gastos[0]
            total_incomes += ingresos[0]
            total_difference += difference
        
            f.write("Periodo: %s - %s\n" % (start_date, end_date))
            f.write("   Ingresos:\n")
            f.write("      Base imponible: %f\n" % ingresos[0])
            f.write("      Importe IVA: %f\n" % ingresos[1])
            f.write("      Importe total: %f\n" % ingresos[2])
            f.write("   Gastos:\n")
            f.write("      Base imponible: %f\n" % gastos[0])
            f.write("      Importe IVA: %f\n" % gastos[1])
            f.write("      Importe total: %f\n" % gastos[2])
            f.write("   Diferencia: %f\n" % difference)
            f.write("\n")
                    
        f.write("Total (base imponible):\n")
        f.write("   Ingresos: %f\n" % total_incomes)
        f.write("   Gastos: %f\n" % total_expenses)
        f.write("   Diferencia: %f\n" % (total_incomes - total_expenses))
        f.write("\n")
                
        f.write("Diferencia (real): %f\n" % total_difference)

