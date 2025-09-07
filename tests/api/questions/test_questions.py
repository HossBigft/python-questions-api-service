import pytest
from sqlalchemy import select
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.db.models import Question, Answer
from app.db.crud import create_question
from app.questions.questions_schemas import QuestionIn
from tests.utils.utils import random_lower_string


@pytest.mark.asyncio
async def test_add_question_success(
    client: AsyncClient, normal_user_token_headers: dict[str, str], db: Session
):
    question_text: str = random_lower_string()
    data = {"text": question_text}
    r = await client.post("/questions/", json=data, headers=normal_user_token_headers)
    assert r.status_code == 200
    assert r.json() == "Question was added successfully"

    q = db.execute(select(Question).where(Question.text == question_text)).scalar()
    assert q
    assert q.text == question_text


@pytest.mark.asyncio
async def test_get_questions_with_pagination(
    client: AsyncClient, normal_user_token_headers: dict[str, str], db: Session
):
    for i in range(15):
        create_question(session=db, question=QuestionIn(text=f"Question {i}"))

    r = await client.get(
        "/questions/?skip=0&limit=10", headers=normal_user_token_headers
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 10


@pytest.mark.asyncio
async def test_get_questions_not_found(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
):
    r = await client.get(
        "/questions/?skip=0&limit=10", headers=normal_user_token_headers
    )

    if r.status_code != 404:
        assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_delete_question_success(
    client: AsyncClient, normal_user_token_headers: dict[str, str], db: Session
):
    q = create_question(session=db, question=QuestionIn(text="sdfgsdfg"))

    r = await client.delete(f"/questions/{q.id}", headers=normal_user_token_headers)
    assert r.status_code == 200

    q_check = db.execute(select(Question).where(Question.id == q.id)).scalar()
    assert q_check is None


@pytest.mark.asyncio
async def test_delete_question_not_found(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
):
    r = await client.delete("/questions/999999", headers=normal_user_token_headers)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_add_answer_to_question_success(
    client: AsyncClient, normal_user_token_headers: dict[str, str], db: Session
):
    question_text: str = random_lower_string()
    answer_text: str = random_lower_string()
    q = create_question(session=db, question=QuestionIn(text=question_text))
    answer_data = {"text": answer_text}
    r = await client.post(
        f"/questions/{q.id}/answers",
        json=answer_data,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200

    db.refresh(q)
    assert len(q.answers) == 1
    assert q.answers[0].text == answer_text


@pytest.mark.asyncio
async def test_add_answer_to_nonexistent_question(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
):
    answer_data = {"text": "Answer"}
    r = await client.post(
        "/questions/999999/answers", json=answer_data, headers=normal_user_token_headers
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_question_cascades_answers(
    client: AsyncClient, db: Session, normal_user_token_headers
):
    question_text: str = random_lower_string()

    resp = await client.post(
        "/questions/",
        json={"text": question_text},
        headers=normal_user_token_headers,
    )
    assert resp.status_code == 200

    question = (
        db.execute(select(Question).where(Question.text == question_text))
        .scalars()
        .first()
    )

    assert question is not None

    for i in range(3):
        answer_text: str = random_lower_string()
        resp = await client.post(
            f"/questions/{question.id}/answers",
            json={"text": f"Answer {answer_text}"},
            headers=normal_user_token_headers,
        )
        assert resp.status_code == 200

    answers_before = (
        db.execute(select(Answer).where(Answer.question_id == question.id))
        .scalars()
        .all()
    )

    assert len(answers_before) == 3

    resp = await client.delete(
        f"/questions/{question.id}",
        headers=normal_user_token_headers,
    )
    assert resp.status_code == 200

    question_in_db = (
        db.execute(select(Question).where(Question.text == question_text))
        .scalars()
        .first()
    )
    assert question_in_db is None

    answers_after = (
        db.execute(select(Answer).where(Answer.question_id == question.id))
        .scalars()
        .all()
    )
    assert len(answers_after) == 0
