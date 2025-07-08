import React, { useState } from "react"
import Navbar from "./components/Navbar"
import NotaUploader from "./components/NotaUploader"
import NotasList from "./components/NotasList"
import DeletarNota from "./components/NotaDelete"

function App() {
  const [tab, setTab] = useState("ver")

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar activeTab={tab} onTabChange={setTab} />

      <div className="max-w-2xl mx-auto mt-6">
        {tab === "ver" && <NotasList />}
        {tab === "enviar" && <NotaUploader />}
        {tab === "deletar" && <DeletarNota />}
      </div>
    </div>
  )
}

export default App
