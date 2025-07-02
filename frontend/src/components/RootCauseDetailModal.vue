<template>
  <q-dialog v-model="isOpen" persistent>
    <q-card style="min-width: 1000px; max-width: 95vw; max-height: 90vh;">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">🔍 Root Cause Investigation</div>
        <q-space />
        <q-btn 
          icon="close" 
          flat 
          round 
          dense 
          @click="closeModal" 
        />
      </q-card-section>

      <q-card-section v-if="rootCause" class="q-pt-none">
        <!-- Root Cause Header -->
        <div class="root-cause-header q-mb-md">
          <div class="row items-center q-mb-sm">
            <q-icon 
              :name="getRootCauseIcon(rootCause.type)" 
              :color="getConfidenceColor(rootCause.confidence)"
              size="md"
              class="q-mr-sm"
            />
            <div class="text-h6">{{ rootCause.title }}</div>
            <q-space />
            <q-circular-progress
              :value="rootCause.confidence * 100"
              size="40px"
              :thickness="0.15"
              :color="getConfidenceColor(rootCause.confidence)"
              track-color="grey-3"
            >
              <div class="text-caption">{{ Math.round(rootCause.confidence * 100) }}%</div>
            </q-circular-progress>
          </div>
          
          <div class="text-subtitle1 text-grey-7 q-mb-sm">
            {{ rootCause.description }}
          </div>
          
          <div class="row q-gutter-md">
            <q-chip 
              :color="getConfidenceColor(rootCause.confidence)" 
              text-color="white"
              icon="trending_up"
            >
              Confidence: {{ Math.round(rootCause.confidence * 100) }}%
            </q-chip>
            <q-chip color="primary" text-color="white" icon="bug_report">
              {{ rootCause.error_count }} Errors
            </q-chip>
            <q-chip color="secondary" text-color="white" icon="category">
              {{ rootCause.type }}
            </q-chip>
          </div>
        </div>

        <q-separator class="q-mb-md" />

        <div class="row q-gutter-lg">
          <!-- Left Column: Analysis Details -->
          <div class="col-12 col-md-6">
            <!-- Recommendation -->
            <q-card flat bordered class="q-mb-md">
              <q-card-section>
                <div class="text-h6 q-mb-sm">💡 Recommendation</div>
                <div class="recommendation-text">
                  {{ rootCause.suggestion }}
                </div>
              </q-card-section>
            </q-card>

            <!-- Timeline Analysis -->
            <q-card flat bordered class="q-mb-md">
              <q-card-section>
                <div class="text-h6 q-mb-sm">⏰ Timeline Analysis</div>
                <div class="timeline-container">
                  <canvas ref="timelineChart" style="height: 200px;"></canvas>
                </div>
              </q-card-section>
            </q-card>

            <!-- Pattern Details -->
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-sm">🔍 Pattern Details</div>
                <q-list>
                  <q-item v-if="analysisData.affectedUsers.length > 0">
                    <q-item-section>
                      <q-item-label class="text-weight-medium">Affected Users</q-item-label>
                      <div class="q-gutter-xs q-mt-xs">
                        <q-chip 
                          v-for="user in analysisData.affectedUsers" 
                          :key="user"
                          size="sm"
                          outline
                          color="secondary"
                        >
                          {{ user }}
                        </q-chip>
                      </div>
                    </q-item-section>
                  </q-item>
                  
                  <q-separator />
                  
                  <q-item v-if="analysisData.errorTypes.length > 0">
                    <q-item-section>
                      <q-item-label class="text-weight-medium">Error Types</q-item-label>
                      <div class="q-gutter-xs q-mt-xs">
                        <q-chip 
                          v-for="errorType in analysisData.errorTypes" 
                          :key="errorType"
                          size="sm"
                          outline
                          color="primary"
                        >
                          {{ errorType }}
                        </q-chip>
                      </div>
                    </q-item-section>
                  </q-item>
                  
                  <q-separator />
                  
                  <q-item>
                    <q-item-section>
                      <q-item-label class="text-weight-medium">Severity Distribution</q-item-label>
                      <div class="severity-distribution q-mt-xs">
                        <div 
                          v-for="(count, severity) in analysisData.severityDistribution" 
                          :key="severity"
                          class="severity-item row items-center q-mb-xs"
                        >
                          <q-chip 
                            :color="getSeverityColor(severity)" 
                            text-color="white" 
                            size="sm"
                            class="q-mr-sm"
                          >
                            {{ severity }}
                          </q-chip>
                          <span>{{ count }} errors</span>
                        </div>
                      </div>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-card-section>
            </q-card>
          </div>

          <!-- Right Column: Related Errors -->
          <div class="col-12 col-md-6">
            <q-card flat bordered>
              <q-card-section>
                <div class="text-h6 q-mb-sm">📋 Related Errors</div>
                <div class="text-caption text-grey-7 q-mb-md">
                  {{ relatedErrors.length }} errors match this root cause pattern
                </div>
                
                <q-list>
                  <q-item
                    v-for="error in relatedErrors.slice(0, 10)"
                    :key="error.id"
                    class="q-mb-sm cursor-pointer error-item"
                    clickable
                    @click="showErrorDetail(error)"
                  >
                    <q-item-section avatar>
                      <q-icon 
                        name="warning" 
                        :color="getSeverityColor(error.severity)" 
                      />
                    </q-item-section>
                    
                    <q-item-section>
                      <q-item-label class="text-weight-medium">
                        {{ error.type }}
                      </q-item-label>
                      <q-item-label caption>
                        {{ error.user }} • {{ error.timestamp }}
                      </q-item-label>
                    </q-item-section>
                    
                    <q-item-section side>
                      <div class="column items-end">
                        <q-chip 
                          :color="getSeverityColor(error.severity)" 
                          text-color="white" 
                          size="sm"
                        >
                          {{ error.severity }}
                        </q-chip>
                        <div class="text-caption">Code {{ error.code }}</div>
                      </div>
                    </q-item-section>
                  </q-item>
                </q-list>
                
                <div v-if="relatedErrors.length > 10" class="text-center q-mt-md">
                  <q-btn 
                    outline 
                    color="primary" 
                    label="View All Related Errors"
                    @click="viewAllRelatedErrors"
                  />
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right" class="q-pa-md">
        <q-btn 
          flat 
          label="Export Analysis" 
          color="primary" 
          icon="download"
          @click="exportAnalysis"
        />
        <q-btn 
          color="secondary" 
          label="Apply Filter to Dashboard"
          icon="filter_alt"
          @click="applyFilterToDashboard"
        />
        <q-btn 
          flat 
          label="Close" 
          color="grey" 
          @click="closeModal"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useQuasar } from 'quasar'
import { Chart, registerables } from 'chart.js'
import type { RootCauseSuggestion } from '@/services/ml-api'

Chart.register(...registerables)

interface Props {
  modelValue: boolean
  rootCause: RootCauseSuggestion | null
  relatedErrors: any[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'filter-dashboard': [filter: any]
  'error-selected': [error: any]
}>()

const $q = useQuasar()

// Chart ref
const timelineChart = ref<HTMLCanvasElement>()
let timelineChartInstance: Chart | null = null

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Analysis data computed from related errors
const analysisData = computed(() => {
  if (!props.relatedErrors) return {
    affectedUsers: [],
    errorTypes: [],
    severityDistribution: {},
    timelineData: []
  }

  const users = [...new Set(props.relatedErrors.map(e => e.user))]
  const errorTypes = [...new Set(props.relatedErrors.map(e => e.type))]
  
  const severityDistribution: Record<string, number> = {}
  props.relatedErrors.forEach(error => {
    severityDistribution[error.severity] = (severityDistribution[error.severity] || 0) + 1
  })

  // Create timeline data
  const timelineData = createTimelineData(props.relatedErrors)

  return {
    affectedUsers: users,
    errorTypes: errorTypes,
    severityDistribution,
    timelineData
  }
})

// Watch for changes and update chart
watch(() => props.rootCause, () => {
  if (props.rootCause && isOpen.value) {
    nextTick(() => {
      createTimelineChart()
    })
  }
})

watch(isOpen, (newVal) => {
  if (newVal && props.rootCause) {
    nextTick(() => {
      createTimelineChart()
    })
  }
})

function createTimelineData(errors: any[]) {
  // Group errors by hour
  const hourlyData: Record<string, number> = {}
  
  errors.forEach(error => {
    const timestamp = new Date(error.timestamp)
    const hour = timestamp.getHours()
    const hourKey = `${hour.toString().padStart(2, '0')}:00`
    hourlyData[hourKey] = (hourlyData[hourKey] || 0) + 1
  })

  const labels = Object.keys(hourlyData).sort()
  const data = labels.map(label => hourlyData[label])

  return { labels, data }
}

function createTimelineChart() {
  if (!timelineChart.value || !analysisData.value.timelineData) return

  // Destroy existing chart
  if (timelineChartInstance) {
    timelineChartInstance.destroy()
  }

  const { labels, data } = analysisData.value.timelineData

  timelineChartInstance = new Chart(timelineChart.value, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Errors per Hour',
        data: data,
        borderColor: '#1976d2',
        backgroundColor: 'rgba(25, 118, 210, 0.1)',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      }
    }
  })
}

function getRootCauseIcon(type: string): string {
  switch (type) {
    case 'User Pattern': return 'person'
    case 'System Correlation': return 'schedule'
    case 'Code Pattern': return 'link'
    case 'Resource Issue': return 'memory'
    default: return 'psychology'
  }
}

function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.8) return 'positive'
  if (confidence >= 0.6) return 'warning'
  if (confidence >= 0.4) return 'orange'
  return 'negative'
}

function getSeverityColor(severity: string): string {
  switch (severity?.toLowerCase()) {
    case 'critical': return 'negative'
    case 'high': return 'orange'
    case 'medium': return 'warning'
    case 'low': return 'positive'
    default: return 'grey'
  }
}

function showErrorDetail(error: any) {
  emit('error-selected', error)
  closeModal()
}

function viewAllRelatedErrors() {
  // Apply filter and close modal
  applyFilterToDashboard()
}

function applyFilterToDashboard() {
  if (!props.rootCause) return
  
  const filter = {
    users: analysisData.value.affectedUsers,
    errorTypes: analysisData.value.errorTypes,
    rootCauseTitle: props.rootCause.title
  }
  
  emit('filter-dashboard', filter)
  closeModal()
  
  $q.notify({
    type: 'positive',
    message: 'Filter applied to dashboard',
    timeout: 2000
  })
}

function exportAnalysis() {
  if (!props.rootCause) return
  
  const analysis = `
Root Cause Analysis Report
==========================

Title: ${props.rootCause.title}
Type: ${props.rootCause.type}
Confidence: ${Math.round(props.rootCause.confidence * 100)}%
Error Count: ${props.rootCause.error_count}

Description:
${props.rootCause.description}

Recommendation:
${props.rootCause.suggestion}

Affected Users: ${analysisData.value.affectedUsers.join(', ')}
Error Types: ${analysisData.value.errorTypes.join(', ')}

Severity Distribution:
${Object.entries(analysisData.value.severityDistribution)
  .map(([severity, count]) => `${severity}: ${count} errors`)
  .join('\n')}

Generated: ${new Date().toLocaleString()}
  `.trim()

  const blob = new Blob([analysis], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `root-cause-analysis-${Date.now()}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  $q.notify({
    type: 'positive',
    message: 'Analysis exported successfully',
    timeout: 2000
  })
}

function closeModal() {
  isOpen.value = false
  if (timelineChartInstance) {
    timelineChartInstance.destroy()
    timelineChartInstance = null
  }
}
</script>

<style scoped>
.root-cause-header {
  background: linear-gradient(135deg, rgba(25, 118, 210, 0.05) 0%, rgba(25, 118, 210, 0.1) 100%);
  padding: 16px;
  border-radius: 8px;
  border: 1px solid rgba(25, 118, 210, 0.2);
}

.recommendation-text {
  background-color: rgba(25, 118, 210, 0.05);
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #1976d2;
  font-style: italic;
  font-weight: 500;
}

.error-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.error-item:hover {
  background-color: rgba(25, 118, 210, 0.05);
  border-color: #1976d2;
}

.severity-item {
  padding: 4px 0;
}

.timeline-container {
  height: 200px;
  position: relative;
}
</style>