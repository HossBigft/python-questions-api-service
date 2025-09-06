from fastapi import APIRouter, HTTPException
from sqlalchemy import select, delete


from app.db.models import Answer
from app.core.dependencies import SessionDep
from app.answers.answers_schemas import AnswerOut

router = APIRouter(tags=["answers"], prefix="/answers")


@router.get("/{id}")
def get_answer(session: SessionDep, id: int) -> AnswerOut:
    """
    Retrieve answer.
    """

    statement = select(Answer).where(Answer.id == id)
    answer = session.execute(statement).scalars().first()
    if not answer:
        raise HTTPException(status_code=404)
    return AnswerOut.model_validate(answer)

@router.delete("/{id}")
def delete_answer(session: SessionDep, id: int) -> str:
    """
    Delete answer by id.
    """
    stmt = delete(Answer).where(Answer.id == id).returning(Answer)
    
    
    result = session.execute(stmt)
    deleted_question = result.fetchone()

    if not deleted_question:
        raise HTTPException(status_code=404, detail="Answer was not found.")

    session.commit()

    return "Answer deleted succesfully."

