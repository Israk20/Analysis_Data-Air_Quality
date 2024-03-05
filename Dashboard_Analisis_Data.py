import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('all_data.csv')

# Split the data into dataframes for each station
stations = df['station'].unique()
dataframes = {station: df[df['station'] == station] for station in stations}

# Create a select box in the sidebar
station = st.sidebar.selectbox(
    'Choose a station',
    list(dataframes.keys())
)

# Display the selected station's dataframe
st.write(f"Selected station: {station}")
df = dataframes[station]
st.dataframe(df)

# Display the description of the dataframe
st.write(f"Description of {station}:")
st.write(df.describe(include="all"))

# Display the temperature trends
grouped_df = df.groupby(by="year").agg({
    "No": "nunique",
    "TEMP": ["max", "min", "mean", "std"]
})
st.write(grouped_df)

# Display the line chart for temperature trends
st.write(f"Temperature Trends for Station {station}")
fig, ax = plt.subplots()
ax.plot(grouped_df.index, grouped_df[(
    'TEMP', 'mean')], label='Mean Temperature')
ax.fill_between(grouped_df.index, grouped_df[(
    'TEMP', 'min')], grouped_df[('TEMP', 'max')], color='g', alpha=.1)
ax.set_title(f'Temperature Trends for Station {station}')
ax.set_xlabel('Year')
ax.set_ylabel('Temperature')
ax.legend()
st.pyplot(fig)

# Display the rainfall trends
grouped_df = df.groupby(by="year").agg({
    "No": "nunique",
    "RAIN": ["max", "min", "mean", "std"]
})
st.write(grouped_df)

# Display the bar chart for rainfall trends
st.write(f"Rainfall Trends for Station {station}")
fig, ax = plt.subplots()
ax.bar(grouped_df.index, grouped_df[('RAIN', 'mean')], label='Mean Rainfall')
ax.set_title(f'Rainfall Trends for Station {station}')
ax.set_xlabel('Year')
ax.set_ylabel('Rainfall')
ax.legend()
st.pyplot(fig)

# Add a checkbox to the sidebar to toggle the display of the CO emission trends
show_co_trends = st.sidebar.checkbox('Show CO emission trends')

if show_co_trends:
    # Calculate the total CO emission for each year for the selected station
    total_per_year = df.groupby('year')['CO'].sum().reset_index()

    # Display the CO emission trends
    st.write(f"CO Emission Trends for every station in 2013-2017")
    fig, ax = plt.subplots()
    ax.plot(total_per_year['year'], total_per_year['CO'], marker='o')
    ax.set_title(f'Total CO Emission per Year for Station {station}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total CO Emission')
    st.pyplot(fig)
