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
Women.objects.filter(title='') # Равен
Women.objects.filter(pk__gte=2) # Больше 2
Women.objects.filter(title__contains='ли') # Включает
Women.objects.filter(pk__in=[2, 5, 11, 12], is_published=1) # Включение в
Women.objects.exclude(pk=2) # Исключение
Women.objects.get(pk=2) # Строго одна запись
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