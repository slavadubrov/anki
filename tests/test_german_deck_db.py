import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from anki.german_deck_db import Base, GermanDeckDatabase, NoteModel


@pytest.fixture(scope="function")
def test_db():
    """Fixture for setting up an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session


def test_add_note_success(test_db):
    """Test that a note can be added successfully to the database."""
    db = GermanDeckDatabase(":memory:")  # Use in-memory database for testing
    db.Session = test_db  # Override Session for testing

    db.add_note(
        german_word="lernen",
        translation="to learn",
        german_sentence="Ich lerne jeden Tag Deutsch.",
        english_sentence="I learn German every day.",
        other_forms="lernte, gelernt",
    )

    session = test_db()
    note = session.query(NoteModel).filter_by(german_word="lernen").first()

    assert note is not None
    assert note.translation == "to learn"
    assert note.german_sentence == "Ich lerne jeden Tag Deutsch."
    assert note.english_sentence == "I learn German every day."
    assert note.other_forms == "lernte, gelernt"
    session.close()


def test_load_notes(test_db):
    """Test that all notes can be loaded from the database."""
    db = GermanDeckDatabase(":memory:")
    db.Session = test_db

    db.add_note(
        german_word="lesen",
        translation="to read",
        german_sentence="Ich lese gerne Bücher.",
        english_sentence="I like reading books.",
        other_forms="las, gelesen",
    )

    db.add_note(
        german_word="schreiben",
        translation="to write",
        german_sentence="Er schreibt einen Brief.",
        english_sentence="He is writing a letter.",
        other_forms="schrieb, geschrieben",
    )

    notes = db.load_notes()

    assert len(notes) == 2
    assert notes[0].german_word == "lesen"
    assert notes[1].german_word == "schreiben"


def test_note_with_no_other_forms(test_db):
    """Test adding a note with no other forms."""
    db = GermanDeckDatabase(":memory:")
    db.Session = test_db

    db.add_note(
        german_word="sprechen",
        translation="to speak",
        german_sentence="Ich spreche Deutsch.",
        english_sentence="I speak German.",
        other_forms=None,
    )

    session = test_db()
    note = session.query(NoteModel).filter_by(german_word="sprechen").first()

    assert note is not None
    assert note.other_forms is None
    session.close()


def test_database_persistence(test_db):
    """Test that notes are correctly persisted in the database."""
    db = GermanDeckDatabase(":memory:")
    db.Session = test_db

    db.add_note(
        german_word="fahren",
        translation="to drive",
        german_sentence="Ich fahre ein Auto.",
        english_sentence="I drive a car.",
        other_forms="fuhr, gefahren",
    )

    notes = db.load_notes()

    assert len(notes) == 1
    assert notes[0].german_word == "fahren"

    # Restart session to check persistence
    new_session = test_db()
    persisted_notes = new_session.query(NoteModel).all()
    assert len(persisted_notes) == 1
    assert persisted_notes[0].german_word == "fahren"
    new_session.close()
