# Signal Mapping Mumbai 🗺️📶

A CSV-based web application for visualizing cellular network signal strength across Mumbai and identifying potential low-signal or dead zones using geographic coordinates.

## Overview

Signal Mapping Mumbai transforms cellular network measurement data into an interactive map. Users can upload CSV datasets, explore signal strength geographically, filter records by network operator, and identify areas where the average signal strength falls below a defined threshold.

The application uses Python and Pandas for data processing, Flask for the backend, and Leaflet with OpenStreetMap for interactive mapping.

## Features

- **CSV Data Upload:** Upload cellular signal datasets in CSV format.
- **Interactive Signal Mapping:** Display geographic signal measurements on a map.
- **Signal Strength Visualization:** Color-coded markers represent signal strength.
- **Network Operator Filtering:** Filter measurements by operator/SIM.
- **Signal Quality Classification:** Categorize measurements as Excellent, Good, Fair, or Poor.
- **Dead-Zone Detection:** Group nearby measurements into geographic grid cells and identify cells with average signal strength below -110 dBm.
- **Data Table:** View latitude, longitude, signal strength, signal quality, network type, and operator.
- **Summary Statistics:** Display the total number of records and average signal strength.
- **Dynamic Map Updates:** Refresh map markers and table results based on the selected filter and visualization mode.

## Technology Stack

- **Programming Language:** Python, JavaScript
- **Backend:** Flask
- **Data Processing:** Pandas
- **Frontend:** HTML, CSS, JavaScript
- **Mapping Library:** Leaflet.js
- **Map Data / Tiles:** OpenStreetMap
- **Data Format:** CSV
- **API:** Flask JSON endpoint

## How It Works

1. Upload a cellular signal measurement dataset in CSV format.
2. The Flask backend validates the file extension and normalizes column names.
3. Pandas converts latitude, longitude, and signal strength into numeric values and removes records with missing or invalid required values.
4. The application classifies signal quality and supports operator-based filtering.
5. In dead-zone mode, measurements are grouped into geographic grid cells and their average signal strength is calculated.
6. Cells with an average signal below -110 dBm are returned as potential dead zones.
7. The frontend displays the results on an interactive map and in a data table.

## CSV Data Format

The dataset should contain the following columns:

| Column | Description |
|---|---|
| `lat` | Latitude |
| `lng` or `long` | Longitude |
| `signal` or `avgsignal` | Signal strength in dBm |
| `radio` | Network technology/type (optional) |
| `sim` | Operator/SIM identifier (optional) |

Column names are normalized, and supported alternatives are mapped to the expected names.

## Signal Classification

| Signal Strength | Classification | Map Color |
|---|---|---|
| -79 dBm and above | Excellent | Green |
| -89 to below -79 dBm | Good | Blue |
| -99 to below -89 dBm | Fair | Orange |
| Below -99 dBm | Poor | Red |

The dead-zone detection threshold is **below -110 dBm average signal strength** per grid cell.

## Installation and Setup

### Prerequisites

- Python 3.9 or later
- pip
- A modern web browser
- Internet access for loading OpenStreetMap tiles

### 1. Clone the repository

```bash
git clone https://github.com/manasvi-1206/signal-mapping-mumbai-.git
cd signal-mapping-mumbai-
```

### 2. Install dependencies

```bash
python -m pip install flask pandas
```

### 3. Run the application

```bash
python app.py
```

### 4. Open the application

Visit:

```text
http://127.0.0.1:5000
```

Upload a CSV dataset to begin exploring the signal measurements.

## API Endpoint

`GET /api/data`

Supported query parameters:

- `operator`: Filter by operator/SIM, or use `All`.
- `mode`: Use `all` for signal measurements or `dead` for dead-zone results.

Example:

```text
/api/data?operator=All&mode=all
```

```text
/api/data?operator=All&mode=dead
```

The endpoint returns the processed records as JSON.

## Project Structure

```text
signal-mapping-mumbai-/
├── app.py
├── script.js
├── style.css
├── templates/
│   └── index.html
└── data/
    └── cleaned_uploaded.csv
```

The `data/` directory and cleaned CSV are created or populated during upload. The HTML template is required by the Flask application.

## Limitations

- Results depend on the quality, coverage, and accuracy of the uploaded dataset.
- Dead-zone detection uses a configurable geographic grid and signal threshold, rather than a predictive machine learning model.
- The current implementation processes uploaded CSV measurements; it does not directly measure live cellular signals.
- OpenStreetMap tiles require an internet connection.

## Future Improvements

- Add signal coverage heatmaps.
- Compare multiple operators across geographic regions.
- Introduce time-based signal analysis.
- Add downloadable reports and filtered CSV exports.
- Improve data validation and secure file handling.

## Author

**Manasvi More**

GitHub: https://github.com/manasvi-1206

