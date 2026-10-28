import React, { useState, useEffect } from 'react';
import api from '../services/api';

interface ProfileData {
  gender?: string;
  height?: number;
  weight?: number;
  fitness_level?: string;
  fitness_goal?: string;
  workout_frequency?: string;
  preferred_training_type?: string;
  calisthenics_skill_goals?: string;
  available_workout_time?: string;
  nutrition_goal?: string;
  food_preferences?: string;
  dietary_preferences?: string;
  allergies?: string;
  water_target?: number;
  available_free_time?: string;
  habit_preferences?: string;
  wake_up_time?: string;
  sleep_time?: string;
  career_status?: string;
  career_goal?: string;
  target_career?: string;
  available_learning_time?: string;
  preferred_learning_style?: string;
  recommendation_frequency?: string;
  daily_plan_generation?: boolean;
  fitness_reminders?: boolean;
  nutrition_reminders?: boolean;
  habit_reminders?: boolean;
  career_reminders?: boolean;
}

export const Profile: React.FC = () => {
  const [activeTab, setActiveTab] = useState('personal');
  const [profile, setProfile] = useState<ProfileData>({});
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/api/profile/');
        setProfile(res.data);
      } catch (err: any) {
        if (err.response && err.response.status === 404) {
          setProfile({}); // Start with empty profile for new users
        } else {
          console.error("Failed to load profile", err);
        }
      }
    };
    fetchProfile();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;
    setProfile({ ...profile, [name]: val });
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');
    try {
      await api.put('/api/profile/', profile);
      setMessage('Profile updated successfully.');
    } catch (err) {
      setMessage('Unable to update your profile. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const tabs = [
    { id: 'personal', label: '👤 Personal' },
    { id: 'fitness', label: '🏃 Fitness' },
    { id: 'nutrition', label: '🍎 Nutrition' },
    { id: 'lifestyle', label: '😴 Lifestyle' },
    { id: 'career', label: '💼 Career' },
    { id: 'ai', label: '⚙️ AI Preferences' }
  ];

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white dark:bg-gray-900 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">My LifeSync Preferences</h1>
      
      {message && (
        <div className={`p-4 mb-6 rounded ${message.includes('success') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {message}
        </div>
      )}

      <div className="flex space-x-2 border-b border-gray-200 dark:border-gray-700 mb-6 overflow-x-auto">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`py-2 px-4 whitespace-nowrap focus:outline-none ${activeTab === t.id ? 'border-b-2 border-purple-500 text-purple-600 font-medium' : 'text-gray-500 hover:text-gray-700'}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="space-y-6">
        {activeTab === 'personal' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Height (cm)</label>
              <input type="text" inputMode="numeric" name="height" value={profile.height || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Weight (kg)</label>
              <input type="text" inputMode="numeric" name="weight" value={profile.weight || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" />
            </div>
          </div>
        )}

        {activeTab === 'fitness' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Fitness Level</label>
              <select name="fitness_level" value={profile.fitness_level || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700">
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Fitness Goal</label>
              <select name="fitness_goal" value={profile.fitness_goal || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700">
                <option value="General Fitness">General Fitness</option>
                <option value="Strength">Strength</option>
                <option value="Muscle Building">Muscle Building</option>
                <option value="Fat Loss">Fat Loss</option>
                <option value="Calisthenics Skills">Calisthenics Skills</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Available Time (mins)</label>
              <input type="text" inputMode="numeric" name="available_workout_time" value={profile.available_workout_time || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" />
            </div>
          </div>
        )}

        {activeTab === 'nutrition' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Nutrition Goal</label>
              <select name="nutrition_goal" value={profile.nutrition_goal || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700">
                <option value="">Select goal...</option>
                <option value="Shed Body Fat (Cut)">Shed Body Fat (Cut)</option>
                <option value="Build Lean Muscle (Bulk)">Build Lean Muscle (Bulk)</option>
                <option value="Recomposition (Build & Lose)">Recomposition (Build & Lose)</option>
                <option value="Maintenance & Longevity">Maintenance & Longevity</option>
                <option value="Athletic Performance">Athletic Performance</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Dietary Preferences</label>
              <select name="dietary_preferences" value={profile.dietary_preferences || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700">
                <option value="">Select diet...</option>
                <option value="Anything Goes (Omnivore)">Anything Goes (Omnivore)</option>
                <option value="Plant-powered (Vegan)">Plant-powered (Vegan)</option>
                <option value="Vegetarian (No meat)">Vegetarian (No meat)</option>
                <option value="Keto / Low-Carb">Keto / Low-Carb</option>
                <option value="Paleo / Whole Foods">Paleo / Whole Foods</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Specific Food Preferences</label>
              <input type="text" name="food_preferences" value={profile.food_preferences || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" placeholder="e.g., Spicy foods, More avocados..." />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Allergies & Intolerances</label>
              <input type="text" name="allergies" value={profile.allergies || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" placeholder="e.g., Peanuts, Dairy, Gluten..." />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Daily Water Target (ml)</label>
              <input type="text" inputMode="numeric" name="water_target" value={profile.water_target || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" placeholder="e.g., 2500" />
            </div>
          </div>
        )}

        {activeTab === 'lifestyle' && (
          <div className="grid grid-cols-1 gap-4">
             <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Available Free Time</label>
              <input type="text" name="available_free_time" value={profile.available_free_time || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" />
            </div>
          </div>
        )}

        {activeTab === 'career' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Career Goal</label>
              <input type="text" name="career_goal" value={profile.career_goal || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Available Learning Time (mins)</label>
              <input type="text" inputMode="numeric" name="available_learning_time" value={profile.available_learning_time || ''} onChange={handleChange} className="mt-1 w-full p-2 border rounded dark:bg-gray-800 dark:border-gray-700" />
            </div>
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="space-y-4">
            <div className="flex items-center">
              <input type="checkbox" name="daily_plan_generation" checked={profile.daily_plan_generation !== false} onChange={handleChange} className="mr-2" />
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Enable Daily Plan Generation</label>
            </div>
          </div>
        )}

        <div className="pt-6 border-t border-gray-200 dark:border-gray-700 flex space-x-4">
          <button
            onClick={handleSave}
            disabled={saving}
            className="px-6 py-2 bg-purple-600 text-white rounded font-medium hover:bg-purple-700 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>
    </div>
  );
};
