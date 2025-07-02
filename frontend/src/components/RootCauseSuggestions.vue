<template>
  <q-card>
    <q-card-section>
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6">🎯 Root Cause Analysis</div>
          <div class="text-caption text-grey-7">
            AI-powered correlation analysis and suggestions
          </div>
        </div>
        <q-btn 
          outline 
          color="primary" 
          icon="psychology" 
          label="Analyze"
          @click="loadRootCauses"
          :loading="loading"
          size="sm"
        />
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-pa-md">
        <q-spinner-dots size="50px" color="primary" />
        <div class="text-subtitle1 q-mt-md">Analyzing error correlations...</div>
      </div>

      <!-- Root Cause Suggestions -->
      <div v-else-if="rootCauses.length > 0">
        <div class="text-caption text-grey-7 q-mb-md">
          Found {{ rootCauses.length }} potential root causes and correlations
        </div>

        <q-list>
          <q-expansion-item
            v-for="(cause, index) in rootCauses"
            :key="index"
            :label="cause.title"
            :caption="cause.description"
            :header-class="getRootCauseClass(cause)"
            expand-separator
            class="root-cause-item q-mb-sm"
          >
            <template v-slot:header>
              <q-item-section avatar>
                <q-icon :name="getRootCauseIcon(cause.type)" :color="getConfidenceColor(cause.confidence)" />
              </q-item-section>

              <q-item-section>
                <q-item-label class="text-weight-medium">
                  {{ cause.title }}
                </q-item-label>
                <q-item-label caption>
                  {{ cause.description }}
                </q-item-label>
              </q-item-section>

              <q-item-section side>
                <div class="column items-end">
                  <q-circular-progress
                    :value="cause.confidence * 100"
                    size="30px"
                    :thickness="0.2"
                    :color="getConfidenceColor(cause.confidence)"
                    track-color="grey-3"
                    class="q-mb-xs"
                  >
                    <div class="text-caption">{{ Math.round(cause.confidence * 100) }}%</div>
                  </q-circular-progress>
                  <q-chip size="xs" :color="getConfidenceColor(cause.confidence)" text-color="white">
                    {{ cause.error_count }} errors
                  </q-chip>
                </div>
              </q-item-section>
            </template>

            <q-card>
              <q-card-section>
                <!-- Suggestion -->
                <div class="q-mb-md">
                  <div class="text-subtitle2 q-mb-sm">💡 Recommendation</div>
                  <div class="suggestion-text">
                    {{ cause.suggestion }}
                  </div>
                </div>

                <!-- Additional Details based on type -->
                <div v-if="cause.type === 'time_burst'" class="q-mb-md">
                  <div class="text-subtitle2 q-mb-sm">⏱️ Time Burst Details</div>
                  <q-list dense>
                    <q-item v-if="cause.start_time">
                      <q-item-section>
                        <q-item-label caption>Start Time</q-item-label>
                        <q-item-label>{{ cause.start_time }}</q-item-label>
                      </q-item-section>
                    </q-item>
                    <q-item v-if="cause.error_types">
                      <q-item-section>
                        <q-item-label caption>Error Types</q-item-label>
                        <div class="q-gutter-xs">
                          <q-chip 
                            v-for="errorType in cause.error_types" 
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
                    <q-item v-if="cause.affected_users">
                      <q-item-section>
                        <q-item-label caption>Affected Users</q-item-label>
                        <div class="q-gutter-xs">
                          <q-chip 
                            v-for="user in cause.affected_users" 
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
                  </q-list>
                </div>

                <div v-else-if="cause.type === 'user_pattern'" class="q-mb-md">
                  <div class="text-subtitle2 q-mb-sm">👤 User Pattern Details</div>
                  <q-list dense>
                    <q-item>
                      <q-item-section>
                        <q-item-label caption>User</q-item-label>
                        <q-item-label>{{ cause.user }}</q-item-label>
                      </q-item-section>
                    </q-item>
                    <q-item>
                      <q-item-section>
                        <q-item-label caption>Dominant Error</q-item-label>
                        <q-item-label>{{ cause.dominant_error }}</q-item-label>
                      </q-item-section>
                    </q-item>
                    <q-item>
                      <q-item-section>
                        <q-item-label caption>Frequency</q-item-label>
                        <q-item-label>{{ cause.frequency }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </div>

                <div v-else-if="cause.type === 'type_correlation'" class="q-mb-md">
                  <div class="text-subtitle2 q-mb-sm">🔗 Error Correlation Details</div>
                  <q-list dense>
                    <q-item>
                      <q-item-section>
                        <q-item-label caption>Error Types</q-item-label>
                        <div class="q-gutter-xs">
                          <q-chip size="sm" outline color="primary">{{ cause.error_type_1 }}</q-chip>
                          <q-icon name="link" />
                          <q-chip size="sm" outline color="primary">{{ cause.error_type_2 }}</q-chip>
                        </div>
                      </q-item-section>
                    </q-item>
                    <q-item>
                      <q-item-section>
                        <q-item-label caption>Co-occurrence Count</q-item-label>
                        <q-item-label>{{ cause.co_occurrence_count }}</q-item-label>
                      </q-item-section>
                    </q-item>
                    <q-item>
                      <q-item-section>
                        <q-item-label caption>Correlation Strength</q-item-label>
                        <q-item-label>{{ (cause.correlation_strength * 100).toFixed(1) }}%</q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </div>

                <!-- Action Buttons -->
                <div class="row q-gutter-sm q-mt-md">
                  <q-btn 
                    outline 
                    color="primary" 
                    size="sm"
                    icon="content_copy"
                    label="Copy Analysis"
                    @click="copyAnalysis(cause)"
                  />
                  <q-btn 
                    color="secondary" 
                    size="sm"
                    icon="filter_alt"
                    label="Filter Dashboard"
                    @click="filterDashboard(cause)"
                  />
                  <q-btn 
                    outline 
                    color="purple" 
                    size="sm"
                    icon="analytics"
                    label="View Details"
                    @click="showRootCauseDetails(cause)"
                  />
                  <q-btn 
                    outline 
                    color="orange" 
                    size="sm"
                    icon="psychology"
                    label="Find Similar"
                    @click="findSimilarPatterns(cause)"
                  />
                </div>
              </q-card-section>
            </q-card>
          </q-expansion-item>
        </q-list>
      </div>

      <!-- No Root Causes -->
      <div v-else class="text-center q-pa-md">
        <q-icon name="psychology_off" size="48px" color="grey-5" />
        <div class="text-h6 q-mt-md">No correlations detected</div>
        <div class="text-caption text-grey-7">
          Errors appear to be independent or more data is needed for analysis
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { MLApiService, type RootCauseSuggestion } from '@/services/ml-api'

const $q = useQuasar()

// Emit events
const emit = defineEmits<{
  'filter-dashboard': [filter: any]
  'show-root-cause-details': [cause: RootCauseSuggestion]
  'find-similar-patterns': [cause: RootCauseSuggestion]
}>()

// Data
const loading = ref(false)
const rootCauses = ref<RootCauseSuggestion[]>([])

// Methods
async function loadRootCauses() {
  loading.value = true
  try {
    rootCauses.value = await MLApiService.getRootCauseSuggestions()
  } catch (error) {
    console.error('Error loading root cause suggestions:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load root cause analysis',
      timeout: 3000
    })
  } finally {
    loading.value = false
  }
}

function getRootCauseIcon(type: string): string {
  switch (type) {
    case 'time_burst': return 'schedule'
    case 'user_pattern': return 'person'
    case 'type_correlation': return 'link'
    default: return 'psychology'
  }
}

function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.8) return 'positive'
  if (confidence >= 0.6) return 'warning'
  if (confidence >= 0.4) return 'orange'
  return 'negative'
}

function getRootCauseClass(cause: RootCauseSuggestion): string {
  const confidence = cause.confidence
  if (confidence >= 0.8) return 'high-confidence'
  if (confidence >= 0.6) return 'medium-confidence'
  return 'low-confidence'
}

function copyAnalysis(cause: RootCauseSuggestion) {
  const analysis = `
Root Cause Analysis:
Title: ${cause.title}
Description: ${cause.description}
Confidence: ${Math.round(cause.confidence * 100)}%
Error Count: ${cause.error_count}

Recommendation:
${cause.suggestion}
  `.trim()

  navigator.clipboard.writeText(analysis).then(() => {
    $q.notify({
      type: 'positive',
      message: 'Analysis copied to clipboard',
      timeout: 2000
    })
  }).catch(() => {
    $q.notify({
      type: 'negative',
      message: 'Failed to copy to clipboard',
      timeout: 2000
    })
  })
}

function filterDashboard(cause: RootCauseSuggestion) {
  // Extract filter criteria from root cause
  const filter = extractFilterFromRootCause(cause)
  
  emit('filter-dashboard', filter)
  
  $q.notify({
    type: 'positive',
    message: `Dashboard filtered for: ${cause.title}`,
    timeout: 3000
  })
}

function showRootCauseDetails(cause: RootCauseSuggestion) {
  emit('show-root-cause-details', cause)
  
  $q.notify({
    type: 'info',
    message: `Opening detailed analysis for: ${cause.title}`,
    timeout: 2000
  })
}

function findSimilarPatterns(cause: RootCauseSuggestion) {
  emit('find-similar-patterns', cause)
  
  $q.notify({
    type: 'info', 
    message: `Searching for similar patterns to: ${cause.title}`,
    timeout: 2000
  })
}

function extractFilterFromRootCause(cause: RootCauseSuggestion): any {
  const filter: any = {
    search: '',
    users: [],
    severities: [],
    errorTypes: [],
    dateFrom: '',
    dateTo: '',
    rootCauseType: cause.type
  }

  // Extract filter criteria based on root cause type and content
  if (cause.type === 'User Pattern') {
    // Extract user from title (e.g., "AVB: Häufige ACCESS VIOLATIONS")
    const userMatch = cause.title.match(/^(\w+):/)
    if (userMatch) {
      filter.users = [userMatch[1]]
    }
    
    // Extract error type from description
    const errorTypeMatch = cause.description.match(/(ACCESS VIOLATION|DATA TYPE ERROR|BOUND ERROR)/i)
    if (errorTypeMatch) {
      filter.errorTypes = [errorTypeMatch[1]]
    }
  } else if (cause.type === 'System Correlation') {
    // Extract error types from description
    const errorTypeMatch = cause.description.match(/(DATA TYPE ERROR|ACCESS VIOLATION|BOUND ERROR)/i)
    if (errorTypeMatch) {
      filter.errorTypes = [errorTypeMatch[1]]
    }
    
    // Extract time range if mentioned
    const timeMatch = cause.description.match(/(\d{2}:\d{2})-(\d{2}:\d{2})/)
    if (timeMatch) {
      filter.timeRange = `${timeMatch[1]}-${timeMatch[2]}`
    }
  } else if (cause.type === 'Code Pattern') {
    // Extract error types from description
    const errorTypeMatches = cause.description.match(/(BOUND ERROR|ACCESS VIOLATION)/gi)
    if (errorTypeMatches) {
      filter.errorTypes = [...new Set(errorTypeMatches)]
    }
  } else if (cause.type === 'Resource Issue') {
    // Set severity to Critical for resource issues
    filter.severities = ['Critical']
    
    // Extract timestamp if mentioned
    const timeMatch = cause.description.match(/(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})/)
    if (timeMatch) {
      filter.specificTime = timeMatch[1]
    }
  }

  return filter
}

// Lifecycle
onMounted(() => {
  loadRootCauses()
})
</script>

<style scoped>
.root-cause-item {
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.high-confidence {
  border-left: 4px solid #4caf50;
}

.medium-confidence {
  border-left: 4px solid #ff9800;
}

.low-confidence {
  border-left: 4px solid #f44336;
}

.suggestion-text {
  background-color: rgba(25, 118, 210, 0.05);
  padding: 12px;
  border-radius: 4px;
  border-left: 3px solid #1976d2;
  font-style: italic;
}
</style>