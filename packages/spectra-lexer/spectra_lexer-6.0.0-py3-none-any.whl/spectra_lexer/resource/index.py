from collections import defaultdict
import random
from typing import Dict, Iterable, List

from .rules import StenoRule
from .translations import TranslationsDictionary
from spectra_lexer.types.codec import JSONDict


class StenoIndex(JSONDict):
    """ A resource-heavy index dict-of-dicts for finding translations that contain a particular steno rule.
        Index search is a two-part search. The first part goes by rule name; only exact matches will work. """

    @classmethod
    def _decode(cls, data:bytes, **kwargs) -> dict:
        """ Make sure this isn't just an arbitrary JSON file. """
        d = super()._decode(data, **kwargs)
        if not all(type(v) is dict for v in d.values()):
            raise TypeError("All first-level values in a JSON index must be objects.")
        return d

    def search(self, index_key:str, pattern:str, **kwargs) -> List[str]:
        """ Translation search dicts are memory hogs, and users tend to look at many results under the same rule.
            Convert native dicts (from JSON) to full-featured search dicts only on demand. """
        d = self.get(index_key)
        if not d:
            return []
        if not isinstance(d, TranslationsDictionary):
            d = self[index_key] = TranslationsDictionary(d)
        # Manually set the search flags.
        kwargs.update(prefix=False, regex=False)
        return d.search(pattern, **kwargs)

    def find_example(self, index_key:str, strokes:bool=False) -> str:
        """ Given a rule/index key by name, return one translation using it at random. """
        d = self.get(index_key) or {"": ""}
        k = random.choice(list(d))
        return k if strokes else d[k]

    @classmethod
    def filters(cls, size:int) -> tuple:
        """ Generate filters to control index size. Larger translations are excluded with smaller index sizes.
            The parameter <size> determines the relative size of a generated index (range 1-20). """
        def filter_in(translation:tuple) -> bool:
            """ Filter function to eliminate larger entries from the index depending on the size factor. """
            return max(map(len, translation)) <= size
        def filter_out(rule:StenoRule) -> bool:
            """ Filter function to eliminate lexer results that are unmatched or basic rules themselves. """
            return len(rule.rulemap) > 1
        return (filter_in if size < 20 else None, filter_out)

    @classmethod
    def compile(cls, rules:Iterable[StenoRule], rev_rules:Dict[StenoRule, str]):
        """ Using rulemaps, make dicts of all translations that use each built-in rule at the top level. """
        tr_dicts = defaultdict(dict)
        for rs in rules:
            keys = rs.keys
            letters = rs.letters
            for item in rs.rulemap:
                tr_dicts[item.rule][keys] = letters
        # Convert the rule keys to strings. Hardcoded and missing rules will map to None.
        d = {rev_rules.get(k): v for k, v in tr_dicts.items()}
        # Entries with no rule are useless, and None/null is not a valid key in JSON, so toss it.
        if None in d:
            del d[None]
        return cls(d)

    def __repr__(self):
        """ Recursive reprs on index objects are deadly. Only show the first level with item counts. """
        item_counts = ", ".join([f"{k!r}: {len(v)} items" for k, v in self.items()])
        return f"<{type(self).__name__}: {{{item_counts}}}>"
