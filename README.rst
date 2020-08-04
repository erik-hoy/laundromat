=================
What Is Occultat?
=================
Protect your personal data in text
----------------------------------
This is a package for anonamyzing norwegian text.

Occultat uses a mix of matching techniques like Regular expression
and a statistical model to recognize and remove personal information in norwegian text. The package is
built around SpaCy NLP. Current functionality of
the package:

* Detecting named entities related to personal and sensitive information.
* Censoring texts containing said information.
* Improving the NER model from new data.
* Scoring the model with various metrics.
* Metrics on how "anonymous" a text is.

Supported entities:

* <PER> - Person
* <DTM> - Date time
* <TLF> (Telephone number)
* OSV....

Current Performance
-------------------
The following table shows the best current performance ran on 500 norwegian training/test data texts.

+-------+----------+-------+
| Enteties         | Score |
+------------------+-------+
| PER              |   0   |
+------------------+-------+
| TLF              |   0   |
+------------------+-------+
| DTM              |   0   |
+------------------+-------+

Requirements
------------

spacy >= 2.3.0

numpy

pandas