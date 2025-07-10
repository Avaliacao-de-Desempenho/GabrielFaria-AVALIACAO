import React, { useState } from "react"
import axios from "axios"

interface Resultado {
  Valor: string
  CNPJ: string
  Data: string
}

const NotaUploader = () => {
  const [arquivo, setArquivo] = useState<File | null>(null)
  const [resultado, setResultado] = useState<Resultado | null>(null)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState<string | null>(null)

  // Função que envia uma nota fiscal para processamento (roda quando o botão de enviar é pressionado)
  const handleUpload = async () => {
    if (!arquivo) return

    // Utilizado pra enviar o arquivo como "multipart/form-data", serve como um dicionário
    const formData = new FormData()
    // Adiciona a chave "arquivo" (nome do parâmetro na API) com o valor arquivo passado pelo usuário
    formData.append("arquivo", arquivo)

    // Faz a requisição pra API
    try {
      setCarregando(true)
      setErro(null)

      const response = await axios.post("https://api-avaliacao-40pbyn1o.uc.gateway.dev/notas/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })

      setResultado(response.data)
    } catch (err: any) {
      setErro( err?.response?.data?.erro || err?.message || "Erro ao processar")
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 mt-10 rounded-2xl shadow-lg bg-white space-y-4">
      <h1 className="text-xl font-bold text-gray-800">Analisar Nota Fiscal</h1>

      <input
        type="file"
        accept="image/*,application/pdf"
        onChange={(e) => setArquivo(e.target.files?.[0] || null)}
        className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:border file:rounded-lg file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />

      <button
        onClick={handleUpload}
        disabled={carregando || !arquivo}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-blue-300"
      >
        {carregando ? "Processando..." : "Enviar"}
      </button>

      {erro && <div className="text-red-600 text-sm">{erro}</div>}

      {resultado && (
        <div className="bg-gray-100 p-4 rounded-lg mt-4">
          <p><strong>Valor:</strong> {resultado.Valor}</p>
          <p><strong>CNPJ:</strong> {resultado.CNPJ}</p>
          <p><strong>Data:</strong> {resultado.Data}</p>
        </div>
      )}
    </div>
  )
}

export default NotaUploader
