import React, { useEffect, useState } from "react"
import axios from "axios"

interface Nota {
  Index: number
  Valor: number
  CNPJ: string
  Data: string
}

const ListarNotas = () => {
  const [notas, setNotas] = useState<Nota[]>([])
  const [erro, setErro] = useState<string | null>(null)

  useEffect(() => {
    // Função que traz os dados da API
    const fetchNotas = async () => {
      try {
        const response = await axios.get("http://localhost:8000/")
        setNotas(response.data.payload)
      } catch (err: any) {
        setErro(err?.message || "Erro ao buscar notas")
      }
    }

    fetchNotas()
  }, [])

  // Formata cada um dos dados do payload em um componente separado no formato de lista
  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Notas Registradas</h2>
      {erro && <div className="text-red-600">{erro}</div>}
      <ul className="space-y-2">
        {notas.map((nota) => (
          <li key={nota.Index} className="bg-white shadow p-4 rounded-lg">
            <p><strong>ID:</strong> {nota.Index}</p>
            <p><strong>Valor:</strong> {nota.Valor}</p>
            <p><strong>CNPJ:</strong> {nota.CNPJ}</p>
            <p><strong>Data:</strong> {nota.Data}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ListarNotas
