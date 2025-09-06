from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, select
from typing import Any

from app.db.models import Question
from app.core.dependencies import SessionDep
from app.questions.questions_schemas import QuestionOut, QuestionIn
from app.db.crud import create_question
from app.answers.answers_schemas import AnswerIn

router = APIRouter(tags=["questions"], prefix="/questions")


@router.get(
    "/",
)
def read_questions(session: SessionDep) -> Any:
    """
    Retrieve questions.
    """

    statement = select(Question)
    questions = session.execute(statement).scalars().all()
    if not questions:
        raise  HTTPException(status_code=404)
    return [QuestionOut.model_validate(question) for question in questions]


@router.post(
    "/",
)
def add_question(session: SessionDep, question: QuestionIn) -> str:
    """
    Add question.
    """
    create_question(session=session, question=question)

    return "Question was added successfully"


@router.delete(
    "/{id}",
)
def delete_question(session: SessionDep, id: int) -> str:
    """
    Delete question by id.
    """
    stmt = delete(Question).where(Question.id == id).returning(Question)

    result = session.execute(stmt)
    deleted_question = result.fetchone()

    if not deleted_question:
        raise HTTPException(status_code=404, detail="Question was not found.")

    session.commit()

    return "Question deleted succesfully"

@router.post(
    "/{id}/answers",
)
def add_answer(session: SessionDep, answer: AnswerIn) -> str:
    """
    Add question.
    """
    create_question(session=session, question=question)

    return "Question was added successfully"
