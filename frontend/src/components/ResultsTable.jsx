function ResultsTable({ results }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="results-wrap">
      <p className="stub-label">{results.length} Matches</p>
      <div className="results-table-scroll">
        <table>
          <thead>
            <tr>
              <th>Institute</th>
              <th>Branch</th>
              <th>State</th>
              <th>Opening Rank</th>
              <th>Closing Rank</th>
              <th>NIRF Rank</th>
              <th>Match Score</th>
            </tr>
          </thead>
          <tbody>
            {results.map((row, idx) => (
              <tr key={idx}>
                <td>{row.institute_name}</td>
                <td>{row.branch}</td>
                <td>{row.state}</td>
                <td className="rank-cell">{row.opening_rank ?? "—"}</td>
                <td className="rank-cell">{row.closing_rank ?? "—"}</td>
                <td className="rank-cell">{row.nirf_rank ?? "—"}</td>
                <td>
                  <span className="match-score">
                    {row.match_score?.toFixed ? row.match_score.toFixed(2) : row.match_score}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ResultsTable;
