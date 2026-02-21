export const knowledgeBases = [
  {
    id: 'kb-hb-standards',
    name: 'HB领域标准',
    description: 'HB领域标准',
    datasetId: 'iron-steel-papers',
    fileCount: 0,
    lastModified: '2026-02-09 15:54:09',
    type: 'general',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'hb_standards',
      dimension: 1536,
      vectorCount: 15420,
      indexType: 'IVF_FLAT'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: '文档解析' },
        { name: 'chunk', status: 'completed', label: '文本切分' },
        { name: 'embed', status: 'completed', label: '向量化' },
        { name: 'index', status: 'completed', label: '索引构建' }
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
      endpoint: '/mcp/kb-hb-standards',
      tools: ['search', 'query', 'traverse']
    }
  },
  {
    id: 'kb-high-temp-alloy-1',
    name: '高温合金上',
    description: '44种牌号数据',
    datasetId: 'materials-genome',
    fileCount: 0,
    lastModified: '2026-02-07 17:47:23',
    type: 'general',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'high_temp_alloy_1',
      dimension: 1536,
      vectorCount: 8930,
      indexType: 'HNSW'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: '文档解析' },
        { name: 'chunk', status: 'completed', label: '文本切分' },
        { name: 'embed', status: 'completed', label: '向量化' },
        { name: 'index', status: 'completed', label: '索引构建' }
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
      endpoint: '/mcp/kb-high-temp-alloy-1',
      tools: ['search', 'query', 'traverse']
    }
  },
  {
    id: 'kb-resume-test',
    name: '简历测试',
    description: '简历测试',
    datasetId: 'clinical-trials-nlp',
    fileCount: 0,
    lastModified: '2026-02-06 17:50:46',
    type: 'general',
    status: 'processing',
    vectorStore: {
      provider: 'milvus',
      collection: 'resume_test',
      dimension: 1536,
      vectorCount: 0,
      indexType: 'IVF_FLAT'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: '文档解析' },
        { name: 'chunk', status: 'completed', label: '文本切分' },
        { name: 'embed', status: 'running', label: '向量化' },
        { name: 'index', status: 'pending', label: '索引构建' }
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
    id: 'kb-high-temp-alloy-handbook',
    name: '高温合金手册-上卷',
    description: '包含77种变形高温合金成分和性能数据。',
    datasetId: 'superconductor-db',
    fileCount: 0,
    lastModified: '2026-02-06 16:08:13',
    type: 'general',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'high_temp_alloy_handbook',
      dimension: 1536,
      vectorCount: 24680,
      indexType: 'HNSW'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: '文档解析' },
        { name: 'chunk', status: 'completed', label: '文本切分' },
        { name: 'embed', status: 'completed', label: '向量化' },
        { name: 'index', status: 'completed', label: '索引构建' }
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
      endpoint: '/mcp/kb-high-temp-alloy-handbook',
      tools: ['search', 'query', 'traverse', 'recommend']
    }
  },
  {
    id: 'kb-polymer-research',
    name: '聚合物研究知识库',
    description: '聚合物专利和技术文献知识库',
    datasetId: 'polymer-patents',
    fileCount: 12,
    lastModified: '2026-02-05 14:32:18',
    type: 'general',
    status: 'ready',
    vectorStore: {
      provider: 'milvus',
      collection: 'polymer_research',
      dimension: 1536,
      vectorCount: 45620,
      indexType: 'HNSW'
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: '文档解析' },
        { name: 'chunk', status: 'completed', label: '文本切分' },
        { name: 'embed', status: 'completed', label: '向量化' },
        { name: 'index', status: 'completed', label: '索引构建' }
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
      endpoint: '/mcp/kb-polymer-research',
      tools: ['search', 'query', 'traverse']
    }
  },
  {
    id: 'kb-chemistry-reference',
    name: '化学参考资料库',
    description: '化学教材和参考书籍知识库',
    datasetId: 'chemistry-books',
    fileCount: 8,
    lastModified: '2026-02-04 09:15:33',
    type: 'general',
    status: 'error',
    vectorStore: {
      provider: 'milvus',
      collection: 'chemistry_reference',
      dimension: 1536,
      vectorCount: 0,
      indexType: null
    },
    pipeline: {
      stages: [
        { name: 'parse', status: 'completed', label: '文档解析' },
        { name: 'chunk', status: 'error', label: '文本切分', error: 'Chunk size too large for some documents' },
        { name: 'embed', status: 'pending', label: '向量化' },
        { name: 'index', status: 'pending', label: '索引构建' }
      ],
      lastRun: '2026-02-04 09:15:33',
      error: '部分文档切分失败，请检查文档格式'
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
  general: { label: '通用', color: 'blue' },
  domain: { label: '领域', color: 'purple' },
  private: { label: '私有', color: 'orange' }
}

export const kbStatusMap = {
  ready: { label: '就绪', color: 'green', icon: 'check' },
  processing: { label: '处理中', color: 'yellow', icon: 'sync' },
  error: { label: '错误', color: 'red', icon: 'error' },
  pending: { label: '待处理', color: 'gray', icon: 'clock' }
}
