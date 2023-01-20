import collections
import html
import itertools

from plants.writers import html_writer as phtml
from plants.writers import writer_utils as wutils
from tqdm import tqdm

from . import writer_utils
from .. import consts
from ..patterns import term_patterns

TITLE_SKIPS = ["start", "end", "dimensions"]
TRAIT_SKIPS = TITLE_SKIPS + ["trait"] + term_patterns.PARTS + term_patterns.SUBPARTS


def write(args, rows):
    classes = phtml.CssClasses()
    formatted = []

    for raw_traits in tqdm(rows):
        text = format_text(raw_traits, classes)
        traits = format_traits(raw_traits, classes)
        formatted.append(phtml.Formatted(text, traits))

    phtml.write_template(args, consts.ROOT_DIR, "mimosa", formatted)


def format_text(raw_traits, classes) -> str:
    """Wrap traits in the text with spans that can be formatted with CSS."""
    frags = []
    prev = 0

    for trait in raw_traits.traits:
        start = trait["start"]
        end = trait["end"]

        if prev < start:
            frags.append(html.escape(raw_traits.text[prev:start]))

        label = writer_utils.get_label(trait)
        cls = get_class(label, classes)

        title = ", ".join(
            f"{k}:&nbsp;{v}" for k, v in trait.items() if k not in TITLE_SKIPS
        )

        frags.append(f'<span class="{cls}" title="{title}">')
        frags.append(html.escape(raw_traits.text[start:end]))
        frags.append("</span>")
        prev = end

    if len(raw_traits.text) > prev:
        frags.append(html.escape(raw_traits.text[prev:]))

    text = "".join(frags)
    return text


def format_traits(raw_traits, classes) -> list[collections.namedtuple]:
    traits = []

    sortable = []
    for trait in raw_traits.traits:
        label = writer_utils.get_label(trait)
        title = raw_traits.text[trait["start"] : trait["end"]]
        if trait["trait"] not in writer_utils.DO_NOT_SHOW:
            sortable.append(phtml.SortableTrait(label, trait["start"], trait, title))

    sortable = sorted(sortable)

    for label, grouped in itertools.groupby(sortable, key=lambda x: x.label):
        cls = get_class(label, classes)
        label = f'<span class="{cls}">{label}</span>'
        trait_list = []
        for trait in grouped:
            fields = ", ".join(
                f'<span title="{trait.title}">{k}:&nbsp;{v}</span>'
                for k, v in trait.trait.items()
                if k not in TRAIT_SKIPS
            )
            if fields:
                trait_list.append(fields)

        if trait_list:
            traits.append(phtml.Trait(label, "<br/>".join(trait_list)))

    return traits


def get_class(label, classes):
    if label not in classes:
        classes[label] = next(phtml.BACKGROUNDS)
    return classes[label]
