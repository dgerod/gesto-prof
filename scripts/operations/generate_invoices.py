import os
from string import Template
import pandas as pd
from fpdf import FPDF
from scripts.common.configuration import Configuration
from scripts.common.db import DataBase
from scripts.common import periods as taxes_periods
from scripts.common.invoices import IncomesLoader


def generate_simplified_invoices(file_name: str):

    configuration = Configuration()
    db = DataBase(configuration.get_db_directory())

    file_path = os.path.join(configuration.get_inputs_directory(),
                             file_name)

    new_incomes = IncomesLoader(file_path).incomes()
    incomes = new_incomes._df

    company_name, company_nif = db.get_company_information()
    
    num_invoices = 0
    periods = taxes_periods.generate_periods()
    for tdx in range(0, len(periods)):

        start_date = pd.to_datetime(periods[tdx][0])
        end_date = pd.to_datetime(periods[tdx][1])

        mask = (incomes["FECHA FACTURA"] > start_date) & (incomes["FECHA FACTURA"] <= end_date)
        period_incomes = incomes.loc[mask]
    
        for index, row in period_incomes.iterrows():
    
            invoice_data = {
                "Empresa": company_name.upper(),
                "NIF": company_nif,
                "NumeroFactura": row["NÚMERO FACTURA"],
                "FechaEmision": row["FECHA FACTURA"].date().strftime("%d/%m/%Y"),
                "Descripcion": row["CONCEPTO"],
                "ImporteBase": row["IMPORTE BASE"],
                "IVA": row["% IVA"],
                "ImporteIVA": row["IMPORTE IVA"],
                "ImporteTotal": row["IMPORTE TOTAL"]}
        
            file_name ="fs_T%s_%s.txt" % (tdx+1, row["NÚMERO FACTURA"])
            temporary_file = os.path.join(configuration.get_temp_directory(), file_name)
            template_file = os.path.join(configuration.get_templates_directory(), "reports", "factura_simplificada.template.txt")
    
            with open(template_file, "r") as ftemp, open(temporary_file, "w") as fout:
        
                template = Template(ftemp.read())
                result = template.substitute(invoice_data)
                fout.write(result)

            file_name ="fs_T%s_%s.pdf" % (tdx+1, row["NÚMERO FACTURA"])
            output_file = os.path.join(configuration.get_outputs_directory(), file_name) 
            
            with open(temporary_file, "r") as fin:
            
                pdf = FPDF()   
                
                pdf.add_page()
                pdf.set_font("Arial", size = 15)
                
                for x in fin:
                    pdf.cell(200, 10, txt = x, ln = 1, align = "L")
                pdf.output(output_file)   

            num_invoices += 1
                    
    print("Num invoices: %s" % num_invoices)


def export_simplified_invoices():

    configuration = Configuration()
    db = DataBase(configuration.get_db_directory())
    incomes = db.retrieve_incomes()
    
    company_name, company_nif = db.get_company_information()
    
    num_invoices = 0
    periods = taxes_periods.generate_periods()
    for tdx in range(0, len(periods)):

        start_date = pd.to_datetime(periods[tdx][0])
        end_date = pd.to_datetime(periods[tdx][1])

        mask = (incomes["FECHA FACTURA"] > start_date) & (incomes["FECHA FACTURA"] <= end_date)
        period_incomes = incomes.loc[mask]
    
        for index, row in period_incomes.iterrows():
    
            invoice_data = {
                "Empresa": company_name,
                "NIF": company_nif,
                "NumeroFactura": row["NÚMERO FACTURA"],
                "FechaEmision": row["FECHA FACTURA"].date().strftime("%d/%m/%Y"),
                "Descripcion": row["CONCEPTO"],
                "ImporteBase": row["IMPORTE BASE"],
                "IVA": row["% IVA"],
                "ImporteIVA": row["IMPORTE IVA"],
                "ImporteTotal": row["IMPORTE TOTAL"]}
        
            file_name ="fs_T%s_%s.txt" % (tdx+1, row["NÚMERO FACTURA"])
            temporary_file = os.path.join(configuration.get_temp_directory(), file_name)
            template_file = os.path.join(configuration.get_templates_directory(), "reports", "factura_simplificada.template.txt")
    
            with open(template_file, "r") as ftemp, open(temporary_file, "w") as fout:
        
                template = Template(ftemp.read())
                result = template.substitute(invoice_data)
                fout.write(result)

            file_name ="fs_T%s_%s.pdf" % (tdx+1, row["NÚMERO FACTURA"])
            output_file = os.path.join(configuration.get_outputs_directory(), file_name) 
            
            with open(temporary_file, "r") as fin:
            
                pdf = FPDF()   
                
                pdf.add_page()
                pdf.set_font("Arial", size = 15)
                
                for x in fin:
                    pdf.cell(200, 10, txt = x, ln = 1, align = "L")
                pdf.output(output_file)   

            num_invoices += 1
                    
    print("Num invoices: %s" % num_invoices)
