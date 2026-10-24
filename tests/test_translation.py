#!/usr/bin/env python
"""Checks on the shipped Russian localization.

The tests read `translation/Russian/*.csv` the way the game reads them, and
compare them against `translation/keys.json`: the row order of the English
source and the inline markup every row has to carry. Nothing here needs the
game to be installed.
"""
from __future__ import annotations

import csv
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLATION = os.path.join(ROOT, "translation", "Russian")
MANIFEST = os.path.join(ROOT, "translation", "keys.json")
GLOSSARY = os.path.join(ROOT, "src", "voice", "glossary.json")
ALLOWLIST = os.path.join(ROOT, "tests", "allowed_latin.json")

FILES = [
    "Dialogs.csv", "EntityInfo.csv", "Feats.csv", "Glossary.csv", "ItemTexts.csv",
    "MiscTexts.csv", "NPCInfo.csv", "Popups.csv", "QuestPoints.csv", "SheetInfo.csv",
    "SpellTexts.csv", "UIElements.csv",
]

SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")
# A word is a run of letters and digits in any script. A word that carries a
# diacritic outside ASCII belongs to one of the world's languages, not to
# English.
WORD = re.compile(r"[^\W_]+", re.UNICODE)
CYRILLIC = re.compile(r"[А-Яа-яЁё]")
ASCII_LATIN = re.compile(r"^[A-Za-z][A-Za-z'\-]*$")

# The rows that stay empty on purpose, and the rows the game fills itself.
EXPECTED_EMPTY = 9

ALLOWED_LATIN = {
    # abbreviations and marks the game itself uses
    "hwbt", "it", "dm", "pc", "np", "ui", "hp", "mp", "dnd", "tv", "id", "dlc",
    "sdk", "api", "www", "http", "https", "com", "org", "steam", "ais", "d20",
    "d4", "d6", "d8", "d10", "d12", "lol", "mhr", "rpg", "fps", "xp", "ppg",
    "ar", "pe", "ro", "qa", "cbs", "flm", "tt", "ost", "vol", "co", "ahplc",
    "fqa", "fc", "ii", "vii", "shift", "she",
    # titles that are titles: a composition, a release, a font
    "act", "scene", "interlude", "let", "be", "dust", "averia", "serif",
    # the words of another language, or a Latin phrase of the world
    "prôv", "carpe", "tenebras", "faux", "pas", "du", "grin", "larp",
    "lingua", "dominans", "maior", "quam", "ullus", "rex", "vox", "operariorum",
    "bellum", "classium", "manifestum", "plebeium", "chalybs", "ddvaerg",
    "rogue",
}

# One row departs from the English on purpose: the display size of a word was
# lowered so that the line fits the panel it is drawn in. The reason is in
# docs/layout.md.
MARKUP_EXCEPTIONS = {
    ("MiscTexts.csv", "AbilityScoreInfo_Wisdom_Uses3"): "<size=44><size=43>",
    ("MiscTexts.csv", "AbilityScoreInfo_Strength_LoreFootNote"): "<b></b><b><size=25></b>",
    ("MiscTexts.csv", "AbilityScoreInfo_Strength_Uses3"): "<size=63><size=45>",
    ("MiscTexts.csv", "AbilityScoreInfo_Dexterity_Uses3"): "<size=40><size=41>",
    ("MiscTexts.csv", "AbilityScoreInfo_Intelligence_Uses1"): "<size=40></size><size=42>",
    ("MiscTexts.csv", "AbilityScoreInfo_Charisma_Uses3"): "<size=42></size><size=40>",
    ("UIElements.csv", "Menu_DeepStorage"): "<size=30></size>",
}


def load_csv(name):
    with open(os.path.join(TRANSLATION, name), encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


def allowed_tokens():
    tokens = set(ALLOWED_LATIN)
    if os.path.exists(ALLOWLIST):
        with open(ALLOWLIST, encoding="utf-8") as fh:
            data = json.load(fh)
        for group in data.get("groups", {}).values():
            tokens.update(w.lower() for w in group)
    if os.path.exists(GLOSSARY):
        with open(GLOSSARY, encoding="utf-8") as fh:
            for key in json.load(fh):
                for tok in WORD.findall(key):
                    tokens.add(tok.lower())
    return tokens


class TestFiles(unittest.TestCase):
    def test_all_files_present(self):
        for name in FILES:
            self.assertTrue(os.path.exists(os.path.join(TRANSLATION, name)), name)

    def test_language_code_in_header(self):
        for name in FILES:
            rows = load_csv(name)
            self.assertTrue(rows, name)
            self.assertEqual(rows[0][-1], "RU", "%s: the last column is the language" % name)

    def test_row_order_matches_the_source(self):
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
        for name in FILES:
            rows = load_csv(name)
            expected = manifest[name]
            self.assertEqual(len(rows) - 1, len(expected), "%s: row count" % name)
            for i, (key, _markup, _has_text) in enumerate(expected):
                self.assertEqual(rows[i + 1][0], key, "%s: row %d" % (name, i))

class TestMarkup(unittest.TestCase):
    def test_markup_matches_the_source(self):
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
        broken = []
        for name in FILES:
            rows = load_csv(name)
            for i, (key, markup, _has_text) in enumerate(manifest[name]):
                expected = MARKUP_EXCEPTIONS.get((name, key), markup)
                cell = rows[i + 1][-1]
                if "".join(SPECIAL.findall(cell)) != expected:
                    broken.append("%s: %s" % (name, key))
        self.assertEqual(broken[:10], [], "markup changed in %d rows" % len(broken))


class TestTypography(unittest.TestCase):
    def test_no_straight_quotes(self):
        for name in FILES:
            for i, row in enumerate(load_csv(name)[1:], 1):
                self.assertNotIn('"', row[-1], "%s: row %d" % (name, i))

    def test_no_three_dot_ellipsis(self):
        for name in FILES:
            for i, row in enumerate(load_csv(name)[1:], 1):
                self.assertNotIn("...", row[-1], "%s: row %d" % (name, i))

    def test_tak_zhe_is_one_word(self):
        for name in FILES:
            for i, row in enumerate(load_csv(name)[1:], 1):
                self.assertIsNone(re.search(r"\bтак же\b", row[-1], re.I),
                                  "%s: row %d" % (name, i))

    def test_quotes_are_balanced(self):
        unbalanced = []
        for name in FILES:
            for i, row in enumerate(load_csv(name)[1:], 1):
                cell = row[-1]
                if cell.count("«") != cell.count("»"):
                    unbalanced.append("%s: row %d" % (name, i))
        # A speech that spans several rows opens in one and closes in another.
        self.assertLessEqual(len(unbalanced), 40, "unbalanced quotes in %d rows" % len(unbalanced))


class TestLanguage(unittest.TestCase):
    def test_no_english_inside_a_russian_sentence(self):
        allowed = allowed_tokens()
        found = []
        for name in FILES:
            for i, row in enumerate(load_csv(name)[1:], 1):
                cell = row[-1]
                if not cell or not CYRILLIC.search(cell):
                    continue
                clean = SPECIAL.sub(" ", cell)
                for tok in WORD.findall(clean):
                    if not ASCII_LATIN.match(tok):
                        continue          # a word of another language
                    if tok.lower() not in allowed:
                        found.append("%s: row %d: %s" % (name, i, tok))
        self.assertEqual(found[:10], [], "english left inside russian in %d rows" % len(found))

    def test_the_words_are_not_fused_across_scripts(self):
        fused = []
        for name in FILES:
            for i, row in enumerate(load_csv(name)[1:], 1):
                for tok in WORD.findall(row[-1]):
                    if CYRILLIC.search(tok) and re.search(r"[A-Za-z]", tok):
                        fused.append("%s: row %d: %s" % (name, i, tok))
        self.assertEqual(fused[:10], [], "a word fused across two scripts in %d rows" % len(fused))


class TestCoverage(unittest.TestCase):
    def test_every_source_line_is_translated(self):
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
        missing = []
        for name in FILES:
            rows = load_csv(name)
            for i, (key, _markup, has_text) in enumerate(manifest[name]):
                if not has_text:
                    continue
                if not rows[i + 1][-1].strip():
                    missing.append("%s: %s" % (name, key))
        self.assertEqual(missing[:10], [], "%d source lines have no translation" % len(missing))

    def test_the_corpus_is_filled(self):
        empty = 0
        for name in FILES:
            for row in load_csv(name)[1:]:
                if not row[-1].strip():
                    empty += 1
        self.assertLessEqual(empty, 750, "%d empty cells" % empty)


class TestSettings(unittest.TestCase):
    def test_the_language_is_registered(self):
        rows = {r[0]: r[-1] for r in load_csv("MiscTexts.csv")[1:]}
        self.assertEqual(rows.get("LanguageDropdown"), "Русский")
        self.assertEqual(rows.get("FallbackLanguage"), "EN")


if __name__ == "__main__":
    unittest.main()
