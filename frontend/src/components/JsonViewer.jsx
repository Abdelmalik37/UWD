export default function JsonViewer({ title, value }) {
  return (
    <section className="card">
      <h3>{title}</h3>
      <pre>{JSON.stringify(value, null, 2)}</pre>
    </section>
  )
}
