function cleanSummary(summary) {
  return summary
    .replace(/\r\n/g, '\n')
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/^#{1,6}\s*/gm, '')
    .replace(/^[\s\-•]+/gm, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}

export default function AISummary({ summary, loading, error, onGenerate, disabled }) {
  const shortSummary = cleanSummary(summary || '')
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, 3)
    .join(' ')

  return (
    <section className="card ai-summary-card">
      <div className="summary-header">
        <h2>AI Clinical Summary</h2>
        <button type="button" onClick={onGenerate} disabled={disabled || loading}>
          {loading ? 'Generating...' : 'Generate AI Summary'}
        </button>
      </div>

      {loading && (
        <div className="summary-loading">
          <span className="spinner" />
          <span>Generating clinical summary...</span>
        </div>
      )}

      {error && <p className="error">{error}</p>}

      {!summary && !loading && !error && (
        <p>Generate a physician-oriented summary after loading or converting a FHIR Bundle.</p>
      )}

      {summary && (
        <article className="summary-section summary-section--single">
          <p>{shortSummary || 'No specific information available in the generated summary.'}</p>
        </article>
      )}
    </section>
  )
}
