const SECTION_TITLES = [
  'Patient Overview',
  'Vital Sign Summary',
  'Activity Summary',
  'Sleep Summary',
  'Clinical Alerts',
  'Trend Analysis',
  'Overall Summary',
]

function extractSection(summary, title) {
  const titles = SECTION_TITLES.map((item) => item.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
  const pattern = new RegExp(`${title}\\s*\\n+([\\s\\S]*?)(?=\\n+(${titles.join('|')})\\s*\\n|$)`, 'i')
  const match = summary.match(pattern)
  return match?.[1]?.trim() || 'No specific information available in the generated summary.'
}

export default function AISummary({ summary, loading, error, onGenerate, disabled }) {
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
        <div className="summary-grid">
          {SECTION_TITLES.map((title) => (
            <article key={title} className="summary-section">
              <h3>{title}</h3>
              <p>{extractSection(summary, title)}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}
