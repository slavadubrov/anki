from unittest.mock import MagicMock, patch

import genanki
import pytest

from anki.german_deck import GermanDeck


# Mock classes for GermanDeckDatabase and GermanModel since they are not provided
class MockGermanDeckDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.notes = []

    def add_note(
        self, german_word, translation, german_sentence, english_sentence, other_forms
    ):
        self.notes.append(
            {
                "german_word": german_word,
                "translation": translation,
                "german_sentence": german_sentence,
                "english_sentence": english_sentence,
                "other_forms": other_forms,
            }
        )

    def load_notes(self):
        return [
            MagicMock(
                german_word=note["german_word"],
                translation=note["translation"],
                german_sentence=note["german_sentence"],
                english_sentence=note["english_sentence"],
                other_forms=note["other_forms"],
            )
            for note in self.notes
        ]


class MockGermanModel:
    def __init__(self, model_id):
        self.model_id = model_id


@pytest.fixture
def german_deck(tmp_path):
    with patch(
        "anki.german_deck_db.GermanDeckDatabase", new=MockGermanDeckDatabase
    ), patch("anki.german_model.GermanModel", new=MockGermanModel):
        deck_id = 2059400110
        model_id = 1607392319
        test_file_path = tmp_path / "test_deck"
        return GermanDeck(deck_id, model_id, str(test_file_path))


def test_german_deck_initialization(german_deck):
    """Test initialization of GermanDeck."""
    assert german_deck.deck_id == 2059400110
    assert german_deck.model.model_id == 1607392319
    assert isinstance(german_deck.deck, genanki.Deck)
    assert german_deck.deck.name == "German Vocabulary"
    assert german_deck.db_path.suffix == ".db"
    assert german_deck.apkg_path.suffix == ".apkg"


def test_add_note_to_deck(german_deck):
    """Test adding a note to the GermanDeck."""
    german_deck.add_note(
        german_word="lernen",
        translation="to learn",
        german_sentence="Ich lerne Deutsch.",
        english_sentence="I am learning German.",
        other_forms="lernte, gelernt",
    )

    assert len(german_deck.deck.notes) == 1
    note = german_deck.deck.notes[0]
    assert note.fields == [
        "lernen",
        "to learn",
        "Ich lerne Deutsch.",
        "I am learning German.",
        "lernte, gelernt",
    ]


def test_save_deck(german_deck):
    """Test saving the GermanDeck to a SQLite database."""
    with patch("anki.german_deck_db.GermanDeckDatabase.add_note") as mock_add_note:
        german_deck.add_note(
            german_word="lernen",
            translation="to learn",
            german_sentence="Ich lerne Deutsch.",
            english_sentence="I am learning German.",
            other_forms="lernte, gelernt",
        )

        german_deck.save_deck()

        # Check if the mock database's add_note method was called
        assert mock_add_note.called
        mock_add_note.assert_called_once_with(
            german_word="lernen",
            translation="to learn",
            german_sentence="Ich lerne Deutsch.",
            english_sentence="I am learning German.",
            other_forms="lernte, gelernt",
        )


def test_load_deck(german_deck):
    """Test loading notes from the SQLite database into the GermanDeck."""
    with patch("anki.german_deck_db.GermanDeckDatabase.load_notes") as mock_load_notes:
        mock_load_notes.return_value = [
            MagicMock(
                german_word="lernen",
                translation="to learn",
                german_sentence="Ich lerne Deutsch.",
                english_sentence="I am learning German.",
                other_forms="lernte, gelernt",
            )
        ]

        german_deck.load_deck()

        assert len(german_deck.deck.notes) == 1
        note = german_deck.deck.notes[0]
        assert note.fields == [
            "lernen",
            "to learn",
            "Ich lerne Deutsch.",
            "I am learning German.",
            "lernte, gelernt",
        ]


def test_save_to_apkg(german_deck):
    """Test saving the GermanDeck to an .apkg file."""
    with patch("genanki.Package.write_to_file") as mock_write:
        german_deck.save_to_apkg()
        mock_write.assert_called_once_with(german_deck.apkg_path)
