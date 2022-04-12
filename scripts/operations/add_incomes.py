import os
from scripts.common.configuration import Configuration
from scripts.common.db import DataBase
from scripts.common.invoices import IncomesLoader


def add_incomes(file_path: str):

    configuration = Configuration()

    if os.path.dirname(file_path) == "":
        abs_file_path = os.path.join(configuration.get_inputs_directory(),
                                     file_path)
    else:
        abs_file_path = os.path.abspath(file_path)

    new_incomes = IncomesLoader(abs_file_path).incomes()

    db = DataBase(configuration.get_db_directory())
    db.add_incomes(new_incomes)

    print("New incomes: %s" % len(new_incomes._df))
