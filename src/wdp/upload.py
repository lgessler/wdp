import re
from typing import List, Tuple

import pywikibot


def upload_formatted_entries(
    formatted_entries: List[Tuple[str, str]],
    lang_name: str,
    wiktionary_language: str = "en",
    page_prefix: str = "",
):
    site = pywikibot.Site(code=wiktionary_language, fam="wiktionary")
    site.login()

    for word_form, entry_string in formatted_entries:
        page = pywikibot.Page(site, page_prefix + word_form)
        order = re.findall(r"(^|\n)==([^=]*?)==[\n]", page.text)

        if order:
            outer_continue = False
            for _, lang in order:
                if lang == lang_name:
                    print(f'Entry already exists for {lang_name} at "{word_form}", skipping.')
                    outer_continue = True
                    break
                elif lang > lang_name:
                    page.text = page.text.replace(f"=={lang}==", f"{entry_string}\n\n----\n\n=={lang}==")
                    break
            if outer_continue:
                continue
        else:
            page.text = entry_string

        page.save(f"Automatic import of {lang_name} entry with WDP.")
