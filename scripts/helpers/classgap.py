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
        
        column_dates = ["Fecha"]
        
        column_types = {
            "NÚMERO CLIENTE" : str,
            "NOMBRE ESTUDIANTE" : str,
            "PRECIO PROFESOR" : str,
            "PRECIO PROFESOR" : str,
            "BASE IMPONIBLE" : str,
            "COMISIÓN" : str,
            "BENEFICIO PROFESOR" : str,
            "BENEFICIO CLASSGAP" : str}

        return pd.read_csv(file_path, sep=';', decimal='.',
                           parse_dates=column_dates, dtype=column_types)

    @staticmethod
    def _clean_symbols(df):

        money = dict(zip(["€",","],["","."]))
        percentage = dict(zip(["%",","],["","."]))

        df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.date
        df["Precio Profesor"] = pd.to_numeric(df["Precio Profesor"].replace(
            money, regex=True))
        df["Precio Promoción"] = pd.to_numeric(df["Precio Promoción"].replace(
            money, regex=True))
        df["Comisión"] = pd.to_numeric(df["Comisión"].replace(
            percentage, regex=True))
        df["Beneficio Profesor"] = pd.to_numeric(df["Beneficio Profesor"].replace(
            money, regex=True))
        df["Beneficio Classgap"] = pd.to_numeric(df["Beneficio Classgap"].replace(
            money, regex=True))

        return df

    def _calculate_lesson_price(self, df):

        prices = []
        for index, row in df.iterrows():

            professor_benefit = float(row["Beneficio Profesor"])
            cg_benefit = float(row["Beneficio Classgap"])

            if cg_benefit > 0.:
                prices.append(professor_benefit + cg_benefit)
            else:
                prices.append(professor_benefit)

        corrected_income = df.copy(True)
        corrected_income['Precio Factura'] = prices

        return corrected_income
