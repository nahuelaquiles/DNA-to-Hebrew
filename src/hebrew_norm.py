import re

# Optional: normalize final forms to standard forms for matching
FINAL_MAP = str.maketrans({
    "ך":"כ",  # ךכ
    "ם":"מ",  # םמ
    "ן":"נ",  # ןנ
    "ף":"פ",  # ףפ
    "ץ":"צ",  # ץצ
})

# Remove niqqud/cantillation
NIQQUD_RE = re.compile(r"[\u0591-\u05C7]")

def norm_hebrew(s: str, unify_finals: bool = True) -> str:
    s = NIQQUD_RE.sub("", s)
    if unify_finals:
        s = s.translate(FINAL_MAP)
    # keep only Hebrew letters
    s = re.sub(r"[^\u05D0-\u05EA]", "", s)
    return s
