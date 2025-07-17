import { useState } from "react";

interface QueryResponse {
  question: string;
  query: string;
  result: any;
  answer: string;
  page: number;
  page_size: number;
}

type Step = "idle" | "thinking" | "generating_sql" | "executing_sql" | "generating_answer" | "done";

export default function App() {
  const [question, setQuestion] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [step, setStep] = useState<Step>("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResponse(null);
    setStep("thinking");
    try {
      // Simulate step-by-step progress
      setStep("generating_sql");
      // Optionally, add a small delay for realism
      await new Promise(res => setTimeout(res, 400));
      setStep("executing_sql");
      await new Promise(res => setTimeout(res, 400));
      setStep("generating_answer");
      // Call backend
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, page, page_size: pageSize }),
      });
      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      setResponse(data);
      setStep("done");
    } catch (err: any) {
      setError(err.message || "Unknown error");
      setStep("idle");
    } finally {
      setLoading(false);
    }
  };

  const getStepMessage = () => {
    switch (step) {
      case "thinking":
        return "Thinking ...";
      case "generating_sql":
        return "Generating SQL query ...";
      case "executing_sql":
        return "Executing SQL query ...";
      case "generating_answer":
        return "Generating answer ...";
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-8 px-2">
      <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">Quick Commerce SQL Agent</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="Ask a question (e.g. Which app has cheapest onions right now?)"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            required
          />
          <div className="flex gap-4">
            <div>
              <label className="block text-sm font-medium">Page</label>
              <input
                type="number"
                min={1}
                className="w-20 px-2 py-1 border rounded"
                value={page}
                onChange={e => setPage(Number(e.target.value))}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Page Size</label>
              <input
                type="number"
                min={1}
                max={100}
                className="w-24 px-2 py-1 border rounded"
                value={pageSize}
                onChange={e => setPageSize(Number(e.target.value))}
              />
            </div>
            <button
              type="submit"
              className="ml-auto px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold disabled:opacity-50"
              disabled={loading}
            >
              {loading ? "Loading..." : "Ask"}
            </button>
          </div>
        </form>
        {error && <div className="mt-4 text-red-600 font-semibold">{error}</div>}
        {/* Step-by-step loading states */}
        {loading && !response && (
          <div className="mt-8 flex flex-col items-center">
            <div className="animate-pulse text-blue-600 font-semibold text-lg">{getStepMessage()}</div>
          </div>
        )}
        {response && (
          <div className="mt-8 space-y-6">
            <div>
              <div className="text-xs text-gray-500 mb-1">SQL Query</div>
              <pre className="bg-gray-100 rounded p-2 text-sm overflow-x-auto">{response.query}</pre>
            </div>
            <div>
              <div className="text-xs text-gray-500 mb-1">SQL Result</div>
              <div className="bg-gray-100 rounded p-2 text-sm overflow-x-auto">
                {Array.isArray(response.result) ? (
                  <table className="min-w-full text-xs">
                    <tbody>
                      {response.result.map((row: any, i: number) => (
                        <tr key={i} className="border-b last:border-b-0">
                          {Array.isArray(row)
                            ? row.map((cell, j) => <td key={j} className="px-2 py-1">{String(cell)}</td>)
                            : <td>{String(row)}</td>}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <span>{String(response.result)}</span>
                )}
              </div>
            </div>
            <div>
              <div className="text-xs text-gray-500 mb-1">LLM Answer</div>
              <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded text-blue-900 font-medium whitespace-pre-line">
                {response.answer}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
