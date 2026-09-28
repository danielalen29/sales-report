# Sales Report

Turn structured sales data into a clear Excel report that saves manual spreadsheet work.

This Python project reads a sales CSV, validates the required fields, calculates revenue, and generates a formatted workbook with product, category, and country summaries.

## Business questions answered

- How much revenue did the included sales generate?
- How many units were sold?
- Which products, categories, and countries generated the most revenue?
- How many records were included or excluded?

Revenue is calculated as **Quantity × Price**. All sample prices and reported monetary values are in **USD**. The project does not convert currencies.

## Example results

The included sample contains 15 records:

| Metric | Result |
|---|---:|
| Revenue from included records | USD 3,350.00 |
| Units sold in included records | 21 |
| Included records | 11 |
| Excluded records | 4 |

Download the [example Excel report](examples/sales_report.xlsx)
and inspect the [excluded records](examples/csv_reports/excluded_sales.csv).

## Input requirements

Place the input file at `data/sales.csv`.

The following column names are required and case-sensitive:

| Column | Expected value |
|---|---|
| Product | Nonblank product name |
| Category | Nonblank category name |
| Quantity | Positive whole number |
| Price | Finite, nonnegative unit price in USD |
| Country | Nonblank country name |

Column order may vary. Extra columns are omitted from the reporting detail.

The program trims surrounding whitespace from text fields and converts quantity and price values to numbers. Rows that fail the reporting rules are excluded; missing values are not estimated. Original excluded records are saved separately for review.

Zero-priced sales are allowed. Returns and negative quantities are outside this project's scope. Duplicate-looking records are retained because the input has no transaction identifier.

## How to run

The project was tested with Python 3.14.0. The following commands are for Windows PowerShell.

From the project folder, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the report:

```powershell
python source/main.py
```

The output folders are created automatically. Close the existing report in Excel before running again so it can be overwritten.

A successful run currently prints no message. Open `output/sales_report.xlsx` to view the result.

## Generated files

The Excel workbook contains four worksheets:

- **Summary:** Product rankings and headline metrics.
- **By Category:** Quantity and revenue by category.
- **By Country:** Quantity and revenue by country.
- **Cleaned Sales:** Included sales records with calculated revenue.

The workbook includes formatted headers, currency formats, filters, frozen headers, and a note explaining excluded records.

Three CSV files are also saved in `output/csv_reports/`:

- `cleaned_sales.csv`
- `sales_summary.csv` — product totals
- `excluded_sales.csv` — original excluded records

`SourceIndex` in the exclusions file is the zero-based pandas row index, not a physical CSV line number.

Successful runs overwrite the generated files. A failed run may leave reports from an earlier run in place.

## Project structure

```text
sales_report/
├── data/
│   └── sales.csv
├── examples/
│   ├── sales_report.xlsx
│   └── csv_reports/
│       └── excluded_sales.csv
├── source/
│   ├── main.py
│   └── modules/
│       ├── report_generator.py
│       ├── utilities.py
│       └── workbook_formatter.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Tools used

- **pandas:** Data preparation, aggregation, and export.
- **openpyxl:** Excel workbook formatting.
- **pathlib:** File and folder paths.

## Scope and limitations

The current version accepts CSV input. Reports are generated snapshots; rerun the program after changing the source data.

The sample has no customer, date, or order identifier, so the report does not calculate customer rankings, time trends, or average order value. Revenue is not profit: costs, taxes, and discounts are not modeled.