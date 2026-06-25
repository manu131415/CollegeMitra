function ResultsTable({ results }) {
  if (!results || results.length === 0) return null;

  return (
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
            <td>{row.opening_rank ?? "—"}</td>
            <td>{row.closing_rank ?? "—"}</td>
            <td>{row.nirf_rank ?? "—"}</td>
            <td>{row.match_score?.toFixed ? row.match_score.toFixed(2) : row.match_score}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ResultsTable;