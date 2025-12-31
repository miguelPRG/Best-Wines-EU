# 🍷 Best Wines EU – Comprehensive EU Wine Quality Analysis

> **Full-Stack platform for analysis and exploration of European wine data with interactive UI, geographic visualizations, and correlation analysis with national happiness.**


## 📸 Screenshots

![Main Dashboard](./dashboard.png)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Implemented Analyses](#implemented-analyses)
- [Key Insights](#key-insights)
- [Author](#author)

---

## 🎯 Overview

**Best Wines EU** is a Full-Stack application I developed during my Master’s in Applied Informatics that combines **advanced data analysis** with a **responsive web interface** to explore the quality of wines produced in European Union countries.

The project processes **130k wine records**, correlates them with national happiness indicators, and presents the results through:
- 📊 Interactive visualizations with Plotly
- 🗺️ Choropleth maps and geographic markers with Folium
- 🔍 An explorable dashboard with dynamic filters
- 📈 Statistical analyses and correlations

**Target audience:** Wine enthusiasts, sommeliers, data researchers, and fans of European wines.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  STREAMLIT WEB APP (Frontend)           │
│  - Responsive, interactive dashboard                    │
│  - Dynamic filters (country, winery, price, etc.)       │
│  - Real-time visualizations                             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│              JUPYTER NOTEBOOK (Backend)                 │
│  - ETL and data cleaning                                │
│  - Feature engineering (points_per_euro)                │
│  - Rankings and correlations                            │
│  - Visualization generation                             │
│  - Pickle serialization (dados_notebook.pkl)            │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────┐
│                  DATASETS (Data Sources)                │
│  - winemag-data-130k-v2.csv (130k wines)                │
│  - happiness.csv (World Happiness Report)               │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend & Processing
- **Python 3.10+** – Main language
- **Pandas** – Data manipulation and analysis
- **NumPy** – Numerical computing
- **Jupyter Notebook** – Iterative development and documentation

### Frontend & Visualization
- **Streamlit** – Responsive, interactive web interface
- **Plotly** – Interactive charts (choropleth, scatter, box plots)
- **Folium** – Interactive and geographic maps
- **Matplotlib & Seaborn** – Static visualizations

### Dependencies & DevOps
- **uv** – Fast, modern Python package manager
- **pyproject.toml** – Dependency management (PEP 517/518)

---

## ✨ Features

### 1. **Main Dashboard**
- Summary metrics: best average quality, best value-for-money, global stats
- Interactive slides with navigation (previous/next)
- Quick navigation between charts

### 2. **Interactive Choropleth Map**
- Average score per EU country
- Reds gradient to represent quality
- Hover with names and scores

### 3. **Comparative Analyses**
- **Top 10 Value-for-Money** – Countries with the best cost efficiency
- **Top 5 Boxplot** – Quality distribution by country
- **Price vs Quality Scatter** – Relationship with smoothed trend

### 4. **Correlation: Happiness vs Wine Quality**
- Pearson correlation between National Happiness Index and average wine score
- Scatter plot with regression line
- Outlier and anomaly identification

### 5. **Advanced Wine Explorer**
- **Text search** – Title, winery, variety, region
- **Multiselect filters** – Countries, wineries, varieties
- **Sliders** – Price and score ranges
- **Sorting** – By quality, price, or value-for-money
- **Dynamic stats** – Calculated on filtered data
- **Pagination** – Control how many results to display

### 6. **Rankings & Tables**
- Full quality ranking by country
- Interactive dataframe view with adjustable height

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10 or newer
- pip and virtualenv (or uv)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/seu-usuario/best-wines-eu.git
cd best-wines-eu
```

### 2. Set Up the Environment

#### Option A: Using `uv` (recommended)
```bash
# Install uv
pip install uv

# Sync dependencies (creates venv automatically)
uv sync --frozen
```

#### Option B: Using pip and virtualenv
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Run the Notebook
```bash
jupyter notebook main.ipynb
```

**Important:** Run all cells sequentially up to cell 11 to generate `dados_notebook.pkl`.

### 4. Start the Streamlit App
```bash
streamlit run app.py
```

The app will open at `http://localhost:3000` (or the configured port).

---

## 🚀 How to Use

### Standard Workflow

```
1. [Jupyter] Run main.ipynb (cells 0–11)
   ↓
2. [Generated] dados_notebook.pkl + PNG + HTML artifacts
   ↓
3. [Streamlit] streamlit run app.py
   ↓
4. [UI] Interact with the dashboard and explorer
```

### Explore the Data

1. **Slide Navigation:**
   - Use “Previous” / “Next” buttons to browse visualizations
   - Use “Quick navigation” to jump directly

2. **Filter Wines:**
   - Enter search terms (e.g., “Douro”, “Chianti”)
   - Select countries, wineries, varieties
   - Adjust price and score sliders
   - Sort by your preferred criterion

3. **Analyze Correlations:**
   - View the Happiness vs Quality scatter plot
   - See whether happier countries tend to make better wines

---

## 📁 Project Structure

```
best-wines-eu/
├── README.md                          # This file
├── pyproject.toml                     # Dependency config (uv/pip)
├── main.ipynb                         # Notebook: ETL, analyses, visualizations
├── app.py                             # Streamlit app (frontend)
│
├── data/
│   ├── winemag-data-130k-v2.csv       # Main wine dataset (~30MB)
│   └── happiness.csv                  # World Happiness Report 2024
│
├── [Generated by the notebook]
│   ├── dados_notebook.pkl             # Serialized data for Streamlit
│   ├── fig_mapa.html                  # Plotly map (interactive)
│   ├── fig_qp.png                     # Top 10 value-for-money chart
│   ├── fig_box.png                    # Top 5 countries boxplot
│   ├── fig_price.png                  # Price vs Quality scatter
│   ├── fig_happiness.png              # Happiness vs Quality scatter
│   └── folium_map.html                # Folium map with markers
│
└── .gitignore                         # Git ignore rules
```

---

## 📊 Implemented Analyses

### 1. ETL & Data Cleaning
- Filtered 130k records to EU wines only (28 countries)
- Smart price imputation (country median)
- Removal of invalid prices (≤ 0)
- Created `points_per_euro` feature

### 2. Descriptive Analyses
- Average quality ranking by country
- Top 10 wines (by score)
- Top 10 countries by value-for-money
- Price and score distributions

### 3. Geospatial Visualizations
- Choropleth map (Plotly) with scores by country
- Proportional marker map (Folium) – radius scales with quality

### 4. Statistical Analyses
- Boxplot: quality distribution for top 5 countries
- Smoothed scatter: log-based price vs score trend

### 5. Multivariate Correlations
- Pearson correlation: National Happiness × Wine Quality
- Visualization with linear regression and per-country annotations

---

## 💡 Key Insights

### Main Findings

📍 **Best Average Quality:** Portugal, Hungary, France, and Italy lead on average score  
💰 **Best Value-for-Money:** Some countries offer superior price–quality ratios  
😊 **Happiness vs Wines:** Weak positive correlation – viticulture tradition matters more than happiness  
📈 **Price vs Quality:** Log relationship – the best quality isn’t always the most expensive  

---

## 🎓 Full-Stack Concepts Demonstrated

### Backend
✅ Large-scale ETL  
✅ Feature engineering and data cleaning  
✅ Statistical analysis and correlations  
✅ Pickle-based caching for performance  

### Frontend
✅ Responsive, intuitive interface  
✅ Dynamic filters and real-time reactivity  
✅ Multiple interactive visualizations  
✅ State and session management (st.session_state)  

### DevOps & Best Practices
✅ Dependency management with pyproject.toml  
✅ Reproducible environments (uv sync)  
✅ Documentation in Jupyter + README  
✅ Clear separation: Processing (Notebook) ↔ Presentation (Streamlit)  

---

## 🚀 Deployment

### Streamlit Cloud
```bash
# Push to GitHub
git add .
git commit -m "Add Best Wines EU"
git push origin main

# On https://share.streamlit.io
# 1. Connect the GitHub repo
# 2. Select main.ipynb and app.py
# 3. Deploy automatically
```

### Docker (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
EXPOSE 3000
CMD ["streamlit", "run", "app.py", "--server.port=3000"]
```

## 📞 Support & Contact

👤 **Author:** Miguel Gonçalves  
📧 **Email:** [miguel@psafe365.com]  
💼 **LinkedIn:** [miguelPRG](https://www.linkedin.com/in/miguel-prg/)

---

## 🙏 Thanks to Recruiters

If you got this far, thank you for your time! 🎯

This project was built to showcase skills in:
- ✅ **Data Cleaning & Analysis** (Pandas, NumPy)
- ✅ **Data Visualization** (Plotly, Folium, Matplotlib)
- ✅ **Backend Development** (Python, ETL, Feature Engineering)
- ✅ **Frontend Development** (Streamlit, UI/UX, Interactivity)
- ✅ **Full-Stack Thinking** (Architecture, Scalability, Best Practices)

**Open to discuss:**
- 🔄 Architectural improvements
- 📊 New analyses or datasets
- 🚀 Deployment and performance
- 💬 Feedback and suggestions

Any questions? Feel free to reach out! 🚀

---

## 📄 License

MIT License – See LICENSE for details.

---

## 🔄 Future Roadmap

- [ ] REST API with FastAPI
- [ ] Caching with Redis
- [ ] Unit tests and CI/CD
- [ ] Multilingual support
- [ ] PDF report export
- [ ] Database integration (PostgreSQL)
- [ ] Improved mobile responsiveness

---

**Built with ❤️ in Python • Data Analysis • Full-Stack Development**
