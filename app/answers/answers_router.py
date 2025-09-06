from fastapi import APIRouter, HTTPException
from sqlalchemy import select


from app.db.models import Answer
from app.core.dependencies import SessionDep
from app.answers.answers_schemas import AnswerOut

router = APIRouter(tags=["answers"], prefix="/answers")


router.get("/{id}")


def get_answer(session: SessionDep, id: int) -> AnswerOut:
    """
    Retrieve answer.
    """

    statement = select(Answer).where(Answer.id == id)
    answer = session.execute(statement).scalars().all()
    if not answer:
        raise HTTPException(status_code=404)
    return AnswerOut.model_validate(answer)
