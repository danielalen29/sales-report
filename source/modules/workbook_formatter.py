from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


def format_workbook(report_path: Path) -> None:
    workbook = load_workbook(report_path)

    summary_worksheet = workbook['Summary']
    category_worksheet = workbook['By Category']
    country_worksheet = workbook['By Country']
    clean_worksheet = workbook['Cleaned Sales']

    header_fill = PatternFill(
        fill_type='solid',
        fgColor='24476B',
    )
    header_font = Font(bold=True, color='FFFFFF')

    for worksheet in workbook.worksheets:
        worksheet.row_dimensions[1].height = 22

        for cell in worksheet[1]:
            if cell.value is not None:
                cell.font = header_font
                cell.fill = header_fill

    for column in ('D', 'F'):
        for cell in clean_worksheet[column][1:]:
            cell.number_format = '$#,##0.00'

    for worksheet in (
        summary_worksheet,
        category_worksheet,
        country_worksheet,
    ):
        for cell in worksheet['C'][1:]:
            cell.number_format = '$#,##0.00'

    for worksheet in workbook.worksheets:
        last_column = get_column_letter(worksheet.max_column)

        worksheet.auto_filter.ref = f'A1:{last_column}{worksheet.max_row}'
        worksheet.freeze_panes = 'A2'

    product_count = sum(
        cell.value is not None
        for cell in summary_worksheet['A'][1:]
    )
    summary_worksheet.auto_filter.ref = f'A1:C{product_count + 1}'

    summary_worksheet['F2'].number_format = '$#,##0.00'

    for row_number in range(3, 6):
        summary_worksheet[f'F{row_number}'].number_format = '#,##0'

    for worksheet in workbook.worksheets:
        for column in worksheet.columns:
            maximum_length = 0

            for cell in column:
                if cell.value is not None:
                    cell_length = len(str(cell.value))

                    if cell_length > maximum_length:
                        maximum_length = cell_length

            column_letter = column[0].column_letter
            worksheet.column_dimensions[column_letter].width = (
                maximum_length + 4
            )

    summary_worksheet.merge_cells('E7:F9')
    coverage_note = summary_worksheet['E7']
    coverage_note.value = (
        "Totals include valid sales records only. "
        "Excluded records are saved in csv_reports/excluded_sales.csv."
    )
    coverage_note.alignment = Alignment(
        wrap_text=True,
        vertical='top',
    )
    coverage_note.font = Font(size=10, color='595959')

    for row_number in range(7, 10):
        summary_worksheet.row_dimensions[row_number].height = 20

    workbook.save(report_path)