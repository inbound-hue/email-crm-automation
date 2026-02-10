# nationality_mapper.py
# Centralized nationality normalization for CRM (HubSpot-compatible)

def normalize_nationality(value: str):
    if not value:
        return None

    key = value.strip().lower()

    NATIONALITY_MAP = {

        # ===== EUROPE =====
        "german": "Deutschland",
        "deutsch": "Deutschland",
        "deutschland": "Deutschland",

        "austrian": "Österreich",
        "austria": "Österreich",

        "swiss": "Schweiz",
        "switzerland": "Schweiz",

        "french": "Frankreich",
        "france": "Frankreich",

        "italian": "Italien",
        "italy": "Italien",

        "spanish": "Spanien",
        "spain": "Spanien",

        "portuguese": "Portugal",
        "portugal": "Portugal",

        "dutch": "Niederlande",
        "netherlands": "Niederlande",
        "holland": "Niederlande",

        "belgian": "Belgien",
        "belgium": "Belgien",

        "luxembourg": "Luxemburg",
        "luxembourgish": "Luxemburg",

        "british": "Vereinigtes Königreich",
        "uk": "Vereinigtes Königreich",
        "united kingdom": "Vereinigtes Königreich",
        "england": "Vereinigtes Königreich",

        "irish": "Irland",
        "ireland": "Irland",

        "scottish": "Vereinigtes Königreich",
        "welsh": "Vereinigtes Königreich",

        "swedish": "Schweden",
        "sweden": "Schweden",

        "norwegian": "Norwegen",
        "norway": "Norwegen",

        "danish": "Dänemark",
        "denmark": "Dänemark",

        "finnish": "Finnland",
        "finland": "Finnland",

        "polish": "Polen",
        "poland": "Polen",

        "czech": "Tschechische Republik",
        "czech republic": "Tschechische Republik",

        "slovak": "Slowakei",
        "slovakia": "Slowakei",

        "hungarian": "Ungarn",
        "hungary": "Ungarn",

        "romanian": "Rumänien",
        "romania": "Rumänien",

        "bulgarian": "Bulgarien",
        "bulgaria": "Bulgarien",

        "croatian": "Kroatien",
        "croatia": "Kroatien",

        "serbian": "Serbien",
        "serbia": "Serbien",

        "slovenian": "Slowenien",
        "slovenia": "Slowenien",

        "greek": "Griechenland",
        "greece": "Griechenland",

        "estonian": "Estland",
        "estonia": "Estland",

        "latvian": "Lettland",
        "latvia": "Lettland",

        "lithuanian": "Litauen",
        "lithuania": "Litauen",

        "ukrainian": "Ukraine",
        "ukraine": "Ukraine",

        "russian": "Russische Föderation",
        "russia": "Russische Föderation",

        # ===== ASIA =====
        "indian": "Indien",
        "india": "Indien",
        "indisch": "Indien",

        "pakistani": "Pakistan",
        "pakistan": "Pakistan",

        "bangladeshi": "Bangladesch",
        "bangladesh": "Bangladesch",

        "chinese": "China",
        "china": "China",

        "japanese": "Japan",
        "japan": "Japan",

        "korean": "Korea, Republik",
        "south korea": "Korea, Republik",

        "vietnamese": "Vietnam",
        "vietnam": "Vietnam",

        "thai": "Thailand",
        "thailand": "Thailand",

        "indonesian": "Indonesien",
        "indonesia": "Indonesien",

        "malaysian": "Malaysia",
        "malaysia": "Malaysia",

        "singaporean": "Singapur",
        "singapore": "Singapur",

        "filipino": "Philippinen",
        "philippines": "Philippinen",

        "sri lankan": "Sri Lanka",
        "sri lanka": "Sri Lanka",

        # ===== MIDDLE EAST =====
        "turkish": "Türkei",
        "turkey": "Türkei",

        "israeli": "Israel",
        "israel": "Israel",

        "emirati": "Vereinigte Arabische Emirate",
        "uae": "Vereinigte Arabische Emirate",

        "saudi": "Saudi-Arabien",
        "saudi arabia": "Saudi-Arabien",

        # ===== AFRICA =====
        "south african": "Südafrika",
        "south africa": "Südafrika",
        "südafrika": "Südafrika",

        "nigerian": "Nigeria",
        "nigeria": "Nigeria",

        "egyptian": "Ägypten",
        "egypt": "Ägypten",

        "kenyan": "Kenia",
        "kenya": "Kenia",

        # ===== AMERICAS =====
        "american": "Vereinigte Staaten",
        "usa": "Vereinigte Staaten",
        "united states": "Vereinigte Staaten",

        "canadian": "Kanada",
        "canada": "Kanada",

        "mexican": "Mexiko",
        "mexico": "Mexiko",

        "brazilian": "Brasilien",
        "brazil": "Brasilien",

        "argentinian": "Argentinien",
        "argentina": "Argentinien",

        "chilean": "Chile",
        "chile": "Chile",

        "colombian": "Kolumbien",
        "colombia": "Kolumbien",

        # ===== OCEANIA =====
        "australian": "Australien",
        "australia": "Australien",

        "new zealand": "Neuseeland",
        "new zealander": "Neuseeland",
    }

    return NATIONALITY_MAP.get(key, value)
