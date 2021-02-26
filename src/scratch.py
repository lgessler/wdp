from pprint import pprint

from wdp import Word, format_entries, export_words, import_words
from wdp.upload import upload_formatted_entries
from wdp.models import UsageExample

# Step 1: build entries
color_word = Word("color")
color_word.add_alternative_form("colour", "Chiefly British")
color_word.add_definition("colordef", "Noun")

bank_word = Word("bank")
bank_word.add_pronunciation("/beŋk/")
bank_word.add_definition("A place where you put your money", "Noun", [UsageExample('I live in the bank', 'this is a translation!')])
bank_word.add_definition("A collection of annoying things, like syntax trees", "Noun")
bank_word.add_definition("<Imaginary verbal sense of bank>", "Verb")
bank_word.add_alternative_form("moneyplace")
bank_word.set_etymology("Test etymology")
bank_word.set_usage_notes("Test usage note")
bank_word.set_references("Test references")
bank_word.set_description("Test description")
print("Step 1 output:")
print(bank_word)
print(bank_word.pretty_format())
print()

other_bank_word = Word("bank")
other_bank_word.add_definition("The edges of a river", "Noun")

# Step 2: format the entries into a list of 2-tuples: first is the word's form, second is the mwtext for the word
words = [color_word, bank_word, other_bank_word]
export_words(words, "foo")
words = import_words("foo.zip")

formatted_entries = format_entries(words, "en", "English")
print("Step 2 output:")
print("#############", formatted_entries[0][0])
print(formatted_entries[0][1])
print("/############")
print("#############", formatted_entries[1][0])
print(formatted_entries[1][1])
print("/############")


# Step 3: upload (page_override forces all word forms to be inserted into a debug page)
upload_formatted_entries(formatted_entries, "English", page_prefix="User:Ldgessler/")
