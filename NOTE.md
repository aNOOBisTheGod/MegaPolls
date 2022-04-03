## Веб-сайт обеспечивает простое создание опросов. Здесь я расскажу вам о структуре сайта и технологиях, которые использует этот сайт.<br>
Структура.<br>
Главная страница, где вы можете прочитать информацию о веб-сайте и перейти на другие страницы (main route).<br>
Страница создания учетной записи / входа в систему, где вы можете создать учетную запись или войти в нее (create_account).<br>
Страница создания опросов, где... Мне не нужно объяснять, что вы можете там сделать (create_poll route).<br>
Страница учетной записи, на которой вы можете выйти из учетной записи (account).<br>
Страница голосования в опросе, где вы можете проголосовать в опросе, и если вы уже проголосовали, вы можете просмотреть результаты<br>
(poll?poll=poll.id route).
Технологии.<br>
## Веб-сайт использует Python 3 с фреймворком flask в качестве бэкэнда (в основном для управления базами данных).<br>
### Библиотеки:<br>
Flask (для создания самого веб-сайта)<br>
sqlalchemy (как управление базами данных)<br>
sqlite3 (как альтернативное управление базами данных)<br>
встроенные библиотеки (например, sys, ast)<br>
## HTML, CSS, JS в качестве интерфейса (большая часть кода).<br>
### Модификации:<br>
Bootstrap icons для html<br>
sweetalert2 для создания красивых оповещений<br>
Heroku в качестве хостинга.<br>
git как система контроля версий.