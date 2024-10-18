from datetime import datetime, timedelta

def is_week_even() -> str:
    # Устанавливаем дату 1 сентября текущего года
    current_year = datetime.now().year
    start_date = datetime(current_year, 9, 2)

    # Получаем текущую дату
    current_date = datetime.now()

    # Вычисляем количество дней между текущей датой и 1 сентября
    days_difference = (current_date - start_date).days

    # Вычисляем номер недели с 1 сентября (прибавляем 1, чтобы не начиналось с нуля)
    week_number = days_difference // 7 + 1

    # Определяем чётность недели
    if week_number % 2 == 0:
        return 0
    else:
        return 1

