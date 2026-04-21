# ==============================
# 1. IMPORT LIBRARIES
# ==============================
import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Hospital Stay Analysis", layout="wide")


# ==============================
# SIDEBAR NAVIGATION
# ==============================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "📊 Summary",
    "📈 Visualization",
    "🤖 Prediction"
])


# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data(file):
    return pd.read_csv(file)


# ==============================
# FILE UPLOAD / DEFAULT
# ==============================
st.sidebar.subheader("Upload Dataset")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
else:
    try:
        df = load_data("../data/hospital_data.csv")
        st.sidebar.success("Default dataset loaded")
    except:
        st.warning("Please upload a dataset")
        st.stop()


# ==============================
# DATA CLEANING
# ==============================
df.drop_duplicates(inplace=True)

# 🔥 FIXED DATE PARSING (ROBUST)
df['Admission_Date'] = pd.to_datetime(
    df['Admission_Date'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)

df['Discharge_Date'] = pd.to_datetime(
    df['Discharge_Date'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)

# Warn user if issues
if df['Admission_Date'].isnull().sum() > 0:
    st.warning("Some Admission_Date values could not be parsed and were removed")

if df['Discharge_Date'].isnull().sum() > 0:
    st.warning("Some Discharge_Date values could not be parsed and were removed")

# Drop invalid rows
df = df.dropna(subset=['Admission_Date', 'Discharge_Date'])


# ==============================
# FEATURE ENGINEERING
# ==============================
df['calculated_stay'] = (df['Discharge_Date'] - df['Admission_Date']).dt.days
df['admission_month'] = df['Admission_Date'].dt.month
df['admission_day'] = df['Admission_Date'].dt.day


# ==============================
# FILTERS
# ==============================
st.sidebar.subheader("Filters")

# Year
years = st.sidebar.multiselect(
    "Year",
    options=sorted(df['Year_of_Admission'].dropna().unique()),
    default=sorted(df['Year_of_Admission'].dropna().unique())
)

# Gender
genders = st.sidebar.multiselect(
    "Gender",
    options=df['Gender'].dropna().unique(),
    default=df['Gender'].dropna().unique()
)

# Condition
conditions = st.sidebar.multiselect(
    "Condition",
    options=df['Condition'].dropna().unique(),
    default=df['Condition'].dropna().unique()
)

# Age
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))


# Apply filters
filtered_df = df[
    (df['Year_of_Admission'].isin(years)) &
    (df['Gender'].isin(genders)) &
    (df['Condition'].isin(conditions)) &
    (df['Age'].between(age_range[0], age_range[1]))
]

if filtered_df.empty:
    st.warning("No data available after applying filters")
    st.stop()


# ==============================
# PAGE 1: SUMMARY
# ==============================
if page == "📊 Summary":

    st.title("📊 Hospital Data Summary")

    st.dataframe(filtered_df.head())

    st.subheader("Statistics")
    st.write(filtered_df.describe())

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", len(filtered_df))
    col2.metric("Avg Stay", round(filtered_df['Length_of_Stay'].mean(), 2))
    col3.metric("Max Stay", filtered_df['Length_of_Stay'].max())

    st.subheader("Missing Values")
    st.write(filtered_df.isnull().sum())


# ==============================
# PAGE 2: VISUALIZATION
# ==============================
elif page == "📈 Visualization":

    st.title("📈 Visualizations")

    fig = px.histogram(filtered_df, x='Length_of_Stay', nbins=20)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(filtered_df, x='Age', y='Length_of_Stay', color='Gender')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(filtered_df, x='Condition', y='Length_of_Stay')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(filtered_df, x='Year_of_Admission', y='Length_of_Stay')
    st.plotly_chart(fig, use_container_width=True)


# ==============================
# PAGE 3: PREDICTION
# ==============================
elif page == "🤖 Prediction":

    st.title("🤖 Prediction Model")

    df_encoded = pd.get_dummies(filtered_df, drop_first=True)

    df_encoded = df_encoded.drop([
        'Patient_ID',
        'Admission_Date',
        'Discharge_Date',
        'Year_of_Admission',
        'admission_day',
        'admission_month'
    ], axis=1, errors='ignore')

    X = df_encoded.drop('Length_of_Stay', axis=1)
    y = df_encoded['Length_of_Stay']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    col1, col2 = st.columns(2)
    col1.metric("R2 Score", round(r2_score(y_test, pred), 3))
    col2.metric("MAE", round(mean_absolute_error(y_test, pred), 3))

    # Feature importance
    importance = pd.Series(model.feature_importances_, index=X.columns)
    importance = importance.sort_values(ascending=False).head(10)

    fig = px.bar(importance, title="Top Features")
    st.plotly_chart(fig, use_container_width=True)

    # Prediction input
    st.subheader("Predict New Value")

    input_data = {}
    for col in X.columns:
        input_data[col] = st.number_input(col, value=0)

    if st.button("Predict"):
        input_df = pd.DataFrame([input_data])
        result = model.predict(input_df)
        st.success(f"Predicted Stay: {round(result[0], 2)} days")