"""Module with anki models"""

import genanki


class GermanModel(genanki.Model):
    def __init__(self, model_id):
        # Predefined values for name, fields, and templates
        name = "German Vocabulary Model"
        fields = [
            {"name": "German Word"},
            {"name": "Translation"},
            {"name": "German Sentence"},
            {"name": "English Sentence"},
            {"name": "Other Forms"},
        ]
        templates = [
            {
                "name": "Card 1",
                "qfmt": "{{German Word}}<br><br>{{German Sentence}}<br><br><b>Other forms:</b> {{Other Forms}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Translation}}<br><br>{{English Sentence}}',
            },
            {
                "name": "Card 2: English to German",
                "qfmt": "{{Translation}}<br><br>{{English Sentence}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{German Word}}<br><br>{{German Sentence}}<br><br><b>Other forms:</b> {{Other Forms}}',
            },
        ]

        # Initialize the parent class (genanki.Model) with these values
        super().__init__(
            model_id=model_id, name=name, fields=fields, templates=templates
        )
