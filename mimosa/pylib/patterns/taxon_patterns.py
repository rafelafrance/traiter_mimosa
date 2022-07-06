"""Get mimosa taxon notations."""
import regex as re
from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns
from .. import consts

ON_TAXON_MATCH = "mimosa.taxon.v1"

LEVEL_LOWER = """ species subspecies variety subvariety form subform """.split()

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
        "9": {"ENT_TYPE": "range"},
    },
    patterns=[
        "M.? taxon+ (? auth*                       )?               9?",
        "M.? taxon+ (? auth+ maybe auth+           )?               9?",
        "M.? taxon+ (? auth*                       )? level .? word 9?",
        "M.? taxon+ (? auth+ maybe auth+           )? level .? word 9?",
        "M.? taxon+ (? auth*             and auth+ )?               9?",
        "M.? taxon+ (? auth+ maybe auth+ and auth+ )?               9?",
        "M.? taxon+ (? auth*             and auth+ )? level .? word 9?",
        "M.? taxon+ (? auth+ maybe auth+ and auth+ )? level .? word 9?",
        "level .? taxon+         9?",
        "taxon+                  9?",
        "M.? taxon level .? word 9?",
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

        elif token.pos_ in ["PROPN", "NOUN"] or token.lower_ in common_patterns.AND:
            if token.shape_ in consts.TITLE_SHAPES:
                auth.append(token.text)
            elif token.lower_ in common_patterns.AND:
                auth.append(token.text)

    if auth:
        ent._.data["authority"] = " ".join(auth)

    if ent._.data.get("plant_taxon"):
        del ent._.data["plant_taxon"]

    ent._.data["taxon"] = " ".join(taxa)
