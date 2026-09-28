import pandas as pd


def validate_required_columns(dataframe: pd.DataFrame) -> None:
    required_columns = {
        'Product', 'Category', 'Quantity', 'Price', 'Country'
    }

    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        missing_names = ', '.join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing_names}")


def prepare_sales_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    prepared = dataframe.copy()

    for column in ('Product', 'Category', 'Country'):
        prepared[column] = prepared[column].astype('string').str.strip()
        prepared[column] = prepared[column].replace('', pd.NA)

    for column in ('Quantity', 'Price'):
        prepared[column] = pd.to_numeric(
            prepared[column],
            errors='coerce',
        )

    return prepared


def summarize_sales(
    sales_dataframe: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    summary = sales_dataframe.groupby(
        group_column,
        as_index=False,
    )[['Quantity', 'Revenue']].sum()

    return summary.sort_values(
        'Revenue',
        ascending=False,
        ignore_index=True,
    )


def calculate_sales_metrics(
    sales_dataframe: pd.DataFrame,
    excluded_row_count: int,
) -> pd.DataFrame:
    return pd.DataFrame({
        'Metric': [
            'Total revenue',
            'Units sold',
            'Included records',
            'Excluded records',
        ],
        'Value': [
            sales_dataframe['Revenue'].sum(),
            sales_dataframe['Quantity'].sum(),
            len(sales_dataframe),
            excluded_row_count,
        ],
    })