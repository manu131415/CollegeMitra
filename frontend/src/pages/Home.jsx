import { useState } from "react";
import PredictorForm from "../components/PredictorForm";
import ResultsTable from "../components/ResultsTable";
import { getPrediction } from "../api/predictor";

function Home() {
  const [results, setResults] = useState([]);
  const [lastFormData, setLastFormData] = useState(null);
  const [preference, setPreference] = useState("best");
  const [loading, setLoading] = useState(false);

  // Called by PredictorForm on initial submit
  const handleResults = (data, formData) => {
    setResults(data.results);
    setLastFormData(formData);
    setPreference(formData.preference);
  };

  // Toggle re-fetches with the new preference, reusing the rest of the form data
  const handleToggle = async (newPreference) => {
    if (!lastFormData || newPreference === preference) return;
    setLoading(true);
    setPreference(newPreference);
    try {
      const data = await getPrediction({ ...lastFormData, preference: newPreference });
      setResults(data.results);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>JEE College Predictor</h1>
      <PredictorForm onResults={handleResults} />

      {results.length > 0 && (
        <div style={{ margin: "16px 0" }}>
          <button
            onClick={() => handleToggle("best")}
            disabled={preference === "best" || loading}
          >
            Best Available
          </button>
          <button
            onClick={() => handleToggle("near_home")}
            disabled={preference === "near_home" || loading}
          >
            Near Home
          </button>
        </div>
      )}

      <ResultsTable results={results} />
    </div>
  );
}

export default Home;