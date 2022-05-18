from spacy.language import Language
from spacy.tokens import Doc

from .patterns import term_patterns

DOC_ANALYSIS = "mimosa.doc_analysis.v1"


def add_extensions():
    if not Doc.has_extension("reject"):
        Doc.set_extension("reject", default=False)


@Language.factory(DOC_ANALYSIS)
class DocAnalysis:
    def __init__(self, nlp: Language, name: str):
        add_extensions()
        self.nlp = nlp
        self.name = name

        self.reject_set = term_patterns.PARTS_SET
        self.reject_set.add("taxon")

    def __call__(self, doc: Doc) -> Doc:
        used = {e._.data["trait"] for e in doc.ents}

        if len(used) == 1 or used <= self.reject_set:
            doc._.reject = True

        return doc
