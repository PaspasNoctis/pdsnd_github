import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = CITY_DATA.keys()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

#  get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please select a city to analyze? You can choose from Chicago, New York City or Washington ").lower()
        if city in CITY_DATA.keys():
            print ("You have chosen", city.title())
            break
        else:
            print ("Please select a city from the 3 options")

        # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Which month do you want to select from january to june? Choose all by typing all").lower()
        if month in months:
            print("You have chosen: ", month.title())
            break
        elif month == "all":
            print ("You have chosen all months")
            break
        else:
            print ("Please select a month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day are you interested in? For every weekday types all").lower()
        if day in days:
            print("You have chosen: ", day.title())
            break
        elif day == "all":
            print ("You have chosen all weekdays")
            break
        else:
            print ("Please select a day")

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.dayofweek

    if month != 'all':
        months = [0,'january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        df = df[df['month'] == month]


    if day != 'all':
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                      'saturday', 'sunday']
        day = weekdays.index(day)
        df = df[df['weekday'] == day]

    df['hour'] = df['Start Time'].dt.hour
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = [0,'january', 'february', 'march', 'april', 'may', 'june']
    weekdays = [0,'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday']
#display the most common month
    if month != 'all':
        print ("You have chosen")
        print (month)
    else:
        monthmode=df['month'].mode()[0]
        print(months[monthmode].title())


    # display the most common day of week
    if day != 'all':
        print ("You have chosen")
        print (day)
    else:
        daymode=df['weekday'].mode()[0]
        print(weekdays[daymode].title())
    #display the most common start hour

    hourmode=df['hour'].mode()[0]
    print(hourmode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    print ("The commonly used start station is {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print ("The commonly used end station is {}".format(df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip
    start_end_station = df['Start Station'] + " " + df['End Station']
    print("The most common combination of start and end station is ", start_end_station.mode()[0])



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    totaltime=((df['End Time'] - df['Start Time']))
    print (totaltime.sum())

    # display mean travel time
    print (totaltime.mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    print(df['User Type'].value_counts())

    #  Display counts of gender
    if "Gender" in df.columns:
        print(df['Gender'].value_counts())
    else:
        print ("Sorry no gender data exists for the chosen city")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print ("The earliest year of birth: {}".format(df['Birth Year'].min()))
        print ("The latest year of birth: {}".format(df['Birth Year'].max()))
        print ("The most common year of birth: {}".format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def showrow(df):
        confirm = input('Do you want to see the first 5 rows of the dataset? Please write yes or no').lower()
        if confirm =='yes':
            rows = len(df.index)
            i=1
            while confirm == 'yes':
                print (df.iloc[i:i+5, :])
                i+=5
                if i >= rows:
                    print ("you have reached the end")
                    break
                confirm = input("Do you want to see 5 more rows? Type yes to show or no to stop").lower()
                if confirm == 'no':
                    break
        if confirm !='no':
            showrow(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        showrow(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
  main()
