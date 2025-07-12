import React, { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { requirementsApi, listingsApi, messagesApi } from '../services/api'
import { ArrowLeft, MessageSquare, ExternalLink, Phone, Mail, Edit, Trash2, RefreshCw, Clock, CheckCircle, AlertCircle, Play, Pause } from 'lucide-react'

interface Requirement {
  id: string
  product_query: string
  category: string
  budget_min: number
  budget_max: number
  timeline: string
  status: string
  total_listings_found: number
  matching_listings_count: number
  last_scraped_at: string | null
  next_scrape_at: string | null
  scraping_status: string
  created_at: string
  updated_at: string
}

interface Listing {
  id: string
  olx_id: string
  title: string
  price: number
  location: string
  posted_date: string
  status: string
  created_at: string
}

interface Message {
  id: string
  listing_id: string
  role: string
  content: string
  created_at: string
}

const RequirementDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [requirement, setRequirement] = useState<Requirement | null>(null)
  const [listings, setListings] = useState<Listing[]>([])
  const [selectedListing, setSelectedListing] = useState<Listing | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [messageLoading, setMessageLoading] = useState(false)
  const [actionLoading, setActionLoading] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return
      
      try {
        const [reqData, listingsData] = await Promise.all([
          requirementsApi.getRequirement(id),
          listingsApi.getListings(id)
        ])
        
        setRequirement(reqData)
        setListings(listingsData.listings || [])
      } catch (error) {
        console.error('Failed to fetch data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [id])

  useEffect(() => {
    if (selectedListing) {
      fetchMessages(selectedListing.id)
    }
  }, [selectedListing])

  const fetchMessages = async (listingId: string) => {
    try {
      const response = await messagesApi.getMessages(listingId)
      setMessages(response.messages || [])
    } catch (error) {
      console.error('Failed to fetch messages:', error)
    }
  }

  const handleSendMessage = async () => {
    if (!selectedListing || !newMessage.trim()) return

    setMessageLoading(true)
    try {
      await messagesApi.sendMessage(selectedListing.id, {
        content: newMessage,
        role: 'user'
      })
      setNewMessage('')
      await fetchMessages(selectedListing.id)
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setMessageLoading(false)
    }
  }

  const handleTriggerScraping = async () => {
    if (!requirement) return
    
    setActionLoading(true)
    try {
      await requirementsApi.triggerScraping(requirement.id)
      // Refresh requirement data
      const updatedRequirement = await requirementsApi.getRequirement(requirement.id)
      setRequirement(updatedRequirement)
    } catch (error) {
      console.error('Failed to trigger scraping:', error)
    } finally {
      setActionLoading(false)
    }
  }

  const handleDeleteRequirement = async () => {
    if (!requirement || !confirm('Are you sure you want to delete this requirement?')) return
    
    setActionLoading(true)
    try {
      await requirementsApi.deleteRequirement(requirement.id)
      navigate('/')
    } catch (error) {
      console.error('Failed to delete requirement:', error)
    } finally {
      setActionLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      case 'fulfilled':
        return 'bg-blue-100 text-blue-800'
      case 'new':
        return 'bg-gray-100 text-gray-800'
      case 'contacted':
        return 'bg-orange-100 text-orange-800'
      case 'responded':
        return 'bg-purple-100 text-purple-800'
      case 'eliminated':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getScrapingStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="h-4 w-4 text-yellow-500" />
      case 'in_progress':
        return <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getScrapingStatusText = (status: string) => {
    switch (status) {
      case 'pending':
        return 'Pending'
      case 'in_progress':
        return 'Scraping...'
      case 'completed':
        return 'Completed'
      case 'failed':
        return 'Failed'
      default:
        return 'Unknown'
    }
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never'
    return new Date(dateString).toLocaleString()
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!requirement) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Requirement not found</h2>
          <Link to="/" className="btn-primary">Back to Dashboard</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <Link to="/" className="flex items-center text-gray-500 hover:text-gray-700">
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back
              </Link>
              <h1 className="text-2xl font-bold text-gray-900">Requirement Details</h1>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={handleTriggerScraping}
                disabled={actionLoading}
                className="btn-secondary flex items-center"
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${actionLoading ? 'animate-spin' : ''}`} />
                {actionLoading ? 'Triggering...' : 'Trigger Scraping'}
              </button>
              <Link
                to={`/requirement/${requirement.id}/edit`}
                className="btn-secondary flex items-center"
              >
                <Edit className="h-4 w-4 mr-2" />
                Edit
              </Link>
              <button
                onClick={handleDeleteRequirement}
                disabled={actionLoading}
                className="btn-danger flex items-center"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Requirement Details */}
          <div className="lg:col-span-1">
            <div className="card">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Requirement Info</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Product Query</label>
                  <p className="mt-1 text-sm text-gray-900">{requirement.product_query}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Category</label>
                  <p className="mt-1 text-sm text-gray-900 capitalize">{requirement.category}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Budget Range</label>
                  <p className="mt-1 text-sm text-gray-900">₹{requirement.budget_min} - ₹{requirement.budget_max}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Timeline</label>
                  <p className="mt-1 text-sm text-gray-900 capitalize">{requirement.timeline}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Status</label>
                  <span className={`mt-1 inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(requirement.status)}`}>
                    {requirement.status}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Scraping Status</label>
                  <div className="mt-1 flex items-center space-x-2">
                    {getScrapingStatusIcon(requirement.scraping_status)}
                    <span className="text-sm text-gray-900">{getScrapingStatusText(requirement.scraping_status)}</span>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Progress</label>
                  <div className="mt-1 space-y-1">
                    <p className="text-sm text-gray-900">Total Found: {requirement.total_listings_found}</p>
                    <p className="text-sm text-gray-900">Matching: {requirement.matching_listings_count}</p>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Last Scraped</label>
                  <p className="mt-1 text-sm text-gray-900">{formatDate(requirement.last_scraped_at)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Next Scrape</label>
                  <p className="mt-1 text-sm text-gray-900">{formatDate(requirement.next_scrape_at)}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Created</label>
                  <p className="mt-1 text-sm text-gray-900">
                    {new Date(requirement.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Listings and Messages */}
          <div className="lg:col-span-2">
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {/* Listings */}
              <div className="card">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Found Listings ({listings.length})</h2>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {listings.length === 0 ? (
                    <p className="text-gray-500 text-center py-4">No listings found yet</p>
                  ) : (
                    listings.map((listing) => (
                      <div
                        key={listing.id}
                        className={`border rounded-lg p-3 cursor-pointer transition-colors ${
                          selectedListing?.id === listing.id
                            ? 'border-primary-500 bg-primary-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => setSelectedListing(listing)}
                      >
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-medium text-gray-900 text-sm">{listing.title}</h3>
                            <p className="text-sm text-gray-600 mt-1">₹{listing.price}</p>
                            <p className="text-xs text-gray-500 mt-1">{listing.location}</p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(listing.status)}`}>
                              {listing.status}
                            </span>
                            <a
                              href={`https://www.olx.in/item/${listing.olx_id}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary-600 hover:text-primary-700"
                            >
                              <ExternalLink className="h-4 w-4" />
                            </a>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Messages */}
              <div className="card">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Messages</h2>
                {selectedListing ? (
                  <div className="space-y-4">
                    <div className="text-sm text-gray-600 mb-2">
                      Chat with seller for: <span className="font-medium">{selectedListing.title}</span>
                    </div>
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {messages.map((message) => (
                        <div
                          key={message.id}
                          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                          <div
                            className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                              message.role === 'user'
                                ? 'bg-primary-600 text-white'
                                : 'bg-gray-200 text-gray-900'
                            }`}
                          >
                            {message.content}
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Type your message..."
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        disabled={messageLoading}
                      />
                      <button
                        onClick={handleSendMessage}
                        disabled={!newMessage.trim() || messageLoading}
                        className="btn-primary"
                      >
                        <MessageSquare className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <MessageSquare className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>Select a listing to start messaging</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RequirementDetail 