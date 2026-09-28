from pathlib import Path

from modules import report_generator, workbook_formatter


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / 'data' / 'sales.csv'
    output_folder = project_root / 'output'

    report_path = output_folder / 'sales_report.xlsx'
    csv_reports_folder = output_folder / 'csv_reports'

    try:
        csv_reports_folder.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Could not create the output folder: {error}")
        return

    try:
        report_generator.generate_sales_report(
            input_path=input_file,
            report_path=report_path,
            csv_reports_folder=csv_reports_folder,
        )
        workbook_formatter.format_workbook(report_path)
    except (ValueError, OSError) as error:
        print(f"Could not generate the sales report: {error}")
        return


if __name__ == '__main__':
    main()