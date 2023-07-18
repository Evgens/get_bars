from datetime import datetime
import time  # Подписка на события по времени
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp


def PrintCallback(data):
    """Пользовательский обработчик событий:
    - Изменение стакана котировок
    - Получение обезличенной сделки
    - Получение новой свечки
    """
    print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data["data"]}')  # Печатаем полученные данные

def ChangedConnection(data):
    """Пользовательский обработчик событий:
    - Соединение установлено
    - Соединение разорвано
    """
    print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}')  # Печатаем полученные данные

if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    # qpProvider = QuikPy(Host='<Ваш IP адрес>')  # Вызываем конструктор QuikPy с подключением к удаленному компьютеру с QUIK

    classCode = 'TQBR'  # Класс тикера Акции ММВБ
    # secCode = 'GAZP'  # Тикер

    sec_codes = ('SBER', 'VTBR', 'GAZP')
             
    # Просмотр изменений состояния соединения терминала QUIK с сервером брокера
    # qpProvider.OnConnected = ChangedConnection  # Нажимаем кнопку "Установить соединение" в QUIK
    # qpProvider.OnDisconnected = ChangedConnection  # Нажимаем кнопку "Разорвать соединение" в QUIK

    # Подписка на новые свечки. При первой подписке получим все свечки с начала прошлой сессии
    # TODO В QUIK 9.2.13.15 перестала работать повторная подписка на минутные бары. Остальные работают
    #  Перед повторной подпиской нужно перезапустить скрипт QuikSharp.lua Подписка станет первой, все заработает
    qpProvider.OnNewCandle = PrintCallback  # Обработчик получения новой свечки
    for secCode in sec_codes:
        for interval in (1,):  # (1, 60, 1440) = Минутки, часовки, дневки
            print(f'Подписка на интервал {interval}:', qpProvider.SubscribeToCandles(classCode, secCode, interval)['data'])
            print(f'Статус подписки на интервал {interval}:', qpProvider.IsSubscribed(classCode, secCode, interval)['data'])
    input('Enter - отмена\n')
    for secCode in sec_codes:
        for interval in (1,):  # (1, 60, 1440) = Минутки, часовки, дневки
            print(f'Отмена подписки на интервал {interval}', qpProvider.UnsubscribeFromCandles(classCode, secCode, interval)['data'])
            print(f'Статус подписки на интервал {interval}:', qpProvider.IsSubscribed(classCode, secCode, interval)['data'])
    qpProvider.OnNewCandle = qpProvider.DefaultHandler  # Возвращаем обработчик по умолчанию

    qpProvider.OnConnected = qpProvider.DefaultHandler  # Возвращаем обработчик по умолчанию
    qpProvider.OnDisconnected = qpProvider.DefaultHandler  # Возвращаем обработчик по умолчанию

    # Выход
    qpProvider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляра
