# traiter_mimosa ![Python application](https://github.com/rafelafrance/traiter_mimosa/workflows/CI/badge.svg)
Extract traits about mimosas from authoritative literature.

The PDFs I'm parsing have rather complicated text flows. For example, a single page may jump from a 2-column format to a 1-column format several times in that page. The standard tools for converting PDFs to text were not handing these cases. So I wrote my own scripts to organize text from these documents. The work much better (for our use case) than the standard poppler libraries. _**Note: that these scripts are far from perfect, just better for our use cases.**_ Also note that, we still use the poppler utilities for parsing the PDFs, just not the text assembly part.

Scripts for converting PDFs into text and then extracting traits:

1. [rename_pdfs.py](./parse/rename_pdfs.py) - This is an _**optional**_ step to make working with the PDFs a bit easier. All this utility does is replace problematic characters in a PDF file name (like space, parentheses, etc.) to underscores.
2. [pdf_to_xhtml.py](./parse/pdf_to_xhtml.py) Convert a PDF into an XHTML document that contains the bounding box of every word in the document. This is used to build the pages.
   1. It's just a wrapper around the poppler utility `pdftotext -bbox -nodiag input.pdf output.xhtml`.
3. [xhtml_to_text.py](./parse/xhtml_to_text.py) Assembles the text.
   1. You need to edit the output to remove flow interrupting text such as page headers, footers, figure captions, etc.
   2. We do use margins for cropping pages that can help remove most headers & footers but pages may be skewed, so you should probably check for outliers.
4. [clean_text.py](./parse/clean_text.py) Now we take the text from step 3 and format it so that we can parse the text with spaCy rule-based parsers. This breaks the text into sentences, joins hyphenated words, fixes mojibake, removes control characters, space normalizes text, etc. Examine the output of this text to make sure things are still working as expected.
   1. The step for breaking the text into sentences is very slow.
5. [extract_traits.py](./parse/extract_traits.py) Finally, we extract traits from the text using spaCy rule-based parsers.
