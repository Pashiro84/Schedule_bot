
def day_rus (day_eng):
    day_mapping = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',               
        'Saturday':'Суббота',
    }
    return day_mapping.get(day_eng, '')
    
