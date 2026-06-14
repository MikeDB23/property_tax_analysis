import pandas as pd

from business_logic import *

NEIGHBORHOOD_COLUMN = "NOMBRE_BARRIO"
NEIGHBORHOOD_MAPPING = {
    "ABRAHAM LINCON": "ABRAHAM LINCOLN"
}

COLUMNS_TO_EXPLORE = ["NOMBRE_LOCALIDAD", "NOMBRE_UPZ", "NOMBRE_BARRIO", "ESTRATO", "ANIO_GRAVABLE", "DESTINO_SHD"]

def require_dataframe(dataframe):
    if dataframe is None:
        print("\nError: imputation failed (missing column). Program will be stoped.")
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

def show_section_title(title: str):
    print(f"\n")
    print("=" * 50)
    print(title)

# 1. Load codes
taxes = load_taxes_data()
# Change the display format of floats
pd.options.display.float_format = "{:,.2f}".format

show_section_title("Basic exploration of the dataset")

show_basic_info(taxes)

show_missing_values(taxes)

for column in COLUMNS_TO_EXPLORE:
    show_value_counts(column, taxes)


show_section_title("Imputation of missing values")

taxes = require_dataframe(normalize_categorical_column(taxes, NEIGHBORHOOD_COLUMN, NEIGHBORHOOD_MAPPING))

# show_numeric_summary(taxes, NUMERIC_COLUMNS_TO_INPUTE)
taxes = require_dataframe(impute_numeric_columns(taxes, NUMERIC_COLUMNS_TO_INPUTE))
# show_numeric_summary(taxes, NUMERIC_COLUMNS_TO_INPUTE)

taxes = require_dataframe(impute_category_columns(taxes, CATEGORY_COLUMNS_TO_INPUTE))
# show_imputation_report(taxes, CATEGORY_COLUMNS_TO_INPUTE)

taxes = require_dataframe(impute_id_columns(taxes, ID_COLUMNS_TO_INPUTE))
# show_imputation_report(taxes, ID_COLUMNS_TO_INPUTE)

# Confirmation of missing values left
show_missing_values(taxes)

enriched_taxes = dataframe_enrichment(taxes)

# print(enriched_taxes)

# show the profitability distribution
print(enriched_taxes[["RENTABILIDAD"]].value_counts())

# show the SHD distribution
print(enriched_taxes[["NOMBRE_SHD"]].value_counts())

# show the media por predio distribution
print(enriched_taxes[["MEDIA_POR_PREDIO"]])

print(enriched_taxes.describe())

show_section_title("Questions")

# ¿Cuantos predios morosos se han registrado por cada estrato?
try:
    print(f"\n{slow_payers_by_stratus(enriched_taxes)}")
except ValueError as err:
    print(f"\nError: {err}")
except TypeError as err:
    print(f"\nError: {err}")

# ¿Cuales son los barrios de los que se recauda mas dinero?
try:
    print(f"\n{payment_total_by_neighborhood(enriched_taxes).head(20)}")
except ValueError as err:
    print(f"\nError: {err}")
except TypeError as err:
    print(f"\nError: {err}")

# ¿Cuanto se ha recaudado en pagos totales por año?
try:
    print(f"\n{adjust_yearly_totals_for_inflation(enriched_taxes, 2023).sort_values("VALOR_ACTUAL", ascending=False)}")
except ValueError as err:
    print(f"\nError: {err}")
except KeyError as err:
    print(f"\nError: {err}")

