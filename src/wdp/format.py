from typing import List, Tuple, Dict, Any
import re
from wdp.models import Word
from jinja2 import Template

# TODO: add IPA handling e.g. {{IPA|en|foo|bar}}
from wdp.validate import validate_word

ENTRY_TEMPLATE = Template(
    """=={{lang_name}}==

{% for word in words %}
    {% if words|length > 1 %}
        {{ section(2, "Etymology " ~ loop.index) }}
    {% endif %}

    {% if word['alternative_forms'] %}
        {{ section(3, "Alternative forms") }}
        {% for form in word['alternative_forms'] %}
            * {{LL}}alter|{{lang_code}}|{{form.alternative_form}}||{{form.description_of_use}}{{RR}}
        {% endfor %}
    {% endif %}
    
    {% if word['description'] %}
      {{ section(3, "Description") }}
      {{ word['description'] }}
    {% endif %}
    
    {% if word['etymology'] %}
      {{ section(3, "Etymology") }}
      {{ word['etymology'] }}
    {% endif %}

    {% if word['pronunciations'] %}
        {{ section(3, "Pronunciation") }}
        {% for pronunciation in word['pronunciations'] %}
            {% if pronunciation.notation|lower == "ipa" %}
                * {{LL}}IPA|{{lang_code}}|{{pronunciation.pronunciation}}{{RR}}
            {% else %}
                * {{pronunciation.pronunciation}}
            {% endif %}
        {% endfor %}
    {% endif %}

    {% for pos in word["grouped_definitions"] %}
        {{ section(3, pos.capitalize()) }}
        {{LL}}head|{{lang_code}}|{{pos}}{{RR}}
        
        {% for definition in word["grouped_definitions"][pos] %} 
            # {{definition.definition}}
            {% for usage_example in definition.usage_examples %}
            #: {{LL}}uxi|{{lang_code}}|{{usage_example.text}}|{{usage_example.translation}}{{RR}}
            {% endfor %}
        {% endfor %}
    {% endfor %}
    
    {% if word['usage_notes'] %}
      {{ section(3, "Usage notes") }}
      {{ word['usage_notes'] }}
    {% endif %}
    
    {% if word['conjugation'] %}
      {{ section(3, "Conjugation") }}
      {{ word['conjugation'] }}
    {% endif %}
    
    {% if word['declension'] %}
      {{ section(3, "Declension") }}
      {{ word['declension'] }}
    {% endif %}
    
    {% if word['inflection'] %}
      {{ section(3, "Inflection") }}
      {{ word['inflection'] }}
    {% endif %}
    
    {% if word['references'] %}
      {{ section(3, "References") }}
      {{ word['references'] }}
    {% endif %}
{% endfor %}
"""
)


def group_definitions_by_pos(context: dict):
    """
    Return a dict mapping from part of speech to a list of all the definitions with that part of speech.
    """
    definitions = context["definitions"]
    parts_of_speech = set(definition["part_of_speech"] for definition in definitions)

    return {pos.lower(): [d for d in definitions if d["part_of_speech"] == pos] for pos in parts_of_speech}


def format_entry(word_group: List[Word], lang_code: str, lang_name: str) -> Tuple[str, str]:
    """
    Turn a list of Word objects into Wikitext.
    """
    # the dict we will use to render the jinja template
    context: Dict[str, Any] = dict(
        lang_code=lang_code,
        lang_name=lang_name,
        words=[],
    )

    # iterate over Word objects
    for word in word_group:
        word_context = word.to_dict()
        # a Word will in general have many definitions with different parts of speech--separate them
        word_context["grouped_definitions"] = group_definitions_by_pos(word_context)
        context["words"].append(word_context)

    def section(depth, content):
        """
        Formats string according to whether there is more than one word group or not.
        Args:
            depth:   the level the section has in an entry with a single etymology
            content: a string to be displayed in a header

        Returns: Formatted section header
        """
        c = len(word_group) > 1
        s = "=" * (depth + c)
        return s + content + s

    output = ENTRY_TEMPLATE.render(section=section, LL="{{", RR="}}", **context)
    # undo formatting that made the jinja template easier to read
    output = "\n".join(re.sub(r"^ +", "", line) for line in output.split("\n"))
    output = re.sub(r"\n\n+#", "\n#", output)
    output = re.sub(r"=\n+=", "=\n=", output)
    output = re.sub(r"\n\n+", "\n\n", output)
    output = re.sub(r"===\n\n", "===\n", output)
    output = re.sub(r"=\n=", "=\n\n=", output) # tyography: an empty section should have extra newline
    output = re.sub(r"({{head\|[^\n]*})\n#", r"\1\n\n#", output) # headword template should have extra newline after
    return word_group[0].word_form, output


def group_words(words: List[Word]) -> List[List[Word]]:
    """ Group words based on their word_form attribute """
    word_forms = set(w.word_form for w in words)
    return [[w for w in words if w.word_form == word_form] for word_form in word_forms]


def format_entries(words: List[Word], lang_code: str, lang_name: str) -> List[Tuple[str, str]]:
    for word in words:
        validate_word(word)
    grouped_words = group_words(words)
    formatted_entries = [format_entry(word_group, lang_code, lang_name) for word_group in grouped_words]
    return formatted_entries
