# CollegeMitra - JEE College Predictor 🎓 

An ML-based college predictor that uses **historical JoSAA/CSAB counseling cut-off data (2019–2025)** to estimate which engineering colleges and branches a candidate can realistically get based on their JEE rank — and goes a step further by **ranking those options** using NIRF rating, median placement package, and fee structure, instead of just dumping a flat list of colleges.

---

## 🚀 Why this is different

Most rank predictors just match your rank against a cut-off table and spit out every college you're eligible for, sorted by rank or alphabetically. This project adds a **recommendation layer on top of eligibility**:

- ✅ Predicts admission probability for a given rank, category, and gender across all colleges/branches you qualify for
- ✅ Re-ranks eligible options using a weighted score combining **NIRF ranking, median package, and fee**
- ✅ Lets users prioritize what matters to them (e.g. "I care more about placements than fees")
- ✅ Built on **6 years of real counseling data (~500K rows)**, not a single year's cut-off sheet

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js |
| Backend | Node.js, Express.js |
| Database | PostgreSQL |
| ML / Data Processing | Python (pandas, scikit-learn) |

---

## 📊 Data

- **Source:** JoSAA and CSAB official counseling cut-off lists
- **Span:** 2019 – 2025 (6 admission cycles)
- **Volume:** ~500,000 rows after cleaning
- **Granularity:** Institute, branch, category, quota, gender, round-wise opening & closing rank
- **Status:** ✅ Collected, cleaned, and normalized into a consistent schema across all years (handled inconsistent column names, merged separate JoSAA/CSAB formats, removed duplicate/withdrawn round entries)

---

## 🧠 How it works (planned pipeline)

1. **Input:** Rank, category (Gen/EWS/OBC/SC/ST/PwD), gender, home state (for HS quota), preferrences
2. **Eligibility filtering:** Query historical cut-offs to shortlist all institute-branch combinations where the rank would have realistically gotten a seat, using closing-rank trends across years (not just the latest year)
3. **Probability scoring:** A model trained on multi-year rank movement estimates the *confidence* of admission for each option (not just a binary yes/no)
4. **Smart ranking:** Eligible results are re-scored using a weighted formula:

   ```
   score = w1 * (1 / NIRF_rank) + w2 * (median_package) - w3 * (fee)
   ```

   Weights are user-adjustable so a student can favor placements over fees, or vice versa.

5. **Output:** A ranked list of college-branch combinations with predicted admission confidence + supporting stats (NIRF rank, median package, total fee)

---

## 📌 Project Status

- [x] Data collection (JoSAA + CSAB, 2019–2025)
- [x] Data cleaning & normalization (~500K rows)
- [x] Basic prediction model built
- [ ] Model evaluation & tuning
- [ ] PostgreSQL schema design & data load
- [ ] Express.js API layer
- [ ] React frontend
- [ ] NIRF/package/fee ranking module integration
- [ ] End-to-end testing

---

## 🗂️ Repository Structure (planned)

```
jee-college-predictor/
├── data/
│   ├── raw/              # original JoSAA/CSAB csvs
│   └── processed/        # cleaned, merged dataset
├── ml/
│   ├── notebooks/         # EDA, model experiments
│   └── model.py           # training/inference scripts
├── server/
│   ├── routes/
│   ├── controllers/
│   └── db/                 # PostgreSQL schema, queries
├── client/
│   └── src/                # React app
└── README.md
```

---

## 📅 Getting Started

> Setup instructions will be added once the backend and frontend scaffolding is in place.

---

## 🤝 Contributing

This is currently a solo learning/portfolio project. Suggestions and feedback are welcome via issues.

---

## 📄 License

MIT
