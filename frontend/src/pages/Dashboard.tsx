import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const [lifeState, setLifeState] = useState<any>(null);
  const [balance, setBalance] = useState<any>(null);
  const [insights, setInsights] = useState<any>(null);
  const [plan, setPlan] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      // Fetch core state independently so partial failures don't crash the UI
      try {
        const stateRes = await api.get('/api/life/state');
        setLifeState(stateRes.data);
      } catch(e) { console.error("Failed to load life state", e); }
      
      try {
        const balanceRes = await api.get('/api/life/balance');
        setBalance(balanceRes.data);
      } catch(e) { console.error("Failed to load balance", e); }
      
      try {
        const insightRes = await api.get('/api/life/insights');
        setInsights(insightRes.data);
      } catch(e) { console.error("Failed to load insights", e); }

      try {
        const planRes = await api.get('/api/planner/today');
        setPlan(planRes.data);
      } catch (e: any) {
        if (e.response?.status === 404) {
          const newPlan = await api.post('/api/planner/generate');
          setPlan(newPlan.data);
        } else {
          console.error("Failed to load planner", e);
        }
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const regeneratePlan = async () => {
    setLoading(true);
    try {
      const newPlan = await api.post('/api/planner/generate');
      setPlan(newPlan.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteTask = async (taskId: number) => {
    try {
      await api.post(`/api/planner/tasks/${taskId}/complete`);
      fetchDashboardData();
    } catch (e) {}
  };

  if (loading) return <div className="p-8 text-white">Loading LifeSync Dashboard...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div className="mb-4 md:mb-0">
            <div className="flex items-center gap-4">
              <h1 className="text-3xl font-bold">Welcome, {user?.name || 'User'}</h1>
              <button onClick={() => navigate('/profile')} className="text-sm bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded-full border border-gray-600 flex items-center gap-2 transition shadow">
                <span>⚙️</span> My Profile & Preferences
              </button>
            </div>
            <p className="text-gray-400 mt-1">LifeSync AI Central Command</p>
          </div>
          <div className="flex flex-wrap gap-2 md:gap-4 mt-2 md:mt-0">
            <button onClick={() => navigate('/fitness')} className="bg-emerald-600 px-4 py-2 rounded text-sm font-bold hover:bg-emerald-500">Fitness</button>
            <button onClick={() => navigate('/nutrition')} className="bg-blue-600 px-4 py-2 rounded text-sm font-bold hover:bg-blue-500">Nutrition</button>
            <button onClick={() => navigate('/lifestyle')} className="bg-purple-600 px-4 py-2 rounded text-sm font-bold hover:bg-purple-500">Lifestyle</button>
            <button onClick={() => navigate('/career')} className="bg-orange-600 px-4 py-2 rounded text-sm font-bold hover:bg-orange-500">Career</button>
            <button onClick={() => navigate('/analytics')} className="bg-gray-600 px-4 py-2 rounded text-sm font-bold hover:bg-gray-500">Analytics</button>
            <button onClick={() => navigate('/gamification')} className="bg-yellow-600 px-4 py-2 rounded text-sm font-bold hover:bg-yellow-500">Level & XP</button>
          </div>
        </header>

        {/* Top KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-gray-400 font-bold mb-2">Overall Growth</h3>
            <div className="text-4xl font-bold text-white">{balance?.overall_growth || 0}%</div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-gray-400 font-bold mb-2">Life Balance</h3>
            <div className="text-4xl font-bold text-blue-400">{balance?.balance_score || 0}%</div>
            <p className="text-xs text-gray-400 mt-2">{balance?.reason}</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-gray-400 font-bold mb-2">Today's Priority</h3>
            <div className="text-3xl font-bold text-yellow-400">{plan?.overall_priority || 'Balanced'}</div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-gray-400 font-bold mb-2">Energy Level</h3>
            <div className="text-3xl font-bold text-green-400">{lifeState?.energy || 0}/10</div>
            <p className="text-xs text-gray-400 mt-2">from last check-in</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Planner / Insight */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* AI Insight Ribbon */}
            <div className="bg-gradient-to-r from-indigo-900 to-purple-900 p-6 rounded-lg border border-indigo-500/30">
              <div className="flex items-start gap-4">
                <div className="text-3xl">🧠</div>
                <div>
                  <h3 className="font-bold text-indigo-300">Cross-Domain AI Insight</h3>
                  <p className="text-gray-200 mt-1">{insights?.insight}</p>
                  <p className="text-indigo-200 font-bold mt-2">→ {insights?.recommendation}</p>
                </div>
              </div>
            </div>

            {/* AI Daily Plan */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold">AI Daily Planner</h2>
                <button onClick={regeneratePlan} className="text-sm bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded">Regenerate</button>
              </div>
              
              <div className="space-y-4">
                {plan?.tasks.map((task: any) => (
                  <div key={task.id} className="bg-gray-900 p-4 rounded flex justify-between items-center border border-gray-700">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className={`text-xs px-2 py-1 rounded font-bold ${
                          task.category === 'Fitness' ? 'bg-emerald-900 text-emerald-300' :
                          task.category === 'Career' ? 'bg-orange-900 text-orange-300' :
                          task.category === 'Nutrition' ? 'bg-blue-900 text-blue-300' :
                          'bg-purple-900 text-purple-300'
                        }`}>
                          {task.category}
                        </span>
                        <h3 className="font-bold">{task.title}</h3>
                      </div>
                      <p className="text-sm text-gray-400 mt-1">{task.duration} mins • Priority: {task.priority}</p>
                    </div>
                    {task.is_completed ? (
                      <span className="text-green-400 font-bold">✓</span>
                    ) : (
                      <button onClick={() => handleCompleteTask(task.id)} className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded text-sm transition">
                        Complete
                      </button>
                    )}
                  </div>
                ))}
                {(!plan?.tasks || plan.tasks.length === 0) && (
                  <p className="text-gray-400">No flexible tasks scheduled. Enjoy your day!</p>
                )}
              </div>
            </div>
            
          </div>

          {/* Right Sidebar - Module States */}
          <div className="space-y-6">
            <h2 className="text-xl font-bold">Domain Status</h2>
            
            <div className="bg-gray-800 p-5 rounded-lg border border-gray-700 flex justify-between items-center">
              <span className="font-bold">Fitness</span>
              <span className="text-emerald-400 font-bold text-xl">{lifeState?.fitness}%</span>
            </div>
            <div className="bg-gray-800 p-5 rounded-lg border border-gray-700 flex justify-between items-center">
              <span className="font-bold">Nutrition</span>
              <span className="text-blue-400 font-bold text-xl">{lifeState?.nutrition}%</span>
            </div>
            <div className="bg-gray-800 p-5 rounded-lg border border-gray-700 flex justify-between items-center">
              <span className="font-bold">Lifestyle</span>
              <span className="text-purple-400 font-bold text-xl">{lifeState?.lifestyle}%</span>
            </div>
            <div className="bg-gray-800 p-5 rounded-lg border border-gray-700 flex justify-between items-center">
              <span className="font-bold">Recovery</span>
              <span className={lifeState?.recovery < 60 ? "text-red-400 font-bold text-xl" : "text-green-400 font-bold text-xl"}>
                {lifeState?.recovery}%
              </span>
            </div>
            <div className="bg-gray-800 p-5 rounded-lg border border-gray-700 flex justify-between items-center">
              <span className="font-bold">Career</span>
              <span className="text-orange-400 font-bold text-xl">{lifeState?.career}%</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
