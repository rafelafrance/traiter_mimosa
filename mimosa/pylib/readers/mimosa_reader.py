"""Parse PDFs about mimosas."""
from ..pipelines import mimosa_pipeline


def read(args):
    """Do the parsing here."""
    with open(args.text_file) as in_file:
        texts = in_file.readlines()

    nlp = mimosa_pipeline.pipeline()

    for i, text in enumerate(texts):
        text = text.strip()

        doc = nlp(text)
        traits = [e._.data for e in doc.ents]

        print(traits)

        if i > 100:
            break
