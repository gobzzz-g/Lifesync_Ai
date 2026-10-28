import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../services/api';

export function WorkoutExecution() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const workout = state?.workout;

  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentSet, setCurrentSet] = useState(1);
  const [isResting, setIsResting] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const [feedback, setFeedback] = useState({
    user_rating: 5,
    energy_before: 5,
    energy_after: 5,
    notes: ''
  });

  useEffect(() => {
    if (!workout) navigate('/fitness');
  }, [workout, navigate]);

  useEffect(() => {
    let timer: any;
    if (isResting && timeLeft > 0) {
      timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
    } else if (isResting && timeLeft === 0) {
      setIsResting(false);
      
      const currentEx = workout.exercises[currentIndex];
      if (currentSet < currentEx.sets) {
        setCurrentSet(s => s + 1);
      } else {
        if (currentIndex < workout.exercises.length - 1) {
          setCurrentIndex(i => i + 1);
          setCurrentSet(1);
        } else {
          setIsComplete(true);
        }
      }
    }
    return () => clearInterval(timer);
  }, [isResting, timeLeft, currentIndex, currentSet, workout]);

  if (!workout) return null;

  const handleCompleteSet = () => {
    const currentEx = workout.exercises[currentIndex];
    if (currentIndex === workout.exercises.length - 1 && currentSet === currentEx.sets) {
      setIsComplete(true);
    } else {
      setTimeLeft(currentEx.rest_time);
      setIsResting(true);
    }
  };

  const handleSkip = () => {
    if (currentIndex < workout.exercises.length - 1) {
      setCurrentIndex(i => i + 1);
      setCurrentSet(1);
      setIsResting(false);
    } else {
      setIsComplete(true);
    }
  };

  const submitCompletion = async () => {
    try {
      await api.post(`/api/fitness/workout/${workout.id}/complete`, {
        ...feedback,
        completion_percentage: 100,
        actual_duration: workout.duration
      });
      navigate('/fitness');
    } catch (e) {
      alert("Failed to save workout");
    }
  };

  if (isComplete) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center p-4">
        <div className="bg-gray-800 p-8 rounded-2xl shadow-2xl max-w-lg w-full text-center border border-gray-700">
          <h1 className="text-5xl mb-4">🎉</h1>
          <h2 className="text-3xl font-bold text-green-400 mb-2">Workout Complete!</h2>
          <p className="text-gray-400 mb-8">+50 XP Awarded</p>
          
          <div className="space-y-6 text-left">
            <div className="bg-gray-700/50 p-4 rounded-xl border border-gray-600">
              <label className="block mb-2 text-sm font-semibold text-gray-200">How difficult was this workout? (1-10)</label>
              <input type="range" min="1" max="10" value={feedback.user_rating} onChange={(e) => setFeedback({...feedback, user_rating: +e.target.value})} className="w-full accent-green-500" />
              <div className="text-center font-bold text-green-400 mt-2">{feedback.user_rating}/10</div>
            </div>
            <div className="bg-gray-700/50 p-4 rounded-xl border border-gray-600">
              <label className="block mb-2 text-sm font-semibold text-gray-200">Energy Level After (1-10)</label>
              <input type="range" min="1" max="10" value={feedback.energy_after} onChange={(e) => setFeedback({...feedback, energy_after: +e.target.value})} className="w-full accent-blue-500" />
              <div className="text-center font-bold text-blue-400 mt-2">{feedback.energy_after}/10</div>
            </div>
            <div>
              <label className="block mb-2 text-sm font-semibold text-gray-200">Notes & Reflections</label>
              <textarea 
                value={feedback.notes} 
                onChange={(e) => setFeedback({...feedback, notes: e.target.value})}
                className="w-full bg-gray-700 border border-gray-600 rounded-xl p-3 text-white focus:outline-none focus:border-green-500" 
                rows={3}
                placeholder="Felt great today! Push-ups felt easier."
              />
            </div>
          </div>

          <button onClick={submitCompletion} className="mt-8 bg-green-600 hover:bg-green-500 text-white font-bold py-4 px-8 rounded-xl transition w-full shadow-lg shadow-green-900/50 tracking-wide">
            SAVE & RETURN TO DASHBOARD
          </button>
        </div>
      </div>
    );
  }

  const currentEx = workout.exercises[currentIndex];

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8 flex flex-col">
      <header className="flex justify-between items-center mb-6">
        <button onClick={() => navigate('/fitness')} className="text-gray-400 hover:text-white font-medium">← Quit Workout</button>
        <span className="bg-gray-800 px-4 py-1 rounded-full text-sm font-bold text-green-400 border border-gray-700">
          Exercise {currentIndex + 1} of {workout.exercises.length}
        </span>
      </header>

      <div className="flex-1 flex flex-col lg:flex-row gap-8 max-w-6xl mx-auto w-full items-start">
        
        {/* Left Side: Execution & Timer */}
        <div className="w-full lg:w-1/2 flex flex-col items-center justify-center">
          {isResting ? (
            <div className="text-center w-full bg-gray-800 p-12 rounded-3xl border border-blue-900/30 shadow-2xl">
              <h2 className="text-3xl font-bold text-blue-400 mb-4 uppercase tracking-widest">Rest & Recover</h2>
              <div className="text-8xl font-bold text-white mb-8 drop-shadow-lg">{timeLeft}s</div>
              <p className="text-gray-400 mb-8 font-medium">
                Next up: {currentIndex < workout.exercises.length - 1 && currentSet === currentEx.sets ? workout.exercises[currentIndex+1].exercise.name : currentEx.exercise.name}
              </p>
              <button onClick={() => setTimeLeft(0)} className="bg-gray-700 hover:bg-gray-600 px-8 py-3 rounded-xl text-sm font-bold text-white transition">SKIP REST</button>
            </div>
          ) : (
            <div className="bg-gray-800 p-8 rounded-3xl shadow-2xl w-full border border-gray-700 text-center">
              <h2 className="text-4xl font-bold text-white mb-2">{currentEx.exercise.name}</h2>
              <p className="text-green-400 font-semibold uppercase tracking-wider mb-8">{currentEx.exercise.muscle_groups}</p>
              
              <div className="text-7xl font-black text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-600 mb-4 drop-shadow-sm">
                {currentEx.reps} <span className="text-3xl text-gray-500 font-bold uppercase">{currentEx.duration ? 'sec' : 'reps'}</span>
              </div>
              <div className="text-xl font-medium text-gray-400 mb-12">
                Set {currentSet} of {currentEx.sets}
              </div>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button onClick={handleSkip} className="bg-gray-700 hover:bg-gray-600 px-8 py-4 rounded-xl font-bold text-white transition">SKIP</button>
                <button onClick={handleCompleteSet} className="bg-green-600 hover:bg-green-500 px-10 py-4 rounded-xl font-bold text-white shadow-lg shadow-green-900/50 transition">COMPLETE SET</button>
              </div>
            </div>
          )}
        </div>

        {/* Right Side: AI Form Guidance */}
        <div className="w-full lg:w-1/2 space-y-6">
          <div className="bg-gray-800 p-6 rounded-3xl shadow-xl border border-gray-700">
            <div className="flex items-center gap-2 mb-6 border-b border-gray-700 pb-4">
              <span className="text-2xl">🤖</span>
              <h2 className="text-xl font-bold text-blue-400 uppercase tracking-widest">AI Form Guidance</h2>
            </div>
            
            <div className="space-y-6 text-sm text-gray-300">
              
              <div>
                <h3 className="text-white font-bold text-base mb-1">1. Starting Position</h3>
                <p className="bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">{currentEx.exercise.form_setup || currentEx.exercise.instructions || "Start in a neutral, balanced position."}</p>
              </div>

              <div>
                <h3 className="text-white font-bold text-base mb-1">2. Movement</h3>
                <p className="bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">{currentEx.exercise.form_movement || "Perform the movement with control."}</p>
              </div>

              <div>
                <h3 className="text-white font-bold text-base mb-1">3. Breathing</h3>
                <p className="bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">{currentEx.exercise.form_breathing || "Inhale during the eccentric phase, exhale on exertion."}</p>
              </div>
              
              {currentEx.exercise.common_mistakes && (
                <div>
                  <h3 className="text-red-400 font-bold text-base mb-1">⚠ Common Mistakes</h3>
                  <p className="bg-red-900/20 text-red-300 p-3 rounded-lg border border-red-900/30">{currentEx.exercise.common_mistakes}</p>
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-800 p-5 rounded-2xl shadow-xl border border-gray-700">
               <h3 className="text-gray-400 font-semibold mb-1 text-xs uppercase tracking-wider">Too hard? Try:</h3>
               <p className="text-white font-medium">{currentEx.exercise.regression || "Easier variation"}</p>
            </div>
            <div className="bg-gray-800 p-5 rounded-2xl shadow-xl border border-gray-700">
               <h3 className="text-gray-400 font-semibold mb-1 text-xs uppercase tracking-wider">Next Target:</h3>
               <p className="text-green-400 font-medium">{currentEx.exercise.progression || "Harder variation"}</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
