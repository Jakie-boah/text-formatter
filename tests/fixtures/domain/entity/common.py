import pytest_asyncio

from src.domain.entities.common import TaskExecutionData, NewsData, Connection

from faker import Faker

fake = Faker()


@pytest_asyncio.fixture
async def task_execution_data_entity():
    def _factory(**overrides) -> TaskExecutionData:
        return TaskExecutionData(
            user_id=1,
            news=news_data_faker(),
            feed=feed_data_faker(feed_id=1),
            connection=connection_data_faker(connection_id=1),
            formatting_result=formatting_result_data_faker(),
            feed_type="newsfeed",
            **overrides
        )

    return _factory


def fake_straight_task_exec():
    return TaskExecutionData(
        user_id=1,
        news=news_data_faker(),
        feed=feed_data_faker(feed_id=1),
        connection=connection_data_faker(connection_id=1),
        formatting_result=formatting_result_data_faker(),
        feed_type="newsfeed",
    )


def news_data_faker():
    return NewsData(
        title=fake.sentence(),
        published_date=fake.date(),
        url=fake.url(),
        publisher=fake.company(),
        text=fake.text(),
        description=fake.text(),
        img=fake.url(),
        summary=fake.text()[:50],
    )


def feed_data_faker(*, feed_id):
    return {
        "feed_id": feed_id,
        "feed_title": fake.text(),
    }


def connection_data_faker(*, connection_id):
    return Connection(
        **{
            "connection_id": connection_id,
            "connection_name": fake.text(),
            "is_connection_primary": True,
            "account_id": fake.text(),
            "access_token": fake.text(),
        }
    )


def formatting_result_data_faker():
    return {"text": fake.text(), "video_url": None, "dict_repr": None}
