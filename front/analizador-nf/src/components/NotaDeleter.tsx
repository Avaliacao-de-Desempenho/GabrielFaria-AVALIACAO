import React, { useState } from "react"
import axios from "axios"

const DeletarNota = () => {
  const [id, setId] = useState("")
  const [mensagem, setMensagem] = useState("")
  const [erro, setErro] = useState<string | null>(null)

  const handleDelete = async () => {
    if (!id) return

    try {
      await axios.delete(`http://localhost:8000/notas/?id=${id}`)
      setMensagem(`Nota com ID ${id} deletada com sucesso.`)
      setErro(null)
      setId("")
    } catch (err: any) {
      setErro(err?.response?.data?.erro || err.message || "Erro ao deletar")
      setMensagem("")
    }
  }

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-xl font-bold">Deletar Nota</h2>
      <input
        type="text"
        placeholder="ID da nota"
        value={id}
        onChange={(e) => setId(e.target.value)}
        className="border rounded px-3 py-2 w-full"
      />
      <button
        onClick={handleDelete}
        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
      >
        Deletar
      </button>
      {mensagem && <div className="text-green-600">{mensagem}</div>}
      {erro && <div className="text-red-600">{erro}</div>}
    </div>
  )
}

export default DeletarNota
