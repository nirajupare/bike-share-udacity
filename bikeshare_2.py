import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = None
    month = None
    day = None
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ['new york city', 'chicago', 'washington']:
        print('These are the cities: new york city, chicago, washington')
        city = input("Please enter City : ").lower()

    # get user input for month (all, january, february, ... , june)
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                        'october', 'november', 'december', 'all']:
        print('These are the options for Month: january, february, march, april, may, june, july, august, september, '
              'october, november, december, all')
        month = input("please enter Month : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('These are options for Day: monday, tuesday, wednesday, thursday, friday, saturday, sunday, all')
        day = input("Please enter Day : ").lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['month'] = df['month'].apply(lambda x: calendar.month_name[x].lower())

    df['day'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())

    if month != 'all':
        df = df.loc[df['month'] == month]

    if day != 'all':
        df = df.loc[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].mode()
    most_month = most_month.values[0]
    print('Most month is {}'.format(most_month))

    # display the most common day of week
    most_day = df['day'].mode()
    most_day = most_day.values[0]
    print('Most day is {}'.format(most_day))

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].apply(lambda x: x.strftime('%H'))

    most_hour = df['hour'].mode()
    most_hour = most_hour.values[0]
    print('Most hour is {}'.format(most_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start = df['Start Station'].mode()
    most_start = most_start.values[0]
    print('Most commonly used start station is {}'.format(most_start))

    # display most commonly used end station
    most_end = df['End Station'].mode().values[0]
    # most_start = most_start.values[0]
    print('Most commonly used end station is {}'.format(most_end))

    # display most frequent combination of start station and end station trip
    # df['combine'] = df[['Start Station', 'End Station']].apply(lambda x, y: x + y)
    df['combine'] = df['Start Station'] + '~' + df['End Station']
    most_combine = df['combine'].mode().values[0]
    most_combine = most_combine.split("~")
    most_combine_start = most_combine[0]
    most_combine_end = most_combine[1]
    print('Most commonly used start station is -> {} \nAND \nMost commonly used end station is -> {}'.format(
        most_combine_start, most_combine_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['total_time'] = df['End Time'] - df['Start Time']
    total_time = df['total_time'].sum()
    print('Total = {}'.format(total_time))

    # display mean travel time
    mean_time = df['total_time'].mean()
    print('Mean = {}'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types \n{} \n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    if city != 'washington':
        print('counts of gender types \n{} \n'.format(df['Gender'].value_counts()))

        # Display earliest, most recent, and most common year of birth
        print('Earliest DoB = {}\n'.format(int(df['Birth Year'].min())))
        print('Latest DoB = {}\n'.format(int(df['Birth Year'].max())))
        print('Common DoB = {}\n'.format(int(df['Birth Year'].mode())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    print('\n First 5 rows of raw data\n{}'.format(df))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        start = 0
        end = 5
        while True:
            ans = input('\nWould you like to display raw data? yes or no\n')
            if ans.lower() == 'yes':
                raw_data(df.iloc[start:end])
                start += 5
                end += 5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
