"""Module for working with sqlite database for storing anki cards"""

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base class for SQLAlchemy models
Base = declarative_base()


# SQLAlchemy model for a Note
class NoteModel(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    german_word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    german_sentence = Column(Text, nullable=False)
    english_sentence = Column(Text, nullable=False)
    other_forms = Column(String, nullable=True)


class GermanDeckDatabase:
    def __init__(self, db_file):
        # Create the engine and bind it to the SQLite database file
        self.engine = create_engine(f"sqlite:///{db_file}")
        Base.metadata.create_all(self.engine)  # Create tables if they don't exist

        # Create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)

    def add_note(
        self, german_word, translation, german_sentence, english_sentence, other_forms
    ):
        """Add a new note to the database."""
        session = self.Session()
        new_note = NoteModel(
            german_word=german_word,
            translation=translation,
            german_sentence=german_sentence,
            english_sentence=english_sentence,
            other_forms=other_forms,
        )
        session.add(new_note)
        session.commit()
        session.close()

    def load_notes(self):
        """Load all notes from the database."""
        session = self.Session()
        notes = session.query(NoteModel).all()
        session.close()
        return notes


# Example usage:
if __name__ == "__main__":
    # Initialize the database
    db = GermanDeckDatabase("german_vocabulary.db")

    # Add a new note
    db.add_note(
        german_word="vereinbaren",
        translation="to agree",
        german_sentence="Wir haben ein Treffen vereinbart.",
        english_sentence="We agreed on a meeting.",
        other_forms="vereinbarte, vereinbart",
    )

    # Load all notes
    notes = db.load_notes()
    for note in notes:
        print(
            f"{note.german_word}: {note.translation} - {note.german_sentence} / {note.english_sentence} - Other forms: {note.other_forms}"
        )
