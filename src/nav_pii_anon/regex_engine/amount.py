from nav_pii_anon.regex_engine.regex_base import RegexBase
import re

class RegexAmount(RegexBase):
    """
    Amount is mainly percent
    """
    @property
    def regex_pattern(self):

        return r"\d{1,3}\s?(\%|prosent)"

    @property
    def context(self):
        return ["amount"]

    @property
    def label(self):
        return "AMOUNT"

    @property
    def score(self):
        return 1

    def validate(self):
        pass
