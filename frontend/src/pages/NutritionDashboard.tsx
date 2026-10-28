import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { FoodLogModal } from '../components/FoodLogModal';

export function NutritionDashboard() {
  const [profile, setProfile] = useState<any>(null);
  const [mealPlan, setMealPlan] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [score, setScore] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const [profRes, planRes, logRes, scoreRes] = await Promise.all([
        api.get('/api/profile'),
        api.get('/api/nutrition/today'),
        api.get('/api/nutrition/logs'),
        api.get('/api/nutrition/score')
      ]);
      setProfile(profRes.data);
      setMealPlan(planRes.data);
      setLogs(logRes.data);
      setScore(scoreRes.data.score);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const addWater = async (amount: number) => {
    try {
      await api.post('/api/nutrition/water', { amount_ml: amount });
      fetchData(); // Refresh to get updated water and XP
    } catch (e) {
      console.error(e);
    }
  };

  const regeneratePlan = async () => {
    setLoading(true);
    try {
      await api.post('/api/nutrition/generate');
      fetchData();
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-white">Loading Nutrition...</div>;

  const consumedCals = logs.reduce((sum, log) => sum + log.calories, 0);
  const consumedProtein = logs.reduce((sum, log) => sum + log.protein, 0);
  
  const targetCals = profile?.target_calories || 2000;
  const targetProtein = profile?.target_protein || 100;
  
  const calPercent = Math.min(100, (consumedCals / targetCals) * 100);
  const proteinPercent = Math.min(100, (consumedProtein / targetProtein) * 100);
  const waterPercent = Math.min(100, ((profile?.water_consumed || 0) / (profile?.water_target || 2500)) * 100);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-blue-400">AI Nutrition</h1>
          <button onClick={() => navigate('/dashboard')} className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded transition">
            Back to Dashboard
          </button>
        </header>

        {/* Top KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 p-4 rounded-lg shadow border border-gray-700">
            <h3 className="text-gray-400 text-sm mb-1">Score</h3>
            <div className="text-3xl font-bold text-green-400">{score}</div>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg shadow border border-gray-700">
            <h3 className="text-gray-400 text-sm mb-1">Calories</h3>
            <div className="text-xl font-bold">{consumedCals} / <span className="text-gray-400">{targetCals}</span></div>
            <div className="w-full bg-gray-700 h-2 mt-2 rounded-full overflow-hidden">
              <div className="bg-blue-500 h-full" style={{width: `${calPercent}%`}}></div>
            </div>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg shadow border border-gray-700">
            <h3 className="text-gray-400 text-sm mb-1">Protein</h3>
            <div className="text-xl font-bold">{consumedProtein.toFixed(0)}g / <span className="text-gray-400">{targetProtein}g</span></div>
            <div className="w-full bg-gray-700 h-2 mt-2 rounded-full overflow-hidden">
              <div className="bg-red-400 h-full" style={{width: `${proteinPercent}%`}}></div>
            </div>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg shadow border border-gray-700 flex flex-col justify-between">
            <div>
              <h3 className="text-gray-400 text-sm mb-1">Water</h3>
              <div className="text-xl font-bold">{profile?.water_consumed || 0}ml / <span className="text-gray-400">{profile?.water_target || 2500}ml</span></div>
              <div className="w-full bg-gray-700 h-2 mt-2 rounded-full overflow-hidden">
                <div className="bg-blue-300 h-full" style={{width: `${waterPercent}%`}}></div>
              </div>
            </div>
            <button onClick={() => addWater(250)} className="mt-2 bg-blue-900/50 hover:bg-blue-800 text-blue-300 text-xs py-1 rounded w-full transition">
              + 250ml
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content: AI Meal Plan */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-white">Today's Meal Plan</h2>
              <button onClick={regeneratePlan} className="text-sm text-blue-400 hover:text-blue-300">Regenerate</button>
            </div>
            
            <div className="space-y-6">
              {['Breakfast', 'Lunch', 'Dinner'].map(mealType => {
                const meal = mealPlan?.meals?.find((m: any) => m.meal_type === mealType);
                if (!meal) return null;
                
                const isLogged = logs.some(l => l.meal_type === mealType && l.food_name?.includes(meal.name));
                
                return (
                  <div key={meal.id} className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden shadow-lg">
                    <div className="bg-gray-700/50 p-4 border-b border-gray-700 flex justify-between items-center">
                      <div className="flex items-center gap-2">
                        <span className="text-xl">
                          {mealType === 'Breakfast' ? '🌅' : mealType === 'Lunch' ? '☀️' : '🌙'}
                        </span>
                        <h3 className="font-bold text-lg text-white uppercase tracking-wider">{mealType}</h3>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-blue-400">{meal.calories} kcal</div>
                        <div className="text-xs text-gray-400">P: {meal.protein}g • C: {meal.carbohydrates}g • F: {meal.fats}g</div>
                      </div>
                    </div>
                    
                    <div className="p-5">
                      <h4 className="font-bold text-lg text-white mb-2">{meal.name}</h4>
                      
                      <div className="mb-4">
                        <p className="text-sm text-gray-300">
                          {Array.isArray(meal.ingredients) ? meal.ingredients.map((i:any) => `${i.name} (${i.amount})`).join(' + ') : ''}
                        </p>
                      </div>
                      
                      {meal.ai_explanation && (
                        <div className="mb-5 bg-blue-900/20 border border-blue-900/50 rounded p-3">
                          <p className="text-xs text-blue-300 font-semibold mb-1">WHY THIS MEAL?</p>
                          <p className="text-xs text-gray-300">{meal.ai_explanation}</p>
                        </div>
                      )}
                      
                      <div className="flex gap-3 mt-4">
                        <button 
                          onClick={async () => {
                            if(isLogged) return;
                            try {
                              await api.post('/api/nutrition/log', {
                                food_name: `${meal.name} (Suggested)`,
                                meal_type: mealType,
                                quantity: 1,
                                calories: meal.calories,
                                protein: meal.protein,
                                carbohydrates: meal.carbohydrates,
                                fats: meal.fats,
                                fiber: 0
                              });
                              fetchData();
                            } catch(e) { console.error(e); }
                          }}
                          disabled={isLogged}
                          className={`flex-1 py-2 rounded font-bold transition ${isLogged ? 'bg-green-600/50 text-green-200 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/20'}`}
                        >
                          {isLogged ? '✓ Logged' : 'Log This Meal'}
                        </button>
                        
                        <button 
                          onClick={async () => {
                            setLoading(true);
                            try {
                              await api.post(`/api/nutrition/replace_meal/${meal.id}`);
                              fetchData();
                            } catch(e) { console.error(e); setLoading(false); }
                          }}
                          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-gray-300 rounded transition text-sm"
                        >
                          Replace
                        </button>
                      </div>
                      
                    </div>
                  </div>
                );
              })}
            </div>
            
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            
            <button 
              onClick={() => setIsModalOpen(true)}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-lg shadow-lg shadow-blue-900/20 transition flex items-center justify-center gap-2"
            >
              <span>+</span> Log Food
            </button>

            <div className="bg-gray-800 p-5 rounded-lg border border-gray-700">
              <h3 className="font-bold mb-4">Today's Logs</h3>
              {logs.length > 0 ? (
                <ul className="space-y-3">
                  {logs.map((log: any) => (
                    <li key={log.id} className="flex justify-between text-sm">
                      <span className="text-gray-300">{log.food_name || 'Food'} ({log.meal_type})</span>
                      <span className="text-green-400">{log.calories} kcal</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-gray-400">Nothing logged yet today.</p>
              )}
            </div>
            
          </div>

        </div>
      </div>

      <FoodLogModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onLogged={fetchData} 
        mealPlan={mealPlan}
        profile={profile}
      />
    </div>
  );
}
