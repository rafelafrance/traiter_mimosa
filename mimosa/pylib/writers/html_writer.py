"""Write the extracted traits to an html file."""
from collections import namedtuple
from datetime import datetime
from html import escape
from itertools import cycle
from itertools import groupby

from jinja2 import Environment
from jinja2 import FileSystemLoader

COLOR_COUNT = 14
BACKGROUNDS = cycle([f"cc{i}" for i in range(COLOR_COUNT)])
BORDERS = cycle([f"bb{i}" for i in range(COLOR_COUNT)])

Formatted = namedtuple("Formatted", "text traits")
Trait = namedtuple("Trait", "label data")
SortableTrait = namedtuple("SortableTrait", "label start trait")


def write(args, data):
    """Output the parsed data."""

    env = Environment(
        loader=FileSystemLoader("./mimosa/pylib/writers/templates"),
        autoescape=True,
    )

    classes = {}
    formatted = []
    for datum in data:
        formatted.append(
            Formatted(
                format_text(datum, classes),
                format_traits(datum, classes),
            )
        )

    template = env.get_template("html_template.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        file_name=args.in_text.name,
        data=formatted,
    )

    with open(args.out_html, "w") as html_file:
        html_file.write(template)
        html_file.close()


def format_text(datum, classes) -> str:
    """Wrap traits in the text with spans that can be formatted with CSS."""
    frags = []
    prev = 0

    for trait in datum.traits:
        start = trait["start"]
        end = trait["end"]

        if prev < start:
            frags.append(escape(datum.text[prev:start]))

        label = get_label(trait)
        cls = get_class(label, classes)

        frags.append(f'<span class="{cls}" title="">')
        frags.append(escape(datum.text[start:end]))
        frags.append("</span>")
        prev = end

    if len(datum.text) > prev:
        frags.append(escape(datum.text[prev:]))

    return "".join(frags)


def format_traits(datum, classes) -> list[namedtuple]:
    """Format the traits for output."""
    SKIPS = {"start", "end", "trait", "part", "subpart"}
    traits = []

    sortable = []
    for trait in datum.traits:
        label = get_label(trait)
        sortable.append(SortableTrait(label, trait["start"], trait))

    sortable = sorted(sortable)

    for label, grouped in groupby(sortable, key=lambda x: x.label):
        cls = get_class(label, classes)
        label = f'<span class="{cls}">{label}</span>'
        trait_list = []
        for trait in grouped:
            trait_list.append(
                ", ".join(
                    f"{k}:&nbsp;{v}" for k, v in trait.trait.items() if k not in SKIPS
                )
            )

        traits.append(Trait(label, "<br/>".join(trait_list)))

    return traits


def get_label(trait):
    """Format the trait's label."""
    parts = []
    if trait.get("part"):
        parts.append(trait["part"])

    if trait.get("subpart"):
        parts.append(trait["subpart"])

    parts.append(trait["trait"])

    label = " ".join(parts)

    return label


def get_class(label, classes):
    """Get the classes for the label."""
    if label not in classes:
        classes[label] = next(BACKGROUNDS)
    return classes[label]
