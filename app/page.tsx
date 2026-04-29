'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MapPin, Star, Search, Clock, Utensils, IndianRupee, Sparkles, X, ChevronRight, ChevronLeft } from 'lucide-react'

export default function Home() {
  const [location, setLocation] = useState('Any')
  const [budgetAmount, setBudgetAmount] = useState(1500)
  const [rating, setRating] = useState(4.0)
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([])
  const [ambiance, setAmbiance] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [locations, setLocations] = useState<string[]>(['Any'])
  const [results, setResults] = useState<any[]>([])
  
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetch(`${API_URL}/api/locations`)
      .then(res => res.json())
      .then(data => {
        if (data.locations) {
          setLocations(data.locations)
        }
      })
      .catch(err => console.error("Failed to fetch locations:", err))
  }, [])


  const cuisines = [
    { id: 'north-indian', name: 'North Indian' },
    { id: 'chinese', name: 'Chinese' },
    { id: 'italian', name: 'Italian' },
    { id: 'street-food', name: 'Street Food' },
    { id: 'cafe', name: 'Cafe' },
    { id: 'desserts', name: 'Desserts' }
  ]

  const toggleCuisine = (cuisineId: string) => {
    setSelectedCuisines(prev => 
      prev.includes(cuisineId) 
        ? prev.filter(id => id !== cuisineId)
        : [...prev, cuisineId]
    )
  }

  const handleSearch = async () => {
    setIsSearching(true)
    try {
      const response = await fetch(`${API_URL}/api/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location: location,
          max_budget: budgetAmount,
          cuisines: selectedCuisines,
          min_rating: rating,
          user_query: ambiance
        })
      })
      const data = await response.json()
      if (data.recommendations) {
        setResults(data.recommendations)
      } else {
        setResults([])
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error)
      setResults([])
    } finally {
      setIsSearching(false)
      setShowResults(true)
    }
  }

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1 }
  }

  return (
    <div className="min-h-screen bg-hero bg-fixed text-white font-sans selection:bg-red-500/30 overflow-x-hidden">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/10 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-red-500/20">
              <Sparkles className="text-white w-6 h-6" />
            </div>
            <span className="text-2xl font-bold tracking-tight">Zomato <span className="text-primary text-3xl">AI</span></span>
          </div>
          <div className="flex items-center gap-8 text-sm font-medium text-white/70">
            {/* Navbar buttons removed as per request */}
          </div>
        </div>
      </nav>

      <main className="pt-32 pb-20 px-6 max-w-7xl mx-auto">
        <AnimatePresence mode="wait">
          {!showResults ? (
            <motion.div
              key="search"
              initial="hidden"
              animate="visible"
              exit={{ opacity: 0, scale: 0.95 }}
              variants={containerVariants}
              className="space-y-12"
            >
              {/* Hero Header */}
              <div className="text-center space-y-4 max-w-3xl mx-auto">
                <motion.h1 
                  variants={itemVariants}
                  className="text-5xl md:text-7xl font-extrabold tracking-tight"
                >
                  Your Personal <br />
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-400">
                    Food Concierge
                  </span>
                </motion.h1>
                <motion.p 
                  variants={itemVariants}
                  className="text-xl text-white/60 font-medium"
                >
                  Describe your craving, and our AI will find the perfect spot.
                </motion.p>
              </div>

              {/* Input Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Location Box */}
                <motion.div variants={itemVariants} className="glass-card p-6 rounded-3xl space-y-4 group">
                  <div className="flex items-center gap-3 text-primary">
                    <MapPin className="w-5 h-5" />
                    <h3 className="font-bold text-sm tracking-widest uppercase">Location</h3>
                  </div>
                  <select 
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="custom-select"
                  >
                    {locations.map(loc => (
                      <option key={loc} value={loc}>{loc}</option>
                    ))}
                  </select>
                  <div className="h-px bg-white/10 group-focus-within:bg-primary/50 transition-colors" />
                </motion.div>

                {/* Pricing Box */}
                <motion.div variants={itemVariants} className="glass-card p-6 rounded-3xl space-y-4">
                  <div className="flex items-center gap-3 text-primary">
                    <IndianRupee className="w-5 h-5" />
                    <h3 className="font-bold text-sm tracking-widest uppercase">Budget</h3>
                  </div>
                  <div className="space-y-2">
                    <input 
                      type="range" 
                      min="200" max="5000" step="100"
                      value={budgetAmount}
                      onChange={(e) => setBudgetAmount(parseInt(e.target.value))}
                      className="w-full accent-primary"
                    />
                    <div className="flex justify-between text-xs font-bold text-white/40">
                      <span>₹200</span>
                      <span className="text-primary text-sm">₹{budgetAmount}</span>
                      <span>₹5000+</span>
                    </div>
                  </div>
                </motion.div>

                {/* Rating Box */}
                <motion.div variants={itemVariants} className="glass-card p-6 rounded-3xl space-y-4">
                  <div className="flex items-center gap-3 text-primary">
                    <Star className="w-5 h-5" />
                    <h3 className="font-bold text-sm tracking-widest uppercase">Rating</h3>
                  </div>
                  <div className="flex items-center justify-between">
                    <input 
                      type="range" 
                      min="3.0" max="5.0" step="0.1"
                      value={rating}
                      onChange={(e) => setRating(parseFloat(e.target.value))}
                      className="w-2/3 accent-primary"
                    />
                    <span className="text-xl font-black">{rating.toFixed(1)}</span>
                  </div>
                </motion.div>

                {/* Search Action */}
                <motion.div variants={itemVariants} className="flex flex-col gap-4">
                  <button 
                    onClick={handleSearch}
                    disabled={isSearching}
                    className="flex-1 bg-primary hover:bg-primary-hover rounded-3xl flex items-center justify-center gap-3 text-xl font-bold transition-all shadow-xl shadow-red-500/20 active:scale-95 disabled:opacity-50"
                  >
                    {isSearching ? (
                      <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                      <>
                        <Search className="w-6 h-6" />
                        Explore
                      </>
                    )}
                  </button>
                </motion.div>
              </div>

              {/* Second Row */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Cuisine Box */}
                <motion.div variants={itemVariants} className="glass-card p-8 rounded-3xl lg:col-span-1 space-y-6">
                  <div className="flex items-center gap-3 text-primary">
                    <Utensils className="w-5 h-5" />
                    <h3 className="font-bold text-sm tracking-widest uppercase">Cuisines</h3>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {cuisines.map((c) => (
                      <button
                        key={c.id}
                        onClick={() => toggleCuisine(c.id)}
                        className={`px-4 py-2 rounded-full text-xs font-medium border transition-all ${
                          selectedCuisines.includes(c.id)
                            ? 'bg-primary border-primary'
                            : 'bg-white/5 border-white/10 hover:bg-white/10'
                        }`}
                      >
                        {c.name}
                      </button>
                    ))}
                  </div>
                </motion.div>

                {/* Ambiance/Query Box */}
                <motion.div variants={itemVariants} className="glass-card p-8 rounded-3xl lg:col-span-2 space-y-6">
                  <div className="flex items-center gap-3 text-primary">
                    <Sparkles className="w-5 h-5" />
                    <h3 className="font-bold text-sm tracking-widest uppercase">Describe the Vibe</h3>
                  </div>
                  <textarea 
                    placeholder="e.g. A romantic rooftop for a dinner date with soft music..."
                    value={ambiance}
                    onChange={(e) => setAmbiance(e.target.value)}
                    className="w-full bg-transparent border-none focus:ring-0 text-xl placeholder:text-white/10 outline-none resize-none h-24"
                  />
                </motion.div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-12"
            >
              <div className="flex flex-col gap-6">
                <button 
                  onClick={() => setShowResults(false)}
                  className="w-fit flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-full border border-white/10 transition-all text-sm font-bold text-white/60 hover:text-white"
                >
                  <ChevronLeft className="w-4 h-4" />
                  Back to Search
                </button>
                
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-4xl font-black">Top Picks For You</h2>

                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {results.length === 0 ? (
                  <div className="col-span-full text-center text-white/50 text-xl py-12">
                    No restaurants found matching your criteria. Try loosening your filters!
                  </div>
                ) : (
                  results.map((res, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 50, scale: 0.9 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      transition={{ 
                        type: 'spring',
                        stiffness: 100,
                        damping: 15,
                        delay: idx * 0.1 
                      }}
                      whileHover={{ y: -10 }}
                      className="glass-card rounded-[2.5rem] overflow-hidden group flex flex-col"
                    >
                      <div className="relative h-64 overflow-hidden shrink-0 bg-white/5 flex items-center justify-center">
                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent z-10" />
                        <img 
                          src={res.Image} 
                          alt={res.Name}
                          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                        />
                        <div className="absolute top-6 right-6 z-20 px-3 py-1 bg-primary rounded-full text-xs font-bold shadow-lg">
                          AI MATCH
                        </div>
                      </div>
                      <div className="p-8 space-y-6 flex flex-col grow">
                        <div className="space-y-1">
                          <h3 className="text-2xl font-bold">{res.Name}</h3>
                          <div className="flex items-center gap-2 text-xs text-white/50 font-bold tracking-widest flex-wrap">
                            <span className="flex items-center gap-1 shrink-0"><Star className="w-3 h-3 text-yellow-400 fill-yellow-400" /> {res.Rating}</span>
                            <span>•</span>
                            <span className="shrink-0">₹{res.Cost} FOR TWO</span>
                            <span>•</span>
                            <span className="truncate">{res.Location}</span>
                          </div>
                        </div>
                        
                        <div className="bg-white/5 border-l-2 border-primary p-4 rounded-r-2xl italic text-sm text-white/80 leading-relaxed group-hover:bg-primary/5 transition-colors grow">
                          "{res.Explanation}"
                        </div>

                        <button className="w-full py-4 bg-white/5 hover:bg-primary rounded-2xl flex items-center justify-center gap-2 text-sm font-bold border border-white/10 transition-all mt-auto">
                          View Details <ChevronRight className="w-4 h-4" />
                        </button>
                      </div>
                    </motion.div>
                  ))
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="mt-20 border-t border-white/10 py-12 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 text-center text-white/20 text-sm">
          &copy; 2024 Zomato AI. Experimental Intelligence.
        </div>
      </footer>
    </div>
  )
}
