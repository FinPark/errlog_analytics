<template>
  <q-card>
    <q-card-section>
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6">📈 Timeline Analysis</div>
          <div class="text-caption text-grey-7">
            Error timeline with trend analysis and filtering
          </div>
        </div>
        <div class="q-gutter-sm">
          <q-btn-toggle
            v-model="viewMode"
            toggle-color="primary"
            :options="[
              {label: 'Daily', value: 'daily'},
              {label: 'Weekly', value: 'weekly'},
              {label: 'Monthly', value: 'monthly'}
            ]"
            @update:model-value="updateTimelineView"
          />
        </div>
      </div>

      <!-- Time Range Filter -->
      <div class="row q-gutter-md q-mb-md">
        <div class="col-12 col-md-3">
          <q-input
            v-model="timeFilter.startDate"
            label="Start Date"
            type="date"
            outlined
            dense
            @update:model-value="filterTimeline"
          >
            <template v-slot:prepend>
              <q-icon name="event" />
            </template>
          </q-input>
        </div>
        
        <div class="col-12 col-md-3">
          <q-input
            v-model="timeFilter.endDate"
            label="End Date"
            type="date"
            outlined
            dense
            @update:model-value="filterTimeline"
          >
            <template v-slot:prepend>
              <q-icon name="event" />
            </template>
          </q-input>
        </div>

        <div class="col-12 col-md-6">
          <div class="text-caption q-mb-sm">Quick ranges:</div>
          <q-btn-group flat>
            <q-btn 
              flat 
              size="sm" 
              label="Last 7 days" 
              @click="setQuickRange(7)"
            />
            <q-btn 
              flat 
              size="sm" 
              label="Last 30 days" 
              @click="setQuickRange(30)"
            />
            <q-btn 
              flat 
              size="sm" 
              label="Last 90 days" 
              @click="setQuickRange(90)"
            />
            <q-btn 
              flat 
              size="sm" 
              label="All Time" 
              @click="clearTimeFilter"
            />
          </q-btn-group>
        </div>
      </div>

      <!-- Trend Statistics -->
      <div class="row q-gutter-md q-mb-md">
        <div class="col">
          <q-linear-progress 
            :value="trendData.errorGrowth / 100" 
            :color="trendData.errorGrowth > 0 ? 'negative' : 'positive'"
            size="md"
            class="q-mb-xs"
          />
          <div class="text-caption">
            Error Growth: 
            <span :class="trendData.errorGrowth > 0 ? 'text-negative' : 'text-positive'">
              {{ trendData.errorGrowth > 0 ? '+' : '' }}{{ trendData.errorGrowth.toFixed(1) }}%
            </span>
          </div>
        </div>
        
        <div class="col">
          <div class="text-h6">{{ trendData.averagePerDay.toFixed(1) }}</div>
          <div class="text-caption text-grey-7">Avg errors/day</div>
        </div>
        
        <div class="col">
          <div class="text-h6">{{ trendData.peakDay.date }}</div>
          <div class="text-caption text-grey-7">Peak day ({{ trendData.peakDay.count }} errors)</div>
        </div>
        
        <div class="col">
          <div class="text-h6">{{ trendData.trendDirection }}</div>
          <div class="text-caption text-grey-7">Overall trend</div>
        </div>
      </div>

      <!-- Timeline Chart -->
      <div class="chart-container" style="height: 400px;">
        <canvas ref="timelineChart"></canvas>
      </div>

      <!-- Trend Insights -->
      <div v-if="trendInsights.length > 0" class="q-mt-md">
        <div class="text-subtitle1 q-mb-sm">💡 Trend Insights</div>
        <q-list dense>
          <q-item 
            v-for="(insight, index) in trendInsights" 
            :key="index"
            class="q-pa-none"
          >
            <q-item-section avatar>
              <q-icon 
                :name="insight.type === 'warning' ? 'warning' : (insight.type === 'info' ? 'info' : 'trending_up')" 
                :color="insight.type === 'warning' ? 'orange' : (insight.type === 'info' ? 'blue' : 'positive')"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ insight.message }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

interface TimelineData {
  labels: string[]
  data: number[]
}

interface ErrorData {
  timestamp: string
  [key: string]: any
}

const props = defineProps<{
  errors: ErrorData[]
  initialData?: TimelineData
}>()

const emit = defineEmits<{
  'update:filtered-data': [data: ErrorData[]]
}>()

// Chart reference
const timelineChart = ref<HTMLCanvasElement>()
let chartInstance: Chart | null = null

// Reactive data
const viewMode = ref<'daily' | 'weekly' | 'monthly'>('daily')
const timeFilter = ref({
  startDate: '',
  endDate: ''
})

const filteredErrors = ref<ErrorData[]>([])
const processedTimelineData = ref<TimelineData>({ labels: [], data: [] })

// Computed trend data
const trendData = computed(() => {
  const data = processedTimelineData.value.data
  if (data.length < 2) return {
    errorGrowth: 0,
    averagePerDay: 0,
    peakDay: { date: 'N/A', count: 0 },
    trendDirection: 'Stable'
  }

  // Calculate growth rate (compare last 7 days with previous 7 days)
  const recentPeriod = data.slice(-7)
  const previousPeriod = data.slice(-14, -7)
  
  const recentAvg = recentPeriod.reduce((a, b) => a + b, 0) / recentPeriod.length
  const previousAvg = previousPeriod.length > 0 
    ? previousPeriod.reduce((a, b) => a + b, 0) / previousPeriod.length 
    : recentAvg

  const errorGrowth = previousAvg > 0 
    ? ((recentAvg - previousAvg) / previousAvg) * 100 
    : 0

  // Find peak day
  const maxIndex = data.indexOf(Math.max(...data))
  const peakDay = {
    date: processedTimelineData.value.labels[maxIndex] || 'N/A',
    count: data[maxIndex] || 0
  }

  // Average per day
  const averagePerDay = data.reduce((a, b) => a + b, 0) / data.length

  // Trend direction
  const firstHalf = data.slice(0, Math.floor(data.length / 2))
  const secondHalf = data.slice(Math.floor(data.length / 2))
  
  const firstAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length
  const secondAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length
  
  let trendDirection = 'Stable'
  if (secondAvg > firstAvg * 1.1) trendDirection = '📈 Increasing'
  else if (secondAvg < firstAvg * 0.9) trendDirection = '📉 Decreasing'

  return {
    errorGrowth,
    averagePerDay,
    peakDay,
    trendDirection
  }
})

// Trend insights
const trendInsights = computed(() => {
  const insights: Array<{type: string, message: string}> = []
  
  if (trendData.value.errorGrowth > 50) {
    insights.push({
      type: 'warning',
      message: `Error rate increased by ${trendData.value.errorGrowth.toFixed(1)}% in recent days`
    })
  } else if (trendData.value.errorGrowth < -30) {
    insights.push({
      type: 'positive',
      message: `Error rate decreased by ${Math.abs(trendData.value.errorGrowth).toFixed(1)}% - improvements detected`
    })
  }

  if (trendData.value.averagePerDay > 10) {
    insights.push({
      type: 'info',
      message: `High activity: averaging ${trendData.value.averagePerDay.toFixed(1)} errors per day`
    })
  }

  if (trendData.value.peakDay.count > trendData.value.averagePerDay * 3) {
    insights.push({
      type: 'warning',
      message: `Spike detected on ${trendData.value.peakDay.date} with ${trendData.value.peakDay.count} errors`
    })
  }

  return insights
})

// Methods
function calculateTrendLine(data: number[]): number[] {
  if (data.length < 2) return data
  
  const n = data.length
  let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0
  
  for (let i = 0; i < n; i++) {
    sumX += i
    sumY += data[i]
    sumXY += i * data[i]
    sumXX += i * i
  }
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX)
  const intercept = (sumY - slope * sumX) / n
  
  return data.map((_, i) => slope * i + intercept)
}

function parseErrorDate(timestamp: string): Date | null {
  try {
    // Handle DD.MM.YYYY HH:MM:SS format
    const parts = timestamp.split(' ')
    if (parts.length >= 1) {
      const datePart = parts[0]
      const dateParts = datePart.split('.')
      
      if (dateParts.length === 3) {
        const [day, month, year] = dateParts
        const parsedDate = new Date(parseInt(year), parseInt(month) - 1, parseInt(day))
        
        // Validate the parsed date
        if (!isNaN(parsedDate.getTime())) {
          return parsedDate
        }
      }
    }
    
    // Fallback: try native Date parsing
    const fallbackDate = new Date(timestamp)
    if (!isNaN(fallbackDate.getTime())) {
      return fallbackDate
    }
    
    return null
  } catch (error) {
    return null
  }
}

function processTimelineData(errors: ErrorData[]): TimelineData {
  const groupedData: Record<string, number> = {}
  
  errors.forEach((error, index) => {
    const date = parseErrorDate(error.timestamp)
    if (!date) return

    let key: string
    if (viewMode.value === 'daily') {
      key = date.toISOString().split('T')[0]
    } else if (viewMode.value === 'weekly') {
      const weekStart = new Date(date)
      weekStart.setDate(date.getDate() - date.getDay())
      key = weekStart.toISOString().split('T')[0]
    } else {
      key = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`
    }

    groupedData[key] = (groupedData[key] || 0) + 1
  })

  const sortedKeys = Object.keys(groupedData).sort()
  
  return {
    labels: sortedKeys.map(key => {
      if (viewMode.value === 'monthly') {
        const [year, month] = key.split('-')
        return new Date(parseInt(year), parseInt(month) - 1).toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short' 
        })
      }
      return new Date(key).toLocaleDateString()
    }),
    data: sortedKeys.map(key => groupedData[key])
  }
}

function filterTimeline() {
  let filtered = [...props.errors]

  if (timeFilter.value.startDate || timeFilter.value.endDate) {
    filtered = filtered.filter(error => {
      const errorDate = parseErrorDate(error.timestamp)
      if (!errorDate) return true

      const startDate = timeFilter.value.startDate ? new Date(timeFilter.value.startDate) : null
      const endDate = timeFilter.value.endDate ? new Date(timeFilter.value.endDate) : null

      if (startDate && errorDate < startDate) return false
      if (endDate && errorDate > endDate) return false

      return true
    })
  }

  filteredErrors.value = filtered
  processedTimelineData.value = processTimelineData(filtered)
  emit('update:filtered-data', filtered)
  
  nextTick(() => {
    updateChart()
  })
}

function setQuickRange(days: number) {
  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(endDate.getDate() - days)

  timeFilter.value.startDate = startDate.toISOString().split('T')[0]
  timeFilter.value.endDate = endDate.toISOString().split('T')[0]
  
  filterTimeline()
}

function clearTimeFilter() {
  timeFilter.value.startDate = ''
  timeFilter.value.endDate = ''
  filterTimeline()
}

function updateTimelineView() {
  filterTimeline()
}

function updateChart() {
  if (!chartInstance || !timelineChart.value) return

  const trendData = calculateTrendLine(processedTimelineData.value.data)
  
  chartInstance.data.labels = processedTimelineData.value.labels
  chartInstance.data.datasets[0].data = processedTimelineData.value.data
  chartInstance.data.datasets[1].data = trendData
  chartInstance.update('active')
}

function initChart() {
  if (!timelineChart.value) return

  // Ensure we have data before initializing
  if (processedTimelineData.value.labels.length === 0) {
    return
  }

  // Destroy existing chart if it exists
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }

  // Calculate trend line data
  const data = processedTimelineData.value.data
  const trendData = calculateTrendLine(data)

  chartInstance = new Chart(timelineChart.value, {
    type: 'line',
    data: {
      labels: processedTimelineData.value.labels,
      datasets: [{
        label: 'Errors',
        data: processedTimelineData.value.data,
        borderColor: '#1976d2',
        backgroundColor: 'rgba(25, 118, 210, 0.1)',
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointHoverRadius: 6
      }, {
        label: 'Trend',
        data: trendData,
        borderColor: '#ff5722',
        backgroundColor: 'transparent',
        borderDash: [5, 5],
        tension: 0,
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: viewMode.value.charAt(0).toUpperCase() + viewMode.value.slice(1)
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: 'Error Count'
          },
          beginAtZero: true
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      }
    }
  })
}

// Watch for prop changes
watch(() => props.errors, (newErrors) => {
  filterTimeline()
}, { immediate: true })

onMounted(() => {
  nextTick(() => {
    initChart()
  })
})
</script>

<style scoped>
.chart-container {
  position: relative;
}
</style>