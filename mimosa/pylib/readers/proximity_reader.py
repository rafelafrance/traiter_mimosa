"""The algorithms for linking traits to the taxon they describe can get involved.
This simple-minded reader associates traits with a taxon by proximity to the nearest
trait mentioned. That is, it will link a trait to the nearest taxon that precedes it
in the text. There is a radius parameter that will stop linking traits and assign the
trait to "Unknown" once the sentence count passes the threshold.
"""
from plants.pylib.patterns import term_patterns
from tqdm import tqdm

from .base_reader import BaseReader


class ProximityReader(BaseReader):
    def __init__(self, args):
        super().__init__(args)
        self.taxon_distance = args.taxon_distance

    def read(self):
        taxon = "Unknown"
        countdown = 0

        for ln in tqdm(self.lines):
            ln = ln.strip()
            sent_doc = self.sent_nlp(ln)
            for sent in sent_doc.sents:
                doc = self.nlp(sent.text)
                traits = []
                for ent in doc.ents:
                    trait = ent._.data
                    trait["start"] += sent.start_char
                    trait["end"] += sent.start_char

                    if trait["trait"] in term_patterns.TAXA:
                        taxon = trait["taxon"]
                        taxon = tuple(taxon) if isinstance(taxon, list) else taxon
                        countdown = self.taxon_distance
                    elif trait["trait"] not in term_patterns.TAXA:
                        trait["taxon"] = taxon
                        self.taxon_traits[taxon].append(trait)

                    traits.append(trait)

                self.text_traits.append((sent.text, traits))

                countdown -= 1
                if countdown <= 0:
                    taxon = "Unknown"

        return self.finish()
