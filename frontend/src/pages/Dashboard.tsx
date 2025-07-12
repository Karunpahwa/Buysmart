import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { requirementsApi } from '../services/api'
import { Plus, LogOut, Search, MessageSquare, TrendingUp, Eye } from 'lucide-react'

interface Requirement {
  id: string
  product_query: string
  category: string
  budget_min: number
  budget_max: number
  status: string
  created_at: string
}

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth()
  const [requirements, setRequirements] = useState<Requirement[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchRequirements = async () => {
      try {
        const response = await requirementsApi.getRequirements()
        setRequirements(response.requirements)
      } catch (error) {
        console.error('Failed to fetch requirements:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchRequirements()
  }, [])

  const handleLogout = () => {
    logout()
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      case 'fulfilled':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">BuySmart Assistant</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Welcome, {user?.email}</span>
              <button
                onClick={handleLogout}
                className="flex items-center text-sm text-gray-500 hover:text-gray-700"
              >
                <LogOut className="h-4 w-4 mr-1" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Search className="h-8 w-8 text-primary-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Active Searches
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {requirements.filter(r => r.status === 'active').length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <MessageSquare className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    In Negotiation
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">0</dd>
                </dl>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Completed Deals
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {requirements.filter(r => r.status === 'fulfilled').length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        {/* Requirements Section */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-medium text-gray-900">Your Requirements</h2>
              <Link
                to="/requirement/new"
                className="btn-primary flex items-center"
              >
                <Plus className="h-4 w-4 mr-2" />
                New Requirement
              </Link>
            </div>

            {loading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>
            ) : requirements.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">No requirements yet. Create your first one!</p>
              </div>
            ) : (
              <div className="space-y-4">
                {requirements.map((requirement) => (
                  <div key={requirement.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="text-lg font-medium text-gray-900">
                          {requirement.product_query}
                        </h3>
                        <p className="text-sm text-gray-500 mt-1">
                          {requirement.category} • ₹{requirement.budget_min} - ₹{requirement.budget_max}
                        </p>
                        <p className="text-xs text-gray-400 mt-1">
                          Created {new Date(requirement.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(requirement.status)}`}>
                          {requirement.status}
                        </span>
                        <Link
                          to={`/requirement/${requirement.id}`}
                          className="flex items-center text-primary-600 hover:text-primary-700 text-sm"
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          View Details
                        </Link>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard 