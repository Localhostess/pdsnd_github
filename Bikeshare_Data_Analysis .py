#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
This script analyzes bikeshare data for New York, Chicago and Washington.
The script provides descriptive statistics upon user input.
Enniye Timiebi (Programming For Data Science Nanodegree)
"""

import time
import pandas as pd
import numpy as np
""" Imports the necessary libraries and modules required
for the analysis"""

CITIES_DATA = {'chicago': 'chicago.csv','new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

CITIES = ['chicago', 'new york city', 'washington']
MONTHS = ['all','january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello there! Thank you choosing our service.\n Please select a city below...\n")
    """This function prompts the user to select their preferred city."""

    while True:
        city = input("\nPlease enter city name:").lower()
        if city not in CITIES_DATA:
            print("\nInvalid selection! Please try again...\n")
        else:
            break

    while True:
        month = input("\nPlease enter preferred month: all, January, February, March, April, May, June.\n").lower()
        if month not in MONTHS:
            print("\nInvalid selection. Please try again..")
        else:
            break

    while True:
        day = input("\nPlease enter preferred week day:\n").lower()
        if day not in DAYS:
            print("\nPlease check for incorrect spellings and try again...")
        else:
            break
    print("_" * 40)
    return(city, month, day)


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

    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    """Reads CSV file of selected city."""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])


    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    """ Splits up Start Time column for proper analysis"""

    return df

def time_stats(df):

    """Displays statistics for the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    busiest_month = df['month'].value_counts().idxmax()
    print("The most common month of travel:", busiest_month)

    busiest_day = df['day_of_week'].value_counts().idxmax()
    print("The most common day of travel:", busiest_day)

    most_travelled_hour = df['hour'].value_counts().idxmax()
    print("The most common hour of travel:", most_travelled_hour)



    df.drop('day_of_week', axis=1,inplace=True)
    df.drop('month', axis=1,inplace=True)
    df.drop('hour',axis=1,inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_popular_sstation = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station:", most_popular_sstation)

    most_popular_estation = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station:", most_popular_estation)

    most_popular_station_combo = df[['End Station','Start Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}".format(most_popular_station_combo[0], most_popular_station_combo[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is:", total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is:", mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].count()
    print("The count of user types:", user_type)

    try:
        gender_count = df['Gender'].value_counts()
        print("The gender count:\n", gender_count)
    except:
        print("We're sorry but this dataset does not contain a gender column.")

    try:
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()
        print("The oldest users were born in:", int(min_birth_year))
        print("The youngest users were born in:", int(max_birth_year))
        print("The most common birth year is:", int(most_common_birth_year))
    except:
        print("We're sorry but this dataset does not contain a birth year column.")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_data(df):
    """Displays five lines of data if user indicates that they would like to see raw data."""
    start_time = time.time()
    while True:
        step = 0
        data = df
        prompt = input("Would you like to see 5 lines of raw data? Please enter yes or no\n")
        if prompt.lower() == 'yes' or prompt.lower() == 'y' or prompt.lower() == 'yeah':
            step = step + 5
            print(df.iloc[:step])
        else:
            break
        prompt2 = input("Would you like to see another 5 lines of raw data? Please enter yes or no\n")
        if prompt2.lower() == 'yes' or prompt2.lower() == 'y' or prompt2.lower() == 'yeah':
            print(df.iloc[:step + 5])
            continue
        else:
            print("\nThis took %s seconds." % (time.time() - start_time))
            break
            print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nHope you found our service helpful.\nWould you like to restart? Enter yes or no.\n').lower()
        print()
        if restart != 'yes' and restart != 'y' and restart != 'yus':
            break

if __name__ == "__main__":
	main()










# In[ ]:





# In[ ]:
