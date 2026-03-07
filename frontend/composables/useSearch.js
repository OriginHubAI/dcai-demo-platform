import { computed, ref, watch } from 'vue'

export function useSearch(items, options = {}) {
  const searchQuery = ref('')
  const filters = ref({})
  const sortBy = ref(options.defaultSort || 'trending')

  const filtered = computed(() => {
    let result = [...items.value || items]

    // Search
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase()
      result = result.filter(item => {
        const name = (item.name || item.title || '').toLowerCase()
        const author = (item.author || '').toLowerCase()
        const desc = (item.description || '').toLowerCase()
        const id = (item.id || '').toLowerCase()
        return name.includes(q) || author.includes(q) || desc.includes(q) || id.includes(q)
      })
    }

    // Standard Filters
    for (const [key, values] of Object.entries(filters.value)) {
      if (values && values.length > 0) {
        // Handle datasetType filter (maps to datasetType field)
        if (key === 'datasetType') {
          result = result.filter(item => values.includes(item.datasetType))
          continue
        }
        
        // Handle autodriving-specific metadata filters
        if (['timeRange', 'weather', 'sceneType'].includes(key)) {
          result = result.filter(item => {
            if (!item.metadata) return false
            const itemConditions = item.metadata.conditions || []
            return values.some(v => itemConditions.includes(v))
          })
          continue
        }
        
        // Standard filters
        result = result.filter(item => {
          const itemVal = item[key]
          if (Array.isArray(itemVal)) {
            return values.some(v => itemVal.includes(v))
          }
          return values.includes(itemVal)
        })
      }
    }
    
    // Semantic Search Query
    if (filters.value.semanticQuery) {
      const semanticQ = filters.value.semanticQuery.toLowerCase()
      result = result.filter(item => {
        // Search in semantic index
        if (item.semanticIndex) {
          const semanticText = JSON.stringify(item.semanticIndex).toLowerCase()
          if (semanticText.includes(semanticQ)) return true
        }
        // Search in description
        if (item.description?.toLowerCase().includes(semanticQ)) return true
        // Search in metadata annotations
        if (item.metadata?.annotations) {
          const annText = item.metadata.annotations.join(' ').toLowerCase()
          if (annText.includes(semanticQ)) return true
        }
        return false
      })
    }
    
    // Spatial Search Query
    if (filters.value.spatialQuery) {
      const spatialQ = filters.value.spatialQuery.toLowerCase()
      result = result.filter(item => {
        if (!item.metadata?.spatial) return false
        const spatial = item.metadata.spatial
        // Search in regions
        if (spatial.regions?.some(r => r.toLowerCase().includes(spatialQ))) return true
        // Search in coverage description
        if (spatial.coverage?.toLowerCase().includes(spatialQ)) return true
        return false
      })
    }

    // Sort - only if not default sort
    if (sortBy.value !== 'default') {
      result.sort((a, b) => {
        switch (sortBy.value) {
          case 'downloads': return (b.downloads || 0) - (a.downloads || 0)
          case 'likes': return (b.likes || 0) - (a.likes || 0)
          case 'recent': return new Date(b.lastModified || 0) - new Date(a.lastModified || 0)
          case 'trending':
          default: return (b.likes || 0) * 0.4 + (b.downloads || 0) * 0.6 - ((a.likes || 0) * 0.4 + (a.downloads || 0) * 0.6)
        }
      })
    }

    return result
  })

  function clearFilters() {
    filters.value = {}
    searchQuery.value = ''
  }

  const activeFilterCount = computed(() => {
    let count = 0
    for (const [key, values] of Object.entries(filters.value)) {
      if (values) {
        if (Array.isArray(values)) {
          count += values.length
        } else if (typeof values === 'string' && values.trim()) {
          count += 1
        }
      }
    }
    return count
  })

  return { searchQuery, filters, sortBy, filtered, clearFilters, activeFilterCount }
}
