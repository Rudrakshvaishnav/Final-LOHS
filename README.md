# Final-LOHS
# 🏥 Hospital Length of Stay Analysis & Prediction App

A **multi-page Streamlit web application** for analyzing hospital data, visualizing insights, and predicting patient length of stay using Machine Learning.

---

## 🚀 Features

### 📊 1. Summary Dashboard

* Dataset preview
* Statistical summary
* Key Performance Indicators (KPIs):

  * Total Patients
  * Average Length of Stay
  * Maximum Stay
* Missing value analysis

---

### 📈 2. Interactive Visualizations

Built using **Plotly** for better interactivity:

* Length of Stay Distribution (Histogram)
* Age vs Length of Stay (Scatter Plot)
* Condition vs Length of Stay (Box Plot)
* Year-wise Analysis (Bar Chart)

---

### 🎯 3. Smart Filters (Sidebar)

Apply real-time filters:

* Year of Admission
* Gender
* Medical Condition
* Age Range

👉 All pages update dynamically based on filters

---

### 🤖 4. Machine Learning Prediction

* Model: Random Forest Regressor
* Metrics:

  * R² Score
  * Mean Absolute Error (MAE)
* Feature Importance Visualization
* Custom user input prediction

---

### 🛠 5. Robust Data Handling

* Handles **multiple date formats (DD-MM-YYYY, mixed)**
* Prevents crashes using safe parsing
* Removes invalid date entries
* Works with uploaded datasets

---

## 📂 Project Structure

```
📁 project-folder
│
├── app.py                  # Main Streamlit app
├── data/
│   └── hospital_data.csv   # Default dataset (optional)
├── README.md              # Project documentation
└── requirements.txt       # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/hospital-analysis-app.git
cd hospital-analysis-app
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv myenv
source myenv/bin/activate   # Mac/Linux
myenv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
streamlit run app.py
```

---

## 📦 Requirements

* Python 3.8+
* Streamlit
* Pandas
* Plotly
* Scikit-learn

---

## 📥 Dataset

* Default dataset is loaded from:

  ```
  ../data/hospital_data.csv
  ```
* You can also upload your own dataset from the sidebar

---

## ⚠️ Important Notes

* Date format is automatically handled (DD-MM-YYYY or mixed)
* Invalid date rows are removed safely
* Ensure dataset contains required columns like:

  * `Age`
  * `Gender`
  * `Condition`
  * `Length_of_Stay`

---

## 🌟 Future Improvements

* Download filtered reports (CSV/PDF)
* Correlation heatmap
* Authentication system
* Deployment on cloud (Streamlit Cloud / AWS)
* UI enhancements

---

## 👨‍💻 Author

**Sanskar Bhardwaj, Kanak Vaishnav , Rudraksh Vaishnav **
B.Tech IT | Data Science Enthusiast

---

## 📌 License

This project is open-source and available under the MIT License.

---

## ⭐ If you like this project

Give it a star on GitHub and share it 🚀
