from wdp import Word, format_entries, upload_formatted_entries

# Step 1: build entries
color_word = Word("color")
color_word.add_alternate_form("colour", "Chiefly British")
color_word.add_definition("colordef", "Noun")

bank_word = Word("bank")
bank_word.add_pronunciation("beŋk", "IPA")
bank_word.add_definition("A place where you put your money", "Noun")
bank_word.add_definition("A collection of annoying things, like syntax trees", "Noun")
bank_word.add_definition("<Imaginary verbal sense of bank>", "Verb")
bank_word.add_alternate_form("moneyplace")
print("Step 1 output:")
print(bank_word)
print()

other_bank_word = Word("bank")
other_bank_word.add_definition("The edges of a river", 'Noun')

# Step 2: format the entries into a list of 2-tuples: first is the word's form, second is the mwtext for the word
entries = [color_word, bank_word, other_bank_word]
formatted_entries = format_entries(entries, "en", "English")
print("Step 2 output:")
print('#############', formatted_entries[0][0])
print(formatted_entries[0][1])
print()
print('#############', formatted_entries[1][0])
print(formatted_entries[1][1])
print()

# Step 3: upload (page_override forces all word forms to be inserted into a debug page)
upload_formatted_entries(formatted_entries, "English", page_prefix="User:Ldgessler/")
print(formatted_entries[0])
