"""The algorithms for linking traits to the taxon they describe can get involved. This
reader looks for treatment header for the taxon. A header a given regular expression
pattern. The very next taxon is grabbed as the one to associate with the traits.
"""
import regex
from plants.pylib.patterns import term_patterns as terms
from tqdm import tqdm

from .base_reader import BaseReader


class MarkedReader(BaseReader):
    def __init__(self, args):
        super().__init__(args)
        self.pattern = regex.compile(args.pattern)

    def read(self):
        taxon = "Unknown"
        looking_for_taxon = False

        for ln in tqdm(self.lines):
            sent_doc = self.sent_nlp(ln.strip())

            for sent in sent_doc.sents:
                doc = self.nlp(sent.text)

                traits = []

                if self.pattern.match(sent.text):
                    looking_for_taxon = True

                for ent in doc.ents:
                    trait = ent._.data
                    trait["start"] += sent.start_char
                    trait["end"] += sent.start_char

                    if looking_for_taxon and trait["trait"] in terms.TAXA:
                        taxon = trait["taxon"]
                        looking_for_taxon = False

                    elif not looking_for_taxon and trait["trait"] not in terms.TAXA:
                        trait["taxon"] = taxon
                        self.taxon_traits[taxon].append(trait)

                    traits.append(trait)

                self.text_traits.append((sent.text, traits))

        return self.finish()
