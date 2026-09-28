from pathlib import Path

import pandas as pd

from modules.utilities import (
    calculate_sales_metrics,
    prepare_sales_data,
    summarize_sales,
    validate_required_columns,
)


def generate_sales_report(
    input_path: Path,
    report_path: Path,
    csv_reports_folder: Path,
) -> None:
    dataframe = pd.read_csv(input_path)
    validate_required_columns(dataframe=dataframe)

    prepared_dataframe = prepare_sales_data(dataframe)

    required_columns = [
        'Product', 'Category', 'Quantity', 'Price', 'Country'
    ]

    quantity = prepared_dataframe['Quantity']
    price = prepared_dataframe['Price']

    valid_rows = (
        prepared_dataframe[required_columns].notna().all(axis=1)
        & (quantity > 0)
        & (quantity % 1 == 0)
        & (price >= 0)
        & (price < float('inf'))
    )

    excluded_rows = dataframe.loc[~valid_rows].copy()
    clean_dataframe = prepared_dataframe.loc[
        valid_rows,
        required_columns,
    ].copy()

    if clean_dataframe.empty:
        raise ValueError("No valid sales rows remain for reporting.")

    clean_dataframe['Revenue'] = (
        clean_dataframe['Quantity'] * clean_dataframe['Price']
    )

    summary_dataframe = summarize_sales(
        clean_dataframe,
        group_column='Product',
    )
    category_summary = summarize_sales(
        clean_dataframe,
        group_column='Category',
    )
    country_summary = summarize_sales(
        clean_dataframe,
        group_column='Country',
    )

    metrics_dataframe = calculate_sales_metrics(
        clean_dataframe,
        excluded_row_count=len(excluded_rows),
    )

    excluded_rows.to_csv(
        csv_reports_folder / 'excluded_sales.csv',
        index=True,
        index_label='SourceIndex',
    )
    clean_dataframe.to_csv(
        csv_reports_folder / 'cleaned_sales.csv',
        index=False,
    )
    summary_dataframe.to_csv(
        csv_reports_folder / 'sales_summary.csv',
        index=False,
    )

    with pd.ExcelWriter(report_path) as writer:
        summary_dataframe.to_excel(
            writer,
            sheet_name='Summary',
            index=False,
        )
        metrics_dataframe.to_excel(
            writer,
            sheet_name='Summary',
            startcol=4,
            index=False,
        )
        category_summary.to_excel(
            writer,
            sheet_name='By Category',
            index=False,
        )
        country_summary.to_excel(
            writer,
            sheet_name='By Country',
            index=False,
        )
        clean_dataframe.to_excel(
            writer,
            sheet_name='Cleaned Sales',
            index=False,
        )