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

    // Filters
    for (const [key, values] of Object.entries(filters.value)) {
      if (values && values.length > 0) {
        result = result.filter(item => {
          const itemVal = item[key]
          if (Array.isArray(itemVal)) {
            return values.some(v => itemVal.includes(v))
          }
          return values.includes(itemVal)
        })
      }
    }

    // Sort
    result.sort((a, b) => {
      switch (sortBy.value) {
        case 'downloads': return (b.downloads || 0) - (a.downloads || 0)
        case 'likes': return (b.likes || 0) - (a.likes || 0)
        case 'recent': return new Date(b.lastModified || 0) - new Date(a.lastModified || 0)
        case 'trending':
        default: return (b.likes || 0) * 0.4 + (b.downloads || 0) * 0.6 - ((a.likes || 0) * 0.4 + (a.downloads || 0) * 0.6)
      }
    })

    return result
  })

  function clearFilters() {
    filters.value = {}
    searchQuery.value = ''
  }

  const activeFilterCount = computed(() => {
    return Object.values(filters.value).reduce((sum, arr) => sum + (arr ? arr.length : 0), 0)
  })

  return { searchQuery, filters, sortBy, filtered, clearFilters, activeFilterCount }
}
