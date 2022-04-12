"""Literals used in the system."""
import os
import string
from pathlib import Path

from traiter import const as t_const
from traiter.terms.db import Db

# #########################################################################
CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path(".." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
VOCAB_DIR = ROOT_DIR / "mimosa" / "vocabulary"
TERM_DB = VOCAB_DIR / "terms.sqlite"


# #########################################################################
TERMS = Db.shared("colors units plant_treatment taxon_levels")
TERMS += Db.hyphenate_terms(TERMS)
TERMS += Db.trailing_dash(TERMS, label="color")
TERMS += Db.select_term_set(TERM_DB, "plant_taxa")
TERMS.drop("imperial_length")

REPLACE = TERMS.pattern_dict("replace")
REMOVE = TERMS.pattern_dict("remove")

LEVELS = TERMS.pattern_dict("level")
LEVELS = {k: v.split() for k, v in LEVELS.items()}

# #########################################################################
# Tokenizer constants
ABBREVS = """
    Jan. Feb. Febr. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    M. Var. Sect. Subsect. Ser. Subser. Subsp. Spec. Sp. Spp.
    m. var. sect. subsect. ser. subser. subsp. spec. sp. spp. nov.
    Acad. Agri. Amer. Ann. Arb. Arq. adj. al. alt. ann.
    Bol. Bot. Bras. Bull. bot. bras.
    Cat. Ci. Coll. Columb. Com. Contr. Cur. ca. cent. centr. cf. coll.
    DC. depto. diam. dtto.
    Encycl. Encyle. Exot. ed. ememd. ent. est.
    FIG. Fig. Figs. Fl. fig. figs. fl. flor. flumin.
    Gard. Gen. Geo. gard. geograph.
    Herb. Hist. Hort. hb. hist.
    Is. illeg. infra. is.
    Jahrb. Jard. Jr. jug.
    Lab. Lam. Leg. Legum. Linn. lam. lat. leg. lin. long.
    Mag. Mem. Mex. Mts. Mus. Nac. mem. mens. monac. mont. mun.
    Nat. Natl. Neg. No. nat. no. nom. nud.
    Ocas.
    PI. PL. Pl. Proc. Prodr. Prov. Pt. Pto. Publ. p. pi. pl. pr. prov.
    reg. revis.
    Sa. Sci. Soc. Sr. Sta. Sto. Sul. Suppl. Syst.
    s. sci. stat. stk. str. superfl. suppl. surv. syn.
    Tex. Trans telegr.
    U.S. US. Univ.
    Veg. veg.
    Wm.
    I. II. III. IV. IX. V. VI. VII. VIII. X. XI. XII. XIII. XIV. XIX. XV. XVI. XVII.
    XVIII. XX. XXI. XXII. XXIII. XXIV. XXV.
    i. ii. iii. iv. ix. v. vi. vii. viii. x. xi. xii. xiii. xiv. xix. xv. xvi. xvii.
    xviii. xx. xxi. xxii. xxiii. xxiv. xxv.
    """.split()
ABBREVS += [f"{c}." for c in string.ascii_uppercase]

# #########################################################################
# Common patterns for parsing
CONJ = ["or", "and"]
TO = ["to"]
MISSING = """
    without missing lack lacking except excepting not rarely obsolete
    """.split()

COMMON_PATTERNS = {
    "(": {"TEXT": {"IN": t_const.OPEN}},
    ")": {"TEXT": {"IN": t_const.CLOSE}},
    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
    "-*": {"TEXT": {"IN": t_const.DASH}, "OP": "*"},
    "[+]": {"TEXT": {"IN": t_const.PLUS}},
    "/": {"TEXT": {"IN": t_const.SLASH}},
    ",": {"TEXT": {"IN": t_const.COMMA}},
    ".": {"TEXT": {"IN": t_const.DOT}},
    "x": {"TEXT": {"IN": t_const.CROSS}},
    ":": {"TEXT": {"IN": t_const.COLON}},
    "to": {"LOWER": {"IN": TO}},
    "-/or": {"LOWER": {"IN": t_const.DASH + TO + CONJ}, "OP": "+"},
    "-/to": {"LOWER": {"IN": t_const.DASH + TO}, "OP": "+"},
    "and/or": {"LOWER": {"IN": CONJ}},
    "missing": {"LOWER": {"IN": MISSING}},
    "9": {"IS_DIGIT": True},
    "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "99-99": {"ENT_TYPE": {"REGEX": "^range"}},
    "99.9-99.9": {"ENT_TYPE": {"REGEX": "^range"}},
}

# #########################################################################
# Entities

TRAITS = set(
    """ color color_mod count location margin_shape part surface
    size shape sex subpart woodiness part_as_loc """.split()
)
