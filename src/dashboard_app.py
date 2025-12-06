import streamlit as st
import pandas as pd

from .data_loading import load_raw_data
from .data_cleaning import full_clean_pipeline, TRIP_DATE_COL
from .analytics import (
    hourly_trip_counts,
    daily_trip_counts,
    weekly_trip_counts,
    user_type_summary,
    trip_duration_summary,
)
from .plots import (
    plot_hourly_usage,
    plot_daily_trends,
    plot_weekly_trends,
    plot_popular_stations,
    plot_duration_histogram,
    plot_user_type_comparison,
    plot_monthly_trends,
    build_station_map_figure,
)


@st.cache_data
def load_and_prepare_data() -> pd.DataFrame:

    """
    Load the raw dataset and apply the full cleaning process
    """
    
    df_raw = load_raw_data()
    df_clean = full_clean_pipeline(df_raw)
    return df_clean


def main():
    st.title("Toronto Bike-Sharing Analytics Dashboard")
    st.markdown(
        """
        This dashboard provides insights into Toronto's bike-sharing usage for August 2024.
        Use the filters on the left to explore different slices of the data.
        """
    )

    df = load_and_prepare_data()

    # ----------------------------------------------------------------------
    # Sidebar Filters
    # ----------------------------------------------------------------------
    
    st.sidebar.header("Filters")
    
    # Date filter based on TRIP_DATE_COL
    min_date = df[TRIP_DATE_COL].min()
    max_date = df[TRIP_DATE_COL].max()
    date_range = st.sidebar.date_input(
        "Trip Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    # User type filter (Casual Member, Annual Member)
    user_types = sorted(df["User Type"].unique())
    selected_user_types = st.sidebar.multiselect(
        "User Types",
        options=user_types,
        default=user_types,
    )
    
    # Bike model filter
    models = sorted(df["Model"].unique())
    selected_models = st.sidebar.multiselect(
        "Bike Model",
        options=models,
        default=models,
    )

    # ----------------------------------------------------------------------
    # Apply filters to the dataset
    # ----------------------------------------------------------------------
    
    filtered = df[
        (df[TRIP_DATE_COL] >= date_range[0])
        & (df[TRIP_DATE_COL] <= date_range[1])
        & (df["User Type"].isin(selected_user_types))
        & (df["Model"].isin(selected_models))
    ]

    # ----------------------------------------------------------------------
    # Summary Metrics Section
    # ----------------------------------------------------------------------
    
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)

    total_trips = len(filtered)
    duration_stats = trip_duration_summary(filtered)
    # Top start station
    top_start_station = (
        filtered["Start Station Name"]
        .value_counts()
        .idxmax()
        if not filtered.empty
        else "N/A"
    )

    col1.metric("Total Trips", f"{total_trips:,}")
    col2.metric(
        "Avg Trip Duration (min)",
        f"{duration_stats.get('mean', 0):.1f}" if duration_stats else "N/A",
    )
    col3.metric("Top Start Station", top_start_station)

    # ----------------------------------------------------------------------
    # Tab layout for different analysis sections
    # ----------------------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Hourly Usage",
            "Daily & Weekly Trends",
            "Popular Stations",
            "Duration Distribution",
            "User Type Comparison",
            "Map (Optional)",
        ]
    )
    # Tab 1: Hourly Usage
    with tab1:
        st.subheader("Trips per Hour")
        fig_hour = plot_hourly_usage(filtered)
        st.pyplot(fig_hour)
        
    # Tab 2: Daily & Weekly Ridership
    with tab2:
        st.subheader("Daily & Weekly Ridership")
        fig_daily = plot_daily_trends(filtered)
        st.pyplot(fig_daily)

        st.markdown("---")
        st.subheader("Weekly Ridership")
        fig_weekly = plot_weekly_trends(filtered)
        st.pyplot(fig_weekly)

    # Tab 3: Popular Stations
    with tab3:
        st.subheader("Popular Start Stations")
        fig_start = plot_popular_stations(filtered, top_n=10, by="start")
        st.pyplot(fig_start)

        st.markdown("---")
        st.subheader("Popular End Stations")
        fig_end = plot_popular_stations(filtered, top_n=10, by="end")
        st.pyplot(fig_end)

    # Tab 4: Duration Distribution
    with tab4:
        st.subheader("Trip Duration Distribution")
        fig_dur = plot_duration_histogram(filtered)
        st.pyplot(fig_dur)

    # Tab 5: User Type Comparison
    with tab5:
        st.subheader("User Type Comparison")
        fig_ut = plot_user_type_comparison(filtered)
        st.pyplot(fig_ut)

    # Tab 6: Map Visualization
    with tab6:
        st.subheader("Station Usage Map (Start Stations)")
        map_fig = build_station_map_figure(filtered)
        if map_fig is None:
            st.info(
                "No station coordinates found. Add 'stations_coordinates.csv' "
                "to the data folder to enable the map."
            )
        else:
            st.plotly_chart(map_fig, use_container_width=True)


if __name__ == "__main__":
    main()
