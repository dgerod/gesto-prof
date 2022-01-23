import os
from scripts.common.configuration import Configuration
from scripts.common.db import DataBase
from scripts.common.invoices import ExpensesLoader


def add_expenses(file_name: str):

    configuration = Configuration()
    file_path = os.path.join(configuration.get_inputs_directory(),
                             file_name)

    new_expenses = ExpensesLoader(file_path).expenses()

    db = DataBase(configuration.get_db_directory())
    db.add_expenses(new_expenses)

    print("New expenses: %s" % len(new_expenses._df))
