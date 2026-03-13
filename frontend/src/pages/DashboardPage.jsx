export default function DashboardPage() {
  return (
    <div className="grid two-col">
      <section className="card">
        <h2>Platform Focus</h2>
        <p>Wearable data ingestion platform that converts uploads into HL7 FHIR resources.</p>
        <ul>
          <li>Upload any wearable file (JSON, CSV, XML, TCX, GPX).</li>
          <li>Parse and extract metrics without device-type detection.</li>
          <li>Generate FHIR Patient, Device, Observation, Bundle.</li>
        </ul>
      </section>

      <section className="card">
        <h2>FHIR Output</h2>
        <p>The system outputs valid FHIR JSON bundles containing:</p>
        <ul>
          <li>Patient resource</li>
          <li>Device resource</li>
          <li>Observation resources for heart rate, steps, sleep, SpO2, calories, activity</li>
        </ul>
      </section>
    </div>
  )
}
