from typing import Callable, Dict, List, NamedTuple, Sequence

from spectra_lexer.resource import RuleFlags, RulesDictionary, StenoRule
from spectra_lexer.types.tree import PrefixTree
from spectra_lexer.utils import str_prefix, str_without


class LexerMatch(NamedTuple):
    """ Container for a steno rule match with s-keys. """
    rule: StenoRule      # Original immutable rule.
    skeys: str           # Lexer-formatted steno keys that make up the rule.
    letters: str = ""    # Raw English text of the word.
    letter_len: int = 0  # Length of <letters>.

    @classmethod
    def special(cls, skeys:str, desc:str):
        """ Create a special (no-letter) rule and match info object. """
        return cls(StenoRule(skeys, "", RuleFlags(), desc, ()), skeys)

    @classmethod
    def convert_dict(cls, rule_dict:RulesDictionary, from_rtfcre:Callable[[str], str]) -> dict:
        """ All rules must have their keys parsed into the case-unique s-keys format for matching. """
        return {n: cls(r, from_rtfcre(r.keys), r.letters, len(r.letters)) for n, r in rule_dict.items()}


class SpecialRuleTypes:
    """ Identifiers for special rules that are handled individually in code. """
    CONFLICT = "CF"
    PROPER = "PR"
    ABBREVIATION = "AB"
    AFFIX = "PS"
    FINGERSPELL = "FS"
    OBSCENE = "OB"


class _PrefixFinder:
    """ Search engine that finds rules matching a prefix of ORDERED keys only. """

    _tree: PrefixTree    # Primary search tree.
    _key_sep: str        # Steno key used as stroke separator.
    _unordered_key: str  # Key to put into unordered set.

    def __init__(self, items:Sequence[LexerMatch], sep:str, unordered_key:str):
        """ Make the tree and the filter that returns which keys will be and won't be tested in prefixes.
            Separate the given sets of keys into ordered keys (which contain any prefix) and unordered keys.
            Index the rules, letters, and unordered keys under the ordered keys and compile the tree. """
        tree = self._tree = PrefixTree()
        self._key_sep = sep
        self._unordered_key = unordered_key
        for r in items:
            ordered, unordered = self._unordered_filter(r.skeys)
            tree[ordered] = (r, r.letters, unordered)
        tree.compile()

    def __call__(self, skeys:str, letters:str) -> list:
        """ Return a list of all rules that match a prefix of the given ordered keys,
            a subset of the given letters, and a subset of the given unordered keys. """
        ordered, unordered = self._unordered_filter(skeys)
        return [r for (r, rl, ru) in self._tree[ordered] if rl in letters and ru <= unordered]

    def _unordered_filter(self, skeys:str, _empty=frozenset()) -> tuple:
        """ Filter out asterisks in the first stroke that may be consumed at any time and return them.
            Also return the remaining ordered keys that must be consumed starting from the left. """
        star = self._unordered_key
        if (star not in skeys) or (star not in skeys.split(self._key_sep, 1)[0]):
            return skeys, _empty
        return str_without(skeys, star), frozenset([star])


class LexerRuleMatcher:
    """ A master dictionary of steno rules. Each component dict maps strings to steno rules in some way. """

    _key_sep: str              # Steno key used as stroke separator in both stroke formats.
    _key_star: str             # Steno key used for special translation-wide matches.
    _rule_sep: LexerMatch      # Separator rule constant.
    _rule_unknown: LexerMatch  # Unknown special rule constant.

    _special_dict: Dict[str, LexerMatch]  # Rules that match by reference name.
    _stroke_dict: Dict[str, LexerMatch]   # Rules that match by full stroke only.
    _word_dict: Dict[str, LexerMatch]     # Rules that match by exact word only (whitespace-separated).
    _prefix_finder: _PrefixFinder         # Rules that match by starting with certain keys in order.

    def __init__(self, sep:str, star:str, rules:Dict[str, LexerMatch]):
        """ Construct constants and a specially-structured series of dictionaries from a steno system. """
        self._key_sep = sep
        self._key_star = star
        # The separator rule constant is specifically matched on its own.
        self._rule_sep = LexerMatch.special(sep, "Stroke separator")
        # The unknown special rule constant is required in case no special rules match (or a matched rule is missing).
        self._rule_unknown = LexerMatch.special(star, "purpose unknown\nPossibly resolves a conflict")
        special_dict = self._special_dict = {}
        stroke_dict = self._stroke_dict = {}
        word_dict = self._word_dict = {}
        prefix_entries = []
        # Sort rules into specific dictionaries based on specific flags for the lexer matching system.
        match_name = RuleFlags.SPECIAL
        match_stroke = RuleFlags.STROKE
        match_word = RuleFlags.WORD
        for n, lr in rules.items():
            # All rules must have their keys parsed into the case-unique s-keys format.
            flags = lr.rule.flags
            # Internal rules are only used in special cases, by name.
            if match_name in flags:
                special_dict[n] = lr
            # Filter stroke and word rules into their own dicts.
            elif match_stroke in flags:
                stroke_dict[lr.skeys] = lr
            elif match_word in flags:
                word_dict[lr.letters] = lr
            # Everything else gets added to the tree-based prefix dictionary.
            else:
                prefix_entries.append(lr)
        # Steno order may be ignored for certain keys. This has a large performance and accuracy cost.
        # Only the asterisk is used in such a way that this treatment is worth it.
        self._prefix_finder = _PrefixFinder(prefix_entries, sep, star)

    def __call__(self, skeys:str, letters:str, all_skeys:str, all_letters:str) -> List[LexerMatch]:
        """ Return a list of rules that match the given keys and letters in any of the dictionaries.
            For single-key end-cases, there are no better matches, so return immediately if one is found. """
        # If our current stroke is empty, a stroke separator is next. Return its rule.
        skeys_fs = skeys.split(self._key_sep, 1)[0]
        if not skeys_fs:
            return [self._rule_sep]
        # If we only have a star left at the end of a stroke, try to match a star rule explicitly by name.
        # If execution reaches the end without finding one, return the "ambiguous" rule.
        if skeys_fs == self._key_star:
            rule_type = self._analyze_star(skeys, all_skeys, all_letters)
            return [self._special_dict.get(f"{self._key_star}:{rule_type}") or self._rule_unknown]
        # Try to match keys by prefix. This may yield a large number of rules.
        matches = self._prefix_finder(skeys, letters)
        # We have a complete stroke next if we just started or a stroke separator was just matched.
        is_start = (skeys == all_skeys)
        if is_start or all_skeys[-len(skeys) - 1] == self._key_sep:
            # For the stroke dictionary, the rule must match the next full stroke and a subset of the given letters.
            stroke_rule = self._stroke_dict.get(skeys_fs)
            if stroke_rule and stroke_rule.letters in letters:
                matches.append(stroke_rule)
        # We have a complete word if we just started or the word pointer is sitting on a space.
        if is_start or letters[:1] == ' ':
            # For the word dictionary, the rule must match a prefix of the given keys and the next full word.
            word_rule = self._word_dict.get(str_prefix(letters.lstrip()))
            if word_rule and skeys.startswith(word_rule.skeys):
                matches.append(word_rule)
        return matches

    def _analyze_star(self, skeys:str, all_skeys:str, all_letters:str) -> str:
        """ Try to guess the meaning of an asterisk from the remaining keys, the full set of keys,
            the full word, and the current rulemap. Return the reference type for the best-guess rule (if any). """
        # If the word contains a period, it's probably an abbreviation (it must have letters to make it this far).
        if "." in all_letters:
            return SpecialRuleTypes.ABBREVIATION
        # If the word has uppercase letters in it, it's probably a proper noun.
        if all_letters != all_letters.lower():
            return SpecialRuleTypes.PROPER
        # If we have a multi-stroke word and are at the beginning or end of it, it's probably a prefix or suffix.
        splits_left, all_splits = skeys.count(self._key_sep), all_skeys.count(self._key_sep)
        if all_splits and (not splits_left or splits_left == all_splits):
            return SpecialRuleTypes.AFFIX
