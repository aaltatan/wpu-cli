# ruff: noqa: RUF001

_arabic_letters = {
    "ا": "\u0627",  # Alif
    "أ": "\u0623",  # Alif with hamza above
    "إ": "\u0625",  # Alif with hamza below
    "آ": "\u0622",  # Alif with madda
    "ب": "\u0628",  # Ba
    "ت": "\u062a",  # Ta
    "ث": "\u062b",  # Tha
    "ج": "\u062c",  # Jim
    "ح": "\u062d",  # Ha
    "خ": "\u062e",  # Kha
    "د": "\u062f",  # Dal
    "ذ": "\u0630",  # Dhal
    "ر": "\u0631",  # Ra
    "ز": "\u0632",  # Zay
    "س": "\u0633",  # Sin
    "ش": "\u0634",  # Shin
    "ص": "\u0635",  # Sad
    "ض": "\u0636",  # Dad
    "ط": "\u0637",  # Ta
    "ظ": "\u0638",  # Za
    "ع": "\u0639",  # Ain
    "غ": "\u063a",  # Ghain
    "ف": "\u0641",  # Fa
    "ق": "\u0642",  # Qaf
    "ك": "\u0643",  # Kaf
    "ل": "\u0644",  # Lam
    "م": "\u0645",  # Mim
    "ن": "\u0646",  # Nun
    "ه": "\u0647",  # Ha
    "و": "\u0648",  # Waw
    "ؤ": "\u0624",  # Waw with hamza
    "ي": "\u064a",  # Ya
    "ئ": "\u0626",  # Ya with hamza
    "ى": "\u0649",  # Alif maqsura
    "ة": "\u0629",  # Ta marbuta
}

# Additional Arabic letters (less common or regional)
_arabic_extended_letters = {
    "پ": "\u067e",  # Peh (Persian/Farsi)
    "چ": "\u0686",  # Cheh (Persian/Farsi)
    "ژ": "\u0698",  # Zheh (Persian/Farsi)
    "گ": "\u06af",  # Gaf (Persian/Farsi)
    "ڤ": "\u06a4",  # Veh (Arabic)
    "ڨ": "\u06a8",  # Qaf with three dots
    "ڭ": "\u06ad",  # Ng
    "ڠ": "\u06a0",  # Ain with three dots
    "ڢ": "\u06a2",  # Feh with dot moved
    "ڧ": "\u06a7",  # Qaf with dot above
    "ک": "\u06a9",  # Keheh (Persian style Kaf)
    "ی": "\u06cc",  # Farsi Yeh
    "ە": "\u06d5",  # Ae
    "ێ": "\u06ce",  # Yeh with small V
    "ۆ": "\u06c6",  # Oe
    "ۇ": "\u06c7",  # U
    "ۈ": "\u06c8",  # Yu
    "ۋ": "\u06cb",  # Ve
    "ې": "\u06d0",  # E
    "ى": "\u0649",  # Alif maqsura
    "ٸ": "\u0678",  # High hamza ya
    "ٹ": "\u0679",  # Tta
    "ڈ": "\u0688",  # Ddal
    "ڑ": "\u0691",  # Rra
    "ٻ": "\u067b",  # Bbeh
    "ڀ": "\u0680",  # Hheh
    "ٺ": "\u067a",  # Tteheh
    "ٿ": "\u067f",  # Tteh
    "ڃ": "\u0683",  # Nyeh
    "ڄ": "\u0684",  # Dyeh
    "څ": "\u0685",  # Hah with three dots
}

# Arabic digits
_arabic_digits = {
    "٠": "\u0660",  # 0
    "١": "\u0661",  # 1
    "٢": "\u0662",  # 2
    "٣": "\u0663",  # 3
    "٤": "\u0664",  # 4
    "٥": "\u0665",  # 5
    "٦": "\u0666",  # 6
    "٧": "\u0667",  # 7
    "٨": "\u0668",  # 8
    "٩": "\u0669",  # 9
}

# Arabic punctuation and symbols
_arabic_symbols = {
    "،": "\u060c",  # Arabic comma
    "؛": "\u061b",  # Arabic semicolon
    "؟": "\u061f",  # Arabic question mark
    "ء": "\u0621",  # Hamza
    "ـ": "\u0640",  # Tatweel (kashida)
    "٪": "\u066a",  # Percent sign
    "٫": "\u066b",  # Decimal separator
    "٬": "\u066c",  # Thousands separator
    "ﷺ": "\ufdfa",  # Sallallahou Alayhe Wasallam
    "ﷲ": "\ufdf2",  # Allah
    "ﷻ": "\ufdfb",  # Jallajalalahou
    "﷽": "\ufdfd",  # Bismillah
}

# Combined dictionary (all Arabic characters)
_arabic_characters = {
    **_arabic_letters,
    **_arabic_extended_letters,
    **_arabic_digits,
    **_arabic_symbols,
}


def get_arabic_unicode(letter: str) -> str:
    if letter not in _arabic_characters:
        message = f"Arabic letter '{letter}' not found"
        raise ValueError(message)

    return _arabic_characters[letter]
