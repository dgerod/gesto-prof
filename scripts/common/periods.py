from datetime import date


def generate_periods():

    T1 = (date(2021,1,1), date(2021,3,31))
    T2 = (date(2021,4,1), date(2021,6,30))
    T3 = (date(2021,7,1), date(2021,9,30))
    T4 = (date(2021,10,1), date(2021,12,31))

    return [T1, T2, T3, T4]


def get_period_info(date, periods):

    T1, T2, T3, T4 =  periods
    year = date.year

    if T1[0] <= date and date <= T1[1]:
        return year, 1
    elif T2[0] <= date and date <= T2[1]:
        return year, 2
    elif T3[0] <= date and date <= T3[1]:
        return year, 3
    elif T4[0] <= date and date <= T4[1]:
        return year, 4
