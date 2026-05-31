import pandas as pd

DATA_FILENAME = "cumplimiento-impuesto-predial_2007_2023.csv"

MISSING_VALUES = ["", "NaN" "NA", "N/A", "NO REGISTRA"]


CATEGORY_COLUMNS_TO_INPUTE = ["NOMBRE_LOCALIDAD", "NOMBRE_BARRIO", "DESTINO_SHD", "ESTRATO", "NOMBRE_UPZ"]

NUMERIC_COLUMNS_TO_INPUTE = ["TOTAL_PREDIOS_OPORTUNOS", "TOTAL_PREDIOS_EXTEMPORANEOS", "TOTAL_PAGADO"]

ID_COLUMNS_TO_INPUTE = ["CODIGO_LOCALIDAD", "CODIGO_UPZ"]


INT_COLUMNS = ["ANIO_GRAVABLE", "TOTAL_PREDIOS", "TOTAL_PREDIOS_OBLIGADOS", "TOTAL_PREDIOS_NO_OBLIGADOS", "TOTAL_PREDIOS_OPORTUNOS", "TOTAL_PREDIOS_EXTEMPORANEOS", "TOTAL_PREDIOS_MOROSOS", "TOTAL_PREDIOS_NO-DECLARAN"]

# Todas las columnas con Identificadores se toman como cadena de caracteres.
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

def show_basic_info(dataframe: pd.DataFrame):
    try:
        print(f"Shape: {dataframe.shape}\nSize: {taxes.size}\n")
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


def impute_numeric_columns(dataframe: pd.DataFrame, columns: list[str]):
    try:
        copy_dataframe = dataframe.copy()
        for numeric_column in columns:
            print(f"\n{copy_dataframe[numeric_column].describe().round(2)}")
            copy_dataframe[f"{numeric_column}_IMPUTED"] = copy_dataframe[numeric_column].isna()
            copy_dataframe[numeric_column] = copy_dataframe[numeric_column].fillna(copy_dataframe[numeric_column].mean().round())
            print(f"\n{copy_dataframe[numeric_column].describe().round(2)}")
        return copy_dataframe
    except KeyError as err:
        print(f"\nError: {err} is not a column")
        return None


def impute_category_columns(dataframe: pd.DataFrame, columns: list[str]):
    try:
        copy_dataframe = dataframe.copy()
        for category_column in columns:
            copy_dataframe[f"{category_column}_IMPUTED"] = copy_dataframe[category_column].isna()
            copy_dataframe[category_column] = copy_dataframe[category_column].fillna(copy_dataframe[category_column].mode()[0])
            print(f"\nTotal imputed in {category_column}: {copy_dataframe[f'{category_column}_IMPUTED'].sum()}")
            show_value_counts(category_column, copy_dataframe)
        return copy_dataframe
    except KeyError as err:
        print(f"\nError: {err} is not a column")
        return None

def impute_id_columns(dataframe: pd.DataFrame, columns: list[str]):
    try:
        copy_dataframe = dataframe.copy()
        for id_column in columns:
            copy_dataframe[f"{id_column}_IMPUTED"] = copy_dataframe[id_column] == "0"
            copy_dataframe.loc[copy_dataframe[f"{id_column}_IMPUTED"], id_column] = copy_dataframe.loc[~copy_dataframe[f"{id_column}_IMPUTED"], id_column].mode()[0]
            print(f"\nTotal imputed in {id_column}: {copy_dataframe[f'{id_column}_IMPUTED'].sum()}")
            show_value_counts(id_column, copy_dataframe)
        return copy_dataframe
    except KeyError as err:
        print(f"\nError: {err} is not a column")
        return None



taxes = pd.read_csv(DATA_FILENAME, delimiter=";", encoding="latin1", dtype=TEXT_COLUMS, na_values=MISSING_VALUES)

taxes[INT_COLUMNS] = taxes[INT_COLUMNS].astype("Int64")



show_basic_info(taxes)

show_missing_values(taxes)

show_value_counts("NOMBRE_LOCALIDAD", taxes)

show_value_counts("NOMBRE_UPZ", taxes)

show_value_counts("NOMBRE_BARRIO", taxes)

show_value_counts("ESTRATO", taxes)

show_value_counts("ANIO_GRAVABLE", taxes)

show_value_counts("DESTINO_SHD", taxes)



print(f"\n")
print("=" * 50)
print("Imputation of missing values")

taxes = impute_numeric_columns(taxes, NUMERIC_COLUMNS_TO_INPUTE)

taxes = impute_category_columns(taxes, CATEGORY_COLUMNS_TO_INPUTE)

taxes = impute_id_columns(taxes, ID_COLUMNS_TO_INPUTE)



show_missing_values(taxes)