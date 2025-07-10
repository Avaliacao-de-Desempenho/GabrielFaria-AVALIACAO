import React from "react"
import { NavLink } from "react-router-dom"

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-center gap-4 rounded-b-xl">
      <NavLink
        to="/"
        className={({ isActive }) =>
          `px-4 py-2 rounded-lg capitalize ${
            isActive ? "bg-white text-blue-600 font-bold" : "hover:bg-blue-500"
          }`
        }
      >
        Ver Notas
      </NavLink>

      <NavLink
        to="/enviar"
        className={({ isActive }) =>
          `px-4 py-2 rounded-lg capitalize ${
            isActive ? "bg-white text-blue-600 font-bold" : "hover:bg-blue-500"
          }`
        }
      >
        Enviar Nota
      </NavLink>

      <NavLink
        to="/deletar"
        className={({ isActive }) =>
          `px-4 py-2 rounded-lg capitalize ${
            isActive ? "bg-white text-blue-600 font-bold" : "hover:bg-blue-500"
          }`
        }
      >
        Deletar Nota
      </NavLink>
    </nav>
  )
}

export default Navbar
