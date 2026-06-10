import pandas as pd

DATA_FILENAME = "cumplimiento-impuesto-predial_2007_2023.csv"
# ENRICHED_DATA_FRAME = "cumplimiento-impuesto-predial_2007_2023_enriched.csv"


MISSING_VALUES = ["", "NaN", "NA", "N/A", "NO REGISTRA"]


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


def mean_per_predio(dataframe: pd.DataFrame) -> pd.DataFrame | None:
    try:
        copy_dataframe = dataframe.copy()
        copy_dataframe["MEDIA_POR_PREDIO"] = (copy_dataframe["TOTAL_PAGADO"] / copy_dataframe["TOTAL_PREDIOS"]).round(2)
        return copy_dataframe
    except KeyError:
        return None


def drop_imputation_flags(dataframe: pd.DataFrame) -> pd.DataFrame:
    flag_columns = [column for column in dataframe.columns if column.endswith("_IMPUTED")]
    return dataframe.drop(columns=flag_columns)


def dataframe_enrichment(dataframe: pd.DataFrame) -> pd.DataFrame | None:
    copy_dataframe = mean_per_predio(dataframe)
    if copy_dataframe is None:
        return None
    copy_dataframe = drop_imputation_flags(copy_dataframe)
    # copy_dataframe.to_csv(ENRICHED_DATA_FRAME, index=False)
    return copy_dataframe




