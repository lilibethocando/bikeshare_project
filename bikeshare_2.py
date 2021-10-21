import time
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

header = st.container()
data_set = st.container()
features = st.container()

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
city = ""
month = ""
day = ""
months = ["january", "february", "march", "april", "may", "june", "all"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

bike_image = Image.open('bicycle.png')
chicago_image = Image.open("chicago.jpg")
washington_image = Image.open("washington.jpg")
nyc_image = Image.open("nyc.jpg")

with header:
    st.title("Welcome to the US bikeshare data explorer!")
    st.image(bike_image, width=700)

with data_set:
    st.header("Below you can select the city, month and day you would like to explore")

    def get_filters():
        """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """
        global city, month, day

        city = st.text_input("Select one city, your options are: Chicago, Washinton or New Your City", key="cities_key").lower()

        if not city:
            st.info("type a city")
        elif city not in ["new york city", "chicago", "washington"]:
            st.error("Your options are: Chicago, Washington or New Your City, no numbers or any other characters are allowed, please try it again")
            st.stop()

        month = st.text_input("Select a month, between January and June or all of them", key="months_key").lower()
        if not month:
            st.info("type a month")
        elif month not in months:
            st.error("Please select only one month between January and June or all of them")
            st.stop()

        day = st.text_input("Select a day, between Monday and Sunday or all of them", key="days_key").lower()
        if not day:
            st.info("type a day")
        elif day not in days:
            st.error("Please select a day, between Monday and Sunday or all of them")
            st.stop()
        if not (city == "" or month == "" or day == ""):
            st.success(f"You have selected city: {city.title()}, month: {month.title()} and day: {day.title()},"
                       f" if this is not what you wanted to type, just go back,"
                       f" delete the word in there and type the new one! Remember to press 'enter' after typing the correct word!")
            if city == "chicago":
                st.image(chicago_image, width=300)
            elif city == "new york city":
                st.image(nyc_image, width=300)
            elif city == "washington":
                st.image(washington_image, width=300)

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

        while city == "" or month == "" or day == "":
            st.stop()
        # load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])
        # convert the Start Time column to datetime
        df["Start Time"] = pd.to_datetime(df["Start Time"])
        # extract month and day of week from Start Time to create new columns
        df["month"] = df["Start Time"].dt.month
        df["day_of_week"] = df["Start Time"].dt.day_name()
        # filter by month if applicable
        if month != "all":
            # use the index of the months list to get the corresponding int
            month = months.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df["month"] == month]
        # filter by day of week if applicable
        if day != "all":
            # filter by day of week to create the new dataframe
            df = df[df["day_of_week"] == day.title()]

        return df


    def time_stats(df):
        # df = load_data(city, month, day)
        """Displays statistics on the most frequent times of travel."""

        st.header("Calculating The Most Frequent Times of Travel...")
        start_time = time.time()

        # display the most common month
        popular_month_number = df["Start Time"].dt.month.mode()[0]
        popular_month = months[popular_month_number-1].title()
        st.write("Most Popular month:", popular_month)

        # display the most common day of week
        popular_day = df["day_of_week"].mode()[0]
        st.write("Most Popular day:", popular_day)

        # display the most common start hour
        df["hour"] = df["Start Time"].dt.hour
        popular_hour = df["hour"].mode()[0]
        st.write("Most Popular Start Hour:", popular_hour)

        st.write("This took %s seconds." % (time.time() - start_time))


    def station_stats(df):
        """Displays statistics on the most popular stations and trip."""

        st.header("Calculating The Most Popular Stations and Trip...")
        start_time = time.time()

        # display most commonly used start station
        popular_start_station = df["Start Station"].mode()[0]
        st.write(f"The most popular start station is: {popular_start_station}")
        # display most commonly used end station
        popular_end_station = df["End Station"].mode()[0]
        st.write(f"The most popular end station is: {popular_end_station}")

        # display most frequent combination of start station and end station trip
        popular_combination = (df["Start Station"] + df["End Station"]).mode()[0]
        st.write(f"The most popular combination is: {popular_combination}")

        st.write("This took %s seconds." % (time.time() - start_time))


    def trip_duration_stats(df):
        """Displays statistics on the total and average trip duration."""

        st.header("Calculating Trip Duration...")
        start_time = time.time()

        # display total travel time
        total_travel_time = df["Trip Duration"].sum()

        # display mean travel time
        mean_travel_time = df["Trip Duration"].mean()
        st.write(f"This is the total trip duration: {round(total_travel_time)}, this is the AVG duration: {round(mean_travel_time)}")

        st.write("This took %s seconds." % (time.time() - start_time))


    def user_stats(df):
        """Displays statistics on bikeshare users."""

        st.header("Calculating User Stats...")
        start_time = time.time()

        st.subheader("Here you can see the type of users, the count for each type and the gender")
        # Display counts of user types
        user_count = df["User Type"].value_counts()
        st.write(user_count)

        # Display counts of gender
        if city == "washington":
            st.write("No gender information available for this city")
        else:
            gender_count = df["Gender"].value_counts()
            st.write(gender_count)

        # Display earliest, most recent, and most common year of birth
        if city == "washington":
            st.write("No birth year information available for this city")
        else:
            earliest_year = df["Birth Year"].min()
            most_recent_year = df["Birth Year"].max()
            most_common_year = df["Birth Year"].mode()[0]

        if city != "washington":
            st.write(f"The oldest user was born in {int(earliest_year)}, the youngest one in {int(most_recent_year)} and most of the users were born in {int(most_common_year)}")


        print("\nThis took %s seconds." % (time.time() - start_time))


    def main():
        #while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        st.info("All the data used on this page has been provided by Udacity for "
                "'Programming for data science with python' nanodegree, specifically "
                "for the 'bikeshare' project.")
        st.markdown("**If you finished click the button below. Otherwise, scroll up and keep exploring the data!**")
        restart = st.button("Goodbye!", key="button_key")
        if restart:
            st.balloons()
            st.stop()


if __name__ == "__main__":
    main()










