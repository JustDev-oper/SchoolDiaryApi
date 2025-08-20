from app.database.base import Base
from app.database.engine import engine
from app.models import *

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

print("Создаём таблицы...")
Base.metadata.create_all(bind=engine)
print("Таблицы успешно созданы!")
