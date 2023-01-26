from dataclasses import dataclass

from plants.patterns import term_patterns
from plants.writers.html_writer import HtmlWriter as BaseWriter
from plants.writers.html_writer import HtmlWriterRow as BaseWriterRow
from tqdm import tqdm

from .. import const

TITLE_SKIPS = ["start", "end", "dimensions"]
TRAIT_SKIPS = TITLE_SKIPS + ["trait"] + term_patterns.PARTS + term_patterns.SUBPARTS


@dataclass
class HtmlWriterRow(BaseWriterRow):
    text_id: int


class HtmlWriter(BaseWriter):
    def __init__(self, out_html):
        super().__init__(
            template_dir=f"{const.ROOT_DIR}/mimosa/pylib/writers/templates",
            out_html=out_html,
        )

    def write(self, mimosa_rows, in_file_name=""):
        for i, mimosa_row in tqdm(enumerate(mimosa_rows)):
            text = self.format_text(mimosa_row)
            traits = self.format_traits(mimosa_row)
            self.formatted.append(
                HtmlWriterRow(
                    text_id=i,
                    formatted_text=text,
                    formatted_traits=traits,
                )
            )

        self.write_template(in_file_name)
