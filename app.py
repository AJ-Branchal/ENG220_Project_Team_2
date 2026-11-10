import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Cuba, New Mexico | Safety Dashboard",
    page_icon="🛡️",
    layout="wide"
)

CSV_FILE = "cuba_safety_project_data.csv"

# ==================================================
# CUSTOM DESIGN
# ==================================================

st.markdown("""
<style>
    .main {
        background-color: #F4F6F9;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #142B4A;
    }

    .hero {
        background: linear-gradient(120deg, #142B4A, #2463A5);
        padding: 32px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #E5EDF8;
        font-size: 17px;
    }

    .section-card {
        background-color: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #E1E6ED;
        margin-bottom: 15px;
    }

    .small-note {
        color: #64748B;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border: 1px solid #E1E6ED;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data(ttl=300)
def load_data():

    data = pd.read_csv(CSV_FILE)

    data.columns = (
        data.columns
        .str.strip()
        .str.lower()
    )

    # Clean text columns
    text_columns = [
        "category",
        "topic",
        "geography",
        "metric",
        "unit",
        "source_name",
        "source_url",
        "status",
        "notes"
    ]

    for col in text_columns:
        if col in data.columns:
            data[col] = (
                data[col]
                .astype("string")
                .str.strip()
            )

    # Convert numeric fields
    if "year" in data.columns:
        data["year"] = pd.to_numeric(
            data["year"], errors="coerce"
        )

    if "value" in data.columns:
        data["value"] = pd.to_numeric(
            data["value"], errors="coerce"
        )

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        f"Cannot find {CSV_FILE}. "
        "Make sure it is in the same folder as app.py."
    )
    st.stop()

except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

@st.cache_data(ttl=300)
def load_local_data():

    local_data = pd.read_csv("Cuba_data.csv")

    # Clean column names
    local_data.columns = (
        local_data.columns
        .str.strip()
        .str.lower()
    )

    # Rename columns to match dashboard conventions
    local_data = local_data.rename(columns={
        "offense type": "topic",
        "metric type": "metric",
        "total per agency": "value",
        "source": "source_name",
        "url": "source_url"
    })

    # Add category
    local_data["category"] = "Crime Statistics"

    # Clean geography
    local_data["geography"] = (
        local_data["geography"]
        .astype("string")
        .str.strip()
    )

    # Convert numeric columns
    local_data["year"] = pd.to_numeric(
        local_data["year"], errors="coerce"
    )

    local_data["value"] = pd.to_numeric(
        local_data["value"], errors="coerce"
    )

    return local_data


local_crime_df = load_local_data()

# ==================================================
# CHECK DATASET
# ==================================================

required_columns = [
    "category",
    "topic",
    "geography",
    "year",
    "metric",
    "value"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "Missing required CSV columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def display_table(data):

    display_data = data.copy()

    if "year" in display_data.columns:
        display_data["year"] = (
            display_data["year"].apply(
                lambda x: int(x) if pd.notna(x) else None
            )
        )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


def get_column_values(data, column):

    if column not in data.columns:
        return []

    return sorted(
        data[column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


def display_sources(data):

    source_columns = [
        col for col in [
            "topic",
            "geography",
            "source_name",
            "source_url",
            "status",
            "notes"
        ]
        if col in data.columns
    ]

    if source_columns:
        st.dataframe(
            data[source_columns],
            use_container_width=True,
            hide_index=True
        )


def show_comparison_chart(data, chart_key):

    chart_data = data.dropna(
        subset=["value"]
    ).copy()

    if chart_data.empty:
        st.info(
            "No numeric values are available for this selection."
        )
        return

    # Select one topic and metric to avoid
    # comparing unrelated measurements.

    topics = get_column_values(
        chart_data, "topic"
    )

    if not topics:
        st.info("No topic information is available.")
        return

    selected_topic = st.selectbox(
        "Choose a topic",
        topics,
        key=f"topic_{chart_key}"
    )

    chart_data = chart_data[
        chart_data["topic"].astype(str) == selected_topic
    ].copy()

    metrics = get_column_values(
        chart_data, "metric"
    )

    if not metrics:
        st.info("No measurement information is available.")
        return

    selected_metric = st.selectbox(
        "Choose a measurement",
        metrics,
        key=f"metric_{chart_key}"
    )

    chart_data = chart_data[
        chart_data["metric"].astype(str) == selected_metric
    ].copy()

    # Select unit if multiple units exist
    if "unit" in chart_data.columns:

        units = get_column_values(
            chart_data, "unit"
        )

        if len(units) > 1:

            selected_unit = st.selectbox(
                "Choose a unit",
                units,
                key=f"unit_{chart_key}"
            )

            chart_data = chart_data[
                chart_data["unit"].astype(str) == selected_unit
            ].copy()

    if chart_data.empty:
        st.info("No matching records were found.")
        return

    chart_data["year_label"] = (
        chart_data["year"].apply(
            lambda x: str(int(x)) if pd.notna(x)
            else "Year not reported"
        )
    )

    # Only show a year chart if years are available.
    if chart_data["year"].notna().any():

        chart_data = chart_data.dropna(
            subset=["year"]
        )

        fig = px.bar(
            chart_data,
            x="geography",
            y="value",
            color="year_label",
            barmode="group",
            hover_data=["topic", "metric"],
            labels={
                "geography": "Geographic Area",
                "value": "Reported Value",
                "year_label": "Year"
            },
            title=f"{selected_topic}: Geographic Comparison"
        )

    else:

        fig = px.bar(
            chart_data,
            x="geography",
            y="value",
            color="topic",
            hover_data=["metric"],
            labels={
                "geography": "Geographic Area",
                "value": "Reported Value"
            },
            title=f"{selected_topic}: Geographic Comparison"
        )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#142B4A",
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if chart_data["geography"].nunique() < 2:
        st.caption(
            "Only one geographic area is available for "
            "this measurement. A geographic comparison "
            "cannot be made yet."
        )


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("🛡️ Cuba Safety Dashboard")

st.sidebar.caption(
    "Safety, Security, and Crime in Cuba, New Mexico"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "DASHBOARD MENU",
    [
        "Project Introduction",
        "State-Wide Data Baseline",
        "Local Village Analysis"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Educational Group Project"
)


# ==================================================
# PAGE 1: PROJECT INTRODUCTION
# ==================================================

if page == "Project Introduction":

    # HERO SECTION
    st.markdown("""
    <div class="hero">
        <h1>🛡️ Safety, Security, and Crime</h1>
        <p>Cuba, New Mexico</p>
        <p>
        Exploring available crime statistics, public safety
        information, and community resources.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ABOUT THE PROJECT
    st.subheader("About This Project")

    st.write("""
    This project examines available information related to
    safety, security, and crime in Cuba, New Mexico.

    It brings together available local information and
    broader geographic data to help readers understand
    the public safety information currently available.
    """)

    st.info(
    
        "Important Note: The dataset contains different types of safety-related information. "
        "Some records report crime statistics, while others provide related information about public safety and community resources. "
        "Therefore, not every record represents a confirmed crime incident or crime count."
    )

    st.divider()

    # DATASET SUMMARY
    st.subheader("Dataset at a Glance")

    col1, col2, col3 = st.columns(3)

    # Count unique years from both data files
    combined_years = pd.concat(
        [
            pd.to_numeric(df["year"], errors="coerce"),
            pd.to_numeric(local_crime_df["year"], errors="coerce")
        ],
        ignore_index=True
    ).dropna().nunique()
    with col1:
        st.metric("Total Records", len(df) + len(local_crime_df))

    with col2:
        st.metric(
            "Data Categories",
            pd.concat(
                [df["category"], local_crime_df["category"]]
            ).nunique()
        )

    with col3:
        st.metric("Years Available", combined_years)
    st.divider()

    # PROJECT OBJECTIVES
    st.subheader("Project Objectives")

    goal1, goal2 = st.columns(2)

    with goal1:
        st.markdown("""
        <div class="section-card">
            <h3>🔎 Explore Available Data</h3>
            <p>
            Examine crime statistics, firearm information,
            and community safety resources.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
            <h3>📊 Understand Data Patterns</h3>
            <p>
            Review available measurements and compare
            geographic areas when appropriate.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with goal2:
        st.markdown("""
        <div class="section-card">
            <h3>📍 Focus on Cuba</h3>
            <p>
            Identify information specifically related
            to Cuba, New Mexico.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
            <h3>📚 Identify Data Gaps</h3>
            <p>
            Highlight missing information and areas
            where additional research is needed.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # DATASET COLUMN EXPLANATIONS
    st.subheader("Understanding the Dataset")

    st.write(
        "The table below explains the information contained "
        "in each column of the project dataset."
    )

    descriptions = {
        "category": "The broad subject or classification of the record.",
        "topic": "The specific crime, safety, or community subject.",
        "geography": "The location associated with the information.",
        "year": "The year associated with the reported information.",
        "metric": "The measurement or type of information reported.",
        "value": "The numerical value, when available.",
        "unit": "The unit used to describe the numerical value.",
        "source_name": "The organization or source providing the information.",
        "source_url": "The web address of the original information source.",
        "status": "The verification or data-quality status of the record.",
        "notes": "Additional explanations or context about the record."
    }

    information = pd.DataFrame({
        "Dataset Column": df.columns,
        "Description": [
            descriptions.get(col, "Additional dataset information.")
            for col in df.columns
        ]
    })

    st.dataframe(
        information,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # COMPLETE DATASET
    st.subheader("Complete Project Dataset")

    st.write(
        "Expand the section below to inspect all records "
        "currently included in the project."
    )

    # Combine both project datasets
    combined_df = pd.concat(
        [df, local_crime_df],
        ignore_index=True,
        sort=False
    )

    with st.expander("View Complete Project Dataset"):
        display_table(combined_df)

    # PROJECT SOURCES AND REFERENCES
    st.divider()
    st.subheader("Project Sources and References")

    st.write(
        "The following file contains source links and references "
        "used for the project."
    )

    @st.cache_data(ttl=300)
    def load_source_links():
        return pd.read_csv("cuba_nm_links.csv")

    links_df = load_source_links()

    with st.expander("View Project Sources and References"):
        display_table(links_df)

# ==================================================
# PAGE 2: STATE-WIDE DATA BASELINE
# ==================================================

elif page == "State-Wide Data Baseline":

    st.title("📊 State-Wide Data Baseline")

    st.write("""
    Explore broader crime and safety information available
    for New Mexico and the United States.
    """)

    st.info(
        "This page focuses on broader geographic records. "
        "Cuba-specific and nearby community information "
        "is presented separately on the Local Village Analysis page."
    )

    st.divider()

    # Keep only broader geographic records.
    broad_geographies = [
        "New Mexico",
        "United States",
        "Sandoval County, New Mexico"
    ]

    baseline_df = df[
        df["geography"].isin(broad_geographies)
    ].copy()

    if baseline_df.empty:

        st.warning(
            "No broader geographic records were found."
        )

    else:

        # FILTERS

        st.subheader("Explore the Data")

        col1, col2, col3 = st.columns(3)

        categories = get_column_values(
            baseline_df, "category"
        )

        geographies = get_column_values(
            baseline_df, "geography"
        )

        topics = get_column_values(
            baseline_df, "topic"
        )

        with col1:
            selected_categories = st.multiselect(
                "Data Category",
                categories,
                default=categories
            )

        with col2:
            selected_geographies = st.multiselect(
                "Geographic Area",
                geographies,
                default=geographies
            )

        with col3:
            selected_topics = st.multiselect(
                "Topic",
                topics,
                default=topics
            )

        filtered_df = baseline_df[
            baseline_df["category"].astype(str)
            .isin(selected_categories)
            & baseline_df["geography"].astype(str)
            .isin(selected_geographies)
            & baseline_df["topic"].astype(str)
            .isin(selected_topics)
        ].copy()

        st.divider()

        # SUMMARY

        st.subheader("Analysis Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Records Displayed",
                len(filtered_df)
            )

        with col2:
            st.metric(
                "Geographic Areas",
                filtered_df["geography"].nunique()
            )

        with col3:
            st.metric(
                "Topics Displayed",
                filtered_df["topic"].nunique()
            )

        st.divider()

        # CHART

        st.subheader("Geographic Data Comparison")

        if filtered_df.empty:

            st.info(
                "No records match your selected filters."
            )

        else:

            show_comparison_chart(
                filtered_df,
                "baseline"
            )

        st.divider()

        # TABLE

        st.subheader("Detailed Data Records")

        display_table(filtered_df)

        st.divider()

        st.subheader("Sources and Verification")

        display_sources(filtered_df)

        st.caption(
            "Only records with comparable topics, measurements, "
            "and units should be interpreted together. "
            "A comparison is descriptive, not evidence of causation."
        )


# ==================================================
# PAGE 3: LOCAL VILLAGE ANALYSIS
# ==================================================

elif page == "Local Village Analysis":

    st.title("📍 Local Village Analysis")

    st.write("""
    Explore information specifically associated with
    Cuba, New Mexico, and distinguish it from nearby
    community information.
    """)

    st.divider()

    # EXACT CUBA RECORDS

    cuba_existing_df = df[
        df["geography"].astype(str).str.strip().str.lower()
        == "cuba, new mexico"
    ].copy()

    # Combine existing Cuba records with the new local crime data
    local_df = pd.concat(
        [cuba_existing_df, local_crime_df],
        ignore_index=True,
        sort=False
    )
    # NEARBY BUT NOT EXACTLY CUBA

    nearby_df = df[
        df["geography"].astype(str).str.contains(
            "Cuba",
            case=False,
            na=False
        )
        & (
            df["geography"].astype(str).str.strip().str.lower()
            != "cuba, new mexico"
        )
    ].copy()

    # SUMMARY

    st.subheader("Cuba Community Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Cuba-Specific Records",
            len(local_df)
        )

    with col2:
        st.metric(
            "Local Topics",
            local_df["topic"].nunique()
        )

    with col3:
        st.metric(
            "Nearby Records",
            len(nearby_df)
        )

    st.divider()
     # CUBA CRIME STATISTICS GRAPH

    st.subheader("Cuba Crime Statistics by Offense Type")

    crime_chart_df = local_df[
        local_df["category"].astype(str).str.lower()
        == "crime statistics"
    ].copy()

    if not crime_chart_df.empty:

        crime_chart_df["metric"] = (
            crime_chart_df["metric"]
            .astype("string")
            .str.strip()
        )

        metric_options = sorted(
            crime_chart_df["metric"].dropna().unique()
        )

        selected_metric = st.selectbox(
            "Select Measurement",
            metric_options,
            key="cuba_metric"
        )

        chart_df = crime_chart_df[
            crime_chart_df["metric"] == selected_metric
        ].copy()

         chart_df = chart_df.dropna(subset=["year", "value"]).copy()
        chart_df["year_label"] = chart_df["year"].astype(int).astype(str)

        value_labels = {
            "Number": "Reported offenses",
            "Rate": "Offenses per 100,000 inhabitants",
            "%": "Percent of reported offenses"
        }
        fig = px.bar(
            chart_df,
            x="topic",
            y="value",
            color="year_label",
            barmode="group",
            title=f"Cuba Crime Statistics — {selected_metric}",
            labels={
                "topic": "Offense Type",
                "value":  value_labels[selected_metric],
                "year_label": "Year"
            }
        )

        fig.update_layout(
            xaxis_tickangle=-35,
            legend_title="Year",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No Cuba-specific crime statistics are available.")

    # CUBA SPECIFIC INFORMATION

    st.subheader("Information Specific to Cuba")

    if local_df.empty:

        st.warning(
            "No records specifically identifying Cuba, "
            "New Mexico, were found."
        )

    else:

        st.write(
            "The following records identify Cuba, New Mexico, "
            "as their geographic area."
        )

        with st.expander("View all Cuba-specific records (66)", expanded=False):

            # Topic cards
            for _, record in local_df.iterrows():

                with st.container(border=True):

                    st.markdown(
                        f"**{record['topic']}**"
                    )

                    st.caption(
                        f"Category: {record['category']}"
                    )

                    if pd.notna(record["year"]):
                        st.write(
                            f"Year: {int(record['year'])}"
                        )
                    else:
                        st.write("Year: Not reported")

                    if pd.notna(record["metric"]):
                        st.write(
                            f"Measurement: {record['metric']}"
                        )

                    if pd.notna(record["value"]):
                        st.write(
                            f"Reported value: {record['value']} {record['unit']}"
                        )
                    else:
                        st.write(
                            "Reported value: Not available"
                        )

                    if "notes" in local_df.columns:
                        if pd.notna(record.get("notes")):
                            st.caption(
                                f"Notes: {record['notes']}"
                            )

                    if "source_name" in local_df.columns:
                        if pd.notna(record.get("source_name")):
                            st.caption(
                                f"Source: {record['source_name']}"
                            )

                    if "source_url" in local_df.columns:
                        url = record.get("source_url")

                        if pd.notna(url) and str(url).startswith(
                            ("http://", "https://")
                        ):
                            st.markdown(
                                f"[Open original source]({url})"
                            )

    st.divider()

    # NEARBY INFORMATION

    st.subheader("Nearby Community Information")

    st.write("""
    These records mention locations near Cuba but do not
    represent information specifically measured for the village.
    """)

    if nearby_df.empty:

        st.info(
            "No nearby records are available in this dataset."
        )

    else:

        display_table(nearby_df)

    st.divider()

    # LOCAL DATA LIMITATIONS

    st.subheader("Local Data Gaps and Limitations")

    st.markdown("""
    - The current dataset has limited Cuba-specific records.
    - Available local records include community resources
      and other safety-related topics.
    - These records should not automatically be interpreted
      as crime incident counts.
    - Nearby information should not be treated as village data.
    - Missing years and values are not equivalent to zero.
    - Source information should be verified before drawing
      conclusions.
    """)

    st.info(
        "Additional verified Cuba-specific crime statistics "
        "would help strengthen future versions of this analysis."
    )

    st.divider()

    st.subheader("Local Data Table")

    if not local_df.empty:
        display_table(local_df)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Cuba, New Mexico Safety Dashboard | "
    "Educational Group Project"
)
