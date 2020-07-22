from nav_pii_anon.spacy.matcher_regex import match_func
from nav_pii_anon.spacy.matcher_list import name_list_matcher
from spacy.matcher import Matcher
from spacy import displacy
import random
import warnings
import spacy
from spacy.util import minibatch, compounding
from pathlib import Path


class SpacyModel:

    def __init__(self, model=None):
        """
        SpacyModel class: A class for managing a SpaCy nlp model with methods for adding custom RegEx and for easy printing
        :param model: an nlp model
        """
        if not model:
            self.model = spacy.load("nb_core_news_lg")
        else:
            self.model = model
        self.matcher = Matcher(self.model.vocab)

    def add_patterns(self, entities: list = None):
        """
        Adds desired patterns to the entity ruler of the SpaCy model
        :param entities: a list of strings denoting which entities the nlp model should detect.
        """
        ruler = name_list_matcher(self.model
                                  )
        self.model.add_pipe(match_func, name="regex_matcher", before='ner')
        self.model.add_pipe(ruler, after="ner")

    def predict(self, text: str):
        """
        Prints the found entities, their labels, start, and end index.
        :param text: a string of text which is to be analysed.
        """
        doc = self.model(text)
        ents = [[ent.text, ent.label_, ent.start, ent.end, "NA"] for ent in doc.ents]

        print(ents)

    def get_doc(self, text: str):
        return self.model(text)

    def display_predictions(self, text: str):
        displacy.render(self.get_doc(text), style='ent', jupyter=True)

    def disable_ner(self):
        self.disabled = self.model.disable_pipes("ner")

    def enable_ner(self):
        self.disabled.restore()

    def replace(self, text: str):
        doc = self.model(text)
        censored_text = text
        ents = [[ent.text, ent.label_, ent.start, ent.end, "NA"] for ent in doc.ents]
        for ent in ents:
            censored_text = censored_text.replace(ent[0], "<" + ent[1] + ">")
        return censored_text

    def train(self, TRAIN_DATA, labels: list =['PER', 'ORG', 'TLF', 'LOC', 'DTM', 'FNR',
                                                'AGE', 'AMOUNT', 'NAV_YTELSER', 'MEDICAL_CONDITIONS'],
              n_iter: int = 30, output_dir=None):

        ner = self.model.get_pipe("ner")
        for lab in labels:
            ner.add_label(lab)
        optimizer = self.model.resume_training()
        move_names = list(ner.move_names)
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in self.model.pipe_names if pipe not in pipe_exceptions]
        with (self.model.disable_pipes(*other_pipes)), warnings.catch_warnings():
            warnings.filterwarnings("once", category=UserWarning, module='spacy')
            sizes = compounding(1.0, 4.0, 1.001)
            # batch up the examples using spaCy's minibatch
            for itn in range(n_iter):
                random.shuffle(TRAIN_DATA)
                batches = minibatch(TRAIN_DATA, size=sizes)
                losses = {}
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self.model.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
                print("Losses", losses)

        # Save model
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            self.model.meta["name"] = 'test_model'  # rename model
            self.model.to_disk(output_dir)
            print("Saved model to", output_dir)

            # test the saved model
            print("Loading from", output_dir)
            nlp2 = spacy.load(output_dir)
            # Check the classes have loaded back consistently
            assert nlp2.get_pipe("ner").move_names == move_names
