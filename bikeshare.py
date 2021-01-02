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
    
    # Get user input for city (chicago, new york city, washington).  Use a while loop to handle invalid inputs
    city = input('Please enter a city name from the following list:  Chicago, New York City, Washington: \n')
    if city.lower() in ['chicago', 'new york city', 'washington']:
        print('You have selected {}'.format(city).title())
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        print('Invalid selection, please re-enter city name \n')
        city = input('Please enter a city name from the following list:  Chicago, New York City, Washington: \n')
        print('You have selected {}'.format(city).title())
    
    # Get user input for month (all, january, february, ... , june)
    month = input('Please select a month from January through June or All:  \n')
    if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print('You have selected {}'.format(month).title())
    while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print('Invalid selection, please re-enter month name \n')
        month = input('Please select a month from January through June or All:  \n')
        print('You have selected {}'.format(month).title())
    
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please select a day of the week Monday through Sunday or All:  \n')
    if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('You have selected {}'.format(day))
    while day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('Invalid selection, please re-enter day name \n')
        day = input('Please select a day of the week Monday through Sunday or All:  \n')
        print('You have selected {} \n'.format(day))
    print('Filters selected:  {}, {}, {}'.format(city, month, day).title())
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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Month Filter
    df['month'] = df['Start Time'].dt.month_name()
    if month.lower() != 'all':
        df = df[df['month'] == month]

    # Day Filter
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if day.lower() != 'all':
	    df = df[df['day_of_week'] == day.title()]
    return df
    
    
def view_raw(df):
    """Gives user the option to view raw data."""
    raw_counter = 0
    view_raw_data = input('Would you like to view some raw data?  Enter yes or no. \n')
    while view_raw_data.lower() == 'yes':
	    print(df[raw_counter : raw_counter+5])
	    raw_counter += 5
	    view_raw_data = input('Would you like to view some raw data?  Enter yes or no. \n')
	    print('-'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is {}.'.format(most_common_month))
    
    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week is {}.'.format(most_common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    if most_common_start_hour == 12:
	    print('\nThe most common start hour is {}pm.'.format(most_common_start_hour))
    elif most_common_start_hour >= 13:
        most_common_start_hour = most_common_start_hour - 12
        print('\nThe most common start hour is {}pm.'.format(most_common_start_hour))
    else:
        print('\nThe most common start hour is {}am.'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is \"{}\".'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is \"{}\".'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['Start to End Station'] = '\"' + df['Start Station'] + '\"' + ' to ' + '\"' + df['End Station'] + '\"'
    most_frequent_combo_stations = df['Start to End Station'].mode()[0]
    print('\nThe most frequent combination of start station and end station is {}.'.format(most_frequent_combo_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minute, second = divmod(total_travel_time, 60)
    hour, minute = divmod(minute, 60)
    print('The total travel time is {} hours, {} minutes, and {} seconds.'.format(hour, minute, second))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    mins, secs = divmod(mean_travel_time, 60)
    hours, mins = divmod(mins, 60)
    print('\nThe average travel time is {} hours, {} minutes, and {} seconds.'.format(hours, mins, secs))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('The following are user types and counts:  \n{}'.format(user_type_count))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nThe following are user counts by gender:  \n{}'.format(gender_count))
    else:
        print('\nUser gender information not available for this data.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode())
        print('\nEarliest birth year:  {}'.format(min_birth_year))
        print('\nMost recent year of birth:  {}'.format(max_birth_year))
        print('\nMost common year of birth:  {}'.format(most_common_birth_year))
    else:
        print('\nUser birth year information not available for this data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_raw(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
