"""Write the extracted traits to an html file."""
from datetime import datetime

from jinja2 import Environment
from jinja2 import FileSystemLoader


def write(args, data):
    """Output the parsed data."""

    env = Environment(
        loader=FileSystemLoader("./mimosa/pylib/writers/templates"),
        autoescape=True,
    )

    template = env.get_template("html_template.html").render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        file_name=args.in_text.name,
        data=data,
    )

    with open(args.out_html, "w") as html_file:
        html_file.write(template)
        html_file.close()
