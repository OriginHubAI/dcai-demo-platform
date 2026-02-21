export const knowledgeBases = [
  {
    id: 'kb-math-olympiad',
    name: 'Math Olympiad Problems',
    description: 'International math olympiad problems with step-by-step solutions',
    datasetId: 'math-olympiad-problems',
    fileCount: 12,
    lastModified: '2026-02-09 15:54:09',
    type: 'general',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'math_olympiad',
      dimension: 1536,
      vectorCount: 15420,
      indexType: 'IVF_FLAT'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: 'Document Parsing' },
        { name: 'chunk', status: 'completed', label: 'Text Chunking' },
        { name: 'embed', status: 'completed', label: 'Embedding' },
        { name: 'index', status: 'completed', label: 'Index Building' }
      ],
      lastRun: '2026-02-09 15:54:09'
    },
    knowledgeGraph: {
      enabled: true,
      entityCount: 3280,
      relationCount: 8540,
      lastUpdated: '2026-02-09 15:54:09'
    },
    mcp: {
      enabled: true,
      endpoint: '/mcp/kb-math-olympiad',
      tools: ['search', 'query', 'traverse']
    }
  },
  {
    id: 'kb-protein-structures',
    name: 'Protein Structures 3D',
    description: 'Three-dimensional protein structure predictions with amino acid sequences',
    datasetId: 'protein-structures-3d',
    fileCount: 8,
    lastModified: '2026-02-07 17:47:23',
    type: 'domain',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'protein_structures',
      dimension: 1536,
      vectorCount: 8930,
      indexType: 'HNSW'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: 'Document Parsing' },
        { name: 'chunk', status: 'completed', label: 'Text Chunking' },
        { name: 'embed', status: 'completed', label: 'Embedding' },
        { name: 'index', status: 'completed', label: 'Index Building' }
      ],
      lastRun: '2026-02-07 17:47:23'
    },
    knowledgeGraph: {
      enabled: true,
      entityCount: 2150,
      relationCount: 5620,
      lastUpdated: '2026-02-07 17:47:23'
    },
    mcp: {
      enabled: true,
      endpoint: '/mcp/kb-protein-structures',
      tools: ['search', 'query', 'traverse']
    }
  },
  {
    id: 'kb-rna-sequences',
    name: 'RNA Sequence Database',
    description: 'Curated RNA sequence data including mRNA, tRNA, and non-coding RNA',
    datasetId: 'rna-sequences',
    fileCount: 5,
    lastModified: '2026-02-06 17:50:46',
    type: 'domain',
    status: 'processing',
    vectorStore: {
      provider: 'milvus',
      collection: 'rna_sequences',
      dimension: 1536,
      vectorCount: 0,
      indexType: 'IVF_FLAT'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: 'Document Parsing' },
        { name: 'chunk', status: 'completed', label: 'Text Chunking' },
        { name: 'embed', status: 'running', label: 'Embedding' },
        { name: 'index', status: 'pending', label: 'Index Building' }
      ],
      lastRun: '2026-02-06 17:50:46',
      progress: 65
    },
    knowledgeGraph: {
      enabled: false,
      entityCount: 0,
      relationCount: 0,
      lastUpdated: null
    },
    mcp: {
      enabled: false,
      endpoint: null,
      tools: []
    }
  },
  {
    id: 'kb-astrophysics',
    name: 'Astrophysics Spectra',
    description: 'Stellar and galactic spectral data from ground-based and space telescopes',
    datasetId: 'astrophysics-spectra',
    fileCount: 15,
    lastModified: '2026-02-06 16:08:13',
    type: 'domain',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'astrophysics_spectra',
      dimension: 1536,
      vectorCount: 24680,
      indexType: 'HNSW'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: 'Document Parsing' },
        { name: 'chunk', status: 'completed', label: 'Text Chunking' },
        { name: 'embed', status: 'completed', label: 'Embedding' },
        { name: 'index', status: 'completed', label: 'Index Building' }
      ],
      lastRun: '2026-02-06 16:08:13'
    },
    knowledgeGraph: {
      enabled: true,
      entityCount: 5620,
      relationCount: 12840,
      lastUpdated: '2026-02-06 16:08:13'
    },
    mcp: {
      enabled: true,
      endpoint: '/mcp/kb-astrophysics',
      tools: ['search', 'query', 'traverse', 'recommend']
    }
  },
  {
    id: 'kb-physics-simulations',
    name: 'Physics Simulations',
    description: 'Numerical simulation outputs for fluid dynamics, quantum mechanics, and thermodynamics',
    datasetId: 'physics-simulations',
    fileCount: 12,
    lastModified: '2026-02-05 14:32:18',
    type: 'domain',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'physics_simulations',
      dimension: 1536,
      vectorCount: 45620,
      indexType: 'HNSW'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: 'Document Parsing' },
        { name: 'chunk', status: 'completed', label: 'Text Chunking' },
        { name: 'embed', status: 'completed', label: 'Embedding' },
        { name: 'index', status: 'completed', label: 'Index Building' }
      ],
      lastRun: '2026-02-05 14:32:18'
    },
    knowledgeGraph: {
      enabled: true,
      entityCount: 8940,
      relationCount: 21560,
      lastUpdated: '2026-02-05 14:32:18'
    },
    mcp: {
      enabled: true,
      endpoint: '/mcp/kb-physics-simulations',
      tools: ['search', 'query', 'traverse']
    }
  },
  {
    id: 'kb-quantum-chemistry',
    name: 'Quantum Chemistry Calculations',
    description: 'Density functional theory calculation results for molecular systems',
    datasetId: 'quantum-chemistry-calcs',
    fileCount: 8,
    lastModified: '2026-02-04 09:15:33',
    type: 'domain',
    status: 'error',
    vectorStore: {
      provider: 'milvus',
      collection: 'quantum_chemistry',
      dimension: 1536,
      vectorCount: 0,
      indexType: null
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: 'Document Parsing' },
        { name: 'chunk', status: 'error', label: 'Text Chunking', error: 'Chunk size too large for some documents' },
        { name: 'embed', status: 'pending', label: 'Embedding' },
        { name: 'index', status: 'pending', label: 'Index Building' }
      ],
      lastRun: '2026-02-04 09:15:33',
      error: 'Some documents failed to chunk. Please check the document format.'
    },
    knowledgeGraph: {
      enabled: false,
      entityCount: 0,
      relationCount: 0,
      lastUpdated: null
    },
    mcp: {
      enabled: false,
      endpoint: null,
      tools: []
    }
  }
]

export function getKnowledgeBaseById(id) {
  return knowledgeBases.find(kb => kb.id === id)
}

export function getKnowledgeBaseByDatasetId(datasetId) {
  return knowledgeBases.filter(kb => kb.datasetId === datasetId)
}

export const kbTypeMap = {
  general: { label: 'General', color: 'blue' },
  domain: { label: 'Domain', color: 'purple' },
  private: { label: 'Private', color: 'orange' }
}

export const kbStatusMap = {
  ready: { label: 'Ready', color: 'green', icon: 'check' },
  processing: { label: 'Processing', color: 'yellow', icon: 'sync' },
  error: { label: 'Error', color: 'red', icon: 'error' },
  pending: { label: 'Pending', color: 'gray', icon: 'clock' }
}
