'use client'

import { useState } from 'react'
import { MapPin, Star } from 'lucide-react'

export default function PreferenceHub() {
  const [location, setLocation] = useState('')
  const [selectedBudget, setSelectedBudget] = useState('30')
  const [rating, setRating] = useState(4.0)
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([])

  const budgets = [
    { id: '15', label: '$15 BUDGET', value: 15 },
    { id: '30', label: '$30 MODERATE', value: 30 },
    { id: '50', label: '$50 UPSCALE', value: 50 },
    { id: '100', label: '$100+ FINE DINING', value: 100 }
  ]

  const cuisines = [
    { id: 'north-indian', name: 'North Indian', image: '/north-indian.jpg' },
    { id: 'chinese', name: 'Chinese', image: '/chinese.jpg' },
    { id: 'italian', name: 'Italian', image: '/italian.jpg' },
    { id: 'street-food', name: 'Street Food', image: '/street-food.jpg' }
  ]

  const toggleCuisine = (cuisineId: string) => {
    setSelectedCuisines(prev => 
      prev.includes(cuisineId) 
        ? prev.filter(id => id !== cuisineId)
        : [...prev, cuisineId]
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-red-500">Zomato AI</h1>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-red-500 font-medium border-b-2 border-red-500 pb-1">Preference Hub</a>
              <a href="#" className="text-gray-700 hover:text-red-500 font-medium">Trending</a>
              <a href="#" className="text-gray-700 hover:text-red-500 font-medium">Saved</a>
              <a href="#" className="text-gray-700 hover:text-red-500 font-medium">History</a>
            </nav>
            <button className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors">
              Sign In
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="bg-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Your Personalized Food Journey</h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Tell us what you're craving, and our AI will curate the perfect dining experiences tailored just for you.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Input Cards */}
          <div className="lg:col-span-2 space-y-6">
            {/* Location Card */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <MapPin className="w-5 h-5 mr-2 text-red-500" />
                Where are you?
              </h3>
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="Enter your delivery location"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                />
                <button className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                  Detect
                </button>
              </div>
            </div>

            {/* Budget Card */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold mb-4">Maximum Budget</h3>
              <div className="grid grid-cols-2 gap-3">
                {budgets.map((budget) => (
                  <button
                    key={budget.id}
                    onClick={() => setSelectedBudget(budget.id)}
                    className={`px-4 py-3 rounded-lg border-2 transition-all font-medium ${
                      selectedBudget === budget.id
                        ? 'bg-red-500 text-white border-red-500'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    {budget.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Rating Card */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Star className="w-5 h-5 mr-2 text-red-500" />
                Minimum Rating
              </h3>
              <div className="space-y-4">
                <input
                  type="range"
                  min="3.0"
                  max="5.0"
                  step="0.1"
                  value={rating}
                  onChange={(e) => setRating(parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-red-500"
                />
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-500">3.0</span>
                  <span className="text-xl font-bold text-red-500">{rating.toFixed(1)} ⭐</span>
                  <span className="text-sm text-gray-500">5.0</span>
                </div>
                <div className="flex items-center space-x-2">
                  <input type="checkbox" id="top-rated" className="w-4 h-4 text-red-500 rounded focus:ring-red-500" />
                  <label htmlFor="top-rated" className="text-sm text-gray-700">Only show top-rated places</label>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Cuisines */}
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h3 className="text-lg font-semibold mb-4">Favorite Cuisines</h3>
              <div className="grid grid-cols-2 gap-4 mb-4">
                {cuisines.map((cuisine) => (
                  <button
                    key={cuisine.id}
                    onClick={() => toggleCuisine(cuisine.id)}
                    className={`relative p-3 rounded-lg border-2 transition-all ${
                      selectedCuisines.includes(cuisine.id)
                        ? 'border-red-500 bg-red-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <div className="w-16 h-16 bg-gray-200 rounded-lg mb-2 mx-auto"></div>
                    <span className="text-sm font-medium text-gray-700">{cuisine.name}</span>
                  </button>
                ))}
              </div>
              <button className="w-full px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                + Explore More Cuisines
              </button>
            </div>
          </div>
        </div>

        {/* CTA Button */}
        <div className="mt-12 text-center">
          <button className="bg-red-500 text-white px-8 py-4 rounded-lg hover:bg-red-600 transition-colors text-lg font-semibold">
            Find my next meal →
          </button>
          <p className="mt-3 text-sm text-gray-600">Our AI will suggest 3 perfect restaurants based on your choices</p>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-bold text-red-500 mb-4">Zomato AI</h3>
            </div>
            <div>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-red-500">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-red-500">Terms of Service</a></li>
                <li><a href="#" className="hover:text-red-500">AI Methodology</a></li>
                <li><a href="#" className="hover:text-red-500">Feedback</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800 text-center text-sm text-gray-400">
            <p>&copy; 2024 Zomato AI Recommendation Engine. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
