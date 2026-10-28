import { useState, useEffect } from 'react';
import api from '../services/api';

export function FoodLogModal({ isOpen, onClose, onLogged, mealPlan, profile }: { isOpen: boolean, onClose: () => void, onLogged: () => void, mealPlan?: any, profile?: any }) {
  const [foods, setFoods] = useState<any[]>([]);
  const [mealType, setMealType] = useState('Breakfast');

  useEffect(() => {
    if (isOpen && foods.length === 0) {
      api.get('/api/nutrition/foods').then(res => setFoods(res.data));
    }
  }, [isOpen, foods.length]);

  const handleLogFood = async (food: any) => {
    try {
      await api.post('/api/nutrition/log', {
        food_id: food.id,
        food_name: food.name,
        meal_type: mealType,
        quantity: 1,
        calories: food.calories,
        protein: food.protein,
        carbohydrates: food.carbohydrates,
        fats: food.fats,
        fiber: food.fiber
      });
      onLogged();
      onClose();
    } catch (e) {
      alert("Failed to log food");
    }
  };

  const handleLogSuggestedMeal = async (meal: any) => {
    try {
      await api.post('/api/nutrition/log', {
        food_name: `${meal.name} (Suggested)`,
        meal_type: meal.meal_type || mealType,
        quantity: 1,
        calories: meal.calories,
        protein: meal.protein,
        carbohydrates: meal.carbohydrates,
        fats: meal.fats,
        fiber: 0
      });
      onLogged();
      onClose();
    } catch (e) {
      alert("Failed to log meal");
    }
  };

  if (!isOpen) return null;

  // Filter foods by user preference
  let allowedFoods = foods;
  const diet = profile?.dietary_preferences || '';
  if (diet.includes('Vegan')) {
    allowedFoods = allowedFoods.filter(f => f.dietary_tags?.includes('Vegan'));
  } else if (diet.includes('Vegetarian')) {
    allowedFoods = allowedFoods.filter(f => f.dietary_tags?.includes('Vegetarian'));
  }

  // Group by category
  const proteins = allowedFoods.filter(f => f.category === 'Protein' || f.category === 'Dairy');
  const carbs = allowedFoods.filter(f => f.category === 'Grain' || f.category === 'Fruit');
  const veggies = allowedFoods.filter(f => f.category === 'Vegetable');

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-800 rounded-lg shadow-2xl p-6 w-full max-w-2xl border border-gray-700 max-h-[90vh] flex flex-col">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-white">Log Food</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">✕</button>
        </div>

        <div className="mb-6 flex gap-4 items-center bg-gray-900 p-3 rounded-lg border border-gray-700">
          <label className="text-gray-300 font-bold whitespace-nowrap">Logging for:</label>
          <select 
            value={mealType} 
            onChange={e => setMealType(e.target.value)}
            className="bg-gray-800 border border-gray-600 rounded p-2 text-white w-full font-bold text-blue-400"
          >
            <option value="Breakfast">Breakfast</option>
            <option value="Lunch">Lunch</option>
            <option value="Dinner">Dinner</option>
            <option value="Snack">Snack</option>
          </select>
        </div>

        <div className="overflow-y-auto flex-1 space-y-8 pr-2">
          
          {/* Section: Full AI Meal Suggestions */}
          <div>
            <h3 className="text-sm text-gray-400 font-bold uppercase tracking-wider mb-3 border-b border-gray-700 pb-2">Full Meal Suggestions</h3>
            {!mealPlan || !mealPlan.meals || mealPlan.meals.length === 0 ? (
              <p className="text-gray-500 text-sm">No full meal suggestions available.</p>
            ) : (
              <div className="grid grid-cols-1 gap-3">
                {mealPlan.meals.filter((m:any) => m.name.toLowerCase().includes(mealType.toLowerCase()) || m.meal_type?.toLowerCase() === mealType.toLowerCase() || true).slice(0,2).map((meal: any) => (
                  <div key={meal.id} className="bg-blue-900/20 p-3 rounded-lg border border-blue-900/50 flex justify-between items-center">
                    <div>
                      <h4 className="text-blue-300 font-bold">{meal.name}</h4>
                      <p className="text-xs text-gray-400 mt-1">{meal.calories} kcal • P: {meal.protein}g</p>
                    </div>
                    <button onClick={() => handleLogSuggestedMeal(meal)} className="bg-blue-600 hover:bg-blue-500 text-white text-xs px-4 py-2 rounded transition">
                      Log Meal
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Section: Individual Foods by Category */}
          <div>
            <h3 className="text-sm text-gray-400 font-bold uppercase tracking-wider mb-3 border-b border-gray-700 pb-2">Individual Foods ({diet || 'All'})</h3>
            <p className="text-xs text-gray-500 mb-4">Build your own {mealType.toLowerCase()} from these options tailored to your preferences.</p>
            
            <div className="space-y-6">
              {/* Proteins */}
              {proteins.length > 0 && (
                <div>
                  <h4 className="text-red-400 font-bold text-sm mb-2">Proteins</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {proteins.map(f => (
                      <div key={f.id} className="bg-gray-700 p-2 rounded flex justify-between items-center group hover:bg-gray-600 transition">
                        <div>
                          <div className="text-white text-sm">{f.name} <span className="text-xs text-gray-400">({f.serving_size})</span></div>
                          <div className="text-xs text-red-300">{f.protein}g protein • {f.calories} kcal</div>
                        </div>
                        <button onClick={() => handleLogFood(f)} className="text-blue-400 opacity-0 group-hover:opacity-100 px-2 py-1 bg-gray-800 rounded text-xs transition">+</button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Carbs */}
              {carbs.length > 0 && (
                <div>
                  <h4 className="text-yellow-400 font-bold text-sm mb-2">Carbs & Grains</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {carbs.map(f => (
                      <div key={f.id} className="bg-gray-700 p-2 rounded flex justify-between items-center group hover:bg-gray-600 transition">
                        <div>
                          <div className="text-white text-sm">{f.name} <span className="text-xs text-gray-400">({f.serving_size})</span></div>
                          <div className="text-xs text-yellow-300">{f.carbohydrates}g carbs • {f.calories} kcal</div>
                        </div>
                        <button onClick={() => handleLogFood(f)} className="text-blue-400 opacity-0 group-hover:opacity-100 px-2 py-1 bg-gray-800 rounded text-xs transition">+</button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Veggies */}
              {veggies.length > 0 && (
                <div>
                  <h4 className="text-green-400 font-bold text-sm mb-2">Vegetables & Fibers</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {veggies.map(f => (
                      <div key={f.id} className="bg-gray-700 p-2 rounded flex justify-between items-center group hover:bg-gray-600 transition">
                        <div>
                          <div className="text-white text-sm">{f.name} <span className="text-xs text-gray-400">({f.serving_size})</span></div>
                          <div className="text-xs text-green-300">{f.fiber}g fiber • {f.calories} kcal</div>
                        </div>
                        <button onClick={() => handleLogFood(f)} className="text-blue-400 opacity-0 group-hover:opacity-100 px-2 py-1 bg-gray-800 rounded text-xs transition">+</button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
