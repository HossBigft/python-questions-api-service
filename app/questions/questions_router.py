from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import delete, select
from typing import Any
from sqlalchemy.orm import selectinload

from app.db.models import Question
from app.core.dependencies import SessionDep, CurrentUser
from app.questions.questions_schemas import QuestionOut, QuestionIn
from app.db.crud import create_question, add_answer
from app.answers.answers_schemas import AnswerIn

router = APIRouter(tags=["questions"], prefix="/questions")


@router.get("/", response_model=list[QuestionOut])
def get_questions_with_answers(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=1000, description="Number of questions to return"),
) -> Any:
    """
    Get questions with list of answers.
    """
    stmt = (
        select(Question)
        .options(selectinload(Question.answers))
        .offset(skip)
        .limit(limit)
    )

    questions = session.execute(stmt).scalars().all()
    if not questions:
        raise HTTPException(status_code=404, detail="Question not found.")

    return [QuestionOut.model_validate(question) for question in questions]


@router.post(
    "/",
)
def add_question(
    session: SessionDep,
    question: QuestionIn,
    current_user: CurrentUser,
) -> str:
    """
    Add question.
    """
    create_question(session=session, question=question)

    return "Question was added successfully"


@router.delete(
    "/{id}",
)
def delete_question(
    session: SessionDep,
    id: int,
    current_user: CurrentUser,
) -> str:
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
def add_answer_to_question(
    session: SessionDep, answer: AnswerIn, id: int, current_user: CurrentUser
) -> str:
    """
    Add question.
    """
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question does not exist.")

    add_answer(
        session=session, answer=answer, question_id=question.id, db_user=current_user
    )
    return "Answer was added successfully"
