import React from "react"

interface NavbarProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

const Navbar: React.FC<NavbarProps> = ({ activeTab, onTabChange }) => {
  const tabs = ["ver", "enviar", "deletar"]

  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-center gap-4 rounded-b-xl">
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => onTabChange(tab)}
          className={`capitalize px-4 py-2 rounded-lg ${
            activeTab === tab ? "bg-white text-blue-600 font-bold" : "hover:bg-blue-500"
          }`}
        >
          {tab === "ver" ? "Ver Notas" : tab === "enviar" ? "Enviar Nota" : "Deletar Nota"}
        </button>
      ))}
    </nav>
  )
}

export default Navbar
