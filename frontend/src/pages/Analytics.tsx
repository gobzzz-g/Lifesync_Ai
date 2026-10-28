import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  BarChart, Bar, Legend,
  PieChart, Pie, Cell
} from 'recharts';

export function Analytics() {
  const [loading, setLoading] = useState(true);
  const [lifeState, setLifeState] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/api/life/state');
        setLifeState(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Use real data to slightly bump the mock data for current day
  const baseScore = lifeState?.overall_score || 70;
  
  // 1. Line Chart Data (Trend)
  const trendData = [
    { day: 'Mon', growth: 60, fitness: 65, career: 50 },
    { day: 'Tue', growth: 62, fitness: 68, career: 55 },
    { day: 'Wed', growth: 65, fitness: 70, career: 58 },
    { day: 'Thu', growth: 64, fitness: 65, career: 60 },
    { day: 'Fri', growth: 68, fitness: 75, career: 65 },
    { day: 'Sat', growth: 71, fitness: 80, career: 70 },
    { day: 'Sun', growth: baseScore, fitness: lifeState?.fitness_score || 82, career: lifeState?.career_score || 75 }
  ];

  // 2. Radar Chart Data (Life Balance)
  const radarData = [
    { subject: 'Fitness', A: lifeState?.fitness_score || 85, fullMark: 100 },
    { subject: 'Nutrition', A: lifeState?.nutrition_score || 75, fullMark: 100 },
    { subject: 'Career', A: lifeState?.career_score || 60, fullMark: 100 },
    { subject: 'Lifestyle', A: lifeState?.lifestyle_score || 70, fullMark: 100 },
    { subject: 'Mental', A: 80, fullMark: 100 },
  ];

  // 3. Bar Chart Data (Macro Adherence for the week)
  const macroData = [
    { name: 'Mon', Protein: 90, Carbs: 110, Fats: 80 },
    { name: 'Tue', Protein: 100, Carbs: 105, Fats: 90 },
    { name: 'Wed', Protein: 95, Carbs: 90, Fats: 85 },
    { name: 'Thu', Protein: 105, Carbs: 100, Fats: 95 },
    { name: 'Fri', Protein: 110, Carbs: 115, Fats: 100 },
    { name: 'Sat', Protein: 90, Carbs: 85, Fats: 75 },
    { name: 'Sun', Protein: 100, Carbs: 100, Fats: 100 },
  ];

  // 4. Pie Chart Data (Task Completion)
  const pieData = [
    { name: 'Completed', value: 12 },
    { name: 'Pending', value: 5 },
    { name: 'Overdue', value: 2 },
  ];
  const COLORS = ['#10B981', '#3B82F6', '#EF4444'];

  if (loading) return <div className="p-8 text-white flex justify-center items-center h-screen">Loading Analytics Module...</div>;

  return (
    <div className="min-h-screen bg-gray-950 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-extrabold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">Analytics & Progress</h1>
            <p className="text-gray-400 text-sm mt-1">Your LifeSync data visualized.</p>
          </div>
          <button onClick={() => navigate('/dashboard')} className="bg-gray-800 hover:bg-gray-700 border border-gray-700 px-4 py-2 rounded-lg transition shadow-lg">
            Back to Dashboard
          </button>
        </header>

        {/* AI Insight Banner */}
        <div className="bg-gradient-to-r from-indigo-900/40 to-blue-900/40 border border-indigo-500/30 p-5 rounded-xl flex items-start gap-4">
          <div className="text-3xl">🤖</div>
          <div>
            <h3 className="text-indigo-300 font-bold mb-1">AI Data Insight</h3>
            <p className="text-gray-300 text-sm leading-relaxed">
              Your overall growth improved by 6% this week. Your strongest domain is currently <strong>Fitness</strong>, while <strong>Career</strong> is trailing slightly behind. You've maintained excellent protein adherence (averaging 98% of target), which correlates strongly with your muscle gain goal. Focus on completing your 5 pending tasks to boost your Career score.
            </p>
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* 1. Growth Trend */}
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl">
            <h2 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">📈 Overall Growth Trend</h2>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                  <XAxis dataKey="day" stroke="#6B7280" tick={{fontSize: 12}} />
                  <YAxis stroke="#6B7280" tick={{fontSize: 12}} domain={['dataMin - 10', 'dataMax + 10']} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                    itemStyle={{ fontSize: '14px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                  <Line type="monotone" dataKey="growth" name="Overall Growth" stroke="#8B5CF6" strokeWidth={3} dot={{r: 4}} activeDot={{r: 6}} />
                  <Line type="monotone" dataKey="fitness" name="Fitness" stroke="#10B981" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="career" name="Career" stroke="#F59E0B" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* 2. Life Balance Radar */}
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl">
            <h2 className="text-lg font-bold text-gray-200 mb-2 flex items-center gap-2">🕸️ Life Balance Profile</h2>
            <p className="text-xs text-gray-500 mb-4">Your equilibrium across the 5 core domains.</p>
            <div className="h-64 w-full flex justify-center items-center">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                  <PolarGrid stroke="#374151" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <Radar name="Balance" dataKey="A" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.4} />
                  <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* 3. Macro Adherence */}
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl">
            <h2 className="text-lg font-bold text-gray-200 mb-2 flex items-center gap-2">📊 Macro Adherence</h2>
            <p className="text-xs text-gray-500 mb-6">% of daily target hit for Protein, Carbs, and Fats.</p>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={macroData} margin={{ top: 5, right: 20, bottom: 5, left: -20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                  <XAxis dataKey="name" stroke="#6B7280" tick={{fontSize: 12}} />
                  <YAxis stroke="#6B7280" tick={{fontSize: 12}} />
                  <Tooltip 
                    cursor={{fill: '#1F2937'}}
                    contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                  <Bar dataKey="Protein" stackId="a" fill="#10B981" radius={[0, 0, 4, 4]} />
                  <Bar dataKey="Carbs" stackId="a" fill="#F59E0B" />
                  <Bar dataKey="Fats" stackId="a" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* 4. Task Productivity Pie */}
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl">
            <h2 className="text-lg font-bold text-gray-200 mb-2 flex items-center gap-2">🎯 Task Productivity</h2>
            <p className="text-xs text-gray-500 mb-6">Distribution of your weekly tasks.</p>
            <div className="h-64 w-full flex justify-center items-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                  >
                    {pieData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                    itemStyle={{ color: '#E5E7EB' }}
                  />
                  <Legend 
                    layout="vertical" 
                    verticalAlign="middle" 
                    align="right"
                    wrapperStyle={{ fontSize: '12px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
