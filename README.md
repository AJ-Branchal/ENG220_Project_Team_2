# Cuba, New Mexico Safety Dashboard

**Live app:** [add your Streamlit link here]

A Streamlit dashboard that explores public safety, crime metrics, and infrastructure security factors affecting New Mexico, with a focus on the rural community of Cuba, NM.

## Purpose

Create a centralized, publicly available source of information that gives a more accurate picture of the issues affecting Cuba, supporting more effective planning as the area grows.

## Dashboard Pages

| Page | What it shows |
|---|---|
| **Project Introduction** | Project overview, dataset summary, column definitions, the full combined dataset, and source links |
| **State-Wide Data Baseline** | New Mexico, Sandoval County, and U.S. figures with filters and a geographic comparison chart |
| **Local Village Analysis** | Cuba-specific crime statistics by offense type and year (2018–2020), local records, nearby-area records, and data limitations |

## Repository Structure

```
app.py                  Streamlit application
requirements.txt        Python packages needed to run the app
data/
  cuba_safety_project_data.csv   State, county, national and local safety records
  Cuba_data.csv                  Cuba offense counts, rates and percentages (UCR, 2018–2020)
  cuba_nm_links.csv              Research source links
  Matlab/
    crime_safety.m               Cuba reported offenses by type, 2018–2020
    firearm.m                    Firearm death rates, New Mexico vs. United States
    local_safety.m               Number of sources per local safety topic
    cuba_links_chart.m           Research links by category and geography
Research/               Source documents collected by the team
```

## Running the App

### Deploy on Streamlit Community Cloud

1. Fork this repository to your own GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in (or create an account).
3. Select **Create app**, then choose to deploy from a GitHub repository.
4. Select your fork, the `main` branch, and set the main file path to `app.py`.
5. Select **Deploy**. Streamlit installs the packages in `requirements.txt` automatically.

### Run locally

Requires Python 3.9 or newer.

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

### MATLAB figures

Open any script in `data/Matlab/` in MATLAB and run it to generate the chart. Each script includes a commented-out `exportgraphics` line that saves the figure as a PNG.

## Data Sources

- **Uniform Crime Reports** – New Mexico Department of Public Safety (Cuba offense data, 2018–2020)
- **USAFacts / FBI** – statewide and national crime rates
- Additional state, county and village sources are listed in `data/cuba_nm_links.csv` and on the dashboard's Project Introduction page.

## Limitations

- Cuba-specific data is limited, and the most recent local crime figures are from 2020.
- Some records describe community resources or research coverage rather than crime counts.
- Data for nearby areas or Sandoval County should not be read as village data.
- Missing years or values are not equivalent to zero.
- Comparisons are descriptive and do not show causation.

This dashboard is an educational project, not an official government report. Verify figures against the original sources before relying on them.

## Team

| Member | Role |
|---|---|
| Max Brewer | Project Manager – project management and team coordination |
| Jan Ziglar | Streamlit application development |
| Rachael Stokes | PowerPoint presentation development |
| Brooke Morenus | Video presentation development |
| Sierra Tsosie | Code development |
| Adam Branchal | Repository management |

## Course

Developed for ENG 220, University of New Mexico, Fall 2026.

*Last updated: 11/10/2026*# ENG220_Project_Team_2
