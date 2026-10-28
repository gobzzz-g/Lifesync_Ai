import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export function Gamification() {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/api/profile');
        setProfile(res.data);
      } catch (e) {
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  if (loading) return <div className="p-8 text-white">Loading Gamification...</div>;

  const xp = profile?.xp || 0;
  const level = Math.floor(xp / 100) + 1;
  const xpToNext = 100 - (xp % 100);
  const progressPercent = (xp % 100);

  const getLevelTitle = (lvl: number) => {
    if (lvl < 5) return "Beginner";
    if (lvl < 10) return "Consistency Builder";
    if (lvl < 20) return "Growth Seeker";
    if (lvl < 50) return "LifeSync Master";
    return "Optimization Expert";
  };

  let unlockedAchievements: string[] = [];
  try {
    if (profile?.achievements) {
      unlockedAchievements = JSON.parse(profile.achievements);
    }
  } catch (e) {
    unlockedAchievements = [];
  }
  
  const allAchievements = [
    { id: 'first_step', title: 'First Step', desc: 'Complete your first LifeSync activity.' },
    { id: 'fitness_starter', title: 'Fitness Starter', desc: 'Complete first workout.' },
    { id: 'career_builder', title: 'Career Builder', desc: 'Complete first career roadmap task.' },
    { id: 'interview_ready', title: 'Interview Ready', desc: 'Complete first mock interview.' },
    { id: 'consistency_master', title: 'Consistency Master', desc: 'Maintain a 14-day streak.' }
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-yellow-500">Gamification & XP</h1>
          <button onClick={() => navigate('/dashboard')} className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded transition">
            Back to Dashboard
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          <div className="lg:col-span-2 space-y-8">
            <div className="bg-gray-800 p-8 rounded-lg border border-gray-700 text-center">
              <h2 className="text-2xl font-bold text-gray-400 mb-2">{getLevelTitle(level)}</h2>
              <div className="text-6xl font-black text-yellow-400 mb-6">Level {level}</div>
              
              <div className="max-w-md mx-auto">
                <div className="flex justify-between text-sm text-gray-400 mb-2">
                  <span>{xp} XP</span>
                  <span>{xp + xpToNext} XP</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-4 mb-2">
                  <div className="bg-yellow-400 h-4 rounded-full" style={{ width: `${progressPercent}%` }}></div>
                </div>
                <p className="text-sm text-gray-400">{xpToNext} XP to next level</p>
              </div>
            </div>

            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-xl font-bold mb-4">Achievements</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {allAchievements.map(a => {
                  const unlocked = unlockedAchievements.includes(a.id) || xp > 20; // fallback mock unlocking
                  return (
                    <div key={a.id} className={`p-4 rounded border ${unlocked ? 'border-yellow-500/50 bg-yellow-500/10' : 'border-gray-700 bg-gray-800 opacity-50'}`}>
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{unlocked ? '🏆' : '🔒'}</span>
                        <div>
                          <h3 className={`font-bold ${unlocked ? 'text-yellow-400' : 'text-gray-500'}`}>{a.title}</h3>
                          <p className="text-xs text-gray-400 mt-1">{a.desc}</p>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 text-center">
              <h2 className="text-xl font-bold mb-4">Streaks</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-4xl mb-2">🔥</div>
                  <div className="text-3xl font-bold text-orange-500">{profile?.streak_days || 0}</div>
                  <div className="text-sm text-gray-400 mt-1">Current Streak</div>
                </div>
                <div>
                  <div className="text-4xl mb-2">⭐</div>
                  <div className="text-3xl font-bold text-yellow-500">{profile?.best_streak || 0}</div>
                  <div className="text-sm text-gray-400 mt-1">Best Streak</div>
                </div>
              </div>
            </div>

            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-xl font-bold mb-4">XP History</h2>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between border-b border-gray-700 pb-2">
                  <span className="text-gray-300">Workout completed</span>
                  <span className="text-green-400 font-bold">+50 XP</span>
                </div>
                <div className="flex justify-between border-b border-gray-700 pb-2">
                  <span className="text-gray-300">Career task completed</span>
                  <span className="text-green-400 font-bold">+20 XP</span>
                </div>
                <div className="flex justify-between pb-2">
                  <span className="text-gray-300">Daily check-in</span>
                  <span className="text-green-400 font-bold">+10 XP</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
