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
from ..patterns import color
from ..patterns import count
from ..patterns import location_linker
from ..patterns import margin
from ..patterns import part_linker
from ..patterns import part_location
from ..patterns import range_
from ..patterns import sex_linker
from ..patterns import shape
from ..patterns import size
from ..patterns import subpart_linker
from ..patterns import taxon_patterns

# from traiter.pipes.debug import DEBUG_TOKENS, DEBUG_ENTITIES

ADD_DATA = [
    color.COLOR,
    margin.MARGIN_SHAPE,
    shape.N_SHAPE,
    shape.SHAPE,
    part_location.PART_AS_LOCATION,
    part_location.SUBPART_AS_LOCATION,
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
            range_.RANGE_LOW,
            range_.RANGE_MIN_LOW,
            range_.RANGE_LOW_HIGH,
            range_.RANGE_LOW_MAX,
            range_.RANGE_MIN_LOW_HIGH,
            range_.RANGE_MIN_LOW_MAX,
            range_.RANGE_LOW_HIGH_MAX,
            range_.RANGE_MIN_LOW_HIGH_MAX,
            range_.NOT_A_RANGE,
        ],
    )

    nlp.add_pipe(SENTENCE, before="parser")

    config = {"overwrite_ents": True}
    match_ruler = nlp.add_pipe("entity_ruler", name="simple_ruler", config=config)
    matcher_patterns.add_ruler_patterns(match_ruler, [taxon_patterns.TAXON])

    nlp.add_pipe("merge_entities", name="term_merger")
    nlp.add_pipe(
        SIMPLE_ENTITY_DATA,
        after="term_merger",
        config={"replace": consts.REPLACE},
    )

    config = {
        "patterns": matcher_patterns.as_dicts(
            [
                size.SIZE,
                size.SIZE_HIGH_ONLY,
                size.SIZE_DOUBLE_DIM,
                size.NOT_A_SIZE,
                part_location.PART_AS_DISTANCE,
            ]
        )
    }
    nlp.add_pipe(MERGE_ENTITY_DATA, name="merge_entities", config=config)

    config = {
        "patterns": matcher_patterns.as_dicts(
            [
                count.COUNT,
                count.COUNT_WORD,
                count.NOT_A_COUNT,
            ]
        )
    }
    nlp.add_pipe(UPDATE_ENTITY_DATA, name="update_entities", config=config)

    # Add a pipe to group tokens into larger traits
    config = {"overwrite_ents": True}
    match_ruler = nlp.add_pipe("entity_ruler", name="match_ruler", config=config)
    matcher_patterns.add_ruler_patterns(match_ruler, ADD_DATA)

    nlp.add_pipe(
        ADD_ENTITY_DATA,
        config={"dispatch": matcher_patterns.patterns_to_dispatch(ADD_DATA)},
    )

    nlp.add_pipe(CLEANUP, config={"forget": consts.FORGET})

    # nlp.add_pipe(DEBUG_TOKENS, config={'message': ''})
    # nlp.add_pipe(DEBUG_ENTITIES, config={'message': ''})

    config = {
        "patterns": matcher_patterns.as_dicts(
            [
                location_linker.LOCATION_LINKER,
                part_linker.PART_LINKER,
                sex_linker.SEX_LINKER,
                subpart_linker.SUBPART_LINKER,
            ]
        )
    }
    nlp.add_pipe(DEPENDENCY, name="part_linker", config=config)

    return nlp
