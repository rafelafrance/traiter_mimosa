"""Utilities for dealing with terms."""
import string

from traiter.terms.db import Db

from .. import consts

TERM_DB = consts.DATA_DIR / "plant_terms.sqlite"
if not TERM_DB.exists():
    TERM_DB = consts.MOCK_DIR / "plant_terms.sqlite"

# #########################################################################
TERMS = Db.shared("colors units taxon_levels time")
TERMS += Db.select_term_set(TERM_DB, "plant_treatment")
TERMS += Db.hyphenate_terms(TERMS)
TERMS += Db.trailing_dash(TERMS, label="color")
TERMS += Db.select_term_set(TERM_DB, "plant_taxa")
TERMS.drop("imperial_length")
TERMS.drop("time_units")

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
