import pandas as pd

from business_logic import *


def require_dataframe(dataframe):
    if dataframe is None:
        print("\nError: la imputacion fallo (alguna columna no existe). Se detiene el proceso.")
        raise SystemExit(1)
    return dataframe


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

# 1. Cargar datos iniciales
taxes = load_taxes_data()

# show_basic_info(taxes)

show_missing_values(taxes)

# show_value_counts("NOMBRE_LOCALIDAD", taxes)

# show_value_counts("NOMBRE_UPZ", taxes)

# show_value_counts("NOMBRE_BARRIO", taxes)

# show_value_counts("ESTRATO", taxes)

# show_value_counts("ANIO_GRAVABLE", taxes)

# show_value_counts("DESTINO_SHD", taxes)

# print(f"\n")
# print("=" * 50)
# print("Imputation of missing values")

# show_numeric_summary(taxes, NUMERIC_COLUMNS_TO_INPUTE)
taxes = require_dataframe(impute_numeric_columns(taxes, NUMERIC_COLUMNS_TO_INPUTE))
# show_numeric_summary(taxes, NUMERIC_COLUMNS_TO_INPUTE)

taxes = require_dataframe(impute_category_columns(taxes, CATEGORY_COLUMNS_TO_INPUTE))
# show_imputation_report(taxes, CATEGORY_COLUMNS_TO_INPUTE)

taxes = require_dataframe(impute_id_columns(taxes, ID_COLUMNS_TO_INPUTE))
# show_imputation_report(taxes, ID_COLUMNS_TO_INPUTE)

# show_missing_values(taxes)

enriched_taxes = dataframe_enrichment(taxes)

print(enriched_taxes)

# print(enriched_taxes.describe())

