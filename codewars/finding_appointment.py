from datetime import datetime, timedelta


# From https://www.codewars.com/kata/finding-an-appointment/train/python
#
# Description:
#
# The businesspeople among you will know that it's often not easy to find an appointment.
# Given the calendars of our businessperson and a duration for the meeting. Your task is to find the earliest time, when every businessperson is free for at least that duration.
# Rules:
#
# *All times in the calendars will be given in 24h format "hh:mm", the result must also be in that format
# *A meeting is represented by its start time (inclusively) and end time (exclusively) -> if a meeting takes place from 09:00 - 11:00, the next possible start time would be 11:00
# *The businesspeople work from 09:00 (inclusively) - 19:00 (exclusively), the appointment must start and end within that range
# *If the meeting does not fit into the schedules, return null or None as result
# *The duration of the meeting will be provided as an integer in minutes




def get_start_time(schedules, duration):
    try:
        convert_schedules(schedules)
    except:
        pass
    start_time = datetime.strptime('09:00', '%H:%M')
    return check_conflict(start_time, duration)


def check_conflict(start_time, duration):
    end_time = start_time + timedelta(minutes=duration)
    if end_time > datetime.strptime('19:00', '%H:%M'):
        return None
    skip = False
    for person in schedules:
        if not skip:
            for meeting in person:
                if meeting[1] <= start_time and meeting[0] <= start_time:
                    continue
                if meeting[0] < end_time:
                    start_time = meeting[1]
                    return check_conflict(start_time, duration)
    return datetime.strftime(start_time, '%I:%M %p')


def convert_schedules(schedules):
    for sch in schedules:
        for meeting in sch:
            for time in meeting:
                new_time = datetime.strptime(time, '%H:%M')
                meeting[meeting.index(time)] = new_time
    return schedules


if __name__ == '__main__':
    schedules = [
        [['09:00', '11:30'], ['13:30', '16:00'], ['18:15', '19:00']],
        [['09:15', '12:00'], ['14:00', '15:30']],
        [['11:30', '12:15'], ['15:00', '16:30'], ['18:00', '19:00']]]

    print get_start_time(schedules, 60)
    print get_start_time(schedules, 90)
    print get_start_time(schedules, 120)
