import { useEffect, useState } from 'react'

import JsonViewer from '../components/JsonViewer'
import { convertUpload, fetchFhir, fetchHistory, fetchUpload } from '../services/api'

export default function HistoryPage() {
  const [history, setHistory] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [detail, setDetail] = useState(null)
  const [fhir, setFhir] = useState(null)
  const [error, setError] = useState('')

  const loadHistory = async () => {
    try {
      const res = await fetchHistory()
      setHistory(res.data || [])
    } catch {
      setError('Unable to load upload history. Start backend first.')
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  const selectUpload = async (id) => {
    setSelectedId(id)
    setFhir(null)
    try {
      const res = await fetchUpload(id)
      setDetail(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to load upload detail.')
    }
  }

  const convertSelected = async () => {
    if (!selectedId) {
      setError('Select an upload first.')
      return
    }
    try {
      const res = await convertUpload(selectedId)
      setFhir(res.data.fhir_bundle)
    } catch (e) {
      setError(e.response?.data?.detail || 'Conversion failed.')
    }
  }

  const loadFhir = async () => {
    if (!selectedId) {
      setError('Select an upload first.')
      return
    }
    try {
      const res = await fetchFhir(selectedId)
      setFhir(res.data.fhir_bundle)
    } catch (e) {
      setError(e.response?.data?.detail || 'FHIR fetch failed.')
    }
  }

  return (
    <div className="grid two-col">
      <section className="card">
        <h2>Upload History</h2>
        {error && <p className="error">{error}</p>}
        <div className="list">
          {history.map((item) => (
            <button
              key={item.id}
              type="button"
              className={selectedId === item.id ? 'list-item active' : 'list-item'}
              onClick={() => selectUpload(item.id)}
            >
              #{item.id} {item.filename} ({item.parse_status})
            </button>
          ))}
        </div>
        <div className="button-row">
          <button type="button" onClick={loadHistory}>Refresh</button>
          <button type="button" onClick={convertSelected}>Convert to FHIR</button>
          <button type="button" onClick={loadFhir}>Load FHIR</button>
        </div>
      </section>

      <section className="card">
        <h2>Raw Parsed Data</h2>
        {detail ? (
          <JsonViewer title={`Upload ${detail.id}`} value={detail} />
        ) : (
          <p>Select an upload to view raw data.</p>
        )}
      </section>

      <section className="card">
        <h2>FHIR Output</h2>
        {fhir ? (
          <JsonViewer title="FHIR Bundle" value={fhir} />
        ) : (
          <p>Run conversion or load FHIR to view output.</p>
        )}
      </section>
    </div>
  )
}
