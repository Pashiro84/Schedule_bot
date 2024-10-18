import schedule as sch
import merge
import week_day as wd
import week_even as we
from datetime import datetime, timedelta
import pytz

def logic():
    krasnoyarsk_tz = pytz.timezone('Asia/Krasnoyarsk')
    today = datetime.now(krasnoyarsk_tz).strftime('%A')
    week = we.is_week_even()
    weekend_two = (week == 0 and today == "Saturday") or (week == 0 and today == "Sunday")
    weekend_one = (week == 1 and today == "Saturday") or (week == 1 and today == "Sunday")
    logic = weekend_two or (week and not(weekend_one))
    return logic



def shedule_day(dayw,day, group):
    krasnoyarsk_tz = pytz.timezone('Asia/Krasnoyarsk')
    today = datetime.now(krasnoyarsk_tz).strftime('%A')
    if logic()==0:
        if group == 'A':
            lessons = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_two_week), sch.schedule_A).get(day, [])
        elif group == 'B':
            lessons = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_two_week), sch.schedule_B).get(day, [])
    elif logic()==1:
        if group == 'A':
            lessons = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_one_week), sch.schedule_A).get(day, [])
        elif group == 'B':
            lessons = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_one_week), sch.schedule_B).get(day, [])
    if lessons:
        reply = f'Пары {dayw} ({wd.day_rus(day)}):\n'
        for lesson_num,  lesson_name, lesson_aud, lesson_type in lessons:
            lesson_time = sch.schedule_time.get(lesson_num, [])
            reply += f'{lesson_num}) {lesson_name}: {lesson_aud}\n {lesson_time[0]}-{lesson_time[1]} - {lesson_type}\n'
    else:
        reply = f'{dayw.title()} нет пар.'
    return reply

def shedule_week(group):
    print(we.is_week_even())
    print(logic())
    krasnoyarsk_tz = pytz.timezone('Asia/Krasnoyarsk')
    today = datetime.now(krasnoyarsk_tz).strftime('%A')
    if logic()==1:
        if group == 'A':
            lessons_week = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_one_week), sch.schedule_A)
        elif group == 'B':
            lessons_week = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_one_week), sch.schedule_B)
    elif logic()==0:
        if group == 'A':
            lessons_week = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_two_week), sch.schedule_A)
        elif group == 'B':
            lessons_week = merge.merge_schedules(merge.merge_schedules(sch.schedule, sch.schedule_two_week), sch.schedule_B)
    reply = f'Расписание на неделю: \n'
    for day, lessons in lessons_week.items():
        reply += f'\n{wd.day_rus(day)}:\n'
        for lesson_num, lesson_name, lesson_aud, lesson_type in lessons:
            lesson_time = sch.schedule_time.get(lesson_num, [])
            reply += f'{lesson_num}) {lesson_name}: {lesson_aud}\n  {lesson_time[0]}-{lesson_time[1]} - {lesson_type}\n'
    return reply