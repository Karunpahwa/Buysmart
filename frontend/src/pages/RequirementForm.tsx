import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { requirementsApi } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import { ArrowLeft } from 'lucide-react'

interface FormData {
  product_query: string
  category: string
  budget_min: number
  budget_max: number
  location_lat?: number
  location_lng?: number
  location_radius_km?: number
  deal_breakers: string[]
  condition_preferences: string[]
  timeline: string
}

const RequirementForm: React.FC = () => {
  const navigate = useNavigate()
  const { token, user, loading } = useAuth()
  const [formLoading, setFormLoading] = useState(false)
  const [error, setError] = useState('')
  
  const [formData, setFormData] = useState<FormData>({
    product_query: '',
    category: 'electronics',
    budget_min: 0,
    budget_max: 0,
    location_lat: undefined,
    location_lng: undefined,
    location_radius_km: undefined,
    deal_breakers: [],
    condition_preferences: [],
    timeline: 'flexible'
  })

  // Debug authentication state
  useEffect(() => {
    console.log('Auth Debug:', { token, user, loading })
    console.log('LocalStorage token:', localStorage.getItem('token'))
  }, [token, user, loading])

  // Redirect if not authenticated
  useEffect(() => {
    if (!loading && !token) {
      console.log('No token found, redirecting to login')
      navigate('/login')
    }
  }, [token, loading, navigate])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setFormLoading(true)

    try {
      console.log('Submitting requirement with token:', token)
      console.log('Form data:', formData)
      
      const result = await requirementsApi.createRequirement(formData)
      console.log('Requirement created successfully:', result)
      navigate('/')
    } catch (error: any) {
      console.error('Error creating requirement:', error)
      setError(error.response?.data?.detail || 'Failed to create requirement')
    } finally {
      setFormLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value ? parseFloat(value) : 0
    }))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!token) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Please log in to create a requirement</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center py-6">
            <button
              onClick={() => navigate('/')}
              className="flex items-center text-sm text-gray-500 hover:text-gray-700 mr-4"
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back
            </button>
            <h1 className="text-2xl font-bold text-gray-900">New Requirement</h1>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="max-w-2xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="product_query" className="block text-sm font-medium text-gray-700">
                What are you looking for?
              </label>
              <input
                type="text"
                id="product_query"
                name="product_query"
                value={formData.product_query}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., iPhone 13, MacBook Pro, etc."
                required
              />
            </div>

            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700">
                Category
              </label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="electronics">Electronics</option>
                <option value="home_decor">Home & Decor</option>
                <option value="furniture">Furniture</option>
                <option value="apparel">Apparel</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="budget_min" className="block text-sm font-medium text-gray-700">
                  Minimum Budget (₹)
                </label>
                <input
                  type="number"
                  id="budget_min"
                  name="budget_min"
                  value={formData.budget_min}
                  onChange={handleNumberChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="0"
                  required
                />
              </div>
              <div>
                <label htmlFor="budget_max" className="block text-sm font-medium text-gray-700">
                  Maximum Budget (₹)
                </label>
                <input
                  type="number"
                  id="budget_max"
                  name="budget_max"
                  value={formData.budget_max}
                  onChange={handleNumberChange}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="10000"
                  required
                />
              </div>
            </div>

            <div>
              <label htmlFor="timeline" className="block text-sm font-medium text-gray-700">
                Timeline
              </label>
              <select
                id="timeline"
                name="timeline"
                value={formData.timeline}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="flexible">Flexible</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={formLoading}
                className="btn-primary"
              >
                {formLoading ? 'Creating...' : 'Create Requirement'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}

export default RequirementForm; 