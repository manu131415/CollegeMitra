import { useState } from "react";
import PredictorForm from "../Components/PredictorForm";
import ResultsTable from "../Components/ResultsTable";

function Home() {
  const [results, setResults] = useState(null);

  const handleResults = (data) => {
    setResults(data?.results ?? data ?? []);
  };

  return (
    <>
      <div className="page-header">
        <span className="eyebrow">College Predictor</span>
        <h1>Find where your rank gets you in.</h1>
        <p>Enter your JEE rank, category, and state to see a shortlist of institutes ranked by fit.</p>
      </div>

      <PredictorForm onResults={handleResults} />

      {results && results.length > 0 ? (
        <ResultsTable results={results} />
      ) : results && results.length === 0 ? (
        <p className="empty-state">No matches for this rank and category yet. Try adjusting your preference.</p>
      ) : null}
    </>
  );
}

export default Home;
