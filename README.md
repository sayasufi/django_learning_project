<a href="https://wakatime.com/badge/user/018c3f04-b140-41f9-a489-5b0143d153f5/project/018cd368-b900-42f1-b5b5-ecc343495400"><img src="https://wakatime.com/badge/user/018c3f04-b140-41f9-a489-5b0143d153f5/project/018cd368-b900-42f1-b5b5-ecc343495400.svg" alt="wakatime"></a>
# Команды:

## 1. Консольные

#### 1) Запуск сервера

```Shell
python3 manage.py runserver
```

#### 2) Запуск сервера в режиме DEBUG = True с загрузкой static файлов

```Shell
python3 manage.py runserver --insecure
```

#### 3) Запуск оболочки для добавления записей в БД

```Shell
python manage.py shell_plus --print-sql
```

#### 4) Создание новой миграции

```Shell
python3 manage.py makemigrations
```

#### 5) Применить миграцию

```Shell
 python3 manage.py migrate
```

## 2. База данных

#### 1) Добавление записи в БД

```python
Women.objects.create(title='', content='')
```

```python
a = Women(title="", content="")
a.save()
```

#### 2) Чтение всех записей из БД

```python
Women.objects.all()
```

```python
Women.objects.all()[0]
```

#### 3) Чтение несколько записей из БД

https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups

```python
Women.objects.filter(title='')  # Равен
Women.objects.filter(pk__gte=2)  # Больше 2
Women.objects.filter(title__contains='ли')  # Включает
Women.objects.filter(pk__in=[2, 5, 11, 12], is_published=1)  # Включение в
Women.objects.exclude(pk=2)  # Исключение
Women.objects.get(pk=2)  # Строго одна запись
```

#### 4) Сортировка записей из БД

```python
Women.objects.all().order_by('title')
```

#### 5) Обновление записей из БД

```python
Women.objects.update(is_published=0)
Women.objects.filter(pk__lte=4).update(is_published=1)
```

#### 6) Удаление записей из БД

```python
Women.objects.filter(pk__gte=5).delete()
```

## 3. ORM-команды с классом Q

```python
from django.db.models import Q
```

```python
Women.objects.filter(Q(pk__lt=5) | Q(cat_id=2))
```

```python
# Первые два выражения будут объединены по ИЛИ, а третье по И
Women.objects.filter(Q(pk__in=[1, 2, 5]) | Q(cat_id=2), title__icontains="ра")
Women.objects.filter(Q(pk__in=[1, 2, 5]) | Q(cat_id=2) & Q(title__icontains="ра"))
```

## 4. Методы выбора записей

#### 1) Первая и последняя записи

```python
Women.objects.first()  # Первая
Women.objects.order_by("pk").last()  # Последняя
```

#### 2) Первая и последняя по времени

```python
Women.objects.earliest("time_update")
Women.objects.latest("time_update")
```

#### 3) Получения предыдущей записи относительно текущей

```python
w = Women.objects.get(pk=2)
w.get_previous_by_time_update()
w.get_next_by_time_update()
w.get_previous_by_time_update(pk__gt=6)
```

#### 4) Методы exists и count

```python
c2 = Category.objects.get(pk=2)
c2.posts.exists()
c2.posts.count()
Women.objects.filter(cat=c2).count()
```

## 5. Класс F, Value и метод annotate()

#### 1) Счетчик числа

```python
from django.db.models import F

Husband.objects.update(m_count=F("m_count") + 1)
```

#### 2) Метод annotate(), создание полей

```python
from django.db.models import Value

lst = Husband.objects.all().annotate(is_married=Value(True))
lst = Husband.objects.all().annotate(is_married=F("m_count"))
lst = Husband.objects.all().annotate(work_age=F("age") - 20, salary=F("age") * 1.10)
```

## 6. Агрегирующие функции Count, Sum, Avg, Max, Min. Метод values()

https://docs.djangoproject.com/en/4.2/ref/models/querysets/#aggregation-functions

```python
from django.db.models import Count, Sum, Avg, Max, Min
```

#### 1) Число записей

```python
Women.objects.filter(pk__gt=2).aggregate(res=Count("cat_id"))
```

#### 2) Минимальное и максимальное значения

```python
Husband.objects.aggregate(Min("age"))
Husband.objects.aggregate(Min("age"), Max("age"))
# Изменить названия ключей словаря
Husband.objects.aggregate(young=Min("age"), old=Max("age"))
```

#### 3) Сумма и среднее

```python
Husband.objects.aggregate(res=Sum("age") - Avg("age"))
```

#### 4) Метод values (возврат определенных полей)

```python
Women.objects.values("title", "cat_id").get(pk=1)
Women.objects.values("title", "cat__name").get(pk=1)
```

## 7. Пагинация
https://docs.djangoproject.com/en/4.2/ref/paginator/
https://docs.djangoproject.com/en/4.2/topics/pagination/

```python
from django.core.paginator import Paginator
p = Paginator(women, 3)

p.count # число элементов в списке
p.num_pages # число страниц (10:3 = 4 – округление до большего)
p.page_range # итератор для перебора номеров страниц

p1 = p.page(1) # получение первой страницы
p1.object_list  # список элементов текущей страницы
p1.has_next() # имеется ли следующая страница
p1.has_previous() # имеется ли предыдущая страница
p1.has_other_pages() # имеются ли вообще страницы
p1.next_page_number() # номер следующей страницы
p1.previous_page_number() # номер предыдущей страницы
```