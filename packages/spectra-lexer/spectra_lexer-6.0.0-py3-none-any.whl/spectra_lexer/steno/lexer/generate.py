from functools import reduce
from operator import attrgetter
from typing import Callable, Iterable, List, Sequence, Tuple

from spectra_lexer.resource import RuleFlags, RuleMapItem, StenoRule

# Flag constants for rule generation.
_RARE_FLAG = RuleFlags.RARE
_UNMATCHED_FLAGS = RuleFlags({RuleFlags.UNMATCHED})
_GENERATED_FLAGS = RuleFlags({RuleFlags.GENERATED})


class LexerRuleGenerator:
    """ Ranks results from the lexer and keeps the best one, converts the keys back to RTFCRE format,
        and creates a new rule with the correct caption and flags. """

    _convert_to_rtfcre: Callable[[str], str]  # Conversion function from s-keys to RTFCRE.

    def __init__(self, key_converter:Callable[[str],str]):
        self._convert_to_rtfcre = key_converter

    def __call__(self, results:List[Tuple[Sequence[RuleMapItem], str, str, str]],
                 default_keys:str, default_word:str) -> StenoRule:
        """ Make a rule out of the map that ranks highest among all. Going in reverse is faster. """
        if not results:
            # If nothing matched at all, return a blank result with the default keys and word.
            return _rule_from_params(default_keys, default_word)
        rulemap, unmatched, keys, letters = reduce(_keep_better, reversed(results))
        if unmatched:
            # The output is nowhere near reliable if some keys couldn't be matched.
            desc = "Incomplete match. Not reliable."
            last_match_end = rulemap[-1].start + rulemap[-1].length
            rulemap.append(_unmatched_item(self._convert_to_rtfcre(unmatched), letters, last_match_end))
        else:
            desc = "Found complete match."
        # Freeze the rulemap and make a new rule.
        return _rule_from_params(keys, letters, desc, tuple(rulemap))


def _rule_from_params(keys:str, word:str, desc:str="No matches found.", rulemap:Tuple[RuleMapItem]=()) -> StenoRule:
    """ Make a new rule marked as lexer-generated. If the rulemap is empty, every key is unmatched. """
    return StenoRule(keys, word, _GENERATED_FLAGS, desc, rulemap or (_unmatched_item(keys, word),))


def _unmatched_item(keys:str, word:str, last_match_end:int=0) -> RuleMapItem:
    """ Make a special rulemap item with unmatched keys to cover everything after the last match. """
    rule = StenoRule(keys, "", _UNMATCHED_FLAGS, "unmatched keys", ())
    return RuleMapItem(rule, last_match_end, len(word) - last_match_end)


def _keep_better(self:tuple, other:tuple) -> tuple:
    """ Foldable function that keeps one of two lexer result tuples based on which has a greater "value".
        Each criterion is lazily evaluated, with the first non-zero result determining the winner.
        Some criteria are negative, meaning that more accurate maps have smaller values.
        As it is called repeatedly by reduce(), the full compare sequence is inlined to avoid method call overhead. """
    rulemap, unmatched, keys, letters = self
    n_rulemap, n_unmatched, n_keys, n_letters = other
    return self if (-len(unmatched)           + len(n_unmatched) or              # Fewest keys unmatched
                    _letters_matched(rulemap) - _letters_matched(n_rulemap) or   # Most letters matched
                    -_rare_count(rulemap)     + _rare_count(n_rulemap) or        # Fewest rare rules
                    -len(keys)                + len(n_keys) or                   # Fewest total keys
                    -len(rulemap)             + len(n_rulemap)) >= 0 else other  # Fewest child rules


def _letters_matched(rulemap:Iterable[RuleMapItem], _get_letters=attrgetter("rule.letters")) -> int:
    """ Get the number of characters matched by mapped rules. """
    return sum(map(len, map(_get_letters, rulemap)))


def _rare_count(rulemap:Iterable[RuleMapItem]) -> int:
    """ Get the number of rare rules in the map. """
    return sum([_RARE_FLAG in i.rule.flags for i in rulemap])
