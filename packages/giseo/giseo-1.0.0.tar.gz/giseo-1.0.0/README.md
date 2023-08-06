# giseo.py
Библиотека для взаимодействия с API https://giseo.rkomi.ru

## Установка
`pip install giseo`

## Пример использования
```python
from giseo import Manager

# создаем объект класса
manager = Manager (login='myusername', password='goodluckpass', studentId=123456)

# получаем записи дневника с 1 января 2020 по 1 января 2021
manager.getDiary (start=1577836800, end=1609459200) # ...
```

## API

### Manager (login: str, password: str, studentId: int)
- **login**: логин пользователя
- **password**: пароль пользователя
- **studentId**: ID пользователя, получается посредством консоли

```python
# создаем объект класса
manager = Manager (login='myusername', password='goodluckpass', studentId=123456)
```

### Manager.getDiary (start: int, end: int)
Получение записей дневника в указанном периоде

- **start**: начальная дата, измеряется в [UNIX-time](https://ru.wikipedia.org/wiki/Unix-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)
- **end**: конечная дата, измеряется в [UNIX-time](https://ru.wikipedia.org/wiki/Unix-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)

```python
# получаем записи дневника с 1 января 2020 по 1 января 2021
manager.getDiary (start=1577836800, end=1609459200) # ...
```

### Manager.getAttachments (assignsIds: list[int])
Получение файлов, прикрепленных к определенным записям дневника

- **assignsIds**: массив из ID записей дневника

```python
# получаем список файлов у записей 123, 456 и 789
manager.getAttachments (assignsIds=[123, 456, 789]) # ...
```
