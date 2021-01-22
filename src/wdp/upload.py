import pywikibot


def upload(self):
    site = pywikibot.Site(code="en", fam="wiktionary")
    site.login()

    page = pywikibot.Page(site, self.word_form)
    order = re.findall(r"(^|\n)==([^=]*?)==[\n]", page.text)
    print(page.text)
    print(order)

    if order:
        for _, lang in order:
            if lang == self.lang_name:
                print(f'Entry already exists for {self.lang_name} at "{self.word_form}", skipping.')
                return
            elif lang > self.lang_name:
                page.text = page.text.replace(f"=={lang}==", f"{self.export()}\n\n----\n\n=={lang}==")
                break
    else:
        page.text = self.export()

    page.save(f"Automatic import of {self.lang_name} entry with WDP.")
