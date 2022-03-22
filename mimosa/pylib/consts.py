"""Literals used in the system."""
import os
import string
from pathlib import Path

from traiter.const import CLOSE
from traiter.const import COMMA
from traiter.const import CROSS
from traiter.const import DASH
from traiter.const import FLOAT_TOKEN_RE
from traiter.const import OPEN
from traiter.const import PLUS
from traiter.const import SLASH
from traiter.terms.csv_ import Csv

# #########################################################################
CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path(".." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
VOCAB_DIR = ROOT_DIR / "mimosa" / "vocabulary"


# #########################################################################
TERMS = Csv.shared("colors units plant_treatment")
TERMS += Csv.hyphenate_terms(TERMS)
TERMS += Csv.trailing_dash(TERMS, label="color")
TERMS += Csv.read_csv(VOCAB_DIR / "taxa.csv")
TERMS.drop("imperial_length")

REPLACE = TERMS.pattern_dict("replace")
REMOVE = TERMS.pattern_dict("remove")

# #########################################################################
# Tokenizer constants
ABBREVS = """
    Jan. Feb. Febr. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    Acad. Amer. Ann. Arq. Bol. Bot. Bull. Cat. Coll. Com. Contr. Exot. FIG.
    Gard. Gen. Geo. Herb. Hort. Hist. Is. Jahrb. Jr. Lab. Leg. Legum. Linn.
    Mem. Mex. Mts. Mus. Nac. Nat. Neg. No. Ocas. Proc. Prodr. Prov. Pto. Publ.
    Sci. Soc. Spec. Ser. Spp. Sr. Sta. Sto. Sul. Suppl. Syst.
    Tex. Trans. Univ. US. U.S. Veg. Wm.
    adj. al. alt. ann. bot. bras. ca. cent. centr. cf. coll. depto. diam. dtto.
    ed. ememd. ent. est.
    fig. figs. fl. flor. flumin. gard. hb. hist. illeg. infra. is. jug.
    lam. lat. leg. lin. long. mem. mens. monac. mont. mun.
    nat. no. nom. nud. p. pi. pr. prov. reg.
    s. sci. spp. stat. stk. str. superfl. suppl. surv. syn. telegr. veg.
    i. ii. iii. iv. v. vi. vii. viii. ix. x. xi. xii. xiii. xiv. xv. xvi. xvii.
    xviii. xix. xx. xxi. xxii. xxiii. xxiv. xxv.
    I. II. III. IV. V. VI. VII. VIII. IX. X. XI. XII. XIII. XIV. XV. XVI. XVII.
    XVIII. XIX. XX. XXI. XXII. XXIII. XXIV. XXV.
    m. var. sect. subsect. ser. subser. subsp. sp. nov.
    """.split()
ABBREVS += [f"{c}." for c in string.ascii_uppercase]

# #########################################################################
# Common patterns for parsing
CONJ = ["or", "and"]
TO = ["to"]
MISSING = """ without missing lack lacking except excepting not rarely """.split()

COMMON_PATTERNS = {
    "(": {"TEXT": {"IN": OPEN}},
    ")": {"TEXT": {"IN": CLOSE}},
    "-": {"TEXT": {"IN": DASH}, "OP": "+"},
    "-*": {"TEXT": {"IN": DASH}, "OP": "*"},
    "[+]": {"TEXT": {"IN": PLUS}},
    "/": {"TEXT": {"IN": SLASH}},
    ",": {"TEXT": {"IN": COMMA}},
    "x": {"TEXT": {"IN": CROSS}},
    "to": {"LOWER": {"IN": TO}},
    "-/or": {"LOWER": {"IN": DASH + TO + CONJ}, "OP": "+"},
    "-/to": {"LOWER": {"IN": DASH + TO}, "OP": "+"},
    "and/or": {"LOWER": {"IN": CONJ}},
    "missing": {"LOWER": {"IN": MISSING}},
    "9": {"IS_DIGIT": True},
    "99.9": {"TEXT": {"REGEX": FLOAT_TOKEN_RE}},
    "99-99": {"ENT_TYPE": {"REGEX": "^range"}},
    "99.9-99.9": {"ENT_TYPE": {"REGEX": "^range"}},
}

# #########################################################################
# Entities

TRAITS = set(
    """ color color_mod count location margin_shape part
    size shape sex subpart woodiness part_as_loc """.split()
)
