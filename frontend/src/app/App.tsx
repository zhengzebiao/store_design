import { Navigate, Route, Routes } from 'react-router-dom'
import StoreDesignHome from '../pages/home/StoreDesignHome'
import StoreDesignEditor from '../pages/edit/StoreDesignEditor'

export default function App() {
  return (
    <Routes>
      <Route path="/home" element={<StoreDesignHome />} />
      <Route path="/edit" element={<StoreDesignEditor />} />
      <Route path="*" element={<Navigate to="/home" replace />} />
    </Routes>
  )
}
