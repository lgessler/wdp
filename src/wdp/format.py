from typing import List
import re
from wdp.models import Entry
from jinja2 import Template

# TODO: add IPA handling e.g. {{IPA|en|foo|bar}}
ENTRY_TEMPLATE = Template(
    """=={{lang_name}}==
{% if alternate_forms %}
===Alternative forms===
{% for form in alternate_forms %}
* {{'{{'}}alter|{{form.lang_code}}|{{form.alternate_form}}|{{form.description_of_use}}{{'}}'}}
{% endfor %}
{% endif %}

{% if pronunciations %}
===Pronunciations===
{% for pronunciation in pronunciations %}
* {{pronunciation.pronunciation}}
{% endfor %}
{% endif %}

{% for pos in grouped_definitions %}
==={{pos}}===
{{'{{'}}head|{{lang_code}}|{{pos}}{{'}}'}}
{% for definition in grouped_definitions[pos] %} 
# {{definition.definition}}{% endfor %}
{% endfor %}
"""
)


def group_definitions_by_pos(context: dict):
    definitions = context["definitions"]
    parts_of_speech = set(definition["part_of_speech"] for definition in definitions)

    context["grouped_definitions"] = {
        pos.capitalize(): [d for d in definitions if d["part_of_speech"] == pos] for pos in parts_of_speech
    }


def format_entry(entry: Entry, lang_code: str, lang_name: str):
    context = entry.to_dict()
    context["lang_code"] = lang_code
    context["lang_name"] = lang_name
    group_definitions_by_pos(context)

    output = ENTRY_TEMPLATE.render(**context)
    output = re.sub(r"\n\n+", "\n\n", output)
    output = re.sub(r"===\n\n", "===\n", output)
    return (entry.word_form, output)


def format_entries(entries: List[Entry], lang_code: str, lang_name: str):
    # TODO: need to find entries with the same form and make sure we add Etymology 1, Etymology 2, etc.
    formatted_entries = [format_entry(entry, lang_code, lang_name) for entry in entries]
    return formatted_entries
