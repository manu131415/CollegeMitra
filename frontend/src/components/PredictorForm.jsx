import { useState } from "react";
import { getPrediction } from "../api/predictor";

const CATEGORY_OPTIONS = [
  { value: "OPEN", label: "Open (General)" },
  { value: "EWS", label: "EWS" },
  { value: "OBC-NCL", label: "OBC-NCL" },
  { value: "SC", label: "SC" },
  { value: "ST", label: "ST" },
  { value: "OPEN (PwD)", label: "Open (PwD)" },
  { value: "EWS (PwD)", label: "EWS (PwD)" },
  { value: "OBC-NCL (PwD)", label: "OBC-NCL (PwD)" },
  { value: "SC (PwD)", label: "SC (PwD)" },
  { value: "ST (PwD)", label: "ST (PwD)" },
];

const EXAM_OPTIONS = [
  { value: "jee_main", label: "JEE Main" },
  { value: "jee_adv", label: "JEE Advanced" },
];

const PREFERENCE_OPTIONS = [
  { value: "best", label: "Best" },
  { value: "near_home", label: "Near Home" },
];

/**
 * A sliding-pill segmented control. The highlighted "thumb" animates
 * between options instead of jumping, so a toggle always reads as motion
 * rather than a state swap.
 */
function SegmentedToggle({ options, value, onChange, name }) {
  const activeIndex = Math.max(
    0,
    options.findIndex((o) => o.value === value)
  );

  return (
    <div
      className="segmented"
      style={{ gridTemplateColumns: `repeat(${options.length}, 1fr)` }}
      role="radiogroup"
      aria-label={name}
    >
      <div
        className="thumb"
        style={{
          width: `calc((100% - 8px) / ${options.length})`,
          transform: `translateX(calc(${activeIndex} * (100% + ${
            2 / options.length
          }px)))`,
        }}
        aria-hidden="true"
      />
      {options.map((opt) => (
        <button
          key={opt.value}
          type="button"
          role="radio"
          aria-checked={value === opt.value}
          className={value === opt.value ? "active" : ""}
          onClick={() => onChange(opt.value)}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}

function PredictorForm({ onResults }) {
  const [formData, setFormData] = useState({
    rank: "",
    category: "",
    home_state: "",
    exam: "jee_main",
    preference: "best",
    branch_preference: [],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const setField = (name) => (value) =>
    setFormData((prev) => ({ ...prev, [name]: value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const payload = {
        ...formData,
        rank: parseInt(formData.rank, 10), // backend expects int, not string
      };
      const data = await getPrediction(payload);
      console.log("API response:", data);
      onResults(data, payload);
    } catch (err) {
      console.error(err.response?.data); // full detail in console for debugging
      setError(err.response?.data?.detail || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="predictor-card">
      <form onSubmit={handleSubmit}>
        <div className="form-stub">
          <p className="stub-label">Rank Entry</p>
          <div className="rank-field">
            <input
              name="rank"
              type="number"
              placeholder="000000"
              value={formData.rank}
              onChange={handleChange}
              required
            />
            <div className="underline" />
          </div>
        </div>

        <div className="form-body">
          <div>
            <p className="stub-label">Category</p>
            <div className="select-wrap">
              <select name="category" value={formData.category} onChange={handleChange} required>
                <option value="">Select category</option>
                {CATEGORY_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
              <span className="chevron" />
            </div>
          </div>

          <div className={`field ${formData.home_state ? "filled" : ""}`}>
            <input
              id="home_state"
              name="home_state"
              type="text"
              value={formData.home_state}
              onChange={handleChange}
              required
            />
            <label htmlFor="home_state">Home State</label>
          </div>

          <div>
            <p className="stub-label">Exam</p>
            <SegmentedToggle
              name="exam"
              options={EXAM_OPTIONS}
              value={formData.exam}
              onChange={setField("exam")}
            />
          </div>

          <div>
            <p className="stub-label">Preference</p>
            <SegmentedToggle
              name="preference"
              options={PREFERENCE_OPTIONS}
              value={formData.preference}
              onChange={setField("preference")}
            />
          </div>

          {/* <select
            name="branch_preference"
            multiple
            value={formData.branch_preference}
            onChange={handleBranchChange}
          >
            <option value="CSE">CSE</option>
            <option value="CSE">AI</option>
            <option value="ECE">ECE</option>
            <option value="ME">Mechanical</option>
            <option value="CE">Civil</option>
          </select> */}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading && <span className="spinner" />}
            {loading ? "Predicting…" : "Predict Colleges"}
          </button>

          {error && <p className="error-msg">{error}</p>}
        </div>
      </form>
    </div>
  );
}

export default PredictorForm;
