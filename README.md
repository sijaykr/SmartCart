# 🛒 SmartCart: Personalized Recommendation Engine  

> 🏆 **National Runner-Up – WWT Unravel Hackathon 2025**  
> Built by Team **JaiMataDi** (Bhaskar Ranjan Karn | Astitva | Sanjay Kumar)  

SmartCart is a **personalized recommendation engine** designed for *Wing R Us* to replace static upsell strategies with **data-driven, real-time personalized suggestions**.  
By analyzing **1.41M historical orders from 563k customers across 138 items**, SmartCart boosts revenue and improves customer satisfaction by delivering **relevant upsell recommendations** across app, web, and kiosk platforms.  

---

## 🚀 Key Features  
- 📦 **Real-time Recommendations** – Updates instantly as customers add/remove items from cart.  
- 🎯 **Personalized Upsells** – Top-3 suggestions tailored to order context (weekday vs weekend, cart contents).  
- ⚡ **High Performance** – Achieved **1.5× higher Recall@3 & Precision@3** compared to baseline.  
- 🌐 **Cross-Platform Support** – Works seamlessly across app, web, and kiosk ordering systems.  
- 📊 **Scalable & Cloud-Ready** – Designed to handle millions of orders efficiently.  

---

## 🧠 Technical Approach  
1. **Data Foundation**  
   - 1.41M orders, 563k customers, 138 unique items.  
   - Extracted order patterns, co-occurrence rules, and customer behavior insights.  

2. **SmartCart Logic**  
   - **Co-occurrence rules** → Detect frequently bought together items.  
   - **Category balancing** → Avoid over-recommending mains, boost underrepresented items (dips, drinks, sides).  
   - **Biasing logic** → Add missing high-value items (sides, drinks, combos).  
   - **Ranking engine** → Return Top-3 relevant upsells instantly.  

3. **Tech Stack**  
   - **Python** – Data processing & ML pipeline  
   - **Pandas, NumPy, Scikit-learn** – Data wrangling & modeling  
   - **Streamlit** – UI prototyping & testing  
   - **Cloud-ready Deployment** – Scalable architecture  

---

## 📊 Results & Impact  
- **Recall@3**: 1.5× higher than baseline  
- **Precision@3**: 1.5× higher than baseline  
- **Business Impact**:  
  - +8–10% uplift in Average Order Value (AOV)  
  - Improved customer satisfaction with relevant upsells  
  - Reduced wasted recommendation slots  

---

## 📈 Example  
**Old Static Recommendation (Generic):**  
- Extra Fries  

**SmartCart Personalized Recommendation:**  
- Ranch Dip (Regular)  
- 20 pc Spicy Feast Deal  
- Regular Buffalo Fries  

✅ More variety, ✅ Higher spend, ✅ Better user experience  

---

## 🏆 Achievements & Recognition  
- **National Runner-Up – WWT Unravel Hackathon 2025**  
- Recognized for **scalable, high-precision recommendation system design**  
- Delivered **1.5× improvement in recall & precision** compared to baseline  
- 📜 [View Certificate](https://drive.google.com/file/d/1Q7ghDW919b7TymWvRtXVV8GQhzgZ4eUE/view?usp=sharing)  
- 🔗 [LinkedIn Announcement Post](https://www.linkedin.com/feed/update/urn:li:activity:7370748579721826304/)  

---

## 📽️ Presentation & Demo  
- 📑 [Hackathon Presentation PDF](https://drive.google.com/file/d/1TBmqcXa23Bv10KX-tYk9j2sWqZagzYBA/view?usp=sharing) 
- 🎥 [Demo Video](https://drive.google.com/file/d/1TnMssAl3otlAfu3KyweY5CyUuQywzuer/view?usp=sharing)  

---

## ⚙️ Installation & Setup  

### 1. Clone the Repository  
```bash
git clone https://github.com/bhaskarkarn1/SmartCart.git
cd SmartCart
