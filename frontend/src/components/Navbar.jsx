import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X, LogIn, UserPlus, LogOut, User, Calendar, CreditCard, BarChart3, Settings } from 'lucide-react';

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">⚽</span>
            </div>
            <span className="text-xl font-bold text-gray-900">Terrains Sport</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-700 hover:text-blue-600 transition">Home</Link>
            <Link to="/search" className="text-gray-700 hover:text-blue-600 transition">Courts</Link>
            {isAuthenticated && (
              <>
                <Link to="/my-reservations" className="flex items-center gap-1 text-gray-700 hover:text-blue-600 transition">
                  <Calendar size={18} />
                  Reservations
                </Link>
                <Link to="/payments" className="flex items-center gap-1 text-gray-700 hover:text-blue-600 transition">
                  <CreditCard size={18} />
                  Payments
                </Link>
                <Link to="/analytics" className="flex items-center gap-1 text-gray-700 hover:text-blue-600 transition">
                  <BarChart3 size={18} />
                  Analytics
                </Link>
              </>
            )}
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link 
                  to="/settings"
                  className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition"
                >
                  <Settings size={20} />
                  <span>Settings</span>
                </Link>
                <button 
                  onClick={handleLogout}
                  className="flex items-center space-x-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                >
                  <LogOut size={20} />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link 
                  to="/login"
                  className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                >
                  <LogIn size={20} />
                  <span>Login</span>
                </Link>
                <Link 
                  to="/signup"
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
                >
                  <UserPlus size={20} />
                  <span>Sign Up</span>
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button 
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <Link to="/" className="block text-gray-700 hover:text-blue-600 py-2 px-2">Home</Link>
            <Link to="/search" className="block text-gray-700 hover:text-blue-600 py-2 px-2">Courts</Link>
            {isAuthenticated && (
              <>
                <Link to="/my-reservations" className="block text-gray-700 hover:text-blue-600 py-2 px-2">Reservations</Link>
                <Link to="/payments" className="block text-gray-700 hover:text-blue-600 py-2 px-2">Payments</Link>
                <Link to="/analytics" className="block text-gray-700 hover:text-blue-600 py-2 px-2">Analytics</Link>
                <Link to="/settings" className="block text-gray-700 hover:text-blue-600 py-2 px-2">Settings</Link>
              </>
            )}
            <div className="flex flex-col space-y-2 pt-2 border-t">
              {isAuthenticated ? (
                <>
                  <div className="px-4 py-2 text-gray-700">
                    Welcome, {user?.first_name || 'User'}
                  </div>
                  <button 
                    onClick={handleLogout}
                    className="w-full px-4 py-2 text-red-600 border border-red-600 rounded-lg hover:bg-red-50"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="w-full px-4 py-2 text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 text-center">
                    Login
                  </Link>
                  <Link to="/signup" className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-center">
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
