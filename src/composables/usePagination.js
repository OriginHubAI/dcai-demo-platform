import { computed, ref, watch } from 'vue'

export function usePagination(items, perPage = 12) {
  const currentPage = ref(1)

  const totalPages = computed(() => {
    return Math.max(1, Math.ceil(items.value.length / perPage))
  })

  const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * perPage
    return items.value.slice(start, start + perPage)
  })

  const totalItems = computed(() => items.value.length)

  watch(items, () => {
    if (currentPage.value > totalPages.value) {
      currentPage.value = 1
    }
  })

  return { currentPage, totalPages, paginatedItems, totalItems }
}
