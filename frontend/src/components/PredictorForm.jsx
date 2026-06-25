import { useState } from "react";
import { getPrediction } from "../api/predictor";

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

  const handleBranchChange = (e) => {
    const options = Array.from(e.target.selectedOptions).map((o) => o.value);
    setFormData((prev) => ({ ...prev, branch_preference: options }));
  };

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
    <form onSubmit={handleSubmit}>
      <input
        name="rank"
        type="number"
        placeholder="JEE Rank"
        value={formData.rank}
        onChange={handleChange}
        required
      />

      <select name="category" value={formData.category} onChange={handleChange} required>
  <option value="">Select Category</option>
  <option value="OPEN">Open (General)</option>
  <option value="EWS">EWS</option>
  <option value="OBC-NCL">OBC-NCL</option>
  <option value="SC">SC</option>
  <option value="ST">ST</option>
  <option value="OPEN (PwD)">Open (PwD)</option>
  <option value="EWS (PwD)">EWS (PwD)</option>
  <option value="OBC-NCL (PwD)">OBC-NCL (PwD)</option>
  <option value="SC (PwD)">SC (PwD)</option>
  <option value="ST (PwD)">ST (PwD)</option>
</select>

      <input
        name="home_state"
        placeholder="Home State"
        value={formData.home_state}
        onChange={handleChange}
        required
      />

      <select name="exam" value={formData.exam} onChange={handleChange} required>
  <option value="jee_main">JEE Main</option>
  <option value="jee_adv">JEE Advanced</option>
</select>

<select name="preference" value={formData.preference} onChange={handleChange} required>
  <option value="best">Best</option>
  <option value="near_home">Near Home</option>
</select>

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

      <button type="submit" disabled={loading}>
        {loading ? "Predicting..." : "Predict Colleges"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}

export default PredictorForm;