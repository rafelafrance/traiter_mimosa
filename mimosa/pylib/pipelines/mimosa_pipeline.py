"""Create a trait pipeline."""
import spacy
from traiter import tokenizer_util
from traiter.patterns import matcher_patterns
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.cleanup import CLEANUP
from traiter.pipes.dependency import DEPENDENCY
from traiter.pipes.merge_entity_data import MERGE_ENTITY_DATA
from traiter.pipes.sentence import SENTENCE
from traiter.pipes.simple_entity_data import SIMPLE_ENTITY_DATA
from traiter.pipes.update_entity_data import UPDATE_ENTITY_DATA

from .. import consts
from ..patterns import color_patterns
from ..patterns import count_patterns
from ..patterns import forget_utils
from ..patterns import location_linker_patterns
from ..patterns import margin_patterns
from ..patterns import part_linker_patterns
from ..patterns import part_location_patterns
from ..patterns import range_patterns
from ..patterns import sex_linker_patterns
from ..patterns import shape_patterns
from ..patterns import size_patterns
from ..patterns import subpart_linker_patterns
from ..patterns import taxon_patterns

# from traiter.pipes.debug import DEBUG_TOKENS, DEBUG_ENTITIES

ADD_DATA = [
    color_patterns.COLOR,
    margin_patterns.MARGIN_SHAPE,
    shape_patterns.N_SHAPE,
    shape_patterns.SHAPE,
    part_location_patterns.PART_AS_LOCATION,
    part_location_patterns.SUBPART_AS_LOCATION,
]


def pipeline():
    """Create a pipeline for extracting traits."""
    nlp = spacy.load("en_core_web_sm", exclude=["ner"])
    tokenizer_util.append_tokenizer_regexes(nlp)
    tokenizer_util.append_abbrevs(nlp, consts.ABBREVS)

    # Add a pipe to identify phrases and patterns as base-level traits.
    config = {"phrase_matcher_attr": "LOWER"}
    term_ruler = nlp.add_pipe(
        "entity_ruler", name="term_ruler", config=config, before="parser"
    )
    term_ruler.add_patterns(consts.TERMS.for_entity_ruler())
    matcher_patterns.add_ruler_patterns(
        term_ruler,
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
        ],
    )

    nlp.add_pipe(SENTENCE, before="parser")

    config = {"overwrite_ents": True}
    match_ruler = nlp.add_pipe("entity_ruler", name="simple_ruler", config=config)
    matcher_patterns.add_ruler_patterns(
        match_ruler,
        [
            taxon_patterns.SPECIES,
            taxon_patterns.SUBSPECIES,
            taxon_patterns.VARIANT,
            taxon_patterns.FAMILY,
            taxon_patterns.TRIBE,
            taxon_patterns.SUBTRIBE,
            taxon_patterns.GENUS,
            taxon_patterns.SECTION,
            taxon_patterns.SUBSECTION,
            taxon_patterns.SERIES,
            taxon_patterns.SUBSERIES,
        ],
    )

    nlp.add_pipe("merge_entities", name="term_merger")
    nlp.add_pipe(
        SIMPLE_ENTITY_DATA,
        after="term_merger",
        config={"replace": consts.REPLACE},
    )

    nlp.add_pipe(
        MERGE_ENTITY_DATA,
        name="merge_entities",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    size_patterns.SIZE,
                    size_patterns.SIZE_HIGH_ONLY,
                    size_patterns.SIZE_DOUBLE_DIM,
                    size_patterns.NOT_A_SIZE,
                    part_location_patterns.PART_AS_DISTANCE,
                ]
            )
        },
    )

    nlp.add_pipe(
        UPDATE_ENTITY_DATA,
        name="update_entities",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    count_patterns.COUNT,
                    count_patterns.COUNT_WORD,
                    count_patterns.NOT_A_COUNT,
                ]
            )
        },
    )

    # Add a pipe to group tokens into larger traits
    config = {"overwrite_ents": True}
    match_ruler = nlp.add_pipe("entity_ruler", name="match_ruler", config=config)
    matcher_patterns.add_ruler_patterns(match_ruler, ADD_DATA)

    nlp.add_pipe(
        ADD_ENTITY_DATA,
        config={"dispatch": matcher_patterns.patterns_to_dispatch(ADD_DATA)},
    )

    nlp.add_pipe(CLEANUP, config={"forget": forget_utils.FORGET})

    # nlp.add_pipe(DEBUG_TOKENS, config={'message': ''})
    # nlp.add_pipe(DEBUG_ENTITIES, config={'message': ''})

    nlp.add_pipe(
        DEPENDENCY,
        name="part_linker",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    location_linker_patterns.LOCATION_LINKER,
                    part_linker_patterns.PART_LINKER,
                    sex_linker_patterns.SEX_LINKER,
                    subpart_linker_patterns.SUBPART_LINKER,
                ]
            )
        },
    )

    nlp.add_pipe(
        CLEANUP,
        name="forget_unlinked",
        config={"forget_when": forget_utils.FORGET_WHEN},
    )

    return nlp
