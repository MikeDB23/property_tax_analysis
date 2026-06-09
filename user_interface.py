import sys

from business_logic import *


def require_dataframe(dataframe):
    if dataframe is None:
        print("\nError: la imputacion fallo (alguna columna no existe). Se detiene el proceso.")
        sys.exit(1)
    return dataframe


taxes = load_taxes_data()


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

show_numeric_summary(taxes, NUMERIC_COLUMNS_TO_INPUTE)
taxes = require_dataframe(impute_numeric_columns(taxes, NUMERIC_COLUMNS_TO_INPUTE))
show_numeric_summary(taxes, NUMERIC_COLUMNS_TO_INPUTE)

taxes = require_dataframe(impute_category_columns(taxes, CATEGORY_COLUMNS_TO_INPUTE))
show_imputation_report(taxes, CATEGORY_COLUMNS_TO_INPUTE)

taxes = require_dataframe(impute_id_columns(taxes, ID_COLUMNS_TO_INPUTE))
show_imputation_report(taxes, ID_COLUMNS_TO_INPUTE)


show_missing_values(taxes)
