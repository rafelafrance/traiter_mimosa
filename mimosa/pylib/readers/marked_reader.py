"""The algorithms for linking traits to the taxon they describe can get involved.
This reader looks for treatment header for the taxon. A header in this case, will
be a line containing "====". The next taxon is grabbed as the one to associate with
the traits. We need to be careful that page numbers to not interfere with this process.
"""
import re
from enum import auto
from enum import Enum

from plants.pylib.patterns import term_patterns as terms
from tqdm import tqdm

from .base_reader import BaseReader


HEADER = re.compile(r"^====$")


class States(Enum):
    TAXON = auto()
    SEP = auto()


class MarkedReader(BaseReader):
    def read(self):
        taxon = "Unknown"
        state = States.TAXON

        for ln in tqdm(self.lines):
            ln = ln.strip()
            sent_doc = self.sent_nlp(ln)
            for sent in sent_doc.sents:
                doc = self.nlp(sent.text)
                traits = []
                if HEADER.match(sent.text):
                    state = States.SEP
                for ent in doc.ents:
                    trait = ent._.data
                    trait["start"] += sent.start_char
                    trait["end"] += sent.start_char

                    if state == States.SEP and trait["trait"] in terms.TAXA:
                        taxon = trait["taxon"]
                        state = States.TAXON
                    elif state == States.TAXON and trait["trait"] not in terms.TAXA:
                        trait["taxon"] = taxon
                        self.taxon_traits[taxon].append(trait)

                    traits.append(trait)

                self.text_traits.append((sent.text, traits))

        return self.finish()
