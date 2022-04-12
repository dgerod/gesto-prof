import os
from scripts.common.configuration import Configuration
from scripts.common.db import DataBase
from scripts.common.invoices import ExpensesLoader


def add_expenses(file_path: str):

    configuration = Configuration()
    
    if os.path.dirname(file_path) == "":
        abs_file_path = os.path.join(configuration.get_inputs_directory(),
                                     file_path)
    else:
        abs_file_path = os.path.abspath(file_path)

    new_expenses = ExpensesLoader(abs_file_path).expenses()

    db = DataBase(configuration.get_db_directory())
    db.add_expenses(new_expenses)

    print("New expenses: %s" % len(new_expenses._df))
