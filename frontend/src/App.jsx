/**
 * App.jsx
 * =======
 * The ROOT component of the application.
 *
 * Routes:
 *   - Landing (/) — landing page (public)
 *   - Login (/login) — login page
 *   - Register (/register) — registration page
 *   - Dashboard (/dashboard) — task overview with stats (protected)
 *   - Tasks (/tasks) — task list with search/filter/pagination (protected)
 *   - Create Task (/tasks/create) — create task modal (protected)
 *   - Task Detail (/tasks/:id) — view a single task (protected)
 *   - Edit Task (/tasks/:id/edit) — edit a task (protected)
 *   - 404 (*) — not found page
 */
import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";

// ── Lazy-loaded pages (code-split for smaller initial bundle) ──
const LandingPage = lazy(() => import("./pages/LandingPage"));
const LoginPage = lazy(() => import("./pages/LoginPage"));
const RegisterPage = lazy(() => import("./pages/RegisterPage"));
const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const TasksPage = lazy(() => import("./pages/TasksPage"));
const TaskDetailPage = lazy(() => import("./pages/TaskDetailPage"));
const NotFoundPage = lazy(() => import("./pages/NotFoundPage"));

// ── Layouts ──
const DashboardLayout = lazy(() => import("./components/DashboardLayout"));

// ═══════════════════════════════════════════════
// FULL-PAGE LOADER
// ═══════════════════════════════════════════════

function PageLoader() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="w-10 h-10 rounded-full border-4 border-blue-200 border-t-blue-600 animate-spin" />
    </div>
  );
}

// ═══════════════════════════════════════════════
// APP COMPONENT
// ═══════════════════════════════════════════════

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Suspense fallback={<PageLoader />}>
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Protected routes with dashboard layout */}
            <Route
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/tasks" element={<TasksPage />} />
              <Route path="/tasks/create" element={<TasksPage />} />
              <Route path="/tasks/:id" element={<TaskDetailPage />} />
              <Route path="/tasks/:id/edit" element={<TaskDetailPage />} />
            </Route>

            {/* 404 */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Suspense>
      </AuthProvider>
    </BrowserRouter>
  );
}

