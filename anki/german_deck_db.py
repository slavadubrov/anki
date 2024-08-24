"""Module for working with SQLite database for storing Anki cards using SQLAlchemy."""

from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Base class for SQLAlchemy models
Base = declarative_base()


class NoteModel(Base):
    """SQLAlchemy model representing a note in the German vocabulary deck."""

    __tablename__ = "notes"

    id: int = Column(Integer, primary_key=True)
    german_word: str = Column(String, nullable=False)
    translation: str = Column(String, nullable=False)
    german_sentence: str = Column(Text, nullable=False)
    english_sentence: str = Column(Text, nullable=False)
    other_forms: Optional[str] = Column(String, nullable=True)


class GermanDeckDatabase:
    """Class for managing the SQLite database containing the German vocabulary deck."""

    def __init__(self, db_file: str) -> None:
        """
        Initialize the GermanDeckDatabase with the given SQLite database file.

        Args:
            db_file (str): The SQLite database file path.
        """
        self.engine = create_engine(f"sqlite:///{db_file}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_note(
        self,
        german_word: str,
        translation: str,
        german_sentence: str,
        english_sentence: str,
        other_forms: Optional[str] = None,
    ) -> None:
        """
        Add a new note to the database.

        Args:
            german_word (str): The German word to add.
            translation (str): The English translation of the German word.
            german_sentence (str): An example sentence in German.
            english_sentence (str): The English translation of the German sentence.
            other_forms (Optional[str]): Other forms of the German word, if any.
        """
        session: Session = self.Session()
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

    def load_notes(self) -> List[NoteModel]:
        """
        Load all notes from the database.

        Returns:
            List[NoteModel]: A list of all notes in the database.
        """
        session: Session = self.Session()
        notes: List[NoteModel] = session.query(NoteModel).all()
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
