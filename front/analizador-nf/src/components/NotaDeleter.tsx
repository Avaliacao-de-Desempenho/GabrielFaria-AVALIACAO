import React, { useState } from "react"
import axios from "axios"

const DeletarNota = () => {
  const [id, setId] = useState("")
  const [mensagem, setMensagem] = useState("")
  const [erro, setErro] = useState<string | null>(null)
  const [carregando, setCarregando] = useState(false)

  // Função que deleta uma linha da tabela de acordo com o id passado
  const handleDelete = async () => {
    if (!id) return

    try {
      setCarregando(true)
      await axios.delete(`https://api-avaliacao-40pbyn1o.uc.gateway.dev/notas/?id=${id}`)
      setMensagem(`Nota com ID ${id} deletada com sucesso.`)
      setErro(null)
      setId("")
    } catch (err: any) {
      setErro(err?.response?.data?.erro || err.message || "Erro ao deletar")
      setMensagem("")
    } finally {
      setCarregando(false)
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
        disabled={carregando}
      />

      <button
        onClick={handleDelete}
        disabled={carregando || !id}
        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:bg-red-300"
      >
        {carregando ? "Deletando..." : "Deletar"}
      </button>

      {carregando && (
        <div className="flex justify-center items-center h-10">
          <div className="animate-spin rounded-full h-6 w-6 border-t-4 border-red-600 border-opacity-50"></div>
        </div>
      )}

      {mensagem && <div className="text-green-600">{mensagem}</div>}
      {erro && <div className="text-red-600">{erro}</div>}
    </div>
  )
}

export default DeletarNota
