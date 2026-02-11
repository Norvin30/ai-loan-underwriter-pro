'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function SubmitApplication() {
  const [formData, setFormData] = useState({
    applicant_id: '12345',
    name: 'John Doe',
    amount: 50000,
    income: 6000,
    expenses: 2000,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/submit`, formData)
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to submit application')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'name' || name === 'applicant_id' ? value : parseFloat(value) || 0
    }))
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Submit Loan Application</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="applicant_id" className="block text-sm font-medium text-gray-700 mb-2">
            Applicant ID
          </label>
          <input
            type="text"
            id="applicant_id"
            name="applicant_id"
            value={formData.applicant_id}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
            Full Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
            Loan Amount ($)
          </label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
            min="0"
            step="100"
          />
        </div>

        <div>
          <label htmlFor="income" className="block text-sm font-medium text-gray-700 mb-2">
            Monthly Income ($)
          </label>
          <input
            type="number"
            id="income"
            name="income"
            value={formData.income}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
            min="0"
            step="100"
          />
        </div>

        <div>
          <label htmlFor="expenses" className="block text-sm font-medium text-gray-700 mb-2">
            Monthly Expenses ($)
          </label>
          <input
            type="number"
            id="expenses"
            name="expenses"
            value={formData.expenses}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
            min="0"
            step="100"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-emerald-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Submitting...' : 'Submit Application'}
        </button>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-medium">Error</p>
          <p className="text-red-600 text-sm mt-1">{error}</p>
        </div>
      )}

      {result && (
        <div className="mt-6 p-6 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800 font-medium text-lg mb-3">✅ Application Submitted Successfully!</p>
          <div className="space-y-2 text-sm">
            <p><span className="font-medium">Workflow ID:</span> <code className="bg-white px-2 py-1 rounded">{result.workflow_id}</code></p>
            <p><span className="font-medium">Run ID:</span> <code className="bg-white px-2 py-1 rounded">{result.run_id}</code></p>
            <p><span className="font-medium">Status:</span> <span className="text-green-600 font-medium">{result.status}</span></p>
          </div>
          <p className="mt-4 text-sm text-gray-600">
            Your application is being processed by AI agents. Switch to the "Review Loan" tab to check the status.
          </p>
        </div>
      )}
    </div>
  )
}
