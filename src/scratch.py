from wdp import Entry

color_entry = Entry('color', 'en', 'English')
color_entry.add_alternate_form('colour', 'Chiefly British')

# Entry(word_form=color,
#       definitions=[],
#       alternate_forms=[AlternateForm(alternate_form=colour, description_of_use=Chiefly British)],
#       pronunciations=[])

bank_entry = Entry('bank', 'en', 'English')
bank_entry.add_pronunciation('beŋk', 'IPA')
bank_entry.add_definition('A place where you put your money', part_of_speech='n')
bank_entry.add_definition(['A collection of annoying things, like syntax trees', '<Other sense tied to this part of speech>'], part_of_speech='n')
bank_entry.add_definition('<Imaginary verbal sense of bank>', part_of_speech='v')
print(bank_entry.export())
# Entry(word_form=bank,
#       definitions=[
#           Definition(definition=A place where you put your money, part_of_speech=n),
#           Definition(definition=A collection of annoying things, like syntax trees, part_of_speech=n),
#           Definition(definition=<Imaginary verbal sense of bank>, part_of_speech=v)
#       ],
#       alternate_forms=[],
#       pronunciations=[Pronunciation(pronunciation=beŋk, notation=IPA)])

other_bank_entry = Entry('bank', 'en', 'English')
other_bank_entry.add_definition('The edges of a river')
# Entry(word_form=bank,
#       definitions=[Definition(definition=The edges of a river, part_of_speech=None)],
#       alternate_forms=[],
#       pronunciations=[])

test_entry = Entry('User:AryamanA/test123', 'hi', 'Hindee')
test_entry.add_definition('idk', part_of_speech='v')
test_entry.upload()

test_entry = Entry('User:AryamanA/test123', 'ur', 'Urdoo')
test_entry.add_definition('idk2', part_of_speech='v')
test_entry.upload()