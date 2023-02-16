from collections import defaultdict
from collections import namedtuple

from plants.pylib import sentence_pipeline
from plants.pylib.patterns import term_patterns
from tqdm import tqdm

from . import pipeline


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
                    countdown = args.taxon_distance
                elif trait["trait"] not in term_patterns.TAXA:
                    taxon_traits[taxon].append(trait)
                    trait["taxon"] = taxon

                traits.append(trait)

            traits_in_text.append(TraitsInText(text=sent.text, traits=traits))

            countdown -= 1
            if countdown <= 0:
                taxon = "Unknown"

    taxon_traits = adjust_taxa(taxon_traits)
    traits_by_taxon = [TraitsByTaxon(k, v) for k, v in taxon_traits.items()]

    return traits_in_text, traits_by_taxon


def adjust_taxa(taxon_traits):
    taxon_traits = split_multi_taxa(taxon_traits)
    taxon_traits = dict(sorted(taxon_traits.items(), key=lambda t: t[0]))
    return taxon_traits


def split_multi_taxa(taxon_traits):
    new_traits = defaultdict(list)
    for taxa, traits in taxon_traits.items():
        if isinstance(taxa, tuple):
            for name in taxa:
                new_traits[name] += traits
        else:
            new_traits[taxa] += traits
    return new_traits
