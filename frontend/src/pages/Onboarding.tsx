import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export function Onboarding() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleNext = () => setStep(step + 1);
  const handleBack = () => setStep(step - 1);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await api.post('/api/profile/onboarding', formData);
      navigate('/dashboard');
    } catch (error) {
      console.error('Onboarding failed', error);
      alert('Failed to save profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-2xl">
        <h1 className="text-2xl font-bold text-blue-400 mb-6 text-center">LifeSync AI Onboarding</h1>
        <div className="mb-8 text-sm text-gray-400 text-center">Step {step} of 6</div>

        {step === 1 && (
          <div className="space-y-4 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4">Basic Information</h2>
            <div>
              <label className="block mb-1">Height (cm)</label>
              <input type="text" inputMode="numeric" name="height" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.height || ''} />
            </div>
            <div>
              <label className="block mb-1">Weight (kg)</label>
              <input type="text" inputMode="numeric" name="weight" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.weight || ''} />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4">Fitness Profile</h2>
            <div>
              <label className="block mb-1">Fitness Level</label>
              <select name="fitness_level" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.fitness_level || ''}>
                <option value="">Select level...</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="block mb-1">Fitness Goal</label>
              <select name="fitness_goal" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.fitness_goal || ''}>
                <option value="">Select goal...</option>
                <option value="Build Strength">Build Strength</option>
                <option value="Fat Loss">Fat Loss</option>
                <option value="Calisthenics Skills">Calisthenics Skills</option>
              </select>
            </div>
            <div>
              <label className="block mb-1">Available Workout Time (mins)</label>
              <input type="text" inputMode="numeric" name="available_workout_time" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.available_workout_time || ''} />
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4">Nutrition Profile</h2>
            <div>
              <label className="block mb-1">Dietary Preference</label>
              <select name="dietary_preferences" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.dietary_preferences || ''}>
                <option value="">Select preference...</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Vegan">Vegan</option>
                <option value="Non-vegetarian">Non-vegetarian</option>
              </select>
            </div>
            <div>
              <label className="block mb-1">Meals Per Day</label>
              <input type="text" inputMode="numeric" name="meals_per_day" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.meals_per_day || ''} />
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-4 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4">Lifestyle Profile</h2>
            <div>
              <label className="block mb-1">Average Sleep Duration (hours)</label>
              <input type="text" inputMode="numeric" name="sleep_duration" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.sleep_duration || ''} />
            </div>
            <div>
              <label className="block mb-1">Daily Work/Study (hours)</label>
              <input type="text" inputMode="numeric" name="daily_work_hours" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.daily_work_hours || ''} />
            </div>
          </div>
        )}

        {step === 5 && (
          <div className="space-y-4 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4">Well-being Profile (1-10)</h2>
            <div>
              <label className="block mb-1">Average Stress Level</label>
              <input type="text" inputMode="numeric" min="1" max="10" name="stress_level" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.stress_level || ''} />
            </div>
            <div>
              <label className="block mb-1">Energy Level</label>
              <input type="text" inputMode="numeric" min="1" max="10" name="energy_level" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.energy_level || ''} />
            </div>
          </div>
        )}

        {step === 6 && (
          <div className="space-y-4 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4">Career Profile</h2>
            <div>
              <label className="block mb-1">Career Status</label>
              <select name="career_status" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.career_status || ''}>
                <option value="">Select status...</option>
                <option value="Student">Student</option>
                <option value="Working">Working</option>
                <option value="Job seeker">Job seeker</option>
              </select>
            </div>
            <div>
              <label className="block mb-1">Target Career</label>
              <input type="text" name="target_career" placeholder="e.g. Full Stack Developer" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.target_career || ''} />
            </div>
            <div>
              <label className="block mb-1">Experience Level</label>
              <select name="career_experience_level" className="w-full bg-gray-700 p-2 rounded" onChange={handleChange} value={formData.career_experience_level || ''}>
                <option value="">Select level...</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>
          </div>
        )}

        <div className="mt-8 flex justify-between">
          {step > 1 ? (
            <button onClick={handleBack} className="bg-gray-600 hover:bg-gray-500 px-4 py-2 rounded transition">Back</button>
          ) : <div></div>}
          
          {step < 6 ? (
            <button onClick={handleNext} className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded transition">Next Step</button>
          ) : (
            <button onClick={handleSubmit} disabled={loading} className="bg-green-600 hover:bg-green-500 px-4 py-2 rounded transition font-bold">
              {loading ? 'Generating Profile...' : 'Complete Setup'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
