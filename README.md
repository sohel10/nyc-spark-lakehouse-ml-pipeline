# 🚕 NYC Taxi Fare Analysis Dashboard

Machine Learning project comparing 16-year transportation market evolution using XGBoost models and interactive visualizations.

---

## 📊 Live Demo

Open your browser and visit:

- 🏠 **Home**: http://localhost:8000
- 📈 **2009 Analysis**: http://localhost:8000/2009
- 📊 **2025 Analysis**: http://localhost:8000/2025
- ⚖️ **Side-by-Side Comparison**: http://localhost:8000/comparison

---

## 🎯 Project Highlights

| Metric | Value |
|--------|-------|
| **Dataset Size** | 46M+ trip records |
| **Time Period** | 2009 vs 2025 (16 years) |
| **Models** | XGBoost regressors |
| **2009 Accuracy** | RMSE $3.18 |
| **2025 Accuracy** | RMSE $8.67 |
| **API Latency** | <100ms |
| **Market Change** | +75-90% fare increase |

---

## 🚀 Quick Start

```bash
# Navigate to project
cd ~/nyc-spark-pipeline

# Start the app
python3 api_main.py
```

Then open: **http://localhost:8000**

---

## 🛑 Stop the App

Press `Ctrl+C` in terminal

---

## 📈 Key Features

✅ **Real-time Fare Prediction** - Input trip details, get instant predictions  
✅ **Interactive Charts** - Chart.js visualizations with trend analysis  
✅ **Market Comparison** - Side-by-side 2009 vs 2025 analysis  
✅ **Professional Design** - Modern, responsive UI  
✅ **Production-Ready API** - FastAPI backend with proper error handling  

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.10+
- FastAPI
- XGBoost (ML models)
- Joblib (model serialization)

**Frontend:**
- HTML5
- CSS3
- Chart.js (data visualization)
- Vanilla JavaScript

**Data:**
- 10.2M trips (2009 sample)
- 36M trips (2025 full dataset)
- XGBoost feature engineering

---

## 📂 Project Structure
``` 
nyc-spark-pipeline/

├── api_main.py              # FastAPI application

├── templates/

│   ├── index.html           # Home dashboard

│   ├── 2009.html            # 2009 analysis (blue)

│   ├── 2025.html            # 2025 analysis (green)

│   └── comparison.html       # Side-by-side comparison (purple)

├── ml/

│   ├── model_2009.pkl       # XGBoost 2009 model

│   └── model_2025.pkl       # XGBoost 2025 model

├── data_processed/          # Processed 2009 data

├── data_2025/               # Processed 2025 data

└── README.md                # This file
```
---

## 💡 What This Dashboard Shows

### 2009 Market (Pre-Uber Era)
- **Status**: Stable pricing (RMSE $3.18)
- **Market**: Taxi monopoly
- **Characteristics**: Predictable fares, low volatility
- **Average Trip**: $12-18

### 2025 Market (Modern Era)
- **Status**: Dynamic pricing (RMSE $8.67)
- **Market**: Multi-platform competition
- **Characteristics**: Volatile fares, surge pricing
- **Average Trip**: $25-35

### Market Insight
**Average fare increase: 75-90% over 16 years**
- Caused by: Competition, inflation, dynamic pricing algorithms

---

## 🔧 Example Prediction

**Input:**
- Distance: 5 miles
- Passengers: 1
- Time: 12:00 PM, Wednesday, June

**2009 Output:** $15.28  
**2025 Output:** $27.81  
**Increase:** +82%

---

## 📚 API Endpoints
```
[200~GET  /              → Home dashboard

GET  /2009          → 2009 analysis page

GET  /2025          → 2025 analysis page

GET  /comparison    → Comparison page
POST /api/predict/2009   → Predict 2009 fare

POST /api/predict/2025   → Predict 2025 fare

POST /api/compare        → Compare both periods~
```
**Example Request:**
```bash
curl -X POST http://localhost:8000/api/predict/2025 \
  -H "Content-Type: application/json" \
  -d '{
    "passenger_count": 1,
    "trip_distance": 5.0,
    "hour": 12,
    "day_of_week": 3,
    "month": 6
  }'
```

**Response:**
```json
{
  "fare": 27.81
}
```

---

## 👤 Author

**Sohel Ahmed**  
Machine Learning Engineer | Data Scientist

- 📍 **Location:** Michigan, USA
- 🔗 **LinkedIn:** [linkedin.com/in/sohelcu06](https://linkedin.com/in/sohelcu06)
- 🐙 **GitHub:** [github.com/sohel10](https://github.com/sohel10)
- 📧 **Email:** sohelcu06@gmail.com

---

## 📊 Data Sources

- **2009 Data:** NYC Yellow Taxi TLC (10.2M trips sample)
- **2025 Data:** NYC Yellow Taxi TLC (36M trips full)
- **Total Records:** 46M+ processed

---

## 🎓 Learning Resources

This project demonstrates:

✅ **Data Engineering** - ETL pipelines, feature engineering  
✅ **Machine Learning** - XGBoost regression, model training  
✅ **API Design** - FastAPI, REST principles  
✅ **Frontend** - Responsive web design, interactive visualizations  
✅ **Production ML** - Model deployment, monitoring  

---

## 📝 License

This project is open source for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- NYC Yellow Taxi TLC for public dataset
- XGBoost for ML model
- Chart.js for visualizations
- FastAPI for web framework

---

**Built with ❤️ using Python, FastAPI, XGBoost, and Chart.js**
