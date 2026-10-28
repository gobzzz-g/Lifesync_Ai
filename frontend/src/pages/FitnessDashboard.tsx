import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function FitnessDashboard() {
  const [workout, setWorkout] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchFitnessData();
  }, []);

  const fetchFitnessData = async () => {
    try {
      const [workoutRes, historyRes] = await Promise.all([
        api.get('/api/fitness/today'),
        api.get('/api/fitness/history')
      ]);
      setWorkout(workoutRes.data);
      setHistory(historyRes.data);
    } catch (error) {
      console.error("Failed to fetch fitness data", error);
    } finally {
      setLoading(false);
    }
  };

  const regenerateWorkout = async () => {
    setLoading(true);
    try {
      const res = await api.post('/api/fitness/generate', { available_time: 20 });
      setWorkout(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-white min-h-screen bg-gray-900 flex justify-center items-center">Loading AI Coach...</div>;

  const chartData = history.slice(0, 10).reverse().map((h, i) => ({
    name: `W${i+1}`,
    rating: h.user_rating,
    duration: h.actual_duration
  }));

  const pushProgress = 35;
  const pullProgress = 20;
  
  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Top Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center bg-gray-800 p-6 rounded-2xl shadow-2xl border border-gray-700 gap-4">
          <div>
            <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">AI CALISTHENICS COACH</h1>
            <p className="text-gray-400 mt-2">Level: <span className="text-white font-medium">Intermediate</span> | Goal: <span className="text-white font-medium">Calisthenics Skills</span></p>
          </div>
          <div className="flex flex-wrap items-center gap-4 mt-4 md:mt-0 text-sm">
            <div className="bg-gray-700 px-4 py-2 rounded-xl flex flex-col items-center">
              <span className="text-gray-400">Recovery</span>
              <span className="text-green-400 font-bold text-lg">{workout?.recovery_level || 100}%</span>
            </div>
            <div className="bg-gray-700 px-4 py-2 rounded-xl flex flex-col items-center">
              <span className="text-gray-400">Streak</span>
              <span className="text-orange-400 font-bold text-lg">3 Days</span>
            </div>
            <button 
              id="back-to-dashboard-btn"
              onClick={() => navigate('/dashboard')} 
              className="bg-gray-700 hover:bg-gray-600 px-4 py-3 rounded-xl border border-gray-600 transition font-semibold text-white flex items-center gap-2 shadow hover:shadow-lg cursor-pointer"
            >
              <span>←</span> Back to Dashboard
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Column - Today's Workout */}
          <div className="lg:col-span-2 space-y-8">
            <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">Today's Adaptive Workout</h2>
                <button onClick={regenerateWorkout} className="text-sm bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded transition">
                  Regenerate
                </button>
              </div>
              
              {workout ? (
                <>
                  <div className="bg-blue-900/30 border border-blue-800/50 p-4 rounded-xl mb-6">
                    <h3 className="text-blue-400 font-semibold mb-2 text-sm uppercase tracking-wider">Why This Workout?</h3>
                    <p className="text-gray-300 whitespace-pre-line text-sm">{workout.reasoning || "Based on your current profile goals and available time, this workout will optimize your progression."}</p>
                  </div>

                  <div className="grid grid-cols-3 gap-4 mb-6 text-sm">
                    <div className="bg-gray-700 p-3 rounded-xl text-center">
                      <span className="block text-gray-400">Duration</span>
                      <span className="font-bold text-white">~{workout.duration} min</span>
                    </div>
                    <div className="bg-gray-700 p-3 rounded-xl text-center">
                      <span className="block text-gray-400">Difficulty</span>
                      <span className="font-bold text-white">{workout.difficulty}</span>
                    </div>
                    <div className="bg-gray-700 p-3 rounded-xl text-center">
                      <span className="block text-gray-400">Focus</span>
                      <span className="font-bold text-white">Strength & Skills</span>
                    </div>
                  </div>

                  <div className="space-y-4 mb-8">
                    {workout.exercises.map((we: any, i: number) => (
                      <div key={we.id} className="bg-gray-700/50 hover:bg-gray-700 p-4 rounded-xl flex justify-between items-center transition border border-transparent hover:border-gray-600">
                        <div className="flex items-center gap-4">
                          <div className="bg-gray-800 w-10 h-10 rounded-full flex items-center justify-center font-bold text-green-400">{i + 1}</div>
                          <div>
                            <h3 className="font-bold text-lg text-gray-100">{we.exercise.name}</h3>
                            <p className="text-xs text-gray-400">{we.exercise.muscle_groups}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-bold text-green-400 text-lg">{we.sets} × {we.reps}</div>
                          <div className="text-xs text-gray-400">Rest: {we.rest_time}s</div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <button 
                    onClick={() => navigate('/fitness/workout', { state: { workout } })}
                    className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-400 hover:to-green-500 text-white font-bold py-4 rounded-xl transition shadow-lg shadow-green-900/50 uppercase tracking-widest"
                  >
                    Start Workout 🚀
                  </button>
                </>
              ) : (
                <p className="text-gray-400">No workout available today.</p>
              )}
            </div>

            {/* Progression Trees */}
            <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700">
               <h2 className="text-2xl font-bold text-white mb-6">Calisthenics Progression</h2>
               
               <div className="space-y-6">
                 <div>
                   <div className="flex justify-between text-sm mb-2">
                     <span className="font-semibold text-gray-200">Push Progression (Push-up)</span>
                     <span className="text-green-400">{pushProgress}%</span>
                   </div>
                   <div className="w-full bg-gray-700 rounded-full h-2">
                     <div className="bg-green-500 h-2 rounded-full" style={{ width: `${pushProgress}%` }}></div>
                   </div>
                   <div className="flex justify-between text-xs text-gray-400 mt-2">
                     <span>Current: Knee Push-up</span>
                     <span>Next: Standard Push-up</span>
                   </div>
                 </div>

                 <div>
                   <div className="flex justify-between text-sm mb-2">
                     <span className="font-semibold text-gray-200">Pull Progression (Pull-up)</span>
                     <span className="text-blue-400">{pullProgress}%</span>
                   </div>
                   <div className="w-full bg-gray-700 rounded-full h-2">
                     <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${pullProgress}%` }}></div>
                   </div>
                   <div className="flex justify-between text-xs text-gray-400 mt-2">
                     <span>Current: Scapular Pulls</span>
                     <span>Next: Assisted Pull-up</span>
                   </div>
                 </div>
               </div>
            </div>
          </div>

          {/* Right Column - Stats, Nutrition, PRs */}
          <div className="space-y-8">
            
            {/* Personal Records */}
            <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">🏆 Personal Records</h2>
              <ul className="space-y-4">
                <li className="flex justify-between items-center border-b border-gray-700 pb-2">
                  <span className="text-gray-300 text-sm">Max Push-ups</span>
                  <span className="font-bold text-yellow-400">15 reps</span>
                </li>
                <li className="flex justify-between items-center border-b border-gray-700 pb-2">
                  <span className="text-gray-300 text-sm">Max Pull-ups</span>
                  <span className="font-bold text-yellow-400">2 reps</span>
                </li>
                <li className="flex justify-between items-center border-b border-gray-700 pb-2">
                  <span className="text-gray-300 text-sm">Longest Plank</span>
                  <span className="font-bold text-yellow-400">90 sec</span>
                </li>
              </ul>
            </div>

            {/* Nutrition Box */}
            <div className="bg-gradient-to-br from-purple-900/40 to-gray-800 p-6 rounded-2xl shadow-xl border border-purple-800/30">
              <h2 className="text-xl font-bold text-purple-400 mb-2">Nutrition for Your Goal</h2>
              <p className="text-sm text-gray-300 mb-4">
                For strength training and skill acquisition, prioritize adequate protein (1.6g/kg), balanced meals, and sufficient hydration to fuel your central nervous system.
              </p>
              <button onClick={() => navigate('/nutrition')} className="text-sm text-purple-400 hover:text-purple-300 font-semibold underline">
                View Nutrition Plan →
              </button>
            </div>

            {/* History Chart */}
            <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700">
              <h2 className="text-xl font-bold mb-4 text-white">Difficulty History</h2>
              {history.length > 0 ? (
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                      <XAxis dataKey="name" stroke="#9CA3AF" tick={{fontSize: 12}} />
                      <YAxis stroke="#9CA3AF" tick={{fontSize: 12}} />
                      <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }} />
                      <Line type="monotone" dataKey="rating" stroke="#4ADE80" strokeWidth={3} dot={{r: 4, fill: '#4ADE80'}} name="Difficulty (1-10)" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p className="text-sm text-gray-400">Complete workouts to see your progress chart.</p>
              )}
            </div>
            
          </div>
        </div>
      </div>
    </div>
  );
}
