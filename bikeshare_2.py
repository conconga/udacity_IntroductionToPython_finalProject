import time, sys
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago'      : 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington'   : 'washington.csv'
} 

VALID_INPUTS = {
    'cities' : list(CITY_DATA.keys()),
    'months' : [ 'all', 'january', 'february', 'march', 'april', 'may', 'june', ],
    'daysWk' : [ 'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', ],
    'yesno'  : [ 'yes', 'no' ],
}

def fn_format_question_and_answer(question, valid_data,):
    """
    Presents the question and waits for a valid answer.

    Args:
        (str)        question   : text with the questions, ending with '?'
        (list(str))  valid_data : possible alternatives that the user is allowed to provide.

    Return:
        (str) choice :  selected option
    """

    while True:

        # the question:
        print(f"\n--> {question}")
        print(f"  [your options is (either numeric or string) ..]")
        for idx, option in enumerate(valid_data):
            print(f"   {idx+1:2d}. '{str(option)}'")

        # and the answer:
        ret = input("  your choice = ")

        # validation of the answer:
        #  1) the answer can be a str(number), or
        #  2) a string possibly in the valid_data.

        errors = False
        # validate the return as a number:
        try:
            idx_choice = int(ret) - 1
        except:
            errors = True

        if not errors:
            # it will get here if idx_choice is a number:
            if not (0 <= idx_choice < len(valid_data)):
                errors = True
        else:
            # the choice still might be a text in the valid_data:
            if ret.lower().strip() in valid_data:
                # nice, the option is valid!
                idx_choice = valid_data.index(ret.lower().strip())
                errors = False # reset this because the option is valid
            else:
                errors = True

        # what to do now? the user chooses...
        if errors:
            print("\n--> INVALID ANSWER. Type '0' to abort or '1' to try again.")
            ret = input("  your choice = ")
            print()

            if ret == '1':
                pass
            else:
                if ret != '0':
                    print('WELL... I GUESS YOU ARE GIVING UP!')
                sys.exit(0) # aborting...

        else: # no errors!
            return valid_data[idx_choice]

def test_format_question_and_answer():
    ret = format_question_and_answer("question?", VALID_INPUTS['cities'])
    print(f"the return was = {str(ret)}")
    assert ret in [(0, None)] + [(1,i) for i in VALID_INPUTS['cities']]


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
    city = fn_format_question_and_answer("From which city you want to analyze the data?", VALID_INPUTS['cities'])

    # get user input for month (all, january, february, ... , june)
    month = fn_format_question_and_answer("Select a month to analyze.", VALID_INPUTS['months'])

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = fn_format_question_and_answer("Select a day of week to analyze.", VALID_INPUTS['daysWk'])

    print('-'*40)
    print(f"your selection: '{city}', month:{month}, day_of_week:{day}")
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month) # 1...12
    # alternative:
    df['month'] = df['Start Time'].dt.month # 1...12

    df['day_of_week'] = df['Start Time'].apply(lambda x: x.dayofweek) # 0...6; 0=Mo
    # alternative:
    df['day_of_week'] = df['Start Time'].dt.dayofweek # 0...6; 0=Mo

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = VALID_INPUTS['months'][1:] # the first entry is "all".
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = VALID_INPUTS['daysWk'][1:] # the first entry is "all".
        day  = days.index(day)

        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    ans = int( pd.to_datetime(df['Start Time']).apply(lambda x: x.month).value_counts().index[0] )
    print(f"  . the most common month is {ans} ({VALID_INPUTS['months'][ans]})")

    # display the most common day of week
    ans = int( pd.to_datetime(df['Start Time']).apply(lambda x: x.dayofweek).value_counts().index[0] )
    ans += 1 # monday is 0, but appears as the second in the list
    print(f"  . the most common day-of-week is {VALID_INPUTS['daysWk'][ans]}")


    # display the most common start hour
    ans = int( pd.to_datetime(df['Start Time']).apply(lambda x: x.hour).value_counts().index[0] )
    print(f"  . the most common start-hour is {ans}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    ans = df['Start Station'].apply(lambda x: x.strip()).value_counts().index[0]
    print(f"  . the most commonly used start station is '{ans}'")

    # display most commonly used end station
    ans = df['End Station'].apply(lambda x: x.strip()).value_counts().index[0]
    print(f"  . the most commonly used end station is '{ans}'")

    # display most frequent combination of start station and end station trip
    ans = pd.DataFrame({'start': df['Start Station'], 'end': df['End Station']})
    ans['trip'] = ans.apply(lambda x: f'from {x["start"].strip()} to {x["end"].strip()}', axis=1)
    ans = ans['trip'].value_counts().index[0]
    print(f"  . the most frequent combination of start- and end-station trip is '{ans}'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ans = pd.DataFrame({'start': pd.to_datetime( df['Start Time'] ), 'end': pd.to_datetime( df['End Time'] )})
    ans['delta'] = ans.apply(lambda x: (x['end'] - x['start']).total_seconds()/60., axis=1) # in minutes
    print(f"  . the total travel time ranges from {ans['delta'].min():1.1f}[min] to {ans['delta'].max():1.1f}[min]")

    # display mean travel time
    print(f"  . the mean travel time is {ans['delta'].mean():1.1f}[min]")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ans = str(df['User Type'].value_counts()).splitlines()
    print("  . counts of user types:")
    for i in ans[1:-1]: # the first row is title and the last row is about datatype.
        print(f'   \\ {i}')

    # Display counts of gender
    ans = str(df['Gender'].value_counts()).splitlines()
    print("\n  . counts of Gender:")
    for i in ans[1:-1]: # the first row is title and the last row is about datatype.
        print(f'   \\ {i}')

    # Display earliest, most recent, and most common year of birth
    ans = df['Birth Year']
    print()
    print(f"  . the earliest year of birth is {int(np.round(ans.min()))}")
    print(f"  . the most recent year of birth is {int(np.round(ans.max()))}")
    print(f"  . the most common year of birth is {int(np.round(ans.value_counts().index[0]))}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def fn_display_raw_data(df):
    """
    Interacts with user to display raw data.
    """

    to_show = fn_format_question_and_answer("Would you like to see 5 entries of the raw data?", VALID_INPUTS['yesno'])
    if to_show == "no":
        return

    idx_next_to_display = 0
    while True:

        # here only the next 5 will be shown:
        print()
        print(df.iloc[idx_next_to_display:(idx_next_to_display+5)])

        # ready for the next chunk:
        idx_next_to_display += 5

        # if there are more 5 items available to display, then offer this to the user.
        if (idx_next_to_display+5) < len(df):

            to_show = fn_format_question_and_answer("Would you like to see the next 5?", VALID_INPUTS['yesno'])
            if to_show == "no":
                break

        else:
            # not enough data to show
            print(f"\n** not enough data to display another chunk (current position = {idx_next_to_display} / data length = {len(df)} **")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        fn_display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
