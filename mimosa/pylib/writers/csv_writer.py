from itertools import groupby

import pandas as pd
from tqdm import tqdm

from . import writer_utils
from ..patterns import term_patterns

SKIP_FIELD = term_patterns.PARTS + term_patterns.SUBPARTS
SKIP_FIELD += """ start end trait dimensions taxon """.split()


def write(args, taxa):
    csv_rows = parse_taxa(taxa)

    df = pd.DataFrame(csv_rows).fillna("")
    df = df.set_index("taxon")
    df.to_csv(args.out_csv)
    df.T.to_csv(args.out_csv.with_stem(args.out_csv.stem + "_T"))


def parse_taxa(taxa):
    csv_rows = []
    for taxon, all_traits in tqdm(taxa.items()):
        row = {"taxon": taxon}

        all_traits = [
            t for t in all_traits if t["trait"] not in writer_utils.DO_NOT_SHOW
        ]

        for trait in all_traits:
            trait["trait"] = writer_utils.get_label(trait)

        all_traits = sorted(all_traits, key=lambda t: t["trait"])

        for trait_name, traits in groupby(all_traits, key=lambda t: t["trait"]):

            for i, trait in enumerate(traits, 1):

                filtered = [(k, v) for k, v in trait.items() if k not in SKIP_FIELD]
                for field_name, value in filtered:

                    col_name = column_name(trait_name, field_name)

                    row[f"{col_name}_{i}"] = value

        csv_rows.append(row)
    return csv_rows


def column_name(trait_name, field_name):
    if trait_name.endswith(field_name):
        col_name = trait_name
    elif trait_name.endswith("_size"):
        col_name = trait_name.removesuffix("size") + field_name
    elif trait_name.endswith("_missing"):
        col_name = trait_name
    else:
        col_name = trait_name + "_" + field_name
    return col_name
