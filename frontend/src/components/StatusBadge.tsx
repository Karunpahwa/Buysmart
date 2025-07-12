import React from 'react'

interface StatusBadgeProps {
  status: string
  size?: 'sm' | 'md'
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
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

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm'
  }

  return (
    <span className={`inline-flex font-medium rounded-full ${getStatusColor(status)} ${sizeClasses[size]}`}>
      {status}
    </span>
  )
}

export default StatusBadge 