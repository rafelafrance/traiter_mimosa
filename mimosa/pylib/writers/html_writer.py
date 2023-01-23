from plants.writers.html_writer import HtmlWriter as BaseWriter
from plants.writers.html_writer import HtmlWriterRow
from tqdm import tqdm

from .. import const
from ..patterns import term_patterns

TITLE_SKIPS = ["start", "end", "dimensions"]
TRAIT_SKIPS = TITLE_SKIPS + ["trait"] + term_patterns.PARTS + term_patterns.SUBPARTS


class HtmlWriter(BaseWriter):
    def __init__(self, out_path):
        super().__init__(
            template_dir=f"{const.ROOT_DIR}/mimosa/pylib/writers/templates",
            out_path=out_path,
        )

    def write(self, mimosa_rows, in_file_name=""):
        for mimosa_row in tqdm(mimosa_rows):
            text = self.format_text(mimosa_row)
            traits = self.format_traits(mimosa_row)
            self.formatted.append(
                HtmlWriterRow(
                    formatted_text=text,
                    formatted_traits=traits,
                )
            )

        self.write_template(in_file_name)
