
from nav_pii_anon.spacy.matcher_regex import match_func
import spacy
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher


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
	
	def add_patterns(self, entities:list = None):
		"""
		Adds desired patterns to the entity ruler of the SpaCy model
		:param entities: a list of strings denoting which entities the nlp model should detect.
		"""
		self.model.add_pipe(match_func, before='ner')

	def predict(self, text:str):
		"""
		Prints the found entities, their labels, start, and end index.
		:param text: a string of text which is to be analysed.
		"""
		doc = self.model(text)
		ents = [[ent.text, ent.label_, ent.start, ent.end, "NA"] for ent in doc.ents]

		print(ents)
	
	def get_doc(self, text:str):
		return self.model(text)


