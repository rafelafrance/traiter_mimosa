"""Write the extracted traits to an html file."""
import collections
import html
import itertools
from datetime import datetime

import jinja2
from tqdm import tqdm

from .. import consts
from ..patterns import term_patterns

COLOR_COUNT = 14
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])
BORDERS = itertools.cycle([f"bb{i}" for i in range(COLOR_COUNT)])

TITLE_SKIPS = ["start", "end"]
TRAIT_SKIPS = TITLE_SKIPS + ["part", "subpart", "trait"]

ALL_PARTS = term_patterns.PARTS_SET.copy() | {"subpart"}

Formatted = collections.namedtuple("Formatted", "text traits debug")
Trait = collections.namedtuple("Trait", "label data")
SortableTrait = collections.namedtuple("SortableTrait", "label start trait title")


def write(args, sentences):
    """Output the parsed data."""

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            f"{consts.ROOT_DIR}/mimosa/pylib/writers/templates"
        ),
        autoescape=True,
    )

    classes = {}
    formatted = []
    for sentence_data in tqdm(sentences):
        text = format_text(sentence_data, classes)
        traits = format_traits(sentence_data, classes)
        cls = "debug" if sentence_data.reject else "real"
        formatted.append(Formatted(text, traits, cls))

    template = env.get_template("html_template.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        file_name=args.in_text.name,
        data=formatted,
    )

    with open(args.out_html, "w") as html_file:
        html_file.write(template)
        html_file.close()


def format_text(sentence_data, classes) -> str:
    """Wrap traits in the text with spans that can be formatted with CSS."""
    frags = []
    prev = 0

    for trait in sentence_data.traits:
        start = trait["start"]
        end = trait["end"]

        if prev < start:
            frags.append(html.escape(sentence_data.text[prev:start]))

        label = get_label(trait)
        cls = get_class(label, classes)

        title = ", ".join(
            f"{k}:&nbsp;{v}" for k, v in trait.items() if k not in TITLE_SKIPS
        )

        frags.append(f'<span class="{cls}" title="{title}">')
        frags.append(html.escape(sentence_data.text[start:end]))
        frags.append("</span>")
        prev = end

    if len(sentence_data.text) > prev:
        frags.append(html.escape(sentence_data.text[prev:]))

    text = "".join(frags)
    return text


def format_traits(sentence_data, classes) -> list[collections.namedtuple]:
    """Format the traits for output."""
    traits = []

    sortable = []
    for trait in sentence_data.traits:
        label = get_label(trait)
        title = sentence_data.text[trait["start"] : trait["end"]]
        sortable.append(SortableTrait(label, trait["start"], trait, title))

    sortable = sorted(sortable)

    for label, grouped in itertools.groupby(sortable, key=lambda x: x.label):
        cls = get_class(label, classes)
        label = f'<span class="{cls}">{label}</span>'
        trait_list = []
        for trait in grouped:
            trait_list.append(
                ", ".join(
                    f'<span title="{trait.title}">{k}:&nbsp;{v}</span>'
                    for k, v in trait.trait.items()
                    if k not in TRAIT_SKIPS
                )
            )

        traits.append(Trait(label, "<br/>".join(trait_list)))

    return traits


def get_label(trait):
    """Format the trait's label."""
    keys = set(trait.keys())
    part_key = list(keys & term_patterns.PARTS_SET)
    part = trait[part_key[0]] if part_key else ""
    part = "_".join(part) if isinstance(part, list) else part
    subpart = trait["subpart"] if trait.get("subpart") else ""
    trait = trait["trait"] if trait["trait"] not in ALL_PARTS else ""
    label = "_".join([p for p in [part, subpart, trait] if p])
    return label


def get_class(label, classes):
    """Get the classes for the label."""
    if label not in classes:
        classes[label] = next(BACKGROUNDS)
    return classes[label]
