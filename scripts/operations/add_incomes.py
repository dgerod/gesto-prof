import os
from scripts.common.configuration import Configuration
from scripts.common.db import DataBase
from scripts.common.invoices import IncomesLoader


def add_incomes(file_name: str):

    configuration = Configuration()
    file_path = os.path.join(configuration.get_inputs_directory(),
                             file_name)

    new_incomes = IncomesLoader(file_path).incomes()

    db = DataBase(configuration.get_db_directory())
    db.add_incomes(new_incomes)

    print("New incomes: %s" % len(new_incomes._df))
