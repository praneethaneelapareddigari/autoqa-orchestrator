from selenium.common.exceptions import NoSuchElementException

FALLBACKS = [
    lambda d, sel: d.find_element('css selector', sel),
    lambda d, sel: d.find_element('xpath', f"//*[@data-test='{sel}']"),
    lambda d, sel: d.find_element('xpath', f"//*[contains(@id,'{sel}') or contains(@class,'{sel}')]")
]

def heal_find(driver, selector):
    last_exc = None
    for strat in FALLBACKS:
        try:
            return strat(driver, selector)
        except Exception as e:
            last_exc = e
            continue
    if last_exc:
        raise last_exc
    raise NoSuchElementException(selector)
