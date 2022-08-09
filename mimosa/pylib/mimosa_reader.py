from collections import defaultdict
from collections import namedtuple

from tqdm import tqdm

from . import mimosa_pipeline
from . import sentence_pipeline
from .patterns import term_patterns


SentenceTraits = namedtuple("SentenceTraits", "text traits")


def read(args):
    with open(args.in_text, encoding="utf_8") as in_file:
        lines = in_file.readlines()

    if args.limit:
        lines = lines[: args.limit]

    nlp = mimosa_pipeline.pipeline()
    sent_nlp = sentence_pipeline.pipeline()

    all_traits = []

    taxa = defaultdict(list)
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
                    countdown = 10
                elif trait["trait"] not in term_patterns.TAXA:
                    taxa[taxon].append(trait)
                    trait["taxon"] = taxon

                traits.append(trait)

            all_traits.append(SentenceTraits(text=sent.text, traits=traits))

            countdown -= 1
            if countdown <= 0:
                taxon = "Unknown"

    return all_traits, taxa
