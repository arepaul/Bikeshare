import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'nyc.csv',
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
    # TO DO: get user input for city (chicago, nyc, washington). HINT: Use a while loop to handle invalid inputs
    city= str(input('Which city do you want to analyze? ').lower())
    while city not in ['chicago', 'nyc', 'washington']:
        city = str(input('WRONG INPUT: Please choose between chicago, nyc or washington: ').lower())

    # TO DO: get user input for month (all, january, february, ... , june)
    month = str(input('Enter a filter by month or type "all" if you do not want to filter: ').lower())
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month = str(input('WRONG INPUT: Please choose between january, february, ... , june or "all": ').lower())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('Enter a filter by day or "all" if you do not want to filter: ').lower())
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day=str(input('WRONG INPUT: Please choose between "all", "monday", ... , "sunday": '))

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

    #load the files which is required
    df=pd.read_csv('{}.csv'.format(city))

    #convert start time and end time in readable format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #extract month from start time to be able to filter
    df['month'] = df['Start Time'].dt.month

    #code to filter per month:
    if month != 'all':
        # index to get the right month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month
        df = df[df['month'] == month]

    # extract day from start time
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    #--statistics on the most frequent times of travel--

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #most common month
    print("The most common month is: ", df['month'].value_counts().idxmax())

    #most common day of week
    print("The most common day is: ", df['day_of_week'].value_counts().idxmax())

    #common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour is: ", df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    #---statistics on the most popular stations and trip---

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: ", df ['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("The most common end station is: ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip")
    most_common_start_and_end_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(most_common_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    #---statistics on the total and average trip duration---

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #total travel time
    total_duration = df['Trip Duration'].sum() / 3600.0
    print("total travel time [h]: ", total_duration)

    #mean travel time
    mean_duration = df['Trip Duration'].mean() / 3600.0
    print("mean travel time [h]: ", mean_duration)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    #---statistics on bikeshare users---

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print('-'*40)

def user_stats_gender_year(df):
    # counts of gender
    
    user_gender = df['Gender'].value_counts()
    print(user_gender)
    
    # earliest, most recent, and most common year of birth
    earliest_year_of_birth = int(df['Birth Year'].min())
    most_recent_year_of_birth = int(df['Birth Year'].max())
    most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
    print("The earliest year of birth is:",earliest_year_of_birth,
          ", most recent one is:",most_recent_year_of_birth,
           "and the most common one is: ",most_common_year_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data (df):
    """Displays the data due filteration.
    5 rows will added in each press"""
    print('press enter to see raw data, press no to skip')
    x = 0
    while (input()!= 'no'):
        x = x+5
        print(df.head(x))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        if city == 'nyc' or 'chicago':
            user_stats_gender_year(df)
        
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
