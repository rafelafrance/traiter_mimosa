from plants.writers import csv_writer as base_writer

from ..patterns import term_patterns

SKIP_FIELD = term_patterns.PARTS + term_patterns.SUBPARTS
SKIP_FIELD += """ start end trait dimensions taxon """.split()


class CsvWriter(base_writer.CsvWriter):
    @staticmethod
    def sort_df(df):
        first = """ taxon """.split()

        rest = sorted(c for c in df.columns if c not in first)
        columns = first + rest

        df = df[columns]

        return df

    def format_row(self, row):
        csv_row = {"taxon": row.taxon}

        return self.row_builder(row, csv_row)
