from io import StringIO
import json
from typing import Optional


from arche.figures import tables
from arche.quality_estimation_algorithm import generate_quality_estimation
from arche.readers.items import CloudItems
from arche.readers.schema import Schema
from arche.report import Report
import arche.rules.coverage as coverage_rules
import arche.rules.duplicates as duplicate_rules
import arche.rules.json_schema as schema_rules
from arche.rules.others import garbage_symbols
import arche.rules.price as price_rules
from arche.tools import api
from arche.tools.s3 import upload_str_stream
import IPython
import pandas as pd
import plotly.io as pio


class DataQualityReport:
    def __init__(
        self,
        items: CloudItems,
        schema: Schema,
        report: Report,
        bucket: Optional[str] = None,
    ):
        """Print a data quality report

        Args:
            items: an Items instance containing items data
            schema: a schema dict
        """
        self.schema = schema
        self.report = report
        self.figures = []
        self.appendix = self.create_appendix(self.schema.raw)
        self.create_figures(items)
        self.plot_to_notebook()

        if bucket:
            self.save_report_to_bucket(
                project_id=items.key.split("/")[0],
                spider=items.job.metadata.get("spider"),
                bucket=bucket,
            )

    def create_figures(self, items: CloudItems):
        name_url_dups = self.report.results.get(
            "Duplicates By **name_field, product_url_field** Tags",
            duplicate_rules.find_by_name_url(items.df, self.schema.tags),
        )

        uniques = self.report.results.get(
            "Duplicates By **unique** Tag",
            duplicate_rules.find_by_unique(items.df, self.schema.tags),
        )

        price_was_now_result = price_rules.compare_was_now(items.df, self.schema.tags)
        no_of_price_warns = price_was_now_result.err_items_count
        no_of_checked_price_items = price_was_now_result.items_count

        crawlera_user = api.get_crawlera_user(items.job)

        validation_errors = self.report.results.get(
            "JSON Schema Validation",
            schema_rules.validate(
                self.schema.raw, raw_items=items.raw, keys=items.df.index, fast=False
            ),
        ).get_errors_count()

        garbage_symbols_result = self.report.results.get(
            "Garbage Symbols", garbage_symbols(items.df)
        )

        quality_estimation, field_accuracy = generate_quality_estimation(
            items.job,
            crawlera_user,
            validation_errors,
            name_url_dups.err_items_count,
            name_url_dups.items_count,
            uniques.err_items_count,
            uniques.items_count,
            no_of_price_warns,
            no_of_checked_price_items,
            tested=True,
            garbage_symbols=garbage_symbols_result,
        )

        self.score_table(quality_estimation, field_accuracy)
        self.job_summary_table(items.job)
        self.rules_summary_table(
            items.df,
            validation_errors,
            self.schema.tags.get("name_field", ""),
            self.schema.tags.get("product_url_field", ""),
            name_url_dups.items_count,
            name_url_dups.err_items_count,
            self.schema.tags.get("unique", []),
            uniques.items_count,
            uniques.err_items_count,
            self.schema.tags.get("product_price_field", ""),
            self.schema.tags.get("product_price_was_field", ""),
            no_of_checked_price_items,
            no_of_price_warns,
            garbage_symbols=garbage_symbols_result,
        )
        self.scraped_fields_coverage(items.df)
        self.coverage_by_categories(items.df, self.schema.tags)

    def plot_to_notebook(self) -> None:
        IPython.display.clear_output()
        for fig in self.figures:
            pio.show(fig)

    def plot_html_to_stream(self) -> StringIO:
        output = StringIO()
        for fig in self.figures:
            output.write(pio.to_html(fig, include_plotlyjs="cdn", full_html=False))
            output.write("\n")
        output.write(self.appendix)
        return output

    def create_appendix(self, schema):
        output = StringIO()
        output.write("<h1>Appendix</h1>\n")
        output.write("<h2>Appendix A: The JSON Schema</h2>\n")
        output.write("<pre>")
        output.write(json.dumps(schema, ensure_ascii=False, indent=2))
        output.write("</pre>")
        contents = output.getvalue()
        output.close()
        return contents

    def save_report_to_bucket(self, project_id, spider, bucket):
        report_stream = self.plot_html_to_stream()
        path = f"reports/dqr/{project_id}/Data Quality Report - {spider}.html"
        self.url = upload_str_stream(bucket, path, report_stream)
        report_stream.close()
        print(self.url)

    def score_table(self, quality_estimation, field_accuracy):
        score_table = tables.score_table(quality_estimation, field_accuracy)
        self.figures.append(score_table)

    def job_summary_table(self, job):
        summary_table = tables.job_summary_table(job)
        self.figures.append(summary_table)

    def rules_summary_table(
        self,
        df,
        no_of_validation_warnings,
        name_field,
        url_field,
        no_of_checked_duplicated_items,
        no_of_duplicated_items,
        unique,
        no_of_checked_skus,
        no_of_duplicated_skus,
        price_field,
        price_was_field,
        no_of_checked_price_items,
        no_of_price_warns,
        **kwargs,
    ):

        table = tables.rules_summary_table(
            df,
            no_of_validation_warnings,
            name_field,
            url_field,
            no_of_checked_duplicated_items,
            no_of_duplicated_items,
            unique,
            no_of_checked_skus,
            no_of_duplicated_skus,
            price_field,
            price_was_field,
            no_of_checked_price_items,
            no_of_price_warns,
            **kwargs,
        )
        self.figures.append(table)

    def scraped_fields_coverage(self, df: pd.DataFrame) -> None:
        coverage_res = self.report.results.get(
            "Fields Coverage", coverage_rules.check_fields_coverage(df)
        )
        self.figures.extend(coverage_res.figures)

    def coverage_by_categories(self, df, tags):
        """Make tables which show the number of items per category,
        set up with a category tag

        Args:
            df: a dataframe of items
            tags: a dict of tags
        """
        category_fields = tags.get("category", list())
        product_url_fields = tags.get("product_url_field")

        for category_field in category_fields:
            cat_table = tables.coverage_by_categories(
                category_field, df, product_url_fields
            )
            if cat_table:
                self.figures.append(cat_table)
