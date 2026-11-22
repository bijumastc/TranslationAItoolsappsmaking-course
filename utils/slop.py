"""Rule-based translation slop checks that run without any API key.

These are signals, not verdicts. Every flag must be checked by a human.
"""
import re

MAL_RANGE = re.compile(r"[ഀ-ൿ]")
LATIN_WORD = re.compile(r"\b[A-Za-z][A-Za-z'\-]+\b")
NUMBER = re.compile(r"\d+(?:[.,:/-]\d+)*")
SENT_SPLIT = re.compile(r"(?<=[.!?।])\s+|\n+")

# Malayalam digits ൦-൯ map to 0-9 so "൨൦൨൬" and "2026" compare as equal.
MAL_DIGITS = str.maketrans("൦൧൨൩൪൫൬൭൮൯", "0123456789")

# A starter list of stock English filler often seen in AI output. Students extend it.
FILLER = [
    "delve", "it is important to note", "in today's world", "tapestry", "navigate the",
    "a testament to", "plays a crucial role", "in conclusion", "furthermore", "seamless",
    "embark on", "unlock the", "vibrant", "rich cultural heritage",
]


def sentences(text: str) -> list:
    return [s.strip() for s in SENT_SPLIT.split(text.strip()) if s.strip()]


def script_of(text: str) -> str:
    mal = len(MAL_RANGE.findall(text))
    lat = len(re.findall(r"[A-Za-z]", text))
    if mal == 0 and lat == 0:
        return "unknown"
    return "Malayalam" if mal >= lat else "English"


def numbers(text: str) -> set:
    return set(NUMBER.findall(text.translate(MAL_DIGITS)))


def run_checks(source: str, target: str) -> list:
    """Return a list of dicts: check, result, severity, evidence."""
    flags = []
    src_s, tgt_s = sentences(source), sentences(target)
    src_script, tgt_script = script_of(source), script_of(target)

    # 1. Script: the target should be in the other script.
    if src_script == tgt_script and src_script != "unknown":
        flags.append({"check": "Script", "severity": "critical",
                      "result": f"Source and target are both {src_script}.",
                      "evidence": "Was the text actually translated?"})

    # 2. Numbers, dates, figures must survive translation.
    missing = numbers(source) - numbers(target)
    extra = numbers(target) - numbers(source)
    if missing:
        flags.append({"check": "Numbers dropped", "severity": "major",
                      "result": "Numbers in the source are missing in the target.",
                      "evidence": ", ".join(sorted(missing))})
    if extra:
        flags.append({"check": "Numbers added", "severity": "major",
                      "result": "Numbers appear in the target that are not in the source.",
                      "evidence": ", ".join(sorted(extra))})

    # 3. Sentence count: big gaps suggest omission or addition.
    if src_s and tgt_s:
        ratio = len(tgt_s) / len(src_s)
        if ratio < 0.7:
            flags.append({"check": "Possible omission", "severity": "major",
                          "result": f"Source has {len(src_s)} sentences, target has {len(tgt_s)}.",
                          "evidence": "Compare the two side by side."})
        elif ratio > 1.4:
            flags.append({"check": "Possible addition", "severity": "minor",
                          "result": f"Source has {len(src_s)} sentences, target has {len(tgt_s)}.",
                          "evidence": "Look for explanations the source did not have."})

    # 4. Length ratio (characters). Malayalam is often longer than English, so the band is wide.
    if source.strip() and target.strip():
        lr = len(target) / len(source)
        if lr < 0.5 or lr > 2.5:
            flags.append({"check": "Length", "severity": "minor",
                          "result": f"Target is {lr:.1f}× the source length.",
                          "evidence": "Unusual ratio: check for dropped or padded content."})

    # 5. English words left in a Malayalam target (names are fine; untranslated phrases are not).
    if tgt_script == "Malayalam":
        leftovers = sorted({w for w in LATIN_WORD.findall(target) if len(w) > 3})
        if leftovers:
            flags.append({"check": "English left in target", "severity": "minor",
                          "result": f"{len(leftovers)} English word(s) remain.",
                          "evidence": ", ".join(leftovers[:15]) + " — names and brand terms may be fine."})

    # 6. Stock AI filler (English side).
    eng_text = target if tgt_script == "English" else source
    hits = [p for p in FILLER if p in eng_text.lower()]
    if hits:
        flags.append({"check": "Stock AI phrasing", "severity": "minor",
                      "result": "Phrases common in AI-generated English.",
                      "evidence": ", ".join(hits)})

    if not flags:
        flags.append({"check": "Rule checks", "severity": "none",
                      "result": "No rule-based flags. This does NOT mean the translation is good.",
                      "evidence": "Run the AI review and read it yourself."})
    return flags


REVIEW_SYSTEM = """You are a strict English–Malayalam translation reviewer using MQM.
Compare SOURCE and TARGET. Return JSON only, with this shape:
{"back_translation": str,
 "issues": [{"sentence": int, "category": "omission|addition|meaning change|calque|register|terminology|name/number|fluency",
             "severity": "minor|major|critical", "evidence": str, "suggestion": str}],
 "verdict": "publish|revise|retranslate",
 "reason": str}
Quote evidence from the texts for every issue. If unsure about a Malayalam usage, say so in evidence.
Never invent issues to fill the list; an empty list is allowed."""
