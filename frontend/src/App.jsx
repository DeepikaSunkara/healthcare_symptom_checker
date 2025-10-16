import { useState } from 'react'
import { checkSymptoms } from './api'
import './App.css'

function App() {
  const [symptoms, setSymptoms] = useState('')
  const [age, setAge] = useState('')
  const [sex, setSex] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const data = await checkSymptoms(symptoms, { age, sex })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Healthcare Symptom Checker</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          placeholder="Enter symptoms (e.g., fever, cough, headache)"
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          required
        />
        <div className="row">
          <input
            placeholder="Age (optional)"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
          <input
            placeholder="Sex (optional)"
            value={sex}
            onChange={(e) => setSex(e.target.value)}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Checking...' : 'Check Symptoms'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="results">
          <h2>Probable Conditions</h2>
          <ul>
            {result.probable_conditions?.map((c, idx) => (
              <li key={idx}>
                <strong>{c.condition}</strong> ({c.likelihood}) <br />
                <em>{c.reasons}</em>
              </li>
            ))}
          </ul>

          <h2>Recommended Next Steps</h2>
          <ol>
            {result.recommended_next_steps?.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ol>

          <h2>Red Flags</h2>
          <ul>
            {result.red_flags?.map((f, idx) => (
              <li key={idx}>{f}</li>
            ))}
          </ul>

          <p className="disclaimer">{result.disclaimer}</p>
        </div>
      )}
    </div>
  )
}

export default App
