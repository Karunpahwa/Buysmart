# BuySmart Assistant Frontend

A modern React application for the BuySmart Assistant platform, helping buyers search and negotiate on OLX India.

## Features

### 🏠 Dashboard
- Overview of all requirements with status tracking
- Statistics cards showing active searches, negotiations, and completed deals
- Quick access to requirement details and messaging

### 📋 Requirements Management
- Create new requirements with detailed specifications
- View requirement details with associated listings
- Track requirement status (active, paused, fulfilled)

### 🏷️ Listings Integration
- View all listings found for each requirement
- Direct links to OLX listings
- Status tracking for each listing (new, contacted, responded, eliminated)

### 💬 Messaging System
- Real-time messaging with sellers
- Message history for each listing
- User-friendly chat interface

### 🔐 Authentication
- Secure login/logout functionality
- Protected routes for authenticated users
- Token-based authentication

## Tech Stack

- **React 18** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Axios** for API communication
- **Vite** for build tooling

## Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend server running (see backend README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:5173](http://localhost:5173) in your browser

### Build for Production

```bash
npm run build
```

### Running Tests

```bash
npm test
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── LoadingSpinner.tsx
│   ├── StatusBadge.tsx
│   ├── ErrorMessage.tsx
│   ├── Navigation.tsx
│   └── ProtectedRoute.tsx
├── contexts/           # React contexts
│   └── AuthContext.tsx
├── pages/             # Page components
│   ├── Dashboard.tsx
│   ├── Login.tsx
│   ├── RequirementForm.tsx
│   └── RequirementDetail.tsx
├── services/          # API services
│   └── api.ts
├── App.tsx           # Main app component
├── main.tsx          # App entry point
└── index.css         # Global styles
```

## API Integration

The frontend communicates with the backend through RESTful APIs:

- **Authentication**: `/api/auth/*`
- **Requirements**: `/api/requirements/*`
- **Listings**: `/api/listings/*`
- **Messages**: `/api/messages/*`

## Key Components

### Authentication Flow
- Login page with email/password
- JWT token storage in localStorage
- Automatic token refresh
- Protected route wrapper

### Dashboard Features
- Real-time statistics
- Requirement cards with quick actions
- Responsive design for mobile/desktop

### Requirement Management
- Form validation
- Category and timeline selection
- Budget range specification
- Status tracking

### Messaging Interface
- Real-time message updates
- User/seller message distinction
- Message history persistence

## Development

### Adding New Features
1. Create components in `src/components/`
2. Add pages in `src/pages/`
3. Update API services in `src/services/api.ts`
4. Add routes in `src/App.tsx`

### Styling Guidelines
- Use Tailwind CSS classes
- Follow the design system in `tailwind.config.js`
- Use the custom CSS classes in `index.css`

### State Management
- Use React Context for global state (auth)
- Local state for component-specific data
- API calls through service functions

## Contributing

1. Follow the existing code structure
2. Use TypeScript for type safety
3. Add proper error handling
4. Test new features thoroughly
5. Update documentation as needed

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Ensure backend server is running
   - Check API base URL configuration
   - Verify CORS settings

2. **Authentication Issues**
   - Clear localStorage and re-login
   - Check token expiration
   - Verify backend auth endpoints

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check TypeScript configuration
   - Verify all dependencies are installed

## License

This project is part of the BuySmart Assistant platform. 