# Лабораторная №6 — задание 1: ActivityLifecycle

Семь методов жизненного цикла Activity выводят реальные события в Logcat.
Тег: `ActivityLifecycle`. В сообщении есть идентификатор экземпляра Activity
и `isChangingConfigurations`.

Открыть проект в Android Studio, выбрать JDK 25 и SDK 37, запустить `app`.

```sh
./gradlew :app:assembleDebug :app:installDebug
python3 scripts/check_lifecycle.py
```

Сценарий проверяет запуск, Home, возврат и поворот, сохраняет настоящие журналы
и снимки локально в `.security-reports/`. Настройки устройства восстанавливаются.

Обязательные проверки перед commit/push, включая Push в Fork: [SECURITY.md](SECURITY.md).
Лабораторный Word-отчёт и локальные диагностические данные не публикуются в этом репозитории.
