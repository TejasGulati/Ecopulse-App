import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, AlertCircle, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setSuccessMessage('');
    try {
      await login(email, password);
      setSuccessMessage('Login successful! Redirecting...');
      setTimeout(() => navigate('/profile'), 2000);
    } catch (error) {
      if (error.response && error.response.data) {
        setErrors(error.response.data);
      } else {
        setErrors({ general: 'An unexpected error occurred. Please try again.' });
      }
    }
  };

  if (isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-800 via-teal-700 to-blue-800 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="absolute inset-0 bg-black opacity-50 z-0"></div>
      <div className="absolute inset-0 z-10">
        <div className="h-full w-full bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjMDAwMDAwNjYiPjwvcmVjdD4KPHBhdGggZD0iTTAgNUw1IDBaTTYgNEw0IDZaTS0xIDFMMSAtMVoiIHN0cm9rZT0iIzg4ODg4ODY2IiBzdHJva2Utd2lkdGg9IjEiPjwvcGF0aD4KPC9zdmc+')] opacity-10"></div>
      </div>
      <div className="sm:mx-auto sm:w-full sm:max-w-md z-20 relative">
        <motion.h2 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mt-6 text-center text-4xl font-extrabold text-white"
        >
          Login to Your Sustainable AI Future
        </motion.h2>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="mt-8 sm:mx-auto sm:w-full sm:max-w-md z-20 relative"
      >
        <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg py-8 px-4 shadow-2xl sm:rounded-lg sm:px-10 border border-white border-opacity-20">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-200">
                Email address
              </label>
              <div className="mt-1 relative">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className={`appearance-none block w-full px-3 py-2 pl-10 border ${errors.email ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm bg-white bg-opacity-10 text-white`}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
              </div>
              {errors.email && <p className="mt-2 text-sm text-red-400">{errors.email}</p>}
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-200">
                Password
              </label>
              <div className="mt-1 relative">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className={`appearance-none block w-full px-3 py-2 pl-10 border ${errors.password ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm bg-white bg-opacity-10 text-white`}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
              </div>
              {errors.password && <p className="mt-2 text-sm text-red-400">{errors.password}</p>}
            </div>

            {(errors.general || successMessage) && (
              <motion.div 
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`rounded-md p-4 flex items-center ${successMessage ? 'bg-green-400 bg-opacity-20 text-green-100' : 'bg-red-400 bg-opacity-20 text-red-100'}`}
              >
                {successMessage ? <CheckCircle className="mr-2" /> : <AlertCircle className="mr-2" />}
                {successMessage || errors.general}
              </motion.div>
            )}

            <div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                type="submit"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-300 ease-in-out"
              >
                Login
              </motion.button>
            </div>
          </form>
        </div>
      </motion.div>
    </div>
  );
}

export default Login;