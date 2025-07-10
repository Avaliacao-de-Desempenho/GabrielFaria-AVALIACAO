import React from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import ListarNotas from "./components/NotaList"
import NotaUploader from "./components/NotaUploader"
import DeletarNota from "./components/NotaDeleter"
import Navbar from "./components/Navbar"

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar />

        <div className="max-w-2xl mx-auto mt-6">
          <Routes>
            <Route path="/" element={<ListarNotas />} />
            <Route path="/enviar" element={<NotaUploader />} />
            <Route path="/deletar" element={<DeletarNota />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
