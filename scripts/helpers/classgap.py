import pandas as pd


class LessonsIncomeLoader:

    def __init__(self, file_path: str):

        df = self._load(file_path)
        self._original = self._clean_symbols(df)
        self._corrected = self._calculate_lesson_price(df)


    def loaded(self):
        return self._original

    def data(self):
        return self._corrected

    @staticmethod
    def _load(file_path):
        
        column_dates = ["FECHA"]
        
        column_types = {
            "NÚMERO CLIENTE" : str,
            "NOMBRE ESTUDIANTE" : str,
            "PRECIO PROFESOR" : str,
            "PRECIO PROMOCIÓN" : str,
            "COMISIÓN" : str,
            "BENEFICIO PROFESOR" : str,
            "BENEFICIO CLASSGAP" : str}

        return pd.read_csv(file_path, sep=';', decimal='.',
                           parse_dates=column_dates, dtype=column_types)

    @staticmethod
    def _clean_symbols(df):

        money = dict(zip(["€",","],["","."]))
        percentage = dict(zip(["%",","],["","."]))

        df["FECHA"] = pd.to_datetime(df["FECHA"]).dt.date
        df["PRECIO PROFESOR"] = pd.to_numeric(df["PRECIO PROFESOR"].replace(
            money, regex=True))
        df["PRECIO PROMOCIÓN"] = pd.to_numeric(df["PRECIO PROMOCIÓN"].replace(
            money, regex=True))
        df["COMISIÓN"] = pd.to_numeric(df["COMISIÓN"].replace(
            percentage, regex=True))
        df["BENEFICIO PROFESOR"] = pd.to_numeric(df["BENEFICIO PROFESOR"].replace(
            money, regex=True))
        df["BENEFICIO CLASSGAP"] = pd.to_numeric(df["BENEFICIO CLASSGAP"].replace(
            money, regex=True))

        return df

    def _calculate_lesson_price(self, df):

        prices = []
        for index, row in df.iterrows():

            professor_benefit = float(row["BENEFICIO PROFESOR"])
            cg_benefit = float(row["BENEFICIO CLASSGAP"])

            if cg_benefit > 0.:
                prices.append(professor_benefit + cg_benefit)
            else:
                prices.append(professor_benefit)

        corrected_income = df.copy(True)
        corrected_income['PRECIO FACTURA'] = prices

        return corrected_income
