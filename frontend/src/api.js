export async function checkSymptoms(symptoms, patientInfo = {}) {
  const payload = {
    symptoms,
    patient_info: patientInfo
  }

  const res = await fetch('/api/symptom-check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`)
  }

  return res.json()
}
