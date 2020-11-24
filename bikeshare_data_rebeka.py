import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Please select from cities you want want to explore: chicago, new york city, washington: ').lower()
    while city not in CITY_DATA:
        print("Invalid city name. Please select from chicago, new york city, washington. ")
        city = input('Please select from cities you want want to explore: chicago, new york city, washington: ').lower()

    # get user input for month (all, january, february, ... , june)
    # created an excluded month list when the user wants to ask data for months that are not in database.
    Month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    Exluded_month_list = ['july', 'august', 'september', 'october', 'november', 'december']
    month = input("Please select the month to filter by: if you don't want to filter please write all. " ).lower()
    while month not in Month_list:
        if month in Exluded_month_list:
            print('No data for this month. Please select from period: january-june.')
        else:
            print('Invalid month name. Please enter a valid full english name for month e.g: january.')
        month = input("Please select the month to filter by: if you don't want to filter please write all. " ).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    Week_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input("Please select the weekday to filter by: if you don't want to filter please write all. " ).lower()
    while day not in Week_list:
        print('Invalid week name. Please select a valid english week name e.g: monday.')
        day = input("Please select the week to filter by: if you don't want to filter please write all. " ).lower()

    print('-'*40)
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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #load datafiles into dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert the start_time column to date
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month is: {} (1=January, 2=February etc...).'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day is:', popular_day)

    # display the most common start hour
    df['hour'] =df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_name = df['Start Station'].mode()[0]
    start_station_amount = df['Start Station'].value_counts()[0]
    print('The most popular start station is {} with {} routes.'.format(start_station_name, start_station_amount))

    # display most commonly used end station
    end_station_name =df['End Station'].mode()[0]
    end_station_amount = df['End Station'].value_counts()[0]
    print('The most popular end station is {} with {} routes.'.format(end_station_name, end_station_amount))

    # display most frequent combination of start station and end station trip
    df_concat = df['Start Station'] + df['End Station']
    comb_station_name =df_concat.mode()[0]
    comb_station_amount = df_concat.value_counts()[0]
    print('The most popular combination is {} with {} routes.'.format(comb_station_name, comb_station_amount))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time =df['Trip Duration'].sum()
    print('The total travel time is: ', total_travel_time)

    # display mean travel time
    mean_time =df['Trip Duration'].mean()
    print('The main travel time is:', mean_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types are:', user_types)

    # Display counts of gender
    #Try statement is added because not all files contained gender data.
    try:
        gender = df['Gender'].value_counts()
        print('The counts of gender are:', gender)
    except KeyError:
        print('Selected filter has has no data for gender. Please try other city.')

    # Display earliest, most recent, and most common year of birth
    #Try statement is added because not all files contained data for year of birth.
    try:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print('The earliest year of bith is {}, \n the most recent year of birth is {} ,\n and the most common year of birth is {}.'.format(earliest_birth, most_recent_birth,most_common_birth))
    except KeyError:
        print('Selected filter has has no data for year of birth. Please try other city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rawdata(df):

    """Displays the first 5 raws of raw data and optionally moves to the next 5 lines etc. on users request.

    Args: df - Pandas DataFrame containing city data filtered by month and day"""

    view_data = input('Would you like to view 5 rows from the row data? Please write yes or no').lower()
    start_loc =0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you wish to continue to the next 5 rows?').lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rawdata(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
