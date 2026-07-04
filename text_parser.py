# -*- coding: utf-8 -*-

import re
import difflib
from reference_values import get_all_aliases, REFERENCE_VALUES

# Matches a decimal or integer number anywhere in a line.
NUMBER_PATTERN = re.compile(r"(-?\d+(?:\.\d+)?)")

# Matches an alphabetic word (3+ letters), used for fuzzy matching candidates.
WORD_PATTERN = re.compile(r"[a-zA-Z]{3,}")

# Known qualitative result phrases (e.g. urine/stool tests). Sorted longest-first
# below so multi-word phrases match before their single-word substrings.
QUALITATIVE_KEYWORDS = [
    "negative", "positive", "non reactive", "non-reactive", "reactive",
    "nil", "absent", "present", "trace", "rare", "few", "many", "numerous",
    "clear", "turbid", "cloudy", "transparent",
    "yellow", "pale yellow", "straw", "amber", "dark yellow", "red", "brown",
    "formed", "semi-formed", "semi formed", "unformed", "watery",
    "yellowish brown", "greenish",
    "normal", "abnormal", "not seen", "seen",
]
QUALITATIVE_KEYWORDS.sort(key=len, reverse=True)


# Keywords that mark the start of a report section. Once one is seen, every
# following line is assumed to belong to that category until a new section
# header appears. This disambiguates aliases shared across sections (e.g.
# "Colour" or "RBCs" appearing in both urine and stool tests).
SECTION_KEYWORDS = {
    "Stool": [
        "stool analysis", "stool examination", "naked eye examination",
        "occult blood", "microscopic examination", "digestion", "parasites",
        "ova and parasites", "helminthes", "protozoa",
    ],
    "Urine": [
        "urine analysis", "urinalysis", "urine examination",
        "physical examination", "chemical examination",
    ],
    "CBC": [
        "complete blood count", "cbc", "haematology", "hematology",
    ],
    "Liver": [
        "liver function", "liver profile", "lft",
    ],
    "Kidney": [
        "kidney function", "renal function", "rft",
    ],
    "Lipid": [
        "lipid profile", "lipid panel",
    ],
}


def detect_section(line_lower: str):
    """Check whether a line contains a known section header and return its category, if any."""
    for category, keywords in SECTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in line_lower:
                return category
    return None


def clean_line(line: str) -> str:
    """Strip common OCR noise characters and collapse repeated whitespace."""
    line = line.replace("|", " ").replace("_", " ")
    line = re.sub(r"\s{2,}", " ", line)
    return line.strip()


def find_matching_test(line_lower: str, alias_map: dict, category_hint: str = None):
    """Find the test (and matched alias) referenced in a line, preferring exact matches over fuzzy ones."""
    candidates = []  # exact matches: (test_name, alias, alias_len)
    for alias, test_name in alias_map.items():
        # Require a whole-word/phrase match, not a substring of another word.
        pattern = r"(?<![a-zA-Z])" + re.escape(alias) + r"(?![a-zA-Z])"
        if re.search(pattern, line_lower):
            candidates.append((test_name, alias, len(alias)))

    if candidates:
        max_len = max(c[2] for c in candidates)
        best_candidates = [(c[0], c[1]) for c in candidates if c[2] == max_len]

        if len(best_candidates) == 1:
            return best_candidates[0]

        # Multiple equally-long matches: prefer the one matching the current section.
        if category_hint:
            for test_name, alias in best_candidates:
                if REFERENCE_VALUES.get(test_name, {}).get("category") == category_hint:
                    return test_name, alias

        return best_candidates[0]

    # No exact match: fall back to fuzzy matching.
    return find_fuzzy_match(line_lower, alias_map)


def find_fuzzy_match(line_lower: str, alias_map: dict, min_ratio: float = 0.82):
    """Fuzzy-match each word in the line against known aliases, tolerating minor OCR misreads."""
    words = WORD_PATTERN.findall(line_lower)
    if not words:
        return None, None

    best_match = None
    best_word = None
    best_ratio = 0.0

    for alias, test_name in alias_map.items():
        if len(alias) < 4 or " " in alias:
            continue  # Skip multi-word and very short aliases for fuzzy matching.
        for word in words:
            ratio = difflib.SequenceMatcher(None, word, alias).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = test_name
                best_word = word

    if best_ratio >= min_ratio:
        return best_match, best_word
    return None, None


def extract_qualitative_value(line: str, alias: str):
    """Extract the patient's qualitative value by position (right after the test name), not by keyword search."""
    line_lower = line.lower()
    idx = line_lower.find(alias.lower())
    if idx == -1:
        return None, ""

    after = line[idx + len(alias):]
    after = re.sub(r"^[\s:.\-–]+", "", after)

    if not after.strip():
        return None, ""

    # Symbol-style values (e.g. "++", "(+)") are common in stool test reports.
    symbol_match = re.match(r"\(?(\++|-)\)?", after.strip())
    if symbol_match:
        remaining = after.strip()[symbol_match.end():]
        return symbol_match.group(1), remaining

    # Capture up to two words: enough to cover compound phrases like "semi formed".
    tokens = re.findall(r"[A-Za-z][A-Za-z.]*", after)
    if not tokens:
        return None, ""

    first_word = tokens[0].lower()

    if len(tokens) >= 2:
        second_word = tokens[1].lower()
        two_word_phrase = f"{first_word} {second_word}"

        if two_word_phrase in QUALITATIVE_KEYWORDS:
            remaining = after[after.lower().find(second_word) + len(second_word):]
            return two_word_phrase, remaining

        # Single-letter abbreviation (e.g. "E." in "E. Histolytica"): merge with next word.
        if len(first_word.rstrip(".")) <= 1 and first_word.endswith("."):
            remaining = after[after.lower().find(second_word) + len(second_word):]
            return two_word_phrase, remaining

    remaining = after[after.lower().find(first_word) + len(first_word):]
    return first_word, remaining


def extract_printed_qualitative_reference(remaining_text: str):
    """Try to find a known qualitative reference phrase in the text following the patient's value."""
    if not remaining_text or not remaining_text.strip():
        return None

    remaining_lower = remaining_text.lower()
    for keyword in QUALITATIVE_KEYWORDS:
        pattern = r"(?<![a-zA-Z])" + re.escape(keyword) + r"(?![a-zA-Z])"
        if re.search(pattern, remaining_lower):
            return keyword
    return None


def extract_printed_numeric_reference(line: str, value_end_idx: int):
    """Try to find a printed numeric range (e.g. "0-10") after the patient's value in the line."""
    remaining = line[value_end_idx:]
    range_pattern = re.compile(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)")
    match = range_pattern.search(remaining)
    if not match:
        return None
    try:
        low = float(match.group(1))
        high = float(match.group(2))
    except ValueError:
        return None
    if low >= high:
        return None
    return low, high


def sanity_fix_value(test_name: str, value: float):
    """Detect and correct common OCR decimal-point errors, or discard implausible values."""
    info = REFERENCE_VALUES.get(test_name)
    if not info:
        return value

    if "sex_specific" in info:
        lows = [v["low"] for v in info["sex_specific"].values()]
        highs = [v["high"] for v in info["sex_specific"].values()]
        low, high = min(lows), max(highs)
    else:
        low, high = info.get("low"), info.get("high")

    if low is None or high is None:
        return value

    plausible_low = low * 0.3
    plausible_high = high * 2

    if plausible_low <= value <= plausible_high:
        return value

    # Try correcting a likely "swallowed" decimal point (e.g. 335 -> 33.5).
    for divisor in (10, 100):
        corrected = value / divisor
        if plausible_low <= corrected <= plausible_high:
            return corrected

    return None


def extract_results_from_text(raw_text: str) -> list:
    """Scan each line of OCR text, match known tests, and extract their values (numeric or qualitative)."""
    alias_map = get_all_aliases()
    results = []
    matched_tests = set()
    current_section = None

    lines = raw_text.split("\n")

    for line in lines:
        line = clean_line(line)
        if not line or len(line) < 3:
            continue

        line_lower = line.lower()

        detected_section = detect_section(line_lower)
        if detected_section:
            current_section = detected_section

        test_name, matched_alias = find_matching_test(line_lower, alias_map, category_hint=current_section)

        if not test_name or test_name in matched_tests:
            continue

        info = REFERENCE_VALUES.get(test_name, {})
        value_type = info.get("value_type", "numeric")

        if value_type == "qualitative":
            value, remaining = extract_qualitative_value(line, matched_alias)
            if value is None:
                continue
            printed_ref = extract_printed_qualitative_reference(remaining)
            results.append({
                "test_name": test_name,
                "raw_line": line,
                "value": value,
                "value_type": "qualitative",
                "printed_reference": printed_ref,
            })
            matched_tests.add(test_name)
            continue

        # Default case: numeric test.
        number_match = NUMBER_PATTERN.search(line)
        if not number_match:
            continue

        try:
            value = float(number_match.group(1))
        except ValueError:
            continue

        value = sanity_fix_value(test_name, value)
        if value is None:
            continue

        printed_ref = extract_printed_numeric_reference(line, number_match.end())

        results.append({
            "test_name": test_name,
            "raw_line": line,
            "value": value,
            "value_type": "numeric",
            "printed_reference": printed_ref,
        })
        matched_tests.add(test_name)

    return results
