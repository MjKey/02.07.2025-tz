# Sightengine NSFW Detector Backend

Это простое backend-приложение на Python с использованием FastAPI, которое принимает изображение, отправляет его в Sightengine API для модерации и возвращает результат.

## Установка

1.  Клонируйте репозиторий:
    ```bash
    git clone <YOUR_GITHUB_REPO_URL>
    cd <YOUR_PROJECT_DIRECTORY>
    ```
    (Замените `<YOUR_GITHUB_REPO_URL>` и `<YOUR_PROJECT_DIRECTORY>` на актуальные значения после создания репозитория.)

2.  Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    # Для Windows
    .\venv\Scripts\activate
    # Для macOS/Linux
    source venv/bin/activate
    ```

3.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4.  Получите API-ключи Sightengine:
    Зарегистрируйтесь на [Sightengine](https://sightengine.com/) и получите ваши API User и API Secret.

5.  Создайте файл `.env` в корневой директории проекта и добавьте ваши API-ключи:
    ```
    SIGHTENGINE_API_USER="YOUR_SIGHTENGINE_API_USER"
    SIGHTENGINE_API_SECRET="YOUR_SIGHTENGINE_API_SECRET"
    ```
    (Замените `"YOUR_SIGHTENGINE_API_USER"` и `"YOUR_SIGHTENGINE_API_SECRET"` на ваши фактические ключи.)

## Запуск приложения

1.  Убедитесь, что виртуальное окружение активировано.
2.  Запустите сервер Uvicorn:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    Сервер будет доступен по адресу `http://localhost:8000`.

## Использование API

Эндпоинт: `POST /moderate`

Принимает изображение (`.jpg`, `.png`) в виде `multipart/form-data`.

### Пример запроса с использованием `curl`

Сохраните изображение, например, `example.jpg`, в той же директории, где вы запускаете команду `curl`.

```bash
curl -X POST -F "file=@example.jpg" http://localhost:8000/moderate
```

### Пример ответа

*   **Безопасное изображение:**
    ```json
    {"status": "OK"}
    ```
*   **Неприемлемый контент (NSFW):**
    ```json
    {"status": "REJECTED", "reason": "NSFW content"}
    ```

## Логика модерации

Приложение использует данные из ответа Sightengine API:

*   Если `sexual_activity`, `sexual_display`, `erotica`, `very_suggestive` или `suggestive` score > 0.7, изображение помечается как `REJECTED`.
*   В противном случае изображение помечается как `OK`.
