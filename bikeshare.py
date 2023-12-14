import datetime, time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ('january', 'february', 'march', 'april', 'may', 'june')
WEEKDAYS = ('monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = select(f'Select city to do analysis {CITY_DATA.keys()}: ', CITY_DATA.keys())
        month = select(f'Select month {MONTHS}: ', MONTHS)
        day = select(f'Select day {WEEKDAYS}: ', WEEKDAYS)
        break

    return city, month, day

def select(userInput, options):
    """
    a simple selection function

    Args:
        question - question to ask user
        options - list of options to select

    Returns:
        selectedOption - user's choice
    """
    while True:
        selectedOptions = input(userInput).lower().strip()
        if selectedOptions == 'exit':
            raise SystemExit
        elif selectedOptions == 'all':
            selectedOptions = options
            break
        else:
            selectedOptions = [x.strip().lower() for x in selectedOptions.split(',')]
            allOptionValid = True
            # Check if options are all valid
            for selectedOption in selectedOptions:
                if selectedOption not in options:
                    allOptionValid = False
                    print(f'Option `{selectedOption}` is not valid')
            if allOptionValid == True:
                break;

    return selectedOptions

def load_data(cities, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Loading data")
    print(f'Filter by cities: {cities}')
    print(f'Filter by months: {month}')
    print(f'Filter by days: {day}')
    
    # Load data then filter by city
    df = pd.concat(map(lambda city: pd.read_csv(
            CITY_DATA[city]), cities), sort=True)            
    
    # Transform Data
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract more info
    df['Start Month'] = df['Start Time'].dt.month
    df['Start Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    
    # Filter data by MONTH
    df = pd.concat(map(lambda month: df[df['Start Month'] == (MONTHS.index(month)+1)], month))
    
    # Filter data by DAY
    df = pd.concat(map(lambda day: df[df['Start Weekday'] == (day.title())], day))
    
    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    mostCommonMonth = df.mode()['Start Month'][0]
    mostCommonMonth = int(mostCommonMonth)
    mostCommonMonth = MONTHS[mostCommonMonth-1].capitalize()
    print(f'Most common Month is `{mostCommonMonth}`')

    # TO DO: display the most common day of week
    mostCommonWeekDay = df.mode()['Start Weekday'][0]
    print(f'Most common Week Day is `{mostCommonWeekDay}`')

    # TO DO: display the most common start hour
    mostCommonHour = df.mode()['Start Hour'][0]
    print(f'Most common Hour is `{mostCommonHour}`')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mostStartStation = df.mode()['Start Station'][0]
    print(f'Most common Start Station is `{mostStartStation}`')

    # TO DO: display most commonly used end station
    mostEndStation = df.mode()['End Station'][0]
    print(f'Most common End Station is `{mostEndStation}`')

    # TO DO: display most frequent combination of start station and end station trip
    mostFrequentRoute = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'Most common Route is `{mostFrequentRoute[0]} - {mostFrequentRoute[1]}`')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    totalTravelTime = df['Trip Duration'].sum()
    totalTravelTime = float(totalTravelTime)
    totalTravelTime = datetime.timedelta(seconds = totalTravelTime)
    print(f'Total travel time: {totalTravelTime}\n')
    # TO DO: display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    userTypeStats = df['User Type'].value_counts().to_string()
    print(f'User Type stats:\n{userTypeStats}\n')
    

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        userGenderStats = df['Gender'].value_counts().to_string()
        print(f'User Gender stats:\n{userGenderStats}\n')
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliestYearOfBirth = int(df['Birth Year'].min())
        mostRecentYearOfBirth = int(df['Birth Year'].max())
        mostCommonYearOfBirth = int(df['Birth Year'].mode()[0])

        print(f'The Earliest year of birth: {earliestYearOfBirth}')
        print(f'Most Recent year of birth: {mostRecentYearOfBirth}')
        print(f'Most Common year of birth: {mostCommonYearOfBirth}')
    else:
        print(f'Birth year stats cannot be calculated because Birth Year does not appear in the dataframe')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
