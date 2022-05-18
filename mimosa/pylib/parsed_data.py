"""A class to hold data parsed from PDFs."""
import dataclasses


@dataclasses.dataclass
class Datum:
    """A class to hold data parsed from PDFs."""

    text: str = ""
    traits: list[dict] = dataclasses.field(default_factory=list)
    reject: bool = False
