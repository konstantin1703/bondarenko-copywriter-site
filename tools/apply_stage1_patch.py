from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly 1 occurrence, found {count}: {old[:80]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def replace_count(path: str, old: str, new: str, expected: int) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrences, found {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


# Data correctness: Serbia calling code typo.
replace_once("v4.js", '"dial":"+381 p"', '"dial":"+381"')

# Static versioned JSON should be cacheable; runtime already keeps an in-memory cache too.
replace_count("v4-locale-v1.js", ",{cache:'no-store'}", "", 2)

# Give the standalone phone input an explicit accessible name and hint relationship.
replace_once(
    "index.html",
    '<div class="request-field full"><span>ТЕЛЕФОН</span><div class="phone-combo"><button class="phone-prefix" id="phoneRegionButton" type="button" aria-haspopup="dialog"><span class="region-symbol is-empty" id="phoneFlag" aria-hidden="true"><svg class="region-globe" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.75"></circle><path d="M3.5 12h17"></path><path d="M12 3.25c2.55 2.35 3.85 5.28 3.85 8.75S14.55 18.4 12 20.75C9.45 18.4 8.15 15.47 8.15 12S9.45 5.6 12 3.25Z"></path></svg></span><b id="phoneDial">Код</b><i>⌄</i></button><input id="reqPhone" name="phone" autocomplete="tel-national" inputmode="tel" required placeholder="Номер телефона"/></div><small class="field-hint" id="phoneHint">Выбери страну или телефонный код.</small></div>',
    '<div class="request-field full"><span id="reqPhoneLabel">ТЕЛЕФОН</span><div class="phone-combo"><button class="phone-prefix" id="phoneRegionButton" type="button" aria-haspopup="dialog"><span class="region-symbol is-empty" id="phoneFlag" aria-hidden="true"><svg class="region-globe" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.75"></circle><path d="M3.5 12h17"></path><path d="M12 3.25c2.55 2.35 3.85 5.28 3.85 8.75S14.55 18.4 12 20.75C9.45 18.4 8.15 15.47 8.15 12S9.45 5.6 12 3.25Z"></path></svg></span><b id="phoneDial">Код</b><i>⌄</i></button><input id="reqPhone" name="phone" autocomplete="tel-national" inputmode="tel" required placeholder="Номер телефона" aria-labelledby="reqPhoneLabel" aria-describedby="phoneHint"/></div><small class="field-hint" id="phoneHint">Выбери страну или телефонный код.</small></div>',
)

# Bust caches for every stage-1 runtime/style touched in this pass.
replace_once("index.html", "v4.css?v=23", "v4.css?v=23")  # guard that the expected release shell is still present
replace_once("index.html", "v4-request-modal-v1.css?v=5", "v4-request-modal-v1.css?v=6")
replace_once("index.html", "v4.js?v=17", "v4.js?v=18")
replace_once("index.html", "v4-locale-v1.js?v=5", "v4-locale-v1.js?v=6")
replace_once("index.html", "v4-request-modal-v1.js?v=4", "v4-request-modal-v1.js?v=5")

print("Stage 1 patch applied successfully")
