import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export function LifestyleDashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [habits, setHabits] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Modals state
  const [showCheckIn, setShowCheckIn] = useState(false);
  const [showSleep, setShowSleep] = useState(false);
  const [showHabitForm, setShowHabitForm] = useState(false);

  // Forms
  const [checkInForm, setCheckInForm] = useState({ energy: 5, stress: 5, mood: 5, productivity: 5, notes: '' });
  const [sleepForm, setSleepForm] = useState({ bedtime: '22:30', wake_time: '06:30', sleep_duration: 8, sleep_quality: 'Good' });
  const [habitForm, setHabitForm] = useState({ name: '', category: 'Health' });

  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const [sumRes, habRes] = await Promise.all([
        api.get('/api/lifestyle/summary'),
        api.get('/api/lifestyle/habits')
      ]);
      setSummary(sumRes.data);
      setHabits(habRes.data);
    } catch (e) {
      console.error("Failed to fetch lifestyle data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCheckIn = async () => {
    try {
      await api.post('/api/lifestyle/check-in', checkInForm);
      setShowCheckIn(false);
      fetchData();
    } catch(e) {}
  };

  const handleSleep = async () => {
    try {
      await api.post('/api/lifestyle/sleep', sleepForm);
      setShowSleep(false);
      fetchData();
    } catch(e) {}
  };

  const handleAddHabit = async () => {
    try {
      await api.post('/api/lifestyle/habits', habitForm);
      setShowHabitForm(false);
      setHabitForm({ name: '', category: 'Health' });
      fetchData();
    } catch(e) {}
  };

  const handleCompleteHabit = async (id: number) => {
    try {
      await api.post(`/api/lifestyle/habits/${id}/complete`);
      fetchData();
    } catch(e) {}
  };

  if (loading) return <div className="p-8 text-white">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-purple-400">Lifestyle & Recovery</h1>
          <button onClick={() => navigate('/dashboard')} className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded transition">
            Back to Dashboard
          </button>
        </header>

        {/* AI Insight */}
        {summary?.ai_insight && (
          <div className="bg-purple-900/30 border border-purple-500/50 p-6 rounded-lg text-purple-200 flex items-start gap-4">
            <span className="text-2xl">🧠</span>
            <p>{summary.ai_insight}</p>
          </div>
        )}

        {/* Scores */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 text-center">
            <h3 className="text-gray-400 mb-2">Lifestyle Score</h3>
            <div className="text-4xl font-bold text-purple-400">{summary?.lifestyle_score}</div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 text-center">
            <h3 className="text-gray-400 mb-2">Recovery</h3>
            <div className="text-4xl font-bold text-blue-400">{summary?.recovery_score}%</div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 text-center">
            <h3 className="text-gray-400 mb-2">Last Sleep</h3>
            <div className="text-4xl font-bold text-indigo-400">{summary?.sleep_duration}h</div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 text-center">
            <h3 className="text-gray-400 mb-2">Habits Done</h3>
            <div className="text-4xl font-bold text-green-400">{summary?.completed_habits_today}/{summary?.active_habits_count}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Quick Actions */}
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 space-y-4">
            <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
            <button onClick={() => setShowCheckIn(true)} className="w-full bg-gray-700 hover:bg-gray-600 py-3 rounded text-left px-4 flex justify-between">
              <span>Daily Check-in (Energy, Stress)</span> <span>→</span>
            </button>
            <button onClick={() => setShowSleep(true)} className="w-full bg-gray-700 hover:bg-gray-600 py-3 rounded text-left px-4 flex justify-between">
              <span>Log Sleep</span> <span>→</span>
            </button>
            <button onClick={() => setShowHabitForm(true)} className="w-full bg-gray-700 hover:bg-gray-600 py-3 rounded text-left px-4 flex justify-between">
              <span>Create New Habit</span> <span>+</span>
            </button>
          </div>

          {/* Habits */}
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h2 className="text-xl font-bold mb-4">Today's Habits</h2>
            {habits.length === 0 ? (
              <p className="text-gray-400">No habits tracked yet.</p>
            ) : (
              <ul className="space-y-3">
                {habits.map((h: any) => (
                  <li key={h.id} className="flex justify-between items-center bg-gray-700 p-3 rounded">
                    <div>
                      <span className="font-semibold">{h.name}</span>
                      <span className="text-xs text-gray-400 ml-2 bg-gray-900 px-2 py-1 rounded">{h.category}</span>
                    </div>
                    {h.is_completed_today ? (
                      <span className="text-green-400 font-bold">✓ Done</span>
                    ) : (
                      <button onClick={() => handleCompleteHabit(h.id)} className="bg-green-600 hover:bg-green-500 px-3 py-1 rounded text-sm transition">
                        Complete
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>

        </div>
      </div>

      {/* Check In Modal */}
      {showCheckIn && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-sm">
            <h2 className="text-xl font-bold mb-4">Daily Check-In</h2>
            <div className="space-y-4">
              <div><label className="block text-sm">Energy (1-10)</label><input type="range" min="1" max="10" value={checkInForm.energy} onChange={e => setCheckInForm({...checkInForm, energy: +e.target.value})} className="w-full"/></div>
              <div><label className="block text-sm">Stress (1-10)</label><input type="range" min="1" max="10" value={checkInForm.stress} onChange={e => setCheckInForm({...checkInForm, stress: +e.target.value})} className="w-full"/></div>
              <div><label className="block text-sm">Productivity (1-10)</label><input type="range" min="1" max="10" value={checkInForm.productivity} onChange={e => setCheckInForm({...checkInForm, productivity: +e.target.value})} className="w-full"/></div>
              <button onClick={handleCheckIn} className="w-full bg-purple-600 py-2 rounded font-bold">Save Check-In</button>
              <button onClick={() => setShowCheckIn(false)} className="w-full bg-gray-700 py-2 rounded">Cancel</button>
            </div>
          </div>
        </div>
      )}

      {/* Sleep Modal */}
      {showSleep && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-sm">
            <h2 className="text-xl font-bold mb-4">Log Sleep</h2>
            <div className="space-y-4">
              <div><label className="block text-sm">Duration (hours)</label><input type="number" step="0.5" value={sleepForm.sleep_duration} onChange={e => setSleepForm({...sleepForm, sleep_duration: +e.target.value})} className="w-full bg-gray-900 p-2 rounded"/></div>
              <div><label className="block text-sm">Quality</label>
                <select value={sleepForm.sleep_quality} onChange={e => setSleepForm({...sleepForm, sleep_quality: e.target.value})} className="w-full bg-gray-900 p-2 rounded">
                  <option>Good</option><option>Fair</option><option>Poor</option>
                </select>
              </div>
              <button onClick={handleSleep} className="w-full bg-blue-600 py-2 rounded font-bold">Save Sleep</button>
              <button onClick={() => setShowSleep(false)} className="w-full bg-gray-700 py-2 rounded">Cancel</button>
            </div>
          </div>
        </div>
      )}

      {/* Habit Modal */}
      {showHabitForm && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-sm">
            <h2 className="text-xl font-bold mb-4">New Habit</h2>
            <div className="space-y-4">
              <div><label className="block text-sm">Habit Name</label><input type="text" value={habitForm.name} onChange={e => setHabitForm({...habitForm, name: e.target.value})} className="w-full bg-gray-900 p-2 rounded"/></div>
              <div><label className="block text-sm">Category</label>
                <select value={habitForm.category} onChange={e => setHabitForm({...habitForm, category: e.target.value})} className="w-full bg-gray-900 p-2 rounded">
                  <option>Health</option><option>Productivity</option><option>Mindfulness</option><option>Learning</option>
                </select>
              </div>
              <button onClick={handleAddHabit} className="w-full bg-green-600 py-2 rounded font-bold">Create Habit</button>
              <button onClick={() => setShowHabitForm(false)} className="w-full bg-gray-700 py-2 rounded">Cancel</button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
