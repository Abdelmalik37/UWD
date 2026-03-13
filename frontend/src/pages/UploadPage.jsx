import { useState } from 'react'

import JsonViewer from '../components/JsonViewer'
import { uploadFile } from '../services/api'

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const submitFile = async (event) => {
    event.preventDefault()
    if (!file) {
      setError('Choose a wearable data file first.')
      return
    }

    setLoading(true)
    setError('')
    try {
      const res = await uploadFile(file)
      setResult(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Upload failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid two-col">
      <section className="card">
        <h2>Upload Data</h2>
        <form onSubmit={submitFile} className="form-block">
          <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <button type="submit" disabled={loading}>Upload and Parse</button>
        </form>
        {error && <p className="error">{error}</p>}
      </section>

      <section className="card">
        <h3>Upload Result</h3>
        {result ? (
          <JsonViewer title="Upload Response" value={result} />
        ) : (
          <p>Upload a file to receive parse status and upload ID.</p>
        )}
      </section>
    </div>
  )
}
