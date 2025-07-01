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
      <!-- Summary Cards -->
      <div class="row q-gutter-md q-mb-md">
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="text-center">
            <q-card-section>
              <q-icon name="error" size="48px" color="negative" />
              <div class="text-h4 q-mt-md">{{ summaryStats.totalErrors }}</div>
              <div class="text-subtitle2">Total Errors</div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="text-center">
            <q-card-section>
              <q-icon name="warning" size="48px" color="orange" />
              <div class="text-h4 q-mt-md">{{ summaryStats.criticalErrors }}</div>
              <div class="text-subtitle2">Critical Errors</div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="text-center">
            <q-card-section>
              <q-icon name="person" size="48px" color="info" />
              <div class="text-h4 q-mt-md">{{ summaryStats.activeUsers }}</div>
              <div class="text-subtitle2">Active Users</div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-sm-6 col-md-3">
          <q-card class="text-center">
            <q-card-section>
              <q-icon name="description" size="48px" color="secondary" />
              <div class="text-h4 q-mt-md">{{ summaryStats.filesAnalyzed }}</div>
              <div class="text-subtitle2">Files Analyzed</div>
            </q-card-section>
          </q-card>
        </div>
    </div>

    <!-- Charts Row -->
    <div class="row q-gutter-md q-mb-md">
      <!-- Error Timeline Chart -->
      <div class="col-12 col-lg-8">
        <q-card>
          <q-card-section>
            <div class="text-h6">Error Timeline</div>
            <div class="text-caption text-grey-7">
              Errors over time with dual timeline (filename vs internal timestamps)
            </div>
          </q-card-section>
          <q-card-section>
            <div class="chart-container" style="height: 300px;">
              <canvas ref="timelineChart"></canvas>
            </div>
          </q-card-section>
        </q-card>
      </div>
      
      <!-- Error Types Distribution -->
      <div class="col-12 col-lg-4">
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
                v-for="error in criticalErrors"
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

    <!-- Data Table -->
    <q-card>
      <q-card-section>
        <div class="text-h6 q-mb-md">Detailed Error Log</div>
        
        <q-table
          :rows="errorTableData"
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
    />
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Chart, registerables } from 'chart.js'
import { useQuasar } from 'quasar'
import ErrorDetailModal from '@/components/ErrorDetailModal.vue'
import ExportMenu from '@/components/ExportMenu.vue'
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
const timelineChart = ref<HTMLCanvasElement>()
const errorTypesChart = ref<HTMLCanvasElement>()
const userActivityChart = ref<HTMLCanvasElement>()

// Chart instances
let timelineChartInstance: Chart | null = null
let errorTypesChartInstance: Chart | null = null
let userActivityChartInstance: Chart | null = null

// Data
const loading = ref(false)
const filter = ref('')
const dashboardData = ref<any>(null)

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
  errors: errorTableData.value,
  summary: summaryStats.value,
  filters: { searchFilter: filter.value }
}))
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

function initializeCharts() {
  if (!dashboardData.value) return

  // Destroy existing charts
  if (timelineChartInstance) {
    timelineChartInstance.destroy()
  }
  if (errorTypesChartInstance) {
    errorTypesChartInstance.destroy()
  }
  if (userActivityChartInstance) {
    userActivityChartInstance.destroy()
  }

  // Timeline Chart
  if (timelineChart.value && dashboardData.value.timeline) {
    timelineChartInstance = new Chart(timelineChart.value, {
      type: 'line',
      data: {
        labels: dashboardData.value.timeline.labels,
        datasets: [{
          label: 'Errors',
          data: dashboardData.value.timeline.data,
          borderColor: '#1976d2',
          backgroundColor: 'rgba(25, 118, 210, 0.1)',
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }

  // Error Types Chart (with click interaction)
  if (errorTypesChart.value && dashboardData.value.errorTypes) {
    errorTypesChartInstance = new Chart(errorTypesChart.value, {
      type: 'doughnut',
      data: {
        labels: dashboardData.value.errorTypes.labels,
        datasets: [{
          data: dashboardData.value.errorTypes.data,
          backgroundColor: ['#f2c037', '#26a69a', '#c10015', '#9c27b0', '#ff5722']
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
            const errorType = dashboardData.value.errorTypes.labels[index]
            filterByErrorType(errorType)
          }
        }
      }
    })
  }

  // User Activity Chart
  if (userActivityChart.value && dashboardData.value.userActivity) {
    userActivityChartInstance = new Chart(userActivityChart.value, {
      type: 'bar',
      data: {
        labels: dashboardData.value.userActivity.labels,
        datasets: [{
          label: 'Error Count',
          data: dashboardData.value.userActivity.data,
          backgroundColor: '#26a69a'
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

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.chart-container {
  position: relative;
}
</style>