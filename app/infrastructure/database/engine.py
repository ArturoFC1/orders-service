from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.logger import get_logger

logger = get_logger(__name__)

DATABASE_URL = "sqlite:///orders.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error("Error en sesion de base de datos: %s", e)
        session.rollback()
        raise
    finally:
        session.close()
