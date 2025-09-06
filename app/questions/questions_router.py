
from fastapi import APIRouter, HTTPException
from sqlalchemy import update, delete, select, func
from typing import Any

from app.db.models import Question
from app.core.dependencies import (
    SessionDep
)
from app.questions.questions_schemas import QuestionSchema
from app.db.crud import create_question


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

    return [QuestionSchema.model_validate(question) for question in questions]

@router.post(
    "/",
)
def add_question(session: SessionDep, question:QuestionSchema) -> None:
    """
    Add question.
    """
    create_question(session=session, question=question)

@router.get(
    "/{id}",
)
def read_questions(session: SessionDep, id:int) -> Any:
    """
    Retrieve questions.
    """

    statement = select(Question)
    questions = session.execute(statement).scalars().all()

    return [QuestionSchema.model_validate(question) for question in questions]