from wdp import Entry
from wdp.format import format_entry

color_entry = Entry("color")
color_entry.add_alternate_form("colour", "Chiefly British")
print(format_entry(color_entry, "en", "English"))

# Entry(word_form=color,
#       definitions=[],
#       alternate_forms=[AlternateForm(alternate_form=colour, description_of_use=Chiefly British)],
#       pronunciations=[])

bank_entry = Entry("bank")
bank_entry.add_pronunciation("beŋk", "IPA")
bank_entry.add_definition("A place where you put your money", part_of_speech="Noun")
bank_entry.add_definition(
    "A collection of annoying things, like syntax trees", part_of_speech="Verb"
)
bank_entry.add_definition("<Imaginary verbal sense of bank>", part_of_speech="Verb")
# Entry(word_form=bank,
#       definitions=[
#           Definition(definition=A place where you put your money, part_of_speech=n),
#           Definition(definition=A collection of annoying things, like syntax trees, part_of_speech=n),
#           Definition(definition=<Imaginary verbal sense of bank>, part_of_speech=v)
#       ],
#       alternate_forms=[],
#       pronunciations=[Pronunciation(pronunciation=beŋk, notation=IPA)])
print(format_entry(bank_entry, "en", "English"))

other_bank_entry = Entry("bank")
other_bank_entry.add_definition("The edges of a river")
# Entry(word_form=bank,
#       definitions=[Definition(definition=The edges of a river, part_of_speech=None)],
#       alternate_forms=[],
#       pronunciations=[])

# test_entry = Entry('User:AryamanA/test123', 'hi', 'Hindee')
# test_entry.add_definition('idk', part_of_speech='v')
# test_entry.upload()
#
# test_entry = Entry('User:AryamanA/test123', 'ur', 'Urdoo')
# test_entry.add_definition('idk2', part_of_speech='v')
# test_entry.upload()
