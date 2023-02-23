"""The algorithms for linking traits to the taxon they describe can get involved. This
reader looks for treatment header for the taxon. A header a given regular expression
pattern. The very next taxon is grabbed as the one to associate with the traits.
"""
import sys

from plants.pylib.patterns import term_patterns as terms

from .base_reader import BaseReader


class MarkedReader(BaseReader):
    def __init__(self, args):
        super().__init__(args)
        self.pattern = args.pattern
        self.taxon_distance = args.taxon_distance

    def read(self):
        taxon = "Unknown"
        looking_for_taxon = False
        distance = 0

        for i, ln in enumerate(self.lines, 1):
            ln = ln.strip()
            doc = self.nlp(ln)

            distance += 1
            print(i, distance, looking_for_taxon)
            print(ln[:20])
            if looking_for_taxon and distance > self.taxon_distance:
                sys.exit(f"Could not find a taxon: {i}")

            traits = []

            if ln.find(self.pattern) > -1:
                distance = 0
                looking_for_taxon = True

            for ent in doc.ents:
                trait = ent._.data
                trait["start"] += ent.start_char
                trait["end"] += ent.start_char

                if looking_for_taxon and trait["trait"] in terms.TAXA:
                    taxon = trait["taxon"]
                    looking_for_taxon = False
                    print("=" * 80)
                    print(taxon)

                elif not looking_for_taxon and trait["trait"] not in terms.TAXA:
                    trait["taxon"] = taxon
                    self.taxon_traits[taxon].append(trait)

                traits.append(trait)

            self.text_traits.append((ln, traits))

        return self.finish()
