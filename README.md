# REST API
## Введение
API интерфейс используется для того, чтобы интегрировать возможности создания, редактирования, управления акциями для тарифов операторов. API предназначен для разработчиков и сопровождается документацией.

## Описание
REST API данного сервиса работает по протоколу HTTP и представляет собой набор методов для подключения пользователя к акции и личный кабинет дилера, в котором последний может создавать/управлять/блокировать акции. Ответы приходят ввиде JSON структур.

## Список запросов
### Получение ID подключеных акций
` /api/stock/get/<MSISDN>`
**Параметры**
* `<MSISDN>` - MSISDN идентификатор абонента

**Вывод**
`Array<Number>`

`Number` - ID акции

### Получение статуса заказа подключения
`/api/stock/status/<MSISDN>`

**Параметры**
* `<MSISDN>` - MSISDN идентификатор абонента

**Вывод**

`Array<Object>`

### Регистрация заказа в базе данных
` /api/stock/add/<MSISDN>&<dealer>&<stock>`

**Параметры**
* `<MSISDN>` - MSISDN идентификатор абонента
* `<dealer>` - ID Диллера
* `<stock>` - ID Акции

**Вывод**

`type` - `success | error`
`message` - Сообщение об ошибки