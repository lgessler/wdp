from wdp import Entry, format_entries, upload_formatted_entries

# Step 1: build entries
color_entry = Entry("color")
color_entry.add_alternate_form("colour", "Chiefly British")

bank_entry = Entry("bank")
bank_entry.add_pronunciation("beŋk", "IPA")
bank_entry.add_definition("A place where you put your money", part_of_speech="Noun")
bank_entry.add_definition("A collection of annoying things, like syntax trees", part_of_speech="Verb")
bank_entry.add_definition("<Imaginary verbal sense of bank>", part_of_speech="Verb")

# other_bank_entry = Entry("bank")
# other_bank_entry.add_definition("The edges of a river")

# Step 2: format the entries into a list of 2-tuples: first is the word's form, second is the mwtext for the entry
entries = [color_entry, bank_entry]
formatted_entries = format_entries(entries, "en", "English")

# Step 3: upload (page_override forces all word forms to be inserted into a debug page)
upload_formatted_entries(formatted_entries, 'English', page_override='User:AryamanA/test123')
print(formatted_entries[0])
