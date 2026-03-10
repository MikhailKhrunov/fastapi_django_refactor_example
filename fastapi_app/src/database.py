from contextlib import contextmanager
from pathlib import Path

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        db_path = base_dir / "kittygram.db"
        
        self._db_url = f"sqlite:///{db_path}"
        self._engine = create_engine(
            self._db_url,
            connect_args={"check_same_thread": False}
        )
        
        @event.listens_for(self._engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    @contextmanager
    def session(self):
        Session = sessionmaker(bind=self._engine)
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


database = Database()
Base = declarative_base()