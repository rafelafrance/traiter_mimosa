"""Get mimosa taxon notations."""
import regex as re
from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

LEVEL_LOWER = """ species subspecies variety subvariety form subform """.split()

ON_TAXON_MATCH = "mimosa.taxon.v1"

M_DOT = r"^[A-Z]\.?$"
M_DOT_RE = re.compile(M_DOT)


TAXON = MatcherPatterns(
    "taxon",
    on_match=ON_TAXON_MATCH,
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "auth": {"POS": "PROPN"},
        "maybe": {"POS": "NOUN"},
        "taxon": {"ENT_TYPE": "plant_taxon"},
        "level": {"ENT_TYPE": "level"},
        "word": {"LOWER": {"REGEX": r"^[a-z-]+$"}},
        "M.": {"TEXT": {"REGEX": M_DOT}},
    },
    patterns=[
        "M.? taxon+ (? auth* )?",
        "M.? taxon+ (? auth+ maybe auth+ )?",
        "M.? taxon+ (? auth* )?             level .? word",
        "M.? taxon+ (? auth+ maybe auth+ )? level .? word",
        "level .? taxon+",
        "taxon+",
        "M.? taxon level .? word",
    ],
)


@registry.misc(ON_TAXON_MATCH)
def on_taxon_match(ent):
    auth = []
    used_levels = []
    taxa = []
    is_level = ""

    for token in ent:
        if token._.cached_label == "level":
            taxa.append(token.lower_)
            is_level = token.lower_
            ent._.data["level"] = term_patterns.REPLACE.get(token.lower_, token.lower_)
        elif is_level:
            if ent._.data["level"] in LEVEL_LOWER:
                taxa.append(token.lower_)
            else:
                taxa.append(token.text.title())
            is_level = ""

        elif M_DOT_RE.match(token.text):
            taxa.append(token.text)
            used_levels.append("genus")

        elif token._.cached_label == "plant_taxon":
            levels = term_patterns.LEVELS.get(token.lower_, ["unknown"])

            # Find the highest unused taxon level
            for level in levels:
                if level not in used_levels:
                    used_levels.append(level)
                    ent._.data["level"] = level
                    if level in LEVEL_LOWER:
                        taxa.append(token.lower_)
                    else:
                        taxa.append(token.text.title())
                    break
            else:
                taxa.append(token.text)

        elif token.pos_ in ["PROPN", "NOUN"]:
            auth.append(token.text)

    if auth:
        ent._.data["authority"] = " ".join(auth)

    ent._.data["taxon"] = " ".join(taxa)
