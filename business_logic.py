import pandas as pd

DATA_FILENAME = "cumplimiento-impuesto-predial_2007_2023.csv"

MISSING_VALUES = ["", "NaN" "NA", "N/A", "NO REGISTRA"]


CATEGORY_COLUMNS_TO_INPUTE = ["NOMBRE_LOCALIDAD", "NOMBRE_BARRIO", "DESTINO_SHD", "ESTRATO", "NOMBRE_UPZ"]

NUMERIC_COLUMNS_TO_INPUTE = ["TOTAL_PREDIOS_OPORTUNOS", "TOTAL_PREDIOS_EXTEMPORANEOS", "TOTAL_PAGADO"]

ID_COLUMNS_TO_INPUTE = ["CODIGO_LOCALIDAD", "CODIGO_UPZ"]


INT_COLUMNS = ["ANIO_GRAVABLE", "TOTAL_PREDIOS", "TOTAL_PREDIOS_OBLIGADOS", "TOTAL_PREDIOS_NO_OBLIGADOS", "TOTAL_PREDIOS_OPORTUNOS", "TOTAL_PREDIOS_EXTEMPORANEOS", "TOTAL_PREDIOS_MOROSOS", "TOTAL_PREDIOS_NO-DECLARAN"]

TEXT_COLUMS = {
    "ID": "string",
    "CODIGO_LOCALIDAD": "string",
    "CODIGO_UPZ" : "string",
    "NOMBRE_LOCALIDAD" : "category",
    "NOMBRE_UPZ": "category",
    "NOMBRE_BARRIO" : "string",
    "DESTINO_SHD" : "string",
    "ESTRATO" : "category",
}


def load_taxes_data() -> pd.DataFrame:
    taxes = pd.read_csv(DATA_FILENAME, delimiter=";", encoding="latin1", na_values=MISSING_VALUES)
    taxes[INT_COLUMNS] = taxes[INT_COLUMNS].astype("Int64")
    return taxes


def show_basic_info(dataframe: pd.DataFrame):
    try:
        print(f"Shape: {dataframe.shape}\nSize: {dataframe.size}\n")
        print(dataframe.info())
    except:
        print(f"\nError: the parameter is no a valid dataframe ({type(pd.DataFrame)})")


def show_value_counts(column: str, dataframe: pd.DataFrame):
    try:
        print(f"\n{column}: \n{dataframe[column].value_counts(dropna=False)}")
    except KeyError as err:
        print(f"\nError: {err} is not a column")


def show_missing_values(dataframe: pd.DataFrame):
    print(f"\nTotal missing values:\n{dataframe.isna().sum()}")


def show_numeric_summary(dataframe: pd.DataFrame, columns: list[str]):
    for numeric_column in columns:
        print(f"\n{dataframe[numeric_column].describe().round(2)}")


def show_imputation_report(dataframe: pd.DataFrame, columns: list[str]):
    for column in columns:
        print(f"\nTotal imputed in {column}: {dataframe[f'{column}_IMPUTED'].sum()}")
        show_value_counts(column, dataframe)


def impute_numeric_columns(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame | None:
    try:
        copy_dataframe = dataframe.copy()
        for numeric_column in columns:
            copy_dataframe[f"{numeric_column}_IMPUTED"] = copy_dataframe[numeric_column].isna()
            copy_dataframe[numeric_column] = copy_dataframe[numeric_column].fillna(copy_dataframe[numeric_column].mean().round())
        return copy_dataframe
    except KeyError:
        return None


def impute_category_columns(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame | None:
    try:
        copy_dataframe = dataframe.copy()
        for category_column in columns:
            copy_dataframe[f"{category_column}_IMPUTED"] = copy_dataframe[category_column].isna()
            copy_dataframe[category_column] = copy_dataframe[category_column].fillna(copy_dataframe[category_column].mode()[0])
        return copy_dataframe
    except KeyError:
        return None


def impute_id_columns(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame | None:
    try:
        copy_dataframe = dataframe.copy()
        for id_column in columns:
            copy_dataframe[f"{id_column}_IMPUTED"] = copy_dataframe[id_column] == "0"
            copy_dataframe.loc[copy_dataframe[f"{id_column}_IMPUTED"], id_column] = copy_dataframe.loc[~copy_dataframe[f"{id_column}_IMPUTED"], id_column].mode()[0]
        return copy_dataframe
    except KeyError:
        return None
