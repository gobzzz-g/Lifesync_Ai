import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export function CareerDashboard() {
  const [gapAnalysis, setGapAnalysis] = useState<any>(null);
  const [roadmap, setRoadmap] = useState<any>(null);
  const [interviews, setInterviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [skillInput, setSkillInput] = useState('');
  const [resumeResult, setResumeResult] = useState<any>(null);
  const [interviewState, setInterviewState] = useState<any>(null);
  const [interviewAnswer, setInterviewAnswer] = useState('');
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const [interviewsRes] = await Promise.all([
        api.get('/api/career/interviews')
      ]);
      setInterviews(interviewsRes.data);
      
      try {
        const gapRes = await api.post('/api/career/analyze-gap');
        setGapAnalysis(gapRes.data);
      } catch(e) {}
      
      try {
        const roadRes = await api.get('/api/career/roadmap');
        setRoadmap(roadRes.data);
      } catch(e) {}
      
    } catch (e) {
      console.error("Failed to fetch career data", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddSkill = async () => {
    if (!skillInput.trim()) return;
    try {
      await api.post('/api/career/skills', { name: skillInput, proficiency_level: 'Beginner' });
      setSkillInput('');
      fetchData();
    } catch (e) {}
  };

  const handleGenerateRoadmap = async () => {
    try {
      await api.post('/api/career/roadmap/generate');
      fetchData();
    } catch(e) {}
  };

  const handleCompleteTask = async (taskId: number) => {
    try {
      await api.put(`/api/career/tasks/${taskId}/complete`);
      fetchData();
    } catch(e) {}
  };

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await api.post('/api/career/resume/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResumeResult(res.data);
    } catch (e) {
      alert("Failed to analyze resume. Ensure it is a PDF or DOCX.");
    }
  };

  const handleStartInterview = async () => {
    try {
      const res = await api.post('/api/career/interview/start', { role: 'Full Stack Developer', interview_type: 'Technical' });
      setInterviewState(res.data);
    } catch (e) {}
  };

  const handleSubmitAnswer = async () => {
    if (!interviewAnswer.trim() || !interviewState) return;
    try {
      const res = await api.post(`/api/career/interview/${interviewState.id}/answer`, { answer: interviewAnswer });
      setInterviewState({ ...interviewState, feedback: res.data });
    } catch(e) {}
  };

  const resetInterview = () => {
    setInterviewState(null);
    setInterviewAnswer('');
    fetchData();
  };

  if (loading) return <div className="p-8 text-white">Loading Career Coach...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-orange-400">AI Career Coach</h1>
          <button onClick={() => navigate('/dashboard')} className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded transition">
            Back to Dashboard
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Roadmap */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Your Learning Roadmap</h2>
                <button onClick={handleGenerateRoadmap} className="text-sm bg-orange-600 hover:bg-orange-500 px-3 py-1 rounded">Generate New</button>
              </div>
              
              {!roadmap ? (
                <p className="text-gray-400">No roadmap generated yet. Ensure you have skills logged and click Generate.</p>
              ) : (
                <div className="space-y-4">
                  {roadmap.tasks.map((task: any) => (
                    <div key={task.id} className="bg-gray-700 p-4 rounded flex justify-between items-center">
                      <div>
                        <h3 className="font-bold text-orange-300">{task.title}</h3>
                        <p className="text-sm text-gray-300 mt-1">Estimated Time: {task.estimated_minutes} mins</p>
                      </div>
                      {task.is_completed ? (
                        <span className="text-green-400 font-bold">✓ Completed</span>
                      ) : (
                        <button onClick={() => handleCompleteTask(task.id)} className="bg-green-600 hover:bg-green-500 px-4 py-2 rounded text-sm transition">
                          Mark Complete (+20 XP)
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Mock Interview */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-xl font-bold mb-4">Mock Interview</h2>
              {!interviewState ? (
                <div>
                  <p className="text-gray-300 mb-4">Practice your technical and behavioral skills with AI.</p>
                  <button onClick={handleStartInterview} className="bg-orange-600 hover:bg-orange-500 px-6 py-2 rounded font-bold">Start Session</button>
                  
                  <div className="mt-6">
                    <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-2">History</h3>
                    {interviews.slice(0, 3).map(i => (
                      <div key={i.id} className="flex justify-between items-center text-sm py-2 border-b border-gray-700">
                        <span>{i.role} ({i.interview_type})</span>
                        <span className="text-orange-400">{i.score}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="bg-gray-900 p-4 rounded border border-orange-500/30">
                    <p className="font-bold text-orange-300 mb-2">Q: {interviewState.question}</p>
                    
                    {!interviewState.feedback ? (
                      <>
                        <textarea 
                          className="w-full bg-gray-800 border border-gray-700 rounded p-3 text-white h-32 mt-2" 
                          placeholder="Type your answer here..."
                          value={interviewAnswer}
                          onChange={e => setInterviewAnswer(e.target.value)}
                        />
                        <button onClick={handleSubmitAnswer} className="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded font-bold mt-2">Submit Answer</button>
                      </>
                    ) : (
                      <div className="mt-4 pt-4 border-t border-gray-700">
                        <div className="flex items-center gap-4 mb-2">
                          <h4 className="font-bold text-xl">Score: <span className={interviewState.feedback.score > 70 ? 'text-green-400' : 'text-orange-400'}>{interviewState.feedback.score}%</span></h4>
                          <span className="text-sm bg-green-900/50 text-green-300 px-2 rounded">+50 XP</span>
                        </div>
                        <p className="text-sm text-gray-300 italic mb-4">"{interviewState.feedback.feedback}"</p>
                        
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <h5 className="font-bold text-green-400">Strengths</h5>
                            <ul className="list-disc pl-4 text-gray-400 mt-1">
                              {interviewState.feedback.strong_areas.map((a:string, i:number) => <li key={i}>{a}</li>)}
                            </ul>
                          </div>
                          <div>
                            <h5 className="font-bold text-red-400">Weaknesses</h5>
                            <ul className="list-disc pl-4 text-gray-400 mt-1">
                              {interviewState.feedback.weak_areas.map((a:string, i:number) => <li key={i}>{a}</li>)}
                            </ul>
                          </div>
                        </div>
                        <button onClick={resetInterview} className="bg-gray-700 hover:bg-gray-600 px-6 py-2 rounded mt-4">Done</button>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
            
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            
            {/* Skill Gap Analysis */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-xl font-bold mb-4">Skill Gap Analysis</h2>
              
              <div className="flex items-center gap-4 mb-6">
                <div className="w-16 h-16 rounded-full border-4 border-orange-500 flex items-center justify-center text-xl font-bold">
                  {gapAnalysis?.readiness_score || 0}%
                </div>
                <div>
                  <h3 className="font-bold">Career Readiness</h3>
                  <p className="text-xs text-gray-400">Based on Full Stack Developer</p>
                </div>
              </div>

              {gapAnalysis && (
                <div className="space-y-4 text-sm">
                  <div>
                    <h4 className="text-green-400 font-bold mb-1">Strong Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {gapAnalysis.strong_skills.map((s:string) => <span key={s} className="bg-green-900/30 text-green-300 px-2 py-1 rounded">{s}</span>)}
                      {gapAnalysis.strong_skills.length === 0 && <span className="text-gray-500">None logged</span>}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-yellow-400 font-bold mb-1">Improving</h4>
                    <div className="flex flex-wrap gap-2">
                      {gapAnalysis.improving_skills.map((s:string) => <span key={s} className="bg-yellow-900/30 text-yellow-300 px-2 py-1 rounded">{s}</span>)}
                      {gapAnalysis.improving_skills.length === 0 && <span className="text-gray-500">None</span>}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-red-400 font-bold mb-1">Missing Priority</h4>
                    <div className="flex flex-wrap gap-2">
                      {gapAnalysis.priority_skills.map((s:string) => <span key={s} className="bg-red-900/30 text-red-300 px-2 py-1 rounded">{s}</span>)}
                    </div>
                  </div>
                </div>
              )}
              
              <div className="mt-6 pt-4 border-t border-gray-700">
                <h4 className="text-sm font-bold mb-2">Log a New Skill</h4>
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    placeholder="e.g. React" 
                    className="flex-1 bg-gray-900 border border-gray-600 rounded px-2"
                    value={skillInput}
                    onChange={e => setSkillInput(e.target.value)}
                  />
                  <button onClick={handleAddSkill} className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded">+</button>
                </div>
              </div>
            </div>

            {/* Resume Analyzer */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-xl font-bold mb-4">Resume Analyzer</h2>
              
              {!resumeResult ? (
                <div className="text-center py-6 border-2 border-dashed border-gray-600 rounded-lg">
                  <p className="text-gray-400 mb-4 text-sm">Upload PDF or DOCX for AI analysis.</p>
                  <input 
                    type="file" 
                    accept=".pdf,.docx"
                    className="hidden" 
                    ref={fileInputRef}
                    onChange={handleResumeUpload}
                  />
                  <button 
                    onClick={() => fileInputRef.current?.click()}
                    className="bg-blue-600 hover:bg-blue-500 px-4 py-2 text-sm rounded transition"
                  >
                    Select File
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="text-3xl font-bold text-blue-400">{resumeResult.score}/100</div>
                    <p className="text-sm text-gray-400">Resume Strength Score</p>
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-green-400">Strengths</h4>
                    <ul className="list-disc pl-4 text-gray-300 text-xs mt-1">
                      {resumeResult.strengths.map((s:string, i:number) => <li key={i}>{s}</li>)}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-orange-400">Suggestions</h4>
                    <ul className="list-disc pl-4 text-gray-300 text-xs mt-1">
                      {resumeResult.improvement_suggestions.map((s:string, i:number) => <li key={i}>{s}</li>)}
                    </ul>
                  </div>
                  <button onClick={() => setResumeResult(null)} className="w-full bg-gray-700 hover:bg-gray-600 py-2 rounded text-sm mt-2">Clear</button>
                </div>
              )}
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}
