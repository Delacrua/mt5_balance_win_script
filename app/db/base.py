from tortoise import Tortoise

from settings import settings


async def tortoise_init():
    await Tortoise.init(
        db_url=settings.DB_URL_asyncpg,
        modules={'models': ['db.models']}
    )
    # # Generate the schema
    # await Tortoise.generate_schemas()
