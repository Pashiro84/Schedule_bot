import schedule as sch


def merge_schedules(common, group):
    merged = {}

    # Сначала копируем общее расписание в итоговый словарь
    for day, lessons in common.items():
        merged[day] = lessons.copy()  # Копируем уроки общего расписания

    # Добавляем уроки подгруппы, соблюдая порядок
    for day, group_lessons in group.items():
        if day in merged:
            # Объединяем списки и сортируем по номеру урока
            merged[day].extend(group_lessons)
            merged[day].sort(key=lambda x: x[0])  # Сортируем по номеру урока
        else:
            # Если день отсутствует, добавляем полностью
            merged[day] = group_lessons

    return merged

