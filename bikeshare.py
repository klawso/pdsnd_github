#!/usr/bin/env python
# coding: utf-8

# In[27]:


import time
import pandas as pd
import numpy as np
import datetime

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
    while True:
        try:
            city = str(input("Enter city name Chicago, New York City, or Washington):")).lower()
            if city not in {"chicago","new york city","washington"}:
                raise Exception
        except Exception:
            print("You have not entered a valid city. Please re-enter.")
        else:
            break
            
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Enter month name (all or anything in between january-june):")).lower()
            if month not in {'all','january', 'february', 'march', 'april', 'may', 'june'}:
                raise Exception                          
        except Exception:
            print("You have not entered a valid month. Please re-enter.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("Enter day of the week (all or any day of the week(eg: monday,tuesday..):")).lower()
            if day not in {'all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'}:
                raise Exception                          
        except Exception:
            print("You have not entered a valid weekday name. Please re-enter.")
        else:
            break
    print('You entered:  \n')
    print(city.title() + ", " + month.title() + ", and " + day.title())
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
    # load data file into a dataframe
    df =  pd.read_csv(CITY_DATA[city])
    

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the Start Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, hour, and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    #create new column concatenating start and end stations
    df['common_station'] = df['Start Station'] + ' → ' + df['End Station']
       

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
    print('\nThe most common month is:  ')
    
    
    # display the most common month as month name
    common_month = df['month'].mode()[0]
    d = datetime.datetime(1,common_month,1)
    print(d.strftime('%B'))

    # display the most common day of week
    print('\nThe most common day of week is:  ')
    common_day = df['day_of_week'].mode()[0]
    print(common_day)

    # display the most common start hour as hour
    print('\nThe most common start hour is:  ')
    common_hour = df['hour'].mode()[0]
    if common_hour <= 12:
        print(common_hour,'AM')
    else:
        print(common_hour - 12,'PM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most common Start Station is:  ')
    common_st_station = df['Start Station'].mode()[0]
    print(common_st_station)

    # display most commonly used end station
    print('\nThe most common End Station is:  ')
    #common_end_station = df.groupby(['End Station'])
    common_end_station = df['End Station'].mode()[0]
    print(common_end_station)

    # display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of Start Station and End Station trip is:  ')
    common_station = df['common_station'].mode()[0]
    print(common_station)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time in seconds, minutes, hours, and days
    print('Total duration in seconds is:  ',df['Trip Duration'].sum())
    print('Total duration in minutes is:  ',df['Trip Duration'].sum()/60)
    print('Total duration in hours is:  ',df['Trip Duration'].sum()/60/60)
    print('Total duration in days is:  ',df['Trip Duration'].sum()/60/60/24)


    # display mean travel time in seconds and minutes
    
    print('The mean duration in seconds is:  ',df['Trip Duration'].mean())
    print('The mean duration in minutes is:  ',df['Trip Duration'].mean()/60)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print('The distribution of User Type is:\n' + user_types.to_string(header=None) +'\n')

    # Display counts of gender with error handling for missing fields
    if 'Gender' in df.columns:
        sex = df.groupby(['Gender'])['Gender'].count()
        print('The distribution of Gender is:\n'+ sex.to_string(header=None))
        print('The count of null values for Gender field is:  ',df['Gender'].isnull().sum())
        
    else:
        print('Cannot display information:  Gender field does not exist\n')


    # Display earliest, most recent, and most common year of birth with error handling for missing fields
    if 'Birth Year' in df.columns:
        df['Birth Year'] = df['Birth Year'].dropna().astype(np.int32)
        minimum = df['Birth Year'].min()

        print('\nThe earliest Birth Year is:  ',str(df['Birth Year'].min()).split('.')[0])
        print('\nThe most recent Birth Year is:  ',str(df['Birth Year'].max()).split('.')[0])
        print('\nThe most common Birth Year is:  ',str(df['Birth Year'].mode()[0]).split('.')[0])
        
    else:
        print('Cannot display information:  Birth Year field does not exist')
    
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
        
        # Display next five rows of data in the data frame 
        i = 0
        j = 5

               
        def displaydata(df):
            for i,j in df.iloc[i:j]:
                i = 0
                j = 5
                return df
                
        while True:
            display2 = input("\n Would you like to view the next five rows of the data? Please write 'yes' or 'no' \n").lower()
            if display2.lower() == 'no':
                break
            if display2 not in ("yes","no"):
                
                print("Invalid entry; please enter yes or no\n")
                
            if display2.lower() == 'yes':
                print(df.iloc[i:j].copy())
                i = i + 5
                j = j + 5
         
        # Do you want to restart "explore bikeshare data" request 
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

#     end of code


# In[ ]:





# In[ ]:





# In[ ]:




