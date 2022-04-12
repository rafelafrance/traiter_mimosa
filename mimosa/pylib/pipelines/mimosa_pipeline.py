"""Create a trait pipeline."""
import spacy
from traiter import tokenizer_util
from traiter.patterns import matcher_patterns
from traiter.pipes.add_traits_pipe import ADD_TRAITS
from traiter.pipes.delete_traits_pipe import DELETE_TRAITS
from traiter.pipes.dependency_pipe import DEPENDENCY
from traiter.pipes.sentence_pipe import SENTENCE
from traiter.pipes.simple_traits_pipe import SIMPLE_TRAITS

from ..patterns import color_patterns
from ..patterns import count_patterns
from ..patterns import delete_trait_utils
from ..patterns import location_linker_patterns
from ..patterns import margin_patterns
from ..patterns import part_linker_patterns
from ..patterns import part_location_patterns
from ..patterns import part_patterns
from ..patterns import range_patterns
from ..patterns import sex_linker_patterns
from ..patterns import shape_patterns
from ..patterns import size_patterns
from ..patterns import subpart_linker_patterns
from ..patterns import subpart_patterns
from ..patterns import taxon_linker_patterns
from ..patterns import taxon_patterns
from ..patterns import terms_utils

# from traiter.pipes import debug_pipes


def pipeline():
    nlp = spacy.load("en_core_web_sm", exclude=["ner"])
    tokenizer_util.append_tokenizer_regexes(nlp)
    tokenizer_util.append_abbrevs(nlp, terms_utils.ABBREVS)

    term_ruler = nlp.add_pipe(
        "entity_ruler",
        name="term_ruler",
        config={"phrase_matcher_attr": "LOWER"},
        before="parser",
    )
    term_ruler.add_patterns(terms_utils.TERMS.for_entity_ruler())

    nlp.add_pipe(SENTENCE, before="parser")

    nlp.add_pipe(
        ADD_TRAITS,
        name="range_pipe",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    range_patterns.RANGE_LOW,
                    range_patterns.RANGE_MIN_LOW,
                    range_patterns.RANGE_LOW_HIGH,
                    range_patterns.RANGE_LOW_MAX,
                    range_patterns.RANGE_MIN_LOW_HIGH,
                    range_patterns.RANGE_MIN_LOW_MAX,
                    range_patterns.RANGE_LOW_HIGH_MAX,
                    range_patterns.RANGE_MIN_LOW_HIGH_MAX,
                    range_patterns.NOT_A_RANGE,
                ]
            )
        },
    )
    nlp.add_pipe("merge_entities")

    # Smaller traits that are part of larger traits
    nlp.add_pipe(
        ADD_TRAITS,
        name="part_traits",
        config={
            "patterns": matcher_patterns.as_dicts(
                [part_patterns.PART, subpart_patterns.SUBPART]
            )
        },
    )

    nlp.add_pipe(SIMPLE_TRAITS, config={"replace": terms_utils.REPLACE})

    nlp.add_pipe(
        ADD_TRAITS,
        name="numeric_traits",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    size_patterns.SIZE,
                    size_patterns.SIZE_HIGH_ONLY,
                    size_patterns.SIZE_DOUBLE_DIM,
                    size_patterns.NOT_A_SIZE,
                    part_location_patterns.PART_AS_DISTANCE,
                    count_patterns.COUNT,
                    count_patterns.COUNT_WORD,
                    count_patterns.NOT_A_COUNT,
                ]
            )
        },
    )

    nlp.add_pipe(
        ADD_TRAITS,
        name="group_traits",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    color_patterns.COLOR,
                    margin_patterns.MARGIN_SHAPE,
                    shape_patterns.N_SHAPE,
                    shape_patterns.SHAPE,
                    part_location_patterns.PART_AS_LOCATION,
                    part_location_patterns.SUBPART_AS_LOCATION,
                    taxon_patterns.TAXON,
                ]
            )
        },
    )

    nlp.add_pipe(DELETE_TRAITS, config={"delete": delete_trait_utils.PARTIAL_TRAITS})

    nlp.add_pipe(
        DEPENDENCY,
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    location_linker_patterns.LOCATION_LINKER,
                    part_linker_patterns.PART_LINKER,
                    sex_linker_patterns.SEX_LINKER,
                    subpart_linker_patterns.SUBPART_LINKER,
                    taxon_linker_patterns.TAXON_LINKER,
                ]
            )
        },
    )

    # debug_pipes.tokens(nlp)

    nlp.add_pipe(
        DELETE_TRAITS,
        name="forget_unlinked",
        config={"delete_when": delete_trait_utils.DELETE_WHEN},
    )

    return nlp
