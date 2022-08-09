from itertools import groupby

from . import writer_utils
from ..patterns import term_patterns

SKIP_FIELD = term_patterns.PARTS + term_patterns.SUBPARTS
SKIP_FIELD += """ start end trait dimensions taxon """.split()


def write(args, taxa):
    print(args)
    for taxon, all_traits in taxa.items():
        print(f"\n{'=' * 80}")
        print(f"{taxon=}")

        all_traits = [
            t for t in all_traits if t["trait"] not in writer_utils.DO_NOT_SHOW
        ]

        for trait in all_traits:
            trait["trait"] = writer_utils.get_label(trait)

        all_traits = sorted(all_traits, key=lambda t: t["trait"])

        for name, traits in groupby(all_traits, key=lambda t: t["trait"]):
            for i, trait in enumerate(traits):

                filtered = [(k, v) for k, v in trait.items() if k not in SKIP_FIELD]
                for key, value in filtered:

                    if name.endswith(key):
                        col = name
                    elif name.endswith("_size"):
                        col = name.removesuffix("size") + key
                    elif name.endswith("_missing"):
                        col = name
                    else:
                        col = name + "_" + key

                    print(f"{col}: {value}")
