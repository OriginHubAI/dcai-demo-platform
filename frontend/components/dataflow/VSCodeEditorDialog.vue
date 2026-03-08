<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="visible"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
        @click="close"
      >
        <div
          class="w-full h-full max-w-[1500px] max-h-[92vh] bg-white rounded-xl shadow-2xl overflow-hidden flex flex-col"
          @click.stop
        >
          <div class="h-11 bg-[#f3f3f3] flex items-center justify-between px-4 border-b border-gray-200">
            <div>
              <div class="text-sm font-semibold text-gray-900">{{ pkg.name }}</div>
              <div class="text-xs text-gray-500">{{ editorLabel }}</div>
            </div>
            <div class="flex items-center gap-2">
              <button class="text-xs px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100" @click="runTests" :disabled="loadingTest">
                {{ loadingTest ? 'Testing...' : 'Run Test' }}
              </button>
              <button class="text-xs px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100" @click="refreshWorkspace" :disabled="loadingWorkspace">
                Refresh
              </button>
              <button class="w-8 h-8 rounded-lg hover:bg-gray-200 flex items-center justify-center text-gray-500" @click="close">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <div class="flex-1 flex min-h-0">
            <div class="w-72 border-r border-gray-200 bg-slate-50 overflow-y-auto">
              <div class="px-4 py-3 border-b border-slate-200">
                <p class="text-xs font-semibold text-slate-600 uppercase tracking-wide">Files</p>
              </div>
              <div class="px-2 py-2">
                <template v-if="fileTree">
                  <FileTreeNode
                    :node="fileTree"
                    :selected-path="activePath"
                    @open="openFile"
                  />
                </template>
                <p v-else class="px-2 py-3 text-sm text-slate-500">Loading package tree...</p>
              </div>
            </div>

            <div class="flex-1 min-w-0 flex flex-col">
              <div class="px-4 py-2 border-b border-gray-200 flex items-center justify-between bg-white">
                <div class="text-sm text-slate-700 truncate">{{ activePath || 'Workspace overview' }}</div>
                <div class="text-xs text-slate-500">{{ editorModeText }}</div>
              </div>

              <div class="flex-1 min-h-0 overflow-hidden bg-[#fbfbfc]">
                <iframe
                  v-if="editorSession?.mode === 'external' && editorSession.url"
                  :src="editorSession.url"
                  class="w-full h-full border-0"
                />
                <div v-else class="h-full overflow-auto p-6">
                  <p class="text-sm text-slate-500 mb-4">
                    {{ editorSession?.reason || 'code-server is unavailable, using file preview mode.' }}
                  </p>
                  <pre
                    v-if="activeContent"
                    class="text-xs leading-6 bg-slate-900 text-slate-100 rounded-xl p-4 overflow-auto"
                  ><code>{{ activeContent }}</code></pre>
                  <div v-else class="text-sm text-slate-500">
                    Select a file from the package tree to preview it.
                  </div>
                </div>
              </div>

              <div class="border-t border-gray-200 bg-white px-4 py-3 max-h-40 overflow-auto">
                <p class="text-xs font-semibold text-slate-600 uppercase tracking-wide mb-2">Test Result</p>
                <p v-if="!testResult" class="text-sm text-slate-500">No test has been run for this package yet.</p>
                <div v-else class="space-y-2">
                  <p class="text-sm" :class="testResult.success ? 'text-emerald-600' : 'text-rose-600'">
                    {{ testResult.success ? 'Package syntax check passed.' : 'Package syntax check failed.' }}
                  </p>
                  <p class="text-xs text-slate-500">{{ testResult.command }}</p>
                  <pre v-if="testResult.stdout" class="text-xs bg-slate-100 rounded-lg p-3 overflow-auto">{{ testResult.stdout }}</pre>
                  <pre v-if="testResult.stderr" class="text-xs bg-rose-50 text-rose-700 rounded-lg p-3 overflow-auto">{{ testResult.stderr }}</pre>
                </div>
              </div>
            </div>

            <AgentDialogSidebar
              :package-id="pkg.id"
              :current-path="activePath"
              @close="close"
            />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, defineComponent, h, ref, watch } from 'vue'

import { dataflowApi } from '@/services/api.js'

import AgentDialogSidebar from './AgentDialogSidebar.vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  pkg: { type: Object, required: true },
})

const emit = defineEmits(['update:visible', 'close'])

const loadingWorkspace = ref(false)
const loadingTest = ref(false)
const fileTree = ref(null)
const activePath = ref('')
const activeContent = ref('')
const editorSession = ref(null)
const testResult = ref(null)

const editorLabel = computed(() => {
  if (!editorSession.value) return 'Preparing workspace...'
  if (editorSession.value.mode === 'external') return `Live editor · ${editorSession.value.url}`
  return 'Preview mode'
})

const editorModeText = computed(() => {
  if (editorSession.value?.mode === 'external') return 'code-server'
  return 'Preview mode'
})

const FileTreeNode = defineComponent({
  name: 'FileTreeNode',
  props: {
    node: { type: Object, required: true },
    selectedPath: { type: String, default: '' },
  },
  emits: ['open'],
  setup(componentProps, { emit: componentEmit }) {
    return () => {
      const node = componentProps.node
      if (node.type === 'file') {
        return h(
          'button',
          {
            class: [
              'w-full text-left px-2 py-1.5 rounded text-sm truncate',
              componentProps.selectedPath === node.path ? 'bg-blue-50 text-blue-700' : 'hover:bg-slate-100 text-slate-700',
            ],
            onClick: () => componentEmit('open', node.path),
          },
          node.name,
        )
      }

      return h('div', { class: 'mb-1' }, [
        h('div', { class: 'px-2 py-1 text-xs font-semibold text-slate-500 uppercase tracking-wide truncate' }, node.name || 'root'),
        ...(node.children || []).map((child) =>
          h('div', { class: 'ml-3' }, [
            h(FileTreeNode, {
              node: child,
              selectedPath: componentProps.selectedPath,
              onOpen: (path) => componentEmit('open', path),
            }),
          ]),
        ),
      ])
    }
  },
})

function findFirstFile(node) {
  if (!node) return ''
  if (node.type === 'file') return node.path
  for (const child of node.children || []) {
    const match = findFirstFile(child)
    if (match) return match
  }
  return ''
}

async function loadTree() {
  fileTree.value = await dataflowApi.getPackageFiles(props.pkg.id)
  const firstFile = findFirstFile(fileTree.value)
  if (firstFile) {
    await openFile(firstFile)
  }
}

async function openFile(path) {
  activePath.value = path
  const payload = await dataflowApi.getPackageFileContent(props.pkg.id, path)
  activeContent.value = payload.content
}

async function refreshWorkspace() {
  loadingWorkspace.value = true
  try {
    editorSession.value = await dataflowApi.startPackageEditor(props.pkg.id)
    await loadTree()
  } finally {
    loadingWorkspace.value = false
  }
}

async function runTests() {
  loadingTest.value = true
  try {
    testResult.value = await dataflowApi.runPackageTest(props.pkg.id)
  } finally {
    loadingTest.value = false
  }
}

async function close() {
  emit('update:visible', false)
  emit('close')
  if (props.pkg?.id) {
    await dataflowApi.stopPackageEditor(props.pkg.id)
  }
}

watch(
  () => props.visible,
  async (visible) => {
    if (!visible) return
    activePath.value = ''
    activeContent.value = ''
    testResult.value = null
    await refreshWorkspace()
  },
)
</script>
