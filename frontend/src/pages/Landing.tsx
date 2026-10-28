import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function Landing() {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans selection:bg-orange-500 selection:text-white">
      
      {/* Navigation */}
      <nav className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center">
        <div className="text-2xl font-black tracking-tighter text-white">
          Life<span className="text-orange-500">Sync</span> AI
        </div>
        <div className="flex gap-4">
          {user ? (
            <button onClick={() => navigate('/dashboard')} className="font-semibold hover:text-orange-400 transition">Go to Dashboard</button>
          ) : (
            <>
              <button onClick={() => navigate('/login')} className="font-semibold hover:text-orange-400 transition">Login</button>
              <button onClick={() => navigate('/register')} className="bg-orange-600 hover:bg-orange-500 px-5 py-2 rounded-full font-bold transition">Get Started</button>
            </>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 pt-20 pb-32 text-center">
        <div className="inline-block mb-6 px-4 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-400 font-bold text-sm tracking-wide">
          ONE AI. YOUR WHOLE LIFE.
        </div>
        <h1 className="text-5xl md:text-7xl font-black mb-8 leading-tight tracking-tight">
          Your Personal AI <br className="hidden md:block"/> Life Optimization Platform.
        </h1>
        <p className="text-xl md:text-2xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
          Synchronize your health, lifestyle, and career with one adaptive AI system that continuously learns from your progress. LifeSync AI doesn't just track your life—it adapts your plan around it.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <button onClick={() => navigate('/register')} className="bg-orange-600 hover:bg-orange-500 text-lg px-8 py-4 rounded-full font-bold transition shadow-lg shadow-orange-600/30">
            Start Your LifeSync Journey
          </button>
          <button onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })} className="bg-gray-800 hover:bg-gray-700 border border-gray-700 text-lg px-8 py-4 rounded-full font-bold transition">
            Explore AI Features
          </button>
        </div>
      </main>

      {/* Pillars Section */}
      <section id="features" className="bg-gray-800/50 py-24 border-y border-gray-800">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Five Pillars of Optimization</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">Our Cross-Domain Intelligence Engine connects every aspect of your life to generate a single, balanced daily plan.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-8">
            <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 hover:border-emerald-500/50 transition">
              <div className="text-4xl mb-4">🏃</div>
              <h3 className="font-bold text-lg mb-2 text-emerald-400">Fitness</h3>
              <p className="text-gray-400 text-sm">Adaptive calisthenics workouts scaled to your daily energy levels.</p>
            </div>
            
            <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 hover:border-blue-500/50 transition">
              <div className="text-4xl mb-4">🍎</div>
              <h3 className="font-bold text-lg mb-2 text-blue-400">Nutrition</h3>
              <p className="text-gray-400 text-sm">Dynamic macro tracking and food logging to fuel your goals.</p>
            </div>

            <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 hover:border-purple-500/50 transition">
              <div className="text-4xl mb-4">😴</div>
              <h3 className="font-bold text-lg mb-2 text-purple-400">Lifestyle</h3>
              <p className="text-gray-400 text-sm">Sleep and habit tracking that actively dictates your central recovery score.</p>
            </div>

            <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 hover:border-orange-500/50 transition">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="font-bold text-lg mb-2 text-orange-400">Career</h3>
              <p className="text-gray-400 text-sm">AI roadmaps, skill gap analysis, and mock interviews to level up your work.</p>
            </div>

            <div className="bg-gradient-to-br from-indigo-900 to-purple-900 p-6 rounded-2xl border border-indigo-500/50 transform md:-translate-y-4 shadow-xl">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="font-bold text-lg mb-2 text-indigo-300">Cross-Domain AI</h3>
              <p className="text-gray-300 text-sm">The central intelligence that reads all pillars to perfectly balance your time.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 text-center border-t border-gray-800 mt-20">
        <div className="text-2xl font-black tracking-tighter text-gray-600 mb-4">
          Life<span className="text-orange-800">Sync</span> AI
        </div>
        <p className="text-gray-500 text-sm">© 2026 LifeSync AI. All rights reserved.</p>
      </footer>
    </div>
  );
}
