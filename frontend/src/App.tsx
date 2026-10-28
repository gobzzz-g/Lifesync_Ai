import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Onboarding } from './pages/Onboarding';
import { FitnessDashboard } from './pages/FitnessDashboard';
import { WorkoutExecution } from './pages/WorkoutExecution';
import { NutritionDashboard } from './pages/NutritionDashboard';
import { LifestyleDashboard } from './pages/LifestyleDashboard';
import { CareerDashboard } from './pages/CareerDashboard';
import { Landing } from './pages/Landing';
import { Analytics } from './pages/Analytics';
import { Gamification } from './pages/Gamification';
import { Profile } from './pages/Profile';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/onboarding" element={<Onboarding />} />
            <Route path="/fitness" element={<FitnessDashboard />} />
            <Route path="/fitness/workout" element={<WorkoutExecution />} />
            <Route path="/nutrition" element={<NutritionDashboard />} />
            <Route path="/lifestyle" element={<LifestyleDashboard />} />
            <Route path="/career" element={<CareerDashboard />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/gamification" element={<Gamification />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
