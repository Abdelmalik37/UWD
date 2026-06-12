import { useEffect, useState } from 'react'

import AISummary from '../components/AISummary'
import JsonViewer from '../components/JsonViewer'
import { generateAISummary } from '../services/aiService'
import { convertUpload, fetchFhir, fetchHistory, fetchUpload } from '../services/api'

export default function HistoryPage() {
  const [history, setHistory] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [detail, setDetail] = useState(null)
  const [fhir, setFhir] = useState(null)
  const [aiSummary, setAiSummary] = useState('')
  const [aiSummaryLoading, setAiSummaryLoading] = useState(false)
  const [aiSummaryError, setAiSummaryError] = useState('')
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
    setAiSummary('')
    setAiSummaryError('')
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

  const downloadFhir = async () => {
    if (!selectedId) {
      setError('Select an upload first.')
      return
    }

    try {
      let bundle = fhir
      if (!bundle) {
        const res = await fetchFhir(selectedId)
        bundle = res.data.fhir_bundle
        setFhir(bundle)
      }

      if (!bundle) {
        setError('No FHIR bundle available to download. Click Convert to FHIR first.')
        return
      }

      const jsonText = JSON.stringify(bundle, null, 2)
      const blob = new Blob([jsonText], { type: 'application/fhir+json' })
      const url = URL.createObjectURL(blob)

      const a = document.createElement('a')
      a.href = url
      a.download = `fhir_bundle_${selectedId}.json`
      document.body.appendChild(a)
      a.click()
      a.remove()

      URL.revokeObjectURL(url)
    } catch (e) {
      setError(e.response?.data?.detail || 'FHIR download failed.')
    }
  }

  const generateSummary = async () => {
    if (!selectedId) {
      setAiSummaryError('Select an upload first.')
      return
    }

    setAiSummaryLoading(true)
    setAiSummaryError('')

    try {
      let bundle = fhir
      if (!bundle) {
        const res = await fetchFhir(selectedId)
        bundle = res.data.fhir_bundle
        setFhir(bundle)
      }

      if (!bundle) {
        setAiSummaryError('No FHIR Bundle available. Click Convert to FHIR first.')
        return
      }

      const res = await generateAISummary(bundle)
      setAiSummary(res.data.summary)
    } catch (e) {
      setAiSummaryError(e.response?.data?.detail || 'Unable to generate AI clinical summary.')
    } finally {
      setAiSummaryLoading(false)
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
          <button type="button" onClick={downloadFhir} disabled={!selectedId}>Download FHIR Bundle</button>
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
          <>
            <JsonViewer title="FHIR Bundle" value={fhir} />
            <AISummary
              summary={aiSummary}
              loading={aiSummaryLoading}
              error={aiSummaryError}
              onGenerate={generateSummary}
              disabled={!selectedId || !fhir}
            />
          </>
        ) : (
          <p>Run conversion or load FHIR to view output.</p>
        )}
      </section>
    </div>
  )
}
