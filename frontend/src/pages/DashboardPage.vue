<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md">
      <div class="row items-center justify-between">
        <div>
          <div class="text-h4">Analytics Dashboard</div>
          <div class="text-subtitle1 text-grey-7">
            Comprehensive analysis of your error logs
          </div>
        </div>
        <div class="q-gutter-sm">
          <ExportMenu 
            :data="exportData" 
            v-if="hasData"
          />
          <q-btn 
            outline 
            color="primary" 
            icon="refresh" 
            label="Refresh Data"
            @click="loadDashboardData"
            :loading="loading"
          />
          <q-btn 
            color="primary" 
            icon="upload" 
            label="Upload More"
            to="/upload"
          />
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center q-pa-xl">
      <q-spinner-dots size="50px" color="primary" />
      <div class="text-h6 q-mt-md">Loading analytics...</div>
    </div>

    <!-- No Data State -->
    <div v-else-if="!hasData" class="text-center q-pa-xl">
      <q-icon name="info" size="64px" color="grey-5" />
      <div class="text-h6 q-mt-md">No data available</div>
      <div class="text-subtitle1 text-grey-7 q-mb-md">
        Upload some log files to see analytics
      </div>
      <q-btn color="primary" icon="upload" label="Upload Files" to="/upload" />
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Advanced Filters -->
      <AdvancedFilters 
        v-model="advancedFilters"
        :errors="errorTableData"
        @filter="handleFilterUpdate"
      />
      
      <!-- Summary Cards -->
      <div class="row q-gutter-md q-mb-lg">
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="ams-stat-card">
            <q-card-section class="q-pa-lg">
              <div class="row items-center">
                <div class="col">
                  <div class="text-caption text-grey-7 text-uppercase">Total Errors</div>
                  <div class="text-h3 text-weight-light q-mt-sm">{{ filteredSummaryStats.totalErrors.toLocaleString() }}</div>
                  <q-chip size="sm" color="grey-3" text-color="grey-8" class="q-mt-sm">
                    <q-icon name="trending_up" size="16px" class="q-mr-xs" />
                    All logged errors
                  </q-chip>
                </div>
                <div class="col-auto">
                  <div class="ams-icon-box bg-negative">
                    <q-icon name="error_outline" size="32px" color="white" />
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="ams-stat-card">
            <q-card-section class="q-pa-lg">
              <div class="row items-center">
                <div class="col">
                  <div class="text-caption text-grey-7 text-uppercase">Critical Errors</div>
                  <div class="text-h3 text-weight-light q-mt-sm">{{ filteredSummaryStats.criticalErrors.toLocaleString() }}</div>
                  <q-chip size="sm" color="red-1" text-color="red-9" class="q-mt-sm">
                    <q-icon name="warning" size="16px" class="q-mr-xs" />
                    High priority
                  </q-chip>
                </div>
                <div class="col-auto">
                  <div class="ams-icon-box bg-warning">
                    <q-icon name="warning_amber" size="32px" color="white" />
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="ams-stat-card">
            <q-card-section class="q-pa-lg">
              <div class="row items-center">
                <div class="col">
                  <div class="text-caption text-grey-7 text-uppercase">Active Users</div>
                  <div class="text-h3 text-weight-light q-mt-sm">{{ filteredSummaryStats.activeUsers.toLocaleString() }}</div>
                  <q-chip size="sm" color="blue-1" text-color="blue-9" class="q-mt-sm">
                    <q-icon name="people" size="16px" class="q-mr-xs" />
                    Affected users
                  </q-chip>
                </div>
                <div class="col-auto">
                  <div class="ams-icon-box bg-info">
                    <q-icon name="group" size="32px" color="white" />
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="ams-stat-card">
            <q-card-section class="q-pa-lg">
              <div class="row items-center">
                <div class="col">
                  <div class="text-caption text-grey-7 text-uppercase">Files Analyzed</div>
                  <div class="text-h3 text-weight-light q-mt-sm">{{ filteredSummaryStats.filesAnalyzed.toLocaleString() }}</div>
                  <q-chip size="sm" color="green-1" text-color="green-9" class="q-mt-sm">
                    <q-icon name="check_circle" size="16px" class="q-mr-xs" />
                    Processed
                  </q-chip>
                </div>
                <div class="col-auto">
                  <div class="ams-icon-box bg-positive">
                    <q-icon name="folder_open" size="32px" color="white" />
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
    </div>

    <!-- Timeline Analysis -->
    <div class="q-mb-md">
      <TimelineAnalysis 
        :errors="masterFilteredData"
        @update:filtered-data="handleTimelineFilter"
      />
    </div>

    <!-- Charts Row -->
    <div class="row q-gutter-md q-mb-md">
      <!-- Error Types Distribution -->
      <div class="col-12 col-lg-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">Error Types</div>
            <div class="text-caption text-grey-7">
              Distribution of error codes
            </div>
          </q-card-section>
          <q-card-section>
            <div class="chart-container" style="height: 300px;">
              <canvas ref="errorTypesChart"></canvas>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- User Activity and Critical Errors -->
    <div class="row q-gutter-md q-mb-md">
      <!-- User Activity Heatmap -->
      <div class="col-12 col-lg-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">User Activity</div>
            <div class="text-caption text-grey-7">
              Error frequency by user
            </div>
          </q-card-section>
          <q-card-section>
            <div class="chart-container" style="height: 300px;">
              <canvas ref="userActivityChart"></canvas>
            </div>
          </q-card-section>
        </q-card>
      </div>
      
      <!-- Critical Errors Alert -->
      <div class="col-12 col-lg-6">
        <q-card>
          <q-card-section>
            <div class="text-h6">Critical Errors Alert</div>
            <div class="text-caption text-grey-7">
              High-priority errors requiring attention
            </div>
          </q-card-section>
          <q-card-section>
            <q-list>
              <q-item
                v-for="error in filteredCriticalErrors"
                :key="error.id"
                class="q-mb-sm cursor-pointer"
                clickable
                @click="showErrorDetail(error)"
              >
                <q-item-section avatar>
                  <q-icon name="warning" color="negative" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ error.type }}</q-item-label>
                  <q-item-label caption>
                    {{ error.user }} • {{ error.timestamp }}
                  </q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-chip color="negative" text-color="white" size="sm">
                    Code {{ error.code }}
                  </q-chip>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Machine Learning Analysis Section -->
    <div class="row q-gutter-md q-mb-md">
      <!-- User Risk Heatmap -->
      <div class="col-12 col-lg-6">
        <UserRiskHeatmap />
      </div>
      
      <!-- Root Cause Suggestions -->
      <div class="col-12 col-lg-6">
        <RootCauseSuggestions 
          @filter-dashboard="handleRootCauseFilter"
          @show-root-cause-details="showRootCauseDetails"
          @find-similar-patterns="findSimilarPatterns"
        />
      </div>
    </div>

    <!-- Data Table -->
    <q-card>
      <q-card-section>
        <div class="text-h6 q-mb-md">Detailed Error Log</div>
        
        <q-table
          :rows="masterFilteredData"
          :columns="errorTableColumns"
          row-key="id"
          :pagination="{ rowsPerPage: 10 }"
          :filter="filter"
          :filter-method="customFilter"
          binary-state-sort
          :loading="loading"
          @row-click="(evt, row) => showErrorDetail(row)"
          class="cursor-pointer"
        >
          <template v-slot:top-right>
            <q-input
              dense
              debounce="300"
              v-model="filter"
              placeholder="Search errors..."
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          
          <template v-slot:body-cell-severity="props">
            <q-td :props="props">
              <q-chip
                :color="getSeverityColor(props.value)"
                text-color="white"
                size="sm"
              >
                {{ props.value }}
              </q-chip>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
    </div>

    <!-- Error Detail Modal -->
    <ErrorDetailModal 
      v-model="showErrorModal" 
      :error="selectedError"
      @error-selected="handleErrorSelected"
    />

    <!-- Root Cause Detail Modal -->
    <RootCauseDetailModal 
      v-model="showRootCauseModal" 
      :root-cause="selectedRootCause"
      :related-errors="getRelatedErrors(selectedRootCause)"
      @filter-dashboard="handleRootCauseFilter"
      @error-selected="handleErrorSelected"
    />

    <!-- Similar Patterns Modal -->
    <SimilarPatternsModal 
      v-model="showSimilarPatternsModal" 
      :root-cause="selectedRootCause"
      @filter-dashboard="handleRootCauseFilter"
      @view-pattern="handlePatternView"
    />
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { useQuasar } from 'quasar'
import ErrorDetailModal from '@/components/ErrorDetailModal.vue'
import ExportMenu from '@/components/ExportMenu.vue'
import AdvancedFilters from '@/components/AdvancedFilters.vue'
import TimelineAnalysis from '@/components/TimelineAnalysis.vue'
import UserRiskHeatmap from '@/components/UserRiskHeatmap.vue'
import RootCauseSuggestions from '@/components/RootCauseSuggestions.vue'
import RootCauseDetailModal from '@/components/RootCauseDetailModal.vue'
import SimilarPatternsModal from '@/components/SimilarPatternsModal.vue'
import { 
  getErrorSummary, 
  getErrors, 
  getErrorTimeline, 
  getErrorTypes, 
  getUserActivity, 
  getCriticalErrors 
} from '@/services/api'

// Register Chart.js components
Chart.register(...registerables)

const $q = useQuasar()

// Chart refs
const errorTypesChart = ref<HTMLCanvasElement>()
const userActivityChart = ref<HTMLCanvasElement>()

// Chart instances
let errorTypesChartInstance: Chart | null = null
let userActivityChartInstance: Chart | null = null

// Data
const loading = ref(false)
const filter = ref('')
const dashboardData = ref<any>(null)

// Root cause investigation
const showRootCauseModal = ref(false)
const selectedRootCause = ref<any>(null)
const showSimilarPatternsModal = ref(false)

const summaryStats = ref({
  totalErrors: 0,
  criticalErrors: 0,
  activeUsers: 0,
  filesAnalyzed: 0
})

const criticalErrors = ref<any[]>([])

// Error detail modal
const showErrorModal = ref(false)
const selectedError = ref<any>(null)

// Export data computed
const exportData = computed(() => ({
  errors: filteredTableData.value,
  summary: summaryStats.value,
  filters: advancedFilters.value
}))

// Advanced filters
const advancedFilters = ref({
  search: '',
  users: [],
  severities: [],
  errorTypes: [],
  dateFrom: '',
  dateTo: ''
})

const filteredTableData = ref<any[]>([])
const advancedFilterActive = ref(false)

// Master filtered data that affects all components
const masterFilteredData = computed(() => {
  // Start with base data
  let data = errorTableData.value
  
  // Apply advanced filters first if active
  if (advancedFilterActive.value && filteredTableData.value.length > 0) {
    data = filteredTableData.value
  }
  
  // Apply search filter on top
  if (filter.value) {
    data = data.filter(error => 
      error.type && error.type.toLowerCase().includes(filter.value.toLowerCase())
    )
  }
  
  return data
})

// Computed data for all components based on filtered data
const filteredSummaryStats = computed(() => {
  const data = masterFilteredData.value
  const criticalErrors = data.filter(e => e.severity === 'Critical')
  const uniqueUsers = [...new Set(data.map(e => e.user))]
  
  return {
    totalErrors: data.length,
    criticalErrors: criticalErrors.length,
    activeUsers: uniqueUsers.length,
    filesAnalyzed: summaryStats.value.filesAnalyzed // This stays the same
  }
})

const filteredErrorTypes = computed(() => {
  const data = masterFilteredData.value
  const typeCounts: Record<string, number> = {}
  
  data.forEach(error => {
    if (error.type) {
      typeCounts[error.type] = (typeCounts[error.type] || 0) + 1
    }
  })
  
  const sorted = Object.entries(typeCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
  
  return {
    labels: sorted.map(([type]) => type),
    data: sorted.map(([, count]) => count)
  }
})

const filteredUserActivity = computed(() => {
  const data = masterFilteredData.value
  const userCounts: Record<string, number> = {}
  
  data.forEach(error => {
    if (error.user) {
      userCounts[error.user] = (userCounts[error.user] || 0) + 1
    }
  })
  
  const sorted = Object.entries(userCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
  
  return {
    labels: sorted.map(([user]) => user),
    data: sorted.map(([, count]) => count)
  }
})

const filteredCriticalErrors = computed(() => {
  return masterFilteredData.value
    .filter(e => e.severity === 'Critical')
    .slice(0, 10)
})

// Filter handler from AdvancedFilters component
function handleFilterUpdate(filteredData: any[]) {
  advancedFilterActive.value = filteredData.length > 0 && filteredData.length < errorTableData.value.length
  filteredTableData.value = filteredData
}

// Timeline filter handler
function handleTimelineFilter(filteredData: any[]) {
  // Don't update filteredTableData here to avoid conflicts
  // Timeline filtering should work independently
}

// Update all charts when filters change
function updateAllCharts() {
  nextTick(() => {
    updateChartData()
  })
}
const hasData = computed(() => dashboardData.value !== null && summaryStats.value.totalErrors > 0)

const errorTableColumns = [
  {
    name: 'timestamp',
    label: 'Timestamp',
    field: 'timestamp',
    sortable: true,
    align: 'left'
  },
  {
    name: 'user',
    label: 'User',
    field: 'user',
    sortable: true,
    align: 'left'
  },
  {
    name: 'type',
    label: 'Error Type',
    field: 'type',
    sortable: true,
    align: 'left'
  },
  {
    name: 'code',
    label: 'Code',
    field: 'code',
    sortable: true,
    align: 'center'
  },
  {
    name: 'severity',
    label: 'Severity',
    field: 'severity',
    sortable: true,
    align: 'center'
  }
]

const errorTableData = ref<any[]>([])

// Methods
function getSeverityColor(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'critical': return 'negative'
    case 'high': return 'orange'
    case 'medium': return 'warning'
    case 'low': return 'positive'
    default: return 'grey'
  }
}

// Error detail functions
function showErrorDetail(error: any) {
  selectedError.value = error
  showErrorModal.value = true
}

function handleErrorSelected(error: any) {
  selectedError.value = error
  showErrorModal.value = true
}

// Custom filter method for the table
function customFilter(rows: any[], terms: string) {
  if (!terms) return rows
  
  const lowerTerms = terms.toLowerCase()
  return rows.filter(row => {
    // Search in all relevant fields
    return (
      row.type?.toLowerCase().includes(lowerTerms) ||
      row.user?.toLowerCase().includes(lowerTerms) ||
      row.timestamp?.toLowerCase().includes(lowerTerms) ||
      row.severity?.toLowerCase().includes(lowerTerms) ||
      row.filename?.toLowerCase().includes(lowerTerms) ||
      row.code?.toString().includes(lowerTerms)
    )
  })
}

function updateChartData() {
  // Update Error Types Chart
  if (errorTypesChartInstance) {
    errorTypesChartInstance.data.labels = filteredErrorTypes.value.labels
    errorTypesChartInstance.data.datasets[0].data = filteredErrorTypes.value.data
    errorTypesChartInstance.update()
  }
  
  // Update User Activity Chart
  if (userActivityChartInstance) {
    userActivityChartInstance.data.labels = filteredUserActivity.value.labels
    userActivityChartInstance.data.datasets[0].data = filteredUserActivity.value.data
    userActivityChartInstance.update()
  }
}

function initializeCharts() {
  if (!dashboardData.value) return

  // Destroy existing charts
  if (errorTypesChartInstance) {
    errorTypesChartInstance.destroy()
  }
  if (userActivityChartInstance) {
    userActivityChartInstance.destroy()
  }

  // Error Types Chart (with click interaction)
  if (errorTypesChart.value && filteredErrorTypes.value) {
    errorTypesChartInstance = new Chart(errorTypesChart.value, {
      type: 'doughnut',
      data: {
        labels: filteredErrorTypes.value.labels,
        datasets: [{
          data: filteredErrorTypes.value.data,
          backgroundColor: ['#003d7a', '#0066cc', '#00a8e1', '#4caf50', '#ff9800']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index
            const errorType = filteredErrorTypes.value.labels[index]
            filterByErrorType(errorType)
          }
        }
      }
    })
  }

  // User Activity Chart
  if (userActivityChart.value && filteredUserActivity.value) {
    userActivityChartInstance = new Chart(userActivityChart.value, {
      type: 'bar',
      data: {
        labels: filteredUserActivity.value.labels,
        datasets: [{
          label: 'Error Count',
          data: filteredUserActivity.value.data,
          backgroundColor: '#0066cc'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }
}

// Filter table by error type (pie chart interaction)
function filterByErrorType(errorType: string) {
  // Toggle filter if clicking the same type
  if (filter.value === errorType) {
    filter.value = ''
    $q.notify({
      type: 'info',
      message: 'Filter cleared',
      timeout: 2000
    })
  } else {
    filter.value = errorType
    $q.notify({
      type: 'info',
      message: `Filtering by: ${errorType}`,
      timeout: 2000
    })
  }
}

// Load dashboard data from API
async function loadDashboardData() {
  loading.value = true
  console.log('Loading dashboard data...')
  
  try {
    // Fetch all data in parallel for better performance
    console.log('Fetching data from APIs...')
    const [
      summaryData,
      errorsData,
      timelineData,
      typesData,
      usersData,
      criticalData
    ] = await Promise.all([
      getErrorSummary(),
      getErrors(1, 1000), // Get first 1000 errors
      getErrorTimeline(),
      getErrorTypes(),
      getUserActivity(),
      getCriticalErrors()
    ])
    
    console.log('Received data:', { summaryData, errorsData, timelineData, typesData, usersData, criticalData })
    
    // Update reactive data
    summaryStats.value = {
      totalErrors: summaryData.total_errors || 0,
      criticalErrors: summaryData.critical_errors || 0,
      activeUsers: summaryData.active_users || 0,
      filesAnalyzed: summaryData.files_analyzed || 0
    }
    
    errorTableData.value = errorsData.errors || []
    filteredTableData.value = [] // Clear filtered data on fresh load
    advancedFilterActive.value = false
    criticalErrors.value = criticalData.critical_errors || []
    
    dashboardData.value = {
      timeline: timelineData,
      errorTypes: typesData,
      userActivity: usersData
    }
    
    // Initialize charts with new data
    setTimeout(initializeCharts, 100)
    
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load dashboard data. Please check your connection.',
      timeout: 5000
    })
    
    // Fallback to demo data if API fails
    loadDemoData()
  } finally {
    loading.value = false
  }
}

// Load demo data as fallback
function loadDemoData() {
  summaryStats.value = {
    totalErrors: 156,
    criticalErrors: 23,
    activeUsers: 12,
    filesAnalyzed: 45
  }
  
  errorTableData.value = [
    {
      id: 1,
      timestamp: '02.12.2024 12:54:19',
      user: 'GAM',
      type: 'DATA TYPE ERROR',
      code: 33,
      severity: 'Medium'
    },
    {
      id: 2,
      timestamp: '26.06.2025 10:35:29',
      user: 'SWE',
      type: 'BOUND ERROR',
      code: 2,
      severity: 'High'
    }
  ]
  
  criticalErrors.value = [
    {
      id: 1,
      type: 'ACCESS VIOLATION',
      user: 'GAM',
      timestamp: '02.12.2024 12:54:19',
      code: 50
    },
    {
      id: 2,
      type: 'DATA TYPE ERROR',
      user: 'SWE',
      timestamp: '26.06.2025 10:35:29',
      code: 33
    }
  ]
  
  dashboardData.value = {
    timeline: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      data: [12, 19, 3, 5, 2, 3]
    },
    errorTypes: {
      labels: ['DATA TYPE ERROR', 'BOUND ERROR', 'ACCESS VIOLATION'],
      data: [45, 30, 25]
    },
    userActivity: {
      labels: ['GAM', 'SWE', 'AVB', 'MSP', 'JAE'],
      data: [15, 8, 6, 4, 3]
    }
  }
  
  setTimeout(initializeCharts, 100)
}

// Root cause investigation handlers
function handleRootCauseFilter(rootCauseFilter: any) {
  // Apply the filter from root cause to advanced filters
  advancedFilters.value = {
    ...advancedFilters.value,
    users: rootCauseFilter.users || [],
    severities: rootCauseFilter.severities || [],
    errorTypes: rootCauseFilter.errorTypes || [],
    search: rootCauseFilter.search || ''
  }
  
  // If there's a specific time mentioned, add it to search
  if (rootCauseFilter.specificTime) {
    advancedFilters.value.search = rootCauseFilter.specificTime
  }
  
  // Trigger filter update
  let filteredData = errorTableData.value
  
  // Apply user filter
  if (rootCauseFilter.users && rootCauseFilter.users.length > 0) {
    filteredData = filteredData.filter(error => 
      rootCauseFilter.users.includes(error.user)
    )
  }
  
  // Apply severity filter
  if (rootCauseFilter.severities && rootCauseFilter.severities.length > 0) {
    filteredData = filteredData.filter(error => 
      rootCauseFilter.severities.includes(error.severity)
    )
  }
  
  // Apply error type filter
  if (rootCauseFilter.errorTypes && rootCauseFilter.errorTypes.length > 0) {
    filteredData = filteredData.filter(error => 
      rootCauseFilter.errorTypes.some(type => 
        error.type && error.type.includes(type)
      )
    )
  }
  
  // Apply search filter
  if (rootCauseFilter.search) {
    filteredData = filteredData.filter(error => 
      error.timestamp && error.timestamp.includes(rootCauseFilter.search)
    )
  }
  
  // Update filtered data
  handleFilterUpdate(filteredData)
  
  $q.notify({
    type: 'positive',
    message: `Filter applied: Found ${filteredData.length} related errors`,
    timeout: 3000
  })
}

function showRootCauseDetails(cause: any) {
  selectedRootCause.value = cause
  showRootCauseModal.value = true
}

function findSimilarPatterns(cause: any) {
  selectedRootCause.value = cause
  showSimilarPatternsModal.value = true
}

function getRelatedErrors(rootCause: any) {
  if (!rootCause || !errorTableData.value) return []
  
  // Filter errors related to the root cause
  return errorTableData.value.filter(error => {
    // Match based on root cause type and content
    if (rootCause.type === 'User Pattern') {
      const userMatch = rootCause.title.match(/^(\w+):/)
      if (userMatch && error.user === userMatch[1]) return true
    }
    
    if (rootCause.type === 'System Correlation') {
      const errorTypeMatch = rootCause.description.match(/(DATA TYPE ERROR|ACCESS VIOLATION|BOUND ERROR)/i)
      if (errorTypeMatch && error.type && error.type.includes(errorTypeMatch[1])) return true
    }
    
    if (rootCause.type === 'Resource Issue') {
      if (error.severity === 'Critical') return true
    }
    
    return false
  }).slice(0, 20) // Limit to 20 related errors
}

function handlePatternView(pattern: any) {
  $q.notify({
    type: 'info',
    message: `Viewing pattern: ${pattern.title}`,
    timeout: 2000
  })
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped lang="scss">
.chart-container {
  position: relative;
}

// AMS Dashboard Card Styles
.ams-stat-card {
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  
  .ams-icon-box {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.9;
  }
}

// Chart Cards
.q-card {
  border-radius: 12px;
  border: none;
  
  .q-card__section {
    &:first-child {
      border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }
  }
}

// Table Styling
.q-table {
  border-radius: 12px;
  
  th {
    background: #f8f9fa;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    color: #6c757d;
  }
  
  tbody tr {
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover {
      background: rgba(0, 61, 122, 0.04);
    }
  }
}

// Page Background - Light Mode
.body--light .q-page {
  background: #f5f5f5;
}

// Page Background - Dark Mode
.body--dark .q-page {
  background: #1a1a1a;
  
  .text-h4, .text-subtitle1 {
    color: #e0e0e0;
  }
  
  .text-grey-7 {
    color: #b0b0b0 !important;
  }
  
  // Dark mode card styles
  .ams-stat-card {
    background: #2a2a2a !important;
    color: #e0e0e0;
    
    .text-caption {
      color: #b0b0b0 !important;
    }
    
    .text-h3 {
      color: #ffffff !important;
    }
  }
  
  .q-card {
    background: #2a2a2a !important;
    color: #e0e0e0;
    
    .text-h6 {
      color: #ffffff !important;
    }
    
    .text-caption {
      color: #b0b0b0 !important;
    }
  }
}
</style>