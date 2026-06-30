export default function DashboardPage() {
  return (
    <div className="grid two-col">
      <section className="card">
        <h2>Platform Focus</h2>
        <p>An intelligent wearable healthcare platform that transforms wearable device data into standardized HL7 FHIR resources and generates AI-powered clinical summaries for faster healthcare insights.
</p>
        <ul>
          <li>Upload wearable data in multiple formats (CSV, JSON, XML, TCX, GPX)</li>
          <li>parse and extract health metrics without device-specific configuration</li>
          <li>Convert data into standardized HL7 FHIR resources (Patient, Device, Observation, Bundle).</li>
          <li>Generate AI-powered summaries highlighting key health insights and trends.</li>
          <li>Enable interoperable healthcare data exchange and support clinical decision-making..</li>
        </ul>
      </section>

      <section className="card">
        <h2>Smart Output</h2>
        <p>The platform transforms wearable data into standardized HL7 FHIR resources and generates AI-powered clinical summaries, providing actionable healthcare insights.</p>
        <p>The system prvides:</p>
        <ul>
          <li>HL7 FHIR Patient resource</li>
          <li>HL7 FHIR Device resource.</li>
          <li>Observation resources for heart rate, sleep, SpO₂, steps, calories, and physical activity</li>
          <li>AI-generated health summary highlighting key findings and trends.</li>
          <li>Downloadable FHIR bundles for seamless interoperability with healthcare systems</li>
        </ul>
      </section>
    </div>
  )
}
