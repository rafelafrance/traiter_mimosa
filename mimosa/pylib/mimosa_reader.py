from collections import defaultdict
from collections import namedtuple

from plants import sentence_pipeline
from tqdm import tqdm

from . import pipeline
from .patterns import term_patterns


TraitsInText = namedtuple("TraitsInText", "text traits")
TraitsByTaxon = namedtuple("TraitsByTaxon", "taxon traits")


def read(args):
    with open(args.in_text, encoding="utf_8") as in_file:
        lines = in_file.readlines()

    if args.limit:
        lines = lines[: args.limit]

    nlp = pipeline.pipeline()
    sent_nlp = sentence_pipeline.pipeline()

    traits_in_text = []

    taxon_traits = defaultdict(list)

    taxon = "Unknown"
    countdown = 0

    for ln in tqdm(lines):
        ln = ln.strip()
        sent_doc = sent_nlp(ln)
        for sent in sent_doc.sents:
            doc = nlp(sent.text)
            traits = []
            for ent in doc.ents:
                trait = ent._.data
                trait["start"] += sent.start_char
                trait["end"] += sent.start_char

                if trait["trait"] in term_patterns.TAXA:
                    taxon = trait["taxon"]
                    taxon = tuple(taxon) if isinstance(taxon, list) else taxon
                    countdown = 10
                elif trait["trait"] not in term_patterns.TAXA:
                    taxon_traits[taxon].append(trait)
                    trait["taxon"] = taxon

                traits.append(trait)

            traits_in_text.append(TraitsInText(text=sent.text, traits=traits))

            countdown -= 1
            if countdown <= 0:
                taxon = "Unknown"

    traits_by_taxon = [TraitsByTaxon(k, v) for k, v in taxon_traits.items()]

    return traits_in_text, traits_by_taxon
