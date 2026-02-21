export const spaces = [
  { id: 'OpenDCAI/Open-NotebookLM', author: 'OpenDCAI', title: 'Open-NotebookLM', emoji: '📓', colorFrom: 'indigo', colorTo: 'purple', description: 'Convert PDFs into podcast-style audio conversations using open-source LLMs and TTS models.', category: 'text-generation', sdk: 'gradio', likes: 3200, status: 'running', hardware: 'A100' },
  { id: 'HuggingFaceH4/chat-ui', author: 'HuggingFaceH4', title: 'HuggingChat', emoji: '💬', colorFrom: 'yellow', colorTo: 'orange', description: 'Open-source chat interface powered by the best open LLMs available.', category: 'text-generation', sdk: 'docker', likes: 22000, status: 'running', hardware: 'A100' },
  { id: 'OpenDCAI/Paper2Any', author: 'OpenDCAI', title: 'Paper2Any', emoji: '📄', colorFrom: 'blue', colorTo: 'cyan', description: 'Convert academic papers into various formats including podcasts, presentations, and summaries.', category: 'text-generation', sdk: 'gradio', likes: 2800, status: 'running', hardware: 'A100' },
  { id: 'OpenDCAI/MCP-VectorSQL', author: 'OpenDCAI', title: 'MCP-VectorSQL', emoji: '🔍', colorFrom: 'green', colorTo: 'teal', description: 'Convert natural language questions into high-quality SQL queries for vector databases.', category: 'text-generation', sdk: 'gradio', likes: 1900, status: 'running', hardware: 'A10G' },
  { id: 'OpenDCAI/Dataflow-LoopAI', author: 'OpenDCAI', title: 'DataFlow-LoopAI', emoji: '🔄', colorFrom: 'purple', colorTo: 'pink', description: 'AI-powered dataflow automation tool for building intelligent workflows and pipelines.', category: 'text-generation', sdk: 'gradio', likes: 1500, status: 'running', hardware: 'A100' },
  { id: 'OpenDCAI/Chem-CoT-Generator', author: 'OpenDCAI', title: 'Chem-CoT-Generator', emoji: '🧪', colorFrom: 'teal', colorTo: 'green', description: 'Generate high-quality chemical chain-of-thought (CoT) data for training and fine-tuning chemistry-focused LLMs.', category: 'text-generation', sdk: 'gradio', likes: 2100, status: 'running', hardware: 'A100' },
]

export function getSpaceById(id) {
  return spaces.find(s => s.id === id)
}
