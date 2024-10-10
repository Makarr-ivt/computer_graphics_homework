# Программа для оценки сжатия видео
Программа представляет собой http сервер, который принимает у пользователя видеофайл, обрабатывает его -- а именно понижает битрейт до 2 Мбит/сек и повышает контрастность в 5 раз, -- а затем анализирует качество сжатия (намеренно плохого сжатия) и выводит график потерь.

## Перед установкой!
Для установки и запуска программы вам потребуется либо Docker, либо Python + FFmpeg

## Установка программы
#### 1.0. Вариант без Docker:
1.1. Скачайте на компьютер FFmpeg, добавьте исполняемые файлы в системную переменную среды `PATH`. [(Инструкция по установке)](https://github.com/kkroening/ffmpeg-python?tab=readme-ov-file#installing-ffmpeg)

1.2. Скачайте наш проект из gitlab в формате .zip, распакуйте его в отдельную папку.

1.3. Создайте виртуальное окружение для проекта средствами IDE или через терминал.
- Чтобы создать виртуальное окружение через терминал, откройте его. Перейдите в папку с проектом и пропишите команду `python -m venv .venv`

1.4. Активируйте виртуальное окружение средствами IDE или через терминал. Чтобы активировать виртуальное окружение в терминале:
- Для Windows: пропишите `.venv/Scripts/activate`
    - если появляется ошибка о том, что имя командлета не распознано, откройте Powershell от имени администратора, введите `Set-ExecutionPolicy RemoteSigned`, затем `A` для подтверждения. Перезапустите терминал и попробуйте снова. (_[Решение взято отсюда](https://gist.github.com/2ik/3ddbef3263dee8e76b63a391e2ffe5d0)_)

- Для UNIX-подобных систем: пропишите `source ./.venv./bin/activate`
    - (_Не знаю, что может случиться тут, у меня нет мака, не тестировал_)

1.5. Установите в виртуальное окружение необходимые библиотеки. Для этого в терминале пропишите: `pip install -r requirements.txt`

1.6. Запустите main.py и откройте в браузере ссылку, которую предложит терминал.


#### 2.0. Вариант с помощью Docker 
2.1. Скачайте проект из gitlab в локальную папку на компьютере;

2.2. Запустите терминал внутри папки;

2.3. Пропишите команду `docker compose build`, затем `docker compose up`и откройте в браузере ссылку, которую предложит терминал.

/## Как пользоваться программой после запуска
После запуска веб-страницы, вы увидите поле для загрузки видео. Нажмите на него и выберите файл. Нажмите кнопку `Загрузить и сжать`. Дождитесь обработки и последующего анализа сжатия. Сжатие видео происходит практически моментально, но анализ занимает какое-то время, наберитесь терпения. По завершении обработки на странице отобразятся кнопки для скачивания сжатого файла, а также png изображения графика потерь.

> **замечание!**
> 
> Если используете программу повторно на том же файле, после загрузки видео перейдите в терминал и подтвердите перезапись сжатого видео, нажав `y` 


