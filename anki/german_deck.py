"""Module for creating and managing Anki decks with German vocabulary notes.

This module provides a `GermanDeck` class to create Anki decks, add notes,
save them to a SQLite database, and export them as Anki package files (.apkg).
"""

from pathlib import Path

import genanki

from anki.german_deck_db import GermanDeckDatabase
from anki.german_model import GermanModel


class GermanDeck:
    def __init__(self, deck_id: int, model_id: int, file_name: str) -> None:
        """Initialize the GermanDeck with deck ID, model ID, and file name.

        Args:
            deck_id (int): The unique ID for the Anki deck.
            model_id (int): The unique ID for the Anki model.
            file_name (str): The base file name used to store the deck.
        """
        self.deck_id = deck_id
        self.model = GermanModel(model_id)
        self.deck = genanki.Deck(deck_id, "German Vocabulary")

        # Store the file name and derive paths for .db and .apkg files
        self.db_path = Path(file_name).with_suffix(".db")
        self.apkg_path = Path(file_name).with_suffix(".apkg")

    def add_note(
        self,
        german_word: str,
        translation: str,
        german_sentence: str,
        english_sentence: str,
        other_forms: str,
    ) -> None:
        """Add a new note to the Anki deck.

        Args:
            german_word (str): The German word to be added.
            translation (str): The English translation of the German word.
            german_sentence (str): A German sentence using the word.
            english_sentence (str): The English translation of the German sentence.
            other_forms (str): Other grammatical forms of the German word.
        """
        note = genanki.Note(
            model=self.model,
            fields=[
                german_word,
                translation,
                german_sentence,
                english_sentence,
                other_forms,
            ],
        )
        self.deck.add_note(note)

    def save_deck(self) -> None:
        """Save the deck to a SQLite database and export it as an Anki package (.apkg) file."""
        # Initialize the database connection
        db = GermanDeckDatabase(self.db_path)

        # Save each note in the deck to the database
        for note in self.deck.notes:
            db.add_note(
                german_word=note.fields[0],
                translation=note.fields[1],
                german_sentence=note.fields[2],
                english_sentence=note.fields[3],
                other_forms=note.fields[4],
            )

        # Save the deck to an Anki package file
        genanki.Package(self.deck).write_to_file(self.apkg_path)

    def load_deck(self) -> None:
        """Load notes from a SQLite database and add them to the Anki deck."""
        # Initialize the database connection
        db = GermanDeckDatabase(self.db_path)

        # Load notes from the database
        notes = db.load_notes()

        # Convert each database record into a genanki.Note and add it to the deck
        for note_model in notes:
            note = genanki.Note(
                model=self.model,
                fields=[
                    note_model.german_word,
                    note_model.translation,
                    note_model.german_sentence,
                    note_model.english_sentence,
                    note_model.other_forms,
                ],
            )
            self.deck.add_note(note)

    def save_to_apkg(self) -> None:
        """Save the Anki deck as an Anki package (.apkg) file."""
        genanki.Package(self.deck).write_to_file(self.apkg_path)


# Example usage:
if __name__ == "__main__":
    # Example deck and model IDs
    deck_id = 2059400110  # Example deck ID
    model_id = 1607392319  # Example model ID

    # Initialize the GermanDeck with a base file name
    german_deck = GermanDeck(deck_id, model_id, "german_vocabulary")

    # Add notes to the deck
    german_deck.add_note(
        german_word="vereinbaren",
        translation="to agree",
        german_sentence="Wir haben ein Treffen vereinbart.",
        english_sentence="We agreed on a meeting.",
        other_forms="vereinbarte, vereinbart",
    )

    german_deck.add_note(
        german_word="das Mädchen",
        translation="the girl",
        german_sentence="Das Mädchen spielt im Park.",
        english_sentence="The girl is playing in the park.",
        other_forms="die Mädchen",
    )

    # Save the deck and store the notes in a SQLite database and .apkg file
    german_deck.save_deck()

    # Load the deck from the SQLite database
    new_german_deck = GermanDeck(deck_id, model_id, "german_vocabulary")
    new_german_deck.load_deck()

    # Optionally save the reloaded deck to a new .apkg file to verify it works
    new_german_deck.save_to_apkg()
