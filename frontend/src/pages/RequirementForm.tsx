import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { requirementsApi } from '../services/api'
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
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  const [formData, setFormData] = useState<FormData>({
    product_query: '',
    category: 'electronics',
    budget_min: 0,
    budget_max: 10000,
    deal_breakers: [],
    condition_preferences: [],
    timeline: 'flexible'
  })

  const categories = [
    { value: 'electronics', label: 'Electronics' },
    { value: 'home_decor', label: 'Home Decor' },
    { value: 'furniture', label: 'Furniture' },
    { value: 'apparel', label: 'Apparel' }
  ]

  const timelines = [
    { value: 'urgent', label: 'Urgent' },
    { value: 'flexible', label: 'Flexible' }
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await requirementsApi.createRequirement(formData)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create requirement')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: keyof FormData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
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
            {/* Product Query */}
            <div>
              <label htmlFor="product_query" className="block text-sm font-medium text-gray-700">
                What are you looking for?
              </label>
              <textarea
                id="product_query"
                value={formData.product_query}
                onChange={(e) => handleInputChange('product_query', e.target.value)}
                className="input-field mt-1"
                rows={3}
                placeholder="Describe the product you want to buy..."
                required
              />
            </div>

            {/* Category */}
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700">
                Category
              </label>
              <select
                id="category"
                value={formData.category}
                onChange={(e) => handleInputChange('category', e.target.value)}
                className="input-field mt-1"
                required
              >
                {categories.map(category => (
                  <option key={category.value} value={category.value}>
                    {category.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Budget Range */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="budget_min" className="block text-sm font-medium text-gray-700">
                  Minimum Budget (₹)
                </label>
                <input
                  type="number"
                  id="budget_min"
                  value={formData.budget_min}
                  onChange={(e) => handleInputChange('budget_min', Number(e.target.value))}
                  className="input-field mt-1"
                  min="0"
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
                  value={formData.budget_max}
                  onChange={(e) => handleInputChange('budget_max', Number(e.target.value))}
                  className="input-field mt-1"
                  min="0"
                  required
                />
              </div>
            </div>

            {/* Timeline */}
            <div>
              <label htmlFor="timeline" className="block text-sm font-medium text-gray-700">
                Timeline
              </label>
              <select
                id="timeline"
                value={formData.timeline}
                onChange={(e) => handleInputChange('timeline', e.target.value)}
                className="input-field mt-1"
                required
              >
                {timelines.map(timeline => (
                  <option key={timeline.value} value={timeline.value}>
                    {timeline.label}
                  </option>
                ))}
              </select>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

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
                disabled={loading}
                className="btn-primary"
              >
                {loading ? 'Creating...' : 'Create Requirement'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}

export default RequirementForm 