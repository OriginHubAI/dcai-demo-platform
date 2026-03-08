<template>
  <div class="data-studio">
    <!-- Tab Navigation -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-4">
        <!-- Split Selector -->
        <div class="relative">
          <button 
            @click="showSplitDropdown = !showSplitDropdown"
            class="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <span class="text-sm text-gray-600">Split ({{ splits.length }})</span>
            <span class="text-sm font-medium text-gray-900">{{ selectedSplit }}</span>
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div v-if="showSplitDropdown" class="absolute top-full left-0 mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
            <div v-for="split in splits" :key="split.name" 
              @click="selectSplit(split)"
              class="px-4 py-2 hover:bg-gray-50 cursor-pointer flex items-center justify-between"
            >
              <span class="text-sm">{{ split.name }}</span>
              <span class="text-xs text-gray-500">{{ formatRows(split.rows) }} rows</span>
            </div>
          </div>
        </div>
      </div>

      <!-- View Toggles -->
      <div class="flex items-center space-x-2">
        <button 
          @click="viewMode = 'table'"
          :class="{ 'bg-gray-100': viewMode === 'table' }"
          class="p-2 rounded-lg hover:bg-gray-50 transition-colors"
          title="Table View"
        >
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>
        <button 
          @click="viewMode = 'grid'"
          :class="{ 'bg-gray-100': viewMode === 'grid' }"
          class="p-2 rounded-lg hover:bg-gray-50 transition-colors"
          title="Grid View"
        >
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Unified Search Bar -->
    <div class="mb-4">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-dc-primary focus:border-transparent"
          placeholder="Search by time, location, keywords, or semantic description..."
        />
        <div v-if="searchQuery" class="absolute inset-y-0 right-0 pr-3 flex items-center">
          <button @click="searchQuery = ''" class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Search Filters -->
      <div class="flex flex-wrap gap-2 mt-2">
        <button 
          @click="searchType = 'all'"
          :class="{ 'bg-dc-primary text-white': searchType === 'all', 'bg-gray-100 text-gray-700': searchType !== 'all' }"
          class="px-3 py-1 rounded-full text-xs font-medium transition-colors"
        >
          All Fields
        </button>
        <button 
          @click="searchType = 'temporal'"
          :class="{ 'bg-blue-500 text-white': searchType === 'temporal', 'bg-gray-100 text-gray-700': searchType !== 'temporal' }"
          class="px-3 py-1 rounded-full text-xs font-medium transition-colors flex items-center space-x-1"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Temporal</span>
        </button>
        <button 
          @click="searchType = 'spatial'"
          :class="{ 'bg-green-500 text-white': searchType === 'spatial', 'bg-gray-100 text-gray-700': searchType !== 'spatial' }"
          class="px-3 py-1 rounded-full text-xs font-medium transition-colors flex items-center space-x-1"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>Spatial</span>
        </button>
        <button 
          @click="searchType = 'semantic'"
          :class="{ 'bg-purple-500 text-white': searchType === 'semantic', 'bg-gray-100 text-gray-700': searchType !== 'semantic' }"
          class="px-3 py-1 rounded-full text-xs font-medium transition-colors flex items-center space-x-1"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          <span>Semantic</span>
        </button>
        <button 
          @click="searchType = 'vector'"
          :class="{ 'bg-orange-500 text-white': searchType === 'vector', 'bg-gray-100 text-gray-700': searchType !== 'vector' }"
          class="px-3 py-1 rounded-full text-xs font-medium transition-colors flex items-center space-x-1"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span>Vector</span>
        </button>
      </div>
    </div>

    <!-- Column Statistics Summary -->
    <div class="mb-4 border border-gray-200 rounded-lg overflow-hidden">
      <table class="w-full" style="table-layout: fixed; min-width: 1160px;">
        <thead>
          <tr>
            <!-- ID Column -->
            <th class="px-4 py-3 text-left bg-gray-50 border-b border-gray-200 whitespace-nowrap" style="width: 140px;">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-medium text-gray-600">ID</span>
                <span class="text-xs text-gray-400">string</span>
              </div>
              <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full" style="width: 100%"></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">unique</div>
            </th>
            <!-- Timestamp Column -->
            <th class="px-4 py-3 text-left bg-gray-50 border-b border-gray-200 whitespace-nowrap" style="width: 160px;">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-medium text-gray-600">Timestamp</span>
                <span class="text-xs text-gray-400">datetime</span>
              </div>
              <div class="h-8 flex items-end space-x-0.5">
                <div v-for="(bar, i) in [30, 45, 60, 80, 100, 85, 70, 50, 35, 25]" :key="i"
                  class="flex-1 bg-blue-400 rounded-t"
                  :style="{ height: bar + '%', opacity: 0.3 + (i / 10) * 0.7 }"
                ></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">2025-01 ~ 2025-03</div>
            </th>
            <!-- Location Column -->
            <th class="px-4 py-3 text-left bg-gray-50 border-b border-gray-200 whitespace-nowrap" style="width: 160px;">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-medium text-gray-600">Location</span>
                <span class="text-xs text-gray-400">geo</span>
              </div>
              <div class="text-xs text-gray-500">1.2°N ~ 42.4°N</div>
              <div class="text-xs text-gray-500 mt-1">Boston, Singapore</div>
            </th>
            <!-- Description Column -->
            <th class="px-4 py-3 text-left bg-gray-50 border-b border-gray-200" style="width: 280px;">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-medium text-gray-600">Description</span>
                <span class="text-xs text-gray-400">text</span>
              </div>
              <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full" style="width: 100%"></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">avg 156 chars</div>
            </th>
            <!-- Image Column -->
            <th class="px-4 py-3 text-left bg-gray-50 border-b border-gray-200 whitespace-nowrap" style="width: 120px;">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-medium text-gray-600">Image</span>
                <span class="text-xs text-gray-400">image</span>
              </div>
              <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full" style="width: 100%"></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">1600×900</div>
            </th>
            <!-- Objects Column -->
            <th class="px-4 py-3 text-left bg-gray-50 border-b border-gray-200 whitespace-nowrap" style="width: 140px;">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-medium text-gray-600">Objects</span>
                <span class="text-xs text-gray-400">semantic</span>
              </div>
              <div class="h-8 flex items-end space-x-0.5">
                <div v-for="(bar, i) in [20, 40, 60, 80, 100, 90, 70, 50, 30, 20]" :key="i"
                  class="flex-1 bg-blue-400 rounded-t"
                  :style="{ height: bar + '%', opacity: 0.3 + (i / 10) * 0.7 }"
                ></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">8 classes</div>
            </th>
            <!-- Vector Column -->
            <th class="px-4 py-3 text-left bg-gray-50 border-b border-gray-200 whitespace-nowrap" style="width: 160px;">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-medium text-gray-600">Vector</span>
                <span class="text-xs text-gray-400">vector</span>
              </div>
              <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full" style="width: 100%"></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">384-dim</div>
            </th>
          </tr>
        </thead>
      </table>
    </div>

    <!-- Table View -->
    <div v-if="viewMode === 'table'" class="border border-gray-200 rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full divide-y divide-gray-200" style="table-layout: fixed; min-width: 1160px;">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 whitespace-nowrap" style="width: 140px;" @click="sortBy('id')">
                <div class="flex items-center space-x-1">
                  <span>ID</span>
                  <span v-if="sortColumn === 'id'" class="text-dc-primary">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
                </div>
                <div class="text-xs text-gray-400 font-normal normal-case">string</div>
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 whitespace-nowrap" style="width: 160px;" @click="sortBy('timestamp')">
                <div class="flex items-center space-x-1">
                  <span>Timestamp</span>
                  <span v-if="sortColumn === 'timestamp'" class="text-dc-primary">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
                </div>
                <div class="text-xs text-gray-400 font-normal normal-case">datetime</div>
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 whitespace-nowrap" style="width: 160px;" @click="sortBy('location')">
                <div class="flex items-center space-x-1">
                  <span>Location</span>
                  <span v-if="sortColumn === 'location'" class="text-dc-primary">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
                </div>
                <div class="text-xs text-gray-400 font-normal normal-case">lat, lon</div>
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100" style="width: 280px;" @click="sortBy('description')">
                <div class="flex items-center space-x-1">
                  <span>Description</span>
                  <span v-if="sortColumn === 'description'" class="text-dc-primary">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
                </div>
                <div class="text-xs text-gray-400 font-normal normal-case">text</div>
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 whitespace-nowrap" style="width: 120px;" @click="sortBy('image')">
                <div class="flex items-center space-x-1">
                  <span>Image</span>
                  <span v-if="sortColumn === 'image'" class="text-dc-primary">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
                </div>
                <div class="text-xs text-gray-400 font-normal normal-case">camera</div>
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 whitespace-nowrap" style="width: 140px;" @click="sortBy('semantic_objects')">
                <div class="flex items-center space-x-1">
                  <span>Objects</span>
                  <span v-if="sortColumn === 'semantic_objects'" class="text-dc-primary">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
                </div>
                <div class="text-xs text-gray-400 font-normal normal-case">semantic</div>
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 whitespace-nowrap" style="width: 160px;" @click="sortBy('semantic_vector')">
                <div class="flex items-center space-x-1">
                  <span>Vector</span>
                  <span v-if="sortColumn === 'semantic_vector'" class="text-dc-primary">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
                </div>
                <div class="text-xs text-gray-400 font-normal normal-case">384-dim</div>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="row in paginatedData" :key="row.id" class="hover:bg-gray-50 transition-colors">
              <!-- ID Column -->
              <td class="px-4 py-3 whitespace-nowrap text-xs font-mono text-gray-600 truncate" style="width: 140px;">
                {{ row.id }}
              </td>

              <!-- Timestamp Column -->
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900" style="width: 160px;">
                <div class="flex items-center space-x-1">
                  <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{{ formatTimestamp(row.timestamp) }}</span>
                </div>
              </td>

              <!-- Location Column -->
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900" style="width: 160px;">
                <div class="flex items-center space-x-1">
                  <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <div>
                    <div class="text-sm">{{ row.location.region }}</div>
                    <div class="text-xs text-gray-500">{{ row.location.lat.toFixed(4) }}, {{ row.location.lon.toFixed(4) }}</div>
                  </div>
                </div>
              </td>

              <!-- Description Column -->
              <td class="px-4 py-3 text-sm text-gray-700" style="width: 280px;">
                <div class="line-clamp-2" :title="row.description">{{ row.description }}</div>
              </td>

              <!-- Image Column -->
              <td class="px-4 py-3 whitespace-nowrap" style="width: 120px;">
                <div class="relative group">
                  <img
                    :src="row.imageUrl"
                    :alt="row.id"
                    class="w-24 h-16 object-cover rounded-lg cursor-pointer hover:opacity-90 transition-opacity"
                    @click="openImageModal(row)"
                    @error="handleImageError($event, row)"
                  />
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 rounded-lg flex items-center justify-center transition-all pointer-events-none">
                    <svg class="w-6 h-6 text-white opacity-0 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
              </td>

              <!-- Semantic Objects Column -->
              <td class="px-4 py-3 whitespace-nowrap" style="width: 140px;">
                <div class="flex flex-wrap gap-1">
                  <span v-for="obj in row.semantic.objects.slice(0, 3)" :key="obj"
                    class="text-xs bg-purple-50 text-purple-700 px-2 py-0.5 rounded"
                  >
                    {{ obj }}
                  </span>
                  <span v-if="row.semantic.objects.length > 3" class="text-xs text-gray-400">
                    +{{ row.semantic.objects.length - 3 }}
                  </span>
                </div>
              </td>

              <!-- Semantic Vector Column -->
              <td class="px-4 py-3 whitespace-nowrap" style="width: 160px;">
                <div class="text-xs font-mono text-gray-600 truncate" :title="formatVector(row.semantic.vector)">
                  {{ formatVector(row.semantic.vector) }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="px-4 py-3 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-500">
          Showing {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, filteredData.length) }} of {{ filteredData.length }} rows
        </div>
        <div class="flex items-center space-x-2">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span class="text-sm text-gray-600">Page {{ currentPage }} of {{ totalPages }}</span>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Grid View -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <div v-for="row in paginatedData" :key="row.id" 
        class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
        @click="openImageModal(row)"
      >
        <div class="relative aspect-video">
          <img
            :src="row.imageUrl"
            :alt="row.id"
            class="w-full h-full object-cover"
            @error="handleImageError($event, row)"
          />
          <div class="absolute top-2 left-2 bg-black bg-opacity-50 text-white text-xs px-2 py-1 rounded">
            {{ formatTimestamp(row.timestamp) }}
          </div>
          <div class="absolute top-2 right-2 bg-green-600 bg-opacity-80 text-white text-xs px-2 py-1 rounded flex items-center space-x-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            </svg>
            <span>{{ row.location.region }}</span>
          </div>
        </div>
        <div class="p-3">
          <p class="text-sm text-gray-700 line-clamp-2 mb-2">{{ row.description }}</p>
          <div class="flex flex-wrap gap-1">
            <span v-for="obj in row.semantic.objects.slice(0, 4)" :key="obj"
              class="text-xs bg-purple-50 text-purple-700 px-2 py-0.5 rounded"
            >
              {{ obj }}
            </span>
          </div>
          <div class="mt-2 flex items-center justify-between">
            <div class="text-xs font-mono text-gray-500 truncate max-w-[150px]" :title="formatVector(row.semantic.vector)">
              {{ formatVector(row.semantic.vector) }}
            </div>
            <span class="text-xs text-gray-400 font-mono">{{ row.id.slice(-8) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="selectedRow" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" @click.self="selectedRow = null">
      <div class="bg-white rounded-xl max-w-5xl w-full max-h-[90vh] overflow-auto">
        <div class="relative">
          <img
            :src="selectedRow.imageUrl"
            :alt="selectedRow.id"
            class="w-full object-contain max-h-[60vh]"
            @error="handleImageError($event, selectedRow)"
          />
          <button @click="selectedRow = null" class="absolute top-4 right-4 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-70">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Sample {{ selectedRow.id }}</h3>
              <p class="text-sm text-gray-500 mt-1">{{ selectedRow.description }}</p>
            </div>
            <div class="text-right">
              <div class="flex items-center space-x-2 text-sm text-gray-600">
                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ formatTimestamp(selectedRow.timestamp) }}</span>
              </div>
              <div class="flex items-center space-x-2 text-sm text-gray-600 mt-1">
                <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                </svg>
                <span>{{ selectedRow.location.lat.toFixed(6) }}, {{ selectedRow.location.lon.toFixed(6) }}</span>
              </div>
            </div>
          </div>
          
          <div class="mt-4 grid grid-cols-2 gap-4">
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Semantic Objects</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="obj in selectedRow.semantic.objects" :key="obj"
                  class="text-sm bg-purple-50 text-purple-700 px-3 py-1 rounded-full"
                >
                  {{ obj }}
                </span>
              </div>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Scene Attributes</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="attr in selectedRow.semantic.attributes" :key="attr"
                  class="text-sm bg-blue-50 text-blue-700 px-3 py-1 rounded-full"
                >
                  {{ attr }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="mt-4">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Semantic Vector (384-dim)</h4>
            <div class="bg-gray-50 rounded-lg p-3 overflow-auto">
              <code class="text-xs font-mono text-gray-700 break-all">{{ formatVector(selectedRow.semantic.vector, 10) }}</code>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { generateAutodrivingData } from '@/data/datasets.js'

const props = defineProps({
  datasetId: { type: String, required: true }
})

// State
const showSplitDropdown = ref(false)
const selectedSplit = ref('train')
const viewMode = ref('table')
const searchQuery = ref('')
const searchType = ref('all')
const currentPage = ref(1)
const pageSize = ref(10)
const sortColumn = ref('timestamp')
const sortDirection = ref('desc')
const selectedRow = ref(null)

// Generate mock data
const allData = computed(() => generateAutodrivingData(props.datasetId))

const splits = [
  { name: 'train', rows: 850000 },
  { name: 'validation', rows: 50000 },
  { name: 'test', rows: 50000 }
]

const columns = [
  { key: 'id', label: 'ID', subLabel: 'string' },
  { key: 'timestamp', label: 'Timestamp', subLabel: 'datetime' },
  { key: 'location', label: 'Location', subLabel: 'lat, lon' },
  { key: 'description', label: 'Description', subLabel: 'text' },
  { key: 'image', label: 'Image', subLabel: 'camera' },
  { key: 'semantic_objects', label: 'Objects', subLabel: 'semantic' },
  { key: 'semantic_vector', label: 'Vector', subLabel: '384-dim' }
]

const columnStats = computed(() => [
  {
    name: 'id', label: 'ID', type: 'string',
    visualization: 'progress', progress: 100,
    stats: 'unique'
  },
  {
    name: 'timestamp', label: 'Timestamp', type: 'datetime',
    visualization: 'histogram', distribution: [30, 45, 60, 80, 100, 85, 70, 50, 35, 25],
    stats: '2025-01 ~ 2025-03'
  },
  {
    name: 'location', label: 'Location', type: 'geo',
    visualization: 'range', min: '1.2°N', max: '42.4°N',
    stats: 'Boston, Singapore'
  },
  {
    name: 'description', label: 'Description', type: 'text',
    visualization: 'progress', progress: 100,
    stats: 'avg 156 chars'
  },
  {
    name: 'image', label: 'Image', type: 'image',
    visualization: 'progress', progress: 100,
    stats: '1600×900'
  },
  {
    name: 'semantic_objects', label: 'Objects', type: 'semantic',
    visualization: 'histogram', distribution: [20, 40, 60, 80, 100, 90, 70, 50, 30, 20],
    stats: '8 classes'
  },
  {
    name: 'semantic_vector', label: 'Vector', type: 'vector',
    visualization: 'progress', progress: 100,
    stats: '384-dim'
  }
])

// Filter and sort data
const filteredData = computed(() => {
  let data = allData.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    data = data.filter(row => {
      // Search based on selected type
      if (searchType.value === 'temporal' || searchType.value === 'all') {
        if (row.timestamp.includes(query)) return true
      }
      if (searchType.value === 'spatial' || searchType.value === 'all') {
        if (row.location.region.toLowerCase().includes(query)) return true
        if (row.location.lat.toString().includes(query)) return true
        if (row.location.lon.toString().includes(query)) return true
      }
      if (searchType.value === 'semantic' || searchType.value === 'all') {
        if (row.description.toLowerCase().includes(query)) return true
        if (row.semantic.objects.some(o => o.toLowerCase().includes(query))) return true
        if (row.semantic.attributes.some(a => a.toLowerCase().includes(query))) return true
      }
      if (searchType.value === 'vector' || searchType.value === 'all') {
        // Vector semantic search simulation
        const queryWords = query.split(/\s+/)
        const semanticText = [...row.semantic.objects, ...row.semantic.attributes].join(' ').toLowerCase()
        if (queryWords.some(w => semanticText.includes(w))) return true
      }
      return false
    })
  }
  
  // Sort
  data = [...data].sort((a, b) => {
    let aVal, bVal
    switch (sortColumn.value) {
      case 'timestamp':
        aVal = new Date(a.timestamp)
        bVal = new Date(b.timestamp)
        break
      case 'location':
        aVal = a.location.region
        bVal = b.location.region
        break
      default:
        aVal = a[sortColumn.value]
        bVal = b[sortColumn.value]
    }
    
    if (sortDirection.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })
  
  return data
})

const totalPages = computed(() => Math.ceil(filteredData.value.length / pageSize.value))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

// Methods
function selectSplit(split) {
  selectedSplit.value = split.name
  showSplitDropdown.value = false
  currentPage.value = 1
}

function sortBy(column) {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
}

function formatTimestamp(ts) {
  const date = new Date(ts)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatRows(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return n.toString()
}

function formatVector(vector, maxItems = 5) {
  if (!vector || vector.length === 0) return '[]'
  const items = vector.slice(0, maxItems).map(v => v.toFixed(2))
  if (vector.length > maxItems) {
    return `[${items.join(', ')}, ...]`
  }
  return `[${items.join(', ')}]`
}

function openImageModal(row) {
  selectedRow.value = row
}

function handleImageError(event, row) {
  // Fallback to a colored placeholder with object labels
  const objects = row?.semantic?.objects || ['scene']
  const objectLabels = objects.slice(0, 2).map(obj => obj.charAt(0).toUpperCase() + obj.slice(1)).join('+')
  const label = encodeURIComponent(objectLabels || 'Scene')
  
  // Generate a deterministic background color based on the first object
  const objectColors = {
    'bus': 'FF6B35',
    'motorcycle': '4ECDC4',
    'truck': '95E1D3',
    'car': 'F38181',
    'pedestrian': 'AA96DA',
    'cyclist': 'FCBAD3',
    'traffic-cone': 'F39422',
    'barrier': 'A8D8EA'
  }
  const primaryObject = objects[0] || 'scene'
  const bgColor = objectColors[primaryObject] || '6C757D'
  
  event.target.src = `https://placehold.co/400x225/${bgColor}/FFFFFF?text=${label}&font=roboto`
}

// Reset page when search changes
watch(searchQuery, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>