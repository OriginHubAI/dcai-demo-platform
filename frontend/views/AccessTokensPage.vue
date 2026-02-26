<template>
  <div class="min-h-screen bg-slate-50/50 py-8">
    <div class="max-w-6xl mx-auto px-6">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900">{{ t('accessTokens.title') }}</h1>
      </div>

      <!-- User Access Tokens Section -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200/60 overflow-hidden">
        <!-- Section Header -->
        <div class="px-6 py-5 border-b border-slate-200/60 flex items-center justify-between">
          <h2 class="text-xl font-semibold text-slate-900">{{ t('accessTokens.userAccessTokens') }}</h2>
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-slate-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 hover:border-slate-400 transition-all duration-200"
          >
            <PlusIcon class="w-4 h-4" />
            {{ t('accessTokens.createNewToken') }}
          </button>
        </div>

        <!-- Description -->
        <div class="px-6 py-4 bg-slate-50/50 border-b border-slate-200/60">
          <p class="text-sm text-slate-600 leading-relaxed">
            {{ t('accessTokens.description') }}
            <span class="inline-flex items-center gap-1.5 ml-1">
              <ExclamationCircleIcon class="w-4 h-4 text-slate-500" />
              <strong class="text-slate-700">{{ t('accessTokens.warning') }}</strong>
            </span>
          </p>
        </div>

        <!-- Tokens Table -->
        <div v-if="tokens.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-200/60">
                <th class="px-6 py-3 text-left">
                  <div class="flex items-center gap-1 text-sm font-semibold text-slate-900">
                    {{ t('accessTokens.name') }}
                    <ChevronUpDownIcon class="w-4 h-4 text-slate-400" />
                  </div>
                </th>
                <th class="px-6 py-3 text-left">
                  <span class="text-sm font-semibold text-slate-900">{{ t('accessTokens.value') }}</span>
                </th>
                <th class="px-6 py-3 text-left">
                  <div class="flex items-center gap-1 text-sm font-semibold text-slate-900">
                    {{ t('accessTokens.lastRefreshedDate') }}
                    <ChevronUpDownIcon class="w-4 h-4 text-slate-400" />
                  </div>
                </th>
                <th class="px-6 py-3 text-left">
                  <div class="flex items-center gap-1 text-sm font-semibold text-slate-900">
                    {{ t('accessTokens.lastUsedDate') }}
                    <ChevronUpDownIcon class="w-4 h-4 text-slate-400" />
                  </div>
                </th>
                <th class="px-6 py-3 text-left">
                  <div class="flex items-center gap-1 text-sm font-semibold text-slate-900">
                    {{ t('accessTokens.permissions') }}
                    <ChevronUpDownIcon class="w-4 h-4 text-slate-400" />
                  </div>
                </th>
                <th class="px-6 py-3 text-right">
                  <span class="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="token in tokens" :key="token.id" class="hover:bg-slate-50/50 transition-colors">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <KeyIcon class="w-4 h-4 text-slate-400" />
                    <span class="text-sm font-medium text-slate-900">{{ token.name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <code class="text-sm text-slate-600 font-mono">{{ maskToken(token.value) }}</code>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm text-slate-600">{{ formatDate(token.lastRefreshed) }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm text-slate-600">{{ token.lastUsed ? formatDate(token.lastUsed) : '-' }}</span>
                </td>
                <td class="px-6 py-4">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium"
                    :class="token.permission === 'WRITE' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'bg-slate-100 text-slate-600'"
                  >
                    {{ token.permission === 'WRITE' ? t('accessTokens.write') : t('accessTokens.read') }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      @click="copyToken(token.value)"
                      class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                      :title="t('accessTokens.copy')"
                    >
                      <ClipboardIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="refreshToken(token)"
                      class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                      :title="t('accessTokens.refresh')"
                    >
                      <ArrowPathIcon class="w-4 h-4" />
                    </button>
                    <div class="relative">
                      <button
                        @click="toggleActionMenu(token.id)"
                        class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                      >
                        <EllipsisVerticalIcon class="w-4 h-4" />
                      </button>
                      <!-- Action Dropdown -->
                      <div
                        v-if="activeActionMenu === token.id"
                        class="absolute right-0 mt-1 w-32 bg-white rounded-lg shadow-lg border border-slate-200 py-1 z-10"
                      >
                        <button
                          @click="deleteToken(token)"
                          class="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                        >
                          <TrashIcon class="w-4 h-4" />
                          {{ t('accessTokens.delete') }}
                        </button>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-else class="px-6 py-16 text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
            <KeyIcon class="w-8 h-8 text-slate-400" />
          </div>
          <h3 class="text-lg font-medium text-slate-900 mb-2">{{ t('accessTokens.noTokens') }}</h3>
          <p class="text-sm text-slate-500 mb-4">{{ t('accessTokens.noTokensHint') }}</p>
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center gap-2 px-4 py-2 bg-dc-primary text-white rounded-lg text-sm font-medium hover:bg-dc-primary-dark transition-colors"
          >
            <PlusIcon class="w-4 h-4" />
            {{ t('accessTokens.createNewToken') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Create Token Modal -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showCreateModal = false"></div>

        <!-- Modal -->
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
          <!-- Header -->
          <div class="px-6 py-4 border-b border-slate-200/60 flex items-center justify-between">
            <h3 class="text-lg font-semibold text-slate-900">{{ t('accessTokens.createTokenTitle') }}</h3>
            <button
              @click="showCreateModal = false"
              class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>

          <!-- Body -->
          <div class="px-6 py-5 space-y-4">
            <!-- Token Name -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">{{ t('accessTokens.tokenName') }}</label>
              <input
                v-model="newToken.name"
                type="text"
                :placeholder="t('accessTokens.tokenNamePlaceholder')"
                class="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-dc-primary/20 focus:border-dc-primary transition-all"
              />
            </div>

            <!-- Permission Level -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">{{ t('accessTokens.permissionLevel') }}</label>
              <div class="space-y-2">
                <label class="flex items-start gap-3 p-3 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50 transition-colors">
                  <input
                    v-model="newToken.permission"
                    type="radio"
                    value="READ"
                    class="mt-0.5 w-4 h-4 text-dc-primary border-slate-300 focus:ring-dc-primary"
                  />
                  <div>
                    <div class="text-sm font-medium text-slate-900">{{ t('accessTokens.read') }}</div>
                    <div class="text-xs text-slate-500">{{ t('accessTokens.readPermission') }}</div>
                  </div>
                </label>
                <label class="flex items-start gap-3 p-3 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50 transition-colors">
                  <input
                    v-model="newToken.permission"
                    type="radio"
                    value="WRITE"
                    class="mt-0.5 w-4 h-4 text-dc-primary border-slate-300 focus:ring-dc-primary"
                  />
                  <div>
                    <div class="text-sm font-medium text-slate-900">{{ t('accessTokens.write') }}</div>
                    <div class="text-xs text-slate-500">{{ t('accessTokens.writePermission') }}</div>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="px-6 py-4 border-t border-slate-200/60 flex items-center justify-end gap-3">
            <button
              @click="showCreateModal = false"
              class="px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
            >
              {{ t('accessTokens.cancel') }}
            </button>
            <button
              @click="createToken"
              :disabled="!newToken.name"
              class="px-4 py-2 bg-dc-primary text-white text-sm font-medium rounded-lg hover:bg-dc-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {{ t('accessTokens.create') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- New Token Display Modal -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="showNewTokenModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showNewTokenModal = false"></div>

        <!-- Modal -->
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
          <!-- Header -->
          <div class="px-6 py-4 border-b border-slate-200/60">
            <h3 class="text-lg font-semibold text-slate-900">{{ t('accessTokens.tokenCreated') }}</h3>
          </div>

          <!-- Body -->
          <div class="px-6 py-5">
            <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-4">
              <div class="flex items-start gap-2">
                <ExclamationTriangleIcon class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <p class="text-sm text-amber-800">{{ t('accessTokens.tokenCreated') }}</p>
              </div>
            </div>

            <div class="bg-slate-900 rounded-lg p-4 flex items-center justify-between">
              <code class="text-sm text-green-400 font-mono">{{ newlyCreatedToken }}</code>
              <button
                @click="copyToken(newlyCreatedToken)"
                class="p-1.5 text-slate-400 hover:text-white transition-colors"
                :title="t('accessTokens.copy')"
              >
                <ClipboardIcon class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Footer -->
          <div class="px-6 py-4 border-t border-slate-200/60 flex items-center justify-end">
            <button
              @click="showNewTokenModal = false"
              class="px-4 py-2 bg-dc-primary text-white text-sm font-medium rounded-lg hover:bg-dc-primary-dark transition-colors"
            >
              {{ t('accessTokens.cancel') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Toast Notification -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-2"
    >
      <div
        v-if="showToast"
        class="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 bg-slate-900 text-white rounded-lg shadow-lg"
      >
        <CheckCircleIcon class="w-5 h-5 text-green-400" />
        <span class="text-sm font-medium">{{ toastMessage }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, h } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// State
const tokens = ref([
  {
    id: 1,
    name: 'dataset',
    value: 'hf_dataset_token_xyz789abc',
    lastRefreshed: '2024-01-30T08:00:00Z',
    lastUsed: null,
    permission: 'WRITE'
  },
  {
    id: 2,
    name: 'gpt',
    value: 'hf_gpt_token_abc123def',
    lastRefreshed: '2023-02-09T08:00:00Z',
    lastUsed: null,
    permission: 'READ'
  }
])

const showCreateModal = ref(false)
const showNewTokenModal = ref(false)
const newlyCreatedToken = ref('')
const activeActionMenu = ref(null)
const showToast = ref(false)
const toastMessage = ref('')

const newToken = ref({
  name: '',
  permission: 'READ'
})

// Icon components
const PlusIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 4v16m8-8H4' })
])

const KeyIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z' })
])

const ChevronUpDownIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4' })
])

const ClipboardIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3' })
])

const ArrowPathIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15' })
])

const EllipsisVerticalIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z' })
])

const TrashIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16' })
])

const XMarkIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M6 18L18 6M6 6l12 12' })
])

const ExclamationCircleIcon = () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
])

const ExclamationTriangleIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
])

const CheckCircleIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
])

// Methods
function maskToken(token) {
  if (!token) return ''
  const prefix = token.substring(0, 3)
  return `${prefix}_...`
}

function formatDate(dateString) {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function toggleActionMenu(tokenId) {
  activeActionMenu.value = activeActionMenu.value === tokenId ? null : tokenId
}

function copyToken(token) {
  navigator.clipboard.writeText(token)
  showToastMessage(t('accessTokens.copied'))
}

function refreshToken(token) {
  // In a real app, this would call an API to refresh the token
  token.lastRefreshed = new Date().toISOString()
  showToastMessage(t('accessTokens.tokenCreated'))
}

function createToken() {
  if (!newToken.value.name) return

  // Generate a new token value
  const randomSuffix = Math.random().toString(36).substring(2, 15)
  const tokenValue = `hf_${newToken.value.name.toLowerCase().replace(/\s+/g, '_')}_${randomSuffix}`

  const token = {
    id: Date.now(),
    name: newToken.value.name,
    value: tokenValue,
    lastRefreshed: new Date().toISOString(),
    lastUsed: null,
    permission: newToken.value.permission
  }

  tokens.value.push(token)
  newlyCreatedToken.value = tokenValue

  // Reset form
  newToken.value = { name: '', permission: 'READ' }
  showCreateModal.value = false
  showNewTokenModal.value = true
}

function deleteToken(token) {
  if (confirm(t('accessTokens.confirmDelete'))) {
    tokens.value = tokens.value.filter(t => t.id !== token.id)
    activeActionMenu.value = null
    showToastMessage(t('accessTokens.tokenDeleted'))
  }
}

function showToastMessage(message) {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// Close action menu when clicking outside
function handleClickOutside(e) {
  if (!e.target.closest('.relative')) {
    activeActionMenu.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
