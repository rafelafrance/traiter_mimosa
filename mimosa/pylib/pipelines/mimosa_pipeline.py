"""Create a trait pipeline."""
import spacy
from traiter.patterns.matcher_patterns import add_ruler_patterns
from traiter.patterns.matcher_patterns import as_dicts
from traiter.patterns.matcher_patterns import patterns_to_dispatch
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.cleanup import CLEANUP
from traiter.pipes.dependency import DEPENDENCY
from traiter.pipes.sentence import SENTENCE
from traiter.pipes.simple_entity_data import SIMPLE_ENTITY_DATA
from traiter.pipes.update_entity_data import UPDATE_ENTITY_DATA
from traiter.tokenizer_util import append_abbrevs
from traiter.tokenizer_util import append_tokenizer_regexes

from .. import consts
from ..patterns.color import COLOR
from ..patterns.count import COUNT
from ..patterns.count import COUNT_WORD
from ..patterns.count import NOT_A_COUNT
from ..patterns.location_linker import LOCATION_LINKER
from ..patterns.margin import MARGIN_SHAPE
from ..patterns.part_linker import PART_LINKER
from ..patterns.part_location import PART_AS_LOCATION
from ..patterns.part_location import SUBPART_AS_LOCATION
from ..patterns.range import NOT_A_RANGE
from ..patterns.range import RANGE_LOW
from ..patterns.range import RANGE_LOW_HIGH
from ..patterns.range import RANGE_LOW_HIGH_MAX
from ..patterns.range import RANGE_LOW_MAX
from ..patterns.range import RANGE_MIN_LOW
from ..patterns.range import RANGE_MIN_LOW_HIGH
from ..patterns.range import RANGE_MIN_LOW_HIGH_MAX
from ..patterns.range import RANGE_MIN_LOW_MAX
from ..patterns.sex_linker import SEX_LINKER
from ..patterns.shape import N_SHAPE
from ..patterns.shape import SHAPE
from ..patterns.size import NOT_A_SIZE
from ..patterns.size import SIZE
from ..patterns.size import SIZE_DOUBLE_DIM
from ..patterns.size import SIZE_HIGH_ONLY
from ..patterns.subpart_linker import SUBPART_LINKER
from ..patterns.taxon_patterns import TAXON

# from traiter.pipes.debug import DEBUG_ENTITIES, DEBUG_TOKENS

SIMPLE_DATA = [TAXON]

TERM_RULES = [
    RANGE_LOW,
    RANGE_MIN_LOW,
    RANGE_LOW_HIGH,
    RANGE_LOW_MAX,
    RANGE_MIN_LOW_HIGH,
    RANGE_MIN_LOW_MAX,
    RANGE_LOW_HIGH_MAX,
    RANGE_MIN_LOW_HIGH_MAX,
    NOT_A_RANGE,
]

ADD_DATA = [COLOR, MARGIN_SHAPE, N_SHAPE, SHAPE, PART_AS_LOCATION, SUBPART_AS_LOCATION]

UPDATE_DATA = [
    COUNT,
    COUNT_WORD,
    NOT_A_COUNT,
    SIZE,
    SIZE_HIGH_ONLY,
    SIZE_DOUBLE_DIM,
    NOT_A_SIZE,
]

LINKERS = [LOCATION_LINKER, PART_LINKER, SEX_LINKER, SUBPART_LINKER]


def pipeline():
    """Create a pipeline for extracting traits."""
    nlp = spacy.load("en_core_web_sm", exclude=["ner"])
    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, consts.ABBREVS)

    # Add a pipe to identify phrases and patterns as base-level traits.
    config = {"phrase_matcher_attr": "LOWER"}
    term_ruler = nlp.add_pipe(
        "entity_ruler", name="term_ruler", config=config, before="parser"
    )
    term_ruler.add_patterns(consts.TERMS.for_entity_ruler())
    add_ruler_patterns(term_ruler, TERM_RULES)

    nlp.add_pipe(SENTENCE, before="parser")

    config = {"overwrite_ents": True}
    match_ruler = nlp.add_pipe("entity_ruler", name="simple_ruler", config=config)
    add_ruler_patterns(match_ruler, SIMPLE_DATA)

    nlp.add_pipe("merge_entities", name="term_merger")
    nlp.add_pipe(
        SIMPLE_ENTITY_DATA, after="term_merger", config={"replace": consts.REPLACE}
    )

    config = {"patterns": as_dicts(UPDATE_DATA)}
    nlp.add_pipe(UPDATE_ENTITY_DATA, name="update_entities", config=config)

    # Add a pipe to group tokens into larger traits
    config = {"overwrite_ents": True}
    match_ruler = nlp.add_pipe("entity_ruler", name="match_ruler", config=config)
    add_ruler_patterns(match_ruler, ADD_DATA)

    nlp.add_pipe(ADD_ENTITY_DATA, config={"dispatch": patterns_to_dispatch(ADD_DATA)})

    nlp.add_pipe(CLEANUP, config={"forget": consts.FORGET})

    # nlp.add_pipe(DEBUG_TOKENS, config={'message': ''})
    # nlp.add_pipe(DEBUG_ENTITIES, config={'message': ''})

    config = {"patterns": as_dicts(LINKERS)}
    nlp.add_pipe(DEPENDENCY, name="part_linker", config=config)

    return nlp
