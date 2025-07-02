<template>
  <q-dialog v-model="isOpen" persistent>
    <q-card style="min-width: 900px; max-width: 95vw; max-height: 90vh;">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">🧠 Similar Pattern Analysis</div>
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
        <!-- Reference Root Cause -->
        <div class="reference-cause q-mb-md">
          <div class="text-subtitle1 text-weight-medium q-mb-xs">Reference Pattern:</div>
          <q-card flat bordered>
            <q-card-section class="q-pa-sm">
              <div class="row items-center">
                <q-icon 
                  :name="getRootCauseIcon(rootCause.type)" 
                  :color="getConfidenceColor(rootCause.confidence)"
                  size="sm"
                  class="q-mr-sm"
                />
                <div class="text-subtitle2">{{ rootCause.title }}</div>
                <q-space />
                <q-chip size="sm" :color="getConfidenceColor(rootCause.confidence)" text-color="white">
                  {{ Math.round(rootCause.confidence * 100) }}%
                </q-chip>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <q-separator class="q-mb-md" />

        <!-- Loading State -->
        <div v-if="loading" class="text-center q-pa-xl">
          <q-spinner-dots size="60px" color="primary" />
          <div class="text-h6 q-mt-md">Analyzing patterns...</div>
          <div class="text-caption">Searching for similar error patterns using ML</div>
        </div>

        <!-- Similar Patterns Results -->
        <div v-else>
          <div class="text-subtitle1 text-weight-medium q-mb-md">
            🔍 Found {{ similarPatterns.length }} Similar Patterns
          </div>

          <div v-if="similarPatterns.length === 0" class="text-center q-pa-xl">
            <q-icon name="search_off" size="64px" color="grey-5" />
            <div class="text-h6 q-mt-md">No Similar Patterns Found</div>
            <div class="text-caption text-grey-7">
              This pattern appears to be unique or requires different analysis criteria
            </div>
          </div>

          <div v-else class="similar-patterns-list">
            <q-card 
              v-for="(pattern, index) in similarPatterns" 
              :key="index"
              flat
              bordered
              class="q-mb-md pattern-card"
            >
              <q-card-section>
                <div class="row items-start q-gutter-md">
                  <!-- Pattern Info -->
                  <div class="col-8">
                    <div class="row items-center q-mb-sm">
                      <q-icon 
                        :name="getPatternIcon(pattern.type)" 
                        :color="getSimilarityColor(pattern.similarity)"
                        size="md"
                        class="q-mr-sm"
                      />
                      <div class="text-h6">{{ pattern.title }}</div>
                      <q-space />
                      <q-circular-progress
                        :value="pattern.similarity * 100"
                        size="35px"
                        :thickness="0.15"
                        :color="getSimilarityColor(pattern.similarity)"
                        track-color="grey-3"
                        class="q-mr-sm"
                      >
                        <div class="text-caption">{{ Math.round(pattern.similarity * 100) }}%</div>
                      </q-circular-progress>
                    </div>

                    <div class="text-body2 text-grey-7 q-mb-sm">
                      {{ pattern.description }}
                    </div>

                    <!-- Pattern Details -->
                    <div class="row q-gutter-sm q-mb-sm">
                      <q-chip size="sm" outline color="primary" icon="schedule">
                        {{ pattern.timeframe }}
                      </q-chip>
                      <q-chip size="sm" outline color="secondary" icon="person">
                        {{ pattern.affected_users }} users
                      </q-chip>
                      <q-chip size="sm" outline color="orange" icon="bug_report">
                        {{ pattern.error_count }} errors
                      </q-chip>
                      <q-chip 
                        size="sm" 
                        :color="getSimilarityColor(pattern.similarity)"
                        text-color="white"
                        icon="psychology"
                      >
                        {{ Math.round(pattern.similarity * 100) }}% similar
                      </q-chip>
                    </div>

                    <!-- Common Characteristics -->
                    <div class="q-mb-sm">
                      <div class="text-caption text-weight-medium q-mb-xs">Common Characteristics:</div>
                      <div class="characteristics-list">
                        <q-chip 
                          v-for="characteristic in pattern.common_characteristics"
                          :key="characteristic"
                          size="xs"
                          outline
                          color="positive"
                        >
                          {{ characteristic }}
                        </q-chip>
                      </div>
                    </div>

                    <!-- Differences -->
                    <div v-if="pattern.differences && pattern.differences.length > 0">
                      <div class="text-caption text-weight-medium q-mb-xs">Key Differences:</div>
                      <div class="differences-list">
                        <q-chip 
                          v-for="difference in pattern.differences"
                          :key="difference"
                          size="xs"
                          outline
                          color="warning"
                        >
                          {{ difference }}
                        </q-chip>
                      </div>
                    </div>
                  </div>

                  <!-- Actions -->
                  <div class="col-4">
                    <div class="column q-gutter-sm">
                      <q-btn 
                        outline 
                        color="primary" 
                        size="sm"
                        icon="visibility"
                        label="View Pattern"
                        @click="viewPattern(pattern)"
                        class="full-width"
                      />
                      <q-btn 
                        outline 
                        color="secondary" 
                        size="sm"
                        icon="compare"
                        label="Compare"
                        @click="comparePatterns(rootCause, pattern)"
                        class="full-width"
                      />
                      <q-btn 
                        outline 
                        color="orange" 
                        size="sm"
                        icon="filter_alt"
                        label="Filter Similar"
                        @click="filterSimilarErrors(pattern)"
                        class="full-width"
                      />
                    </div>
                  </div>
                </div>

                <!-- Expanded Details -->
                <q-expansion-item
                  v-if="pattern.detailed_analysis"
                  label="Detailed Analysis"
                  icon="analytics"
                  class="q-mt-md"
                >
                  <div class="q-pa-md bg-grey-1">
                    <div class="text-body2">
                      {{ pattern.detailed_analysis }}
                    </div>
                    
                    <div v-if="pattern.recommended_actions" class="q-mt-md">
                      <div class="text-subtitle2 q-mb-xs">Recommended Actions:</div>
                      <ul class="q-pl-md">
                        <li 
                          v-for="action in pattern.recommended_actions"
                          :key="action"
                          class="text-body2"
                        >
                          {{ action }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </q-expansion-item>
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
          @click="exportSimilarPatterns"
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
import { ref, computed, watch } from 'vue'
import { useQuasar } from 'quasar'
import type { RootCauseSuggestion } from '@/services/ml-api'

interface SimilarPattern {
  id: string
  type: string
  title: string
  description: string
  similarity: number
  timeframe: string
  affected_users: number
  error_count: number
  common_characteristics: string[]
  differences: string[]
  detailed_analysis?: string
  recommended_actions?: string[]
}

interface Props {
  modelValue: boolean
  rootCause: RootCauseSuggestion | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'filter-dashboard': [filter: any]
  'view-pattern': [pattern: SimilarPattern]
}>()

const $q = useQuasar()

const loading = ref(false)
const similarPatterns = ref<SimilarPattern[]>([])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Watch for root cause changes and search for similar patterns
watch(() => props.rootCause, async (newRootCause) => {
  if (newRootCause && isOpen.value) {
    await searchSimilarPatterns(newRootCause)
  }
})

watch(isOpen, async (newVal) => {
  if (newVal && props.rootCause) {
    await searchSimilarPatterns(props.rootCause)
  }
})

async function searchSimilarPatterns(rootCause: RootCauseSuggestion) {
  loading.value = true
  
  try {
    // Simulate ML pattern search - in real implementation, this would call an API
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Generate demo similar patterns based on the root cause
    similarPatterns.value = generateSimilarPatterns(rootCause)
    
  } catch (error) {
    console.error('Error searching similar patterns:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to search for similar patterns',
      timeout: 3000
    })
  } finally {
    loading.value = false
  }
}

function generateSimilarPatterns(rootCause: RootCauseSuggestion): SimilarPattern[] {
  // Generate demo patterns based on the root cause type
  const patterns: SimilarPattern[] = []
  
  if (rootCause.type === 'User Pattern') {
    patterns.push({
      id: 'pattern_1',
      type: 'User Pattern',
      title: 'GAM: Recurring DATA TYPE ERRORs',
      description: 'Benutzer GAM zeigt ähnliche Fehlermuster wie AVB, aber mit DATA TYPE ERRORs',
      similarity: 0.78,
      timeframe: 'Last 7 days',
      affected_users: 1,
      error_count: 18,
      common_characteristics: ['Single user focus', 'High error frequency', 'Same time patterns'],
      differences: ['Different error type', 'Lower severity'],
      detailed_analysis: 'Both patterns show concentrated error activity from specific users during business hours, suggesting similar workflow or system usage patterns.',
      recommended_actions: [
        'Review user training for both AVB and GAM',
        'Check if both users use similar software versions',
        'Implement user-specific monitoring'
      ]
    })
    
    patterns.push({
      id: 'pattern_2',
      type: 'User Pattern',
      title: 'SWE: Historical ACCESS VIOLATION Pattern',
      description: 'Ähnliches ACCESS VIOLATION Muster von SWE vor 2 Wochen',
      similarity: 0.65,
      timeframe: '2 weeks ago',
      affected_users: 1,
      error_count: 8,
      common_characteristics: ['ACCESS VIOLATION type', 'Single user', 'Critical severity'],
      differences: ['Resolved automatically', 'Lower frequency', 'Different time window'],
      detailed_analysis: 'Historical pattern that resolved itself, possibly due to system updates or user behavior changes.',
      recommended_actions: [
        'Apply same resolution that worked for SWE',
        'Check system updates timeline',
        'Document resolution process'
      ]
    })
  }
  
  if (rootCause.type === 'System Correlation') {
    patterns.push({
      id: 'pattern_3',
      type: 'Time Pattern',
      title: 'BOUND ERRORs Peak at 10:00-12:00',
      description: 'Ähnliche zeitbasierte Korrelation, aber mit BOUND ERRORs am Vormittag',
      similarity: 0.82,
      timeframe: 'Last 30 days',
      affected_users: 4,
      error_count: 31,
      common_characteristics: ['Time-based correlation', 'Multiple users', 'Predictable pattern'],
      differences: ['Different time window', 'Different error type', 'Higher user count'],
      detailed_analysis: 'Both patterns show clear time-based correlations suggesting system load or scheduled process influences.',
      recommended_actions: [
        'Implement load balancing during peak hours',
        'Schedule maintenance outside peak times',
        'Monitor system resources during correlations'
      ]
    })
  }
  
  if (rootCause.type === 'Resource Issue') {
    patterns.push({
      id: 'pattern_4',
      type: 'Resource Pattern',
      title: 'Multi-user Memory Issues',
      description: 'Ähnliche gleichzeitige Fehler bei mehreren Benutzern, aber memory-related',
      similarity: 0.71,
      timeframe: 'Last month',
      affected_users: 5,
      error_count: 12,
      common_characteristics: ['Multi-user impact', 'Simultaneous occurrence', 'Resource-related'],
      differences: ['Memory vs access violations', 'Different users', 'Longer duration'],
      detailed_analysis: 'Pattern suggests systemic resource constraints affecting multiple users simultaneously.',
      recommended_actions: [
        'Upgrade system memory',
        'Implement resource monitoring',
        'Set up automatic scaling'
      ]
    })
  }
  
  return patterns
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

function getPatternIcon(type: string): string {
  switch (type) {
    case 'User Pattern': return 'person'
    case 'Time Pattern': return 'schedule'
    case 'Resource Pattern': return 'memory'
    case 'Code Pattern': return 'code'
    default: return 'pattern'
  }
}

function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.8) return 'positive'
  if (confidence >= 0.6) return 'warning'
  if (confidence >= 0.4) return 'orange'
  return 'negative'
}

function getSimilarityColor(similarity: number): string {
  if (similarity >= 0.8) return 'positive'
  if (similarity >= 0.6) return 'primary'
  if (similarity >= 0.4) return 'warning'
  return 'orange'
}

function viewPattern(pattern: SimilarPattern) {
  emit('view-pattern', pattern)
  $q.notify({
    type: 'info',
    message: `Viewing pattern: ${pattern.title}`,
    timeout: 2000
  })
}

function comparePatterns(original: RootCauseSuggestion, similar: SimilarPattern) {
  $q.notify({
    type: 'info',
    message: `Comparing "${original.title}" with "${similar.title}"`,
    timeout: 3000
  })
}

function filterSimilarErrors(pattern: SimilarPattern) {
  const filter = {
    search: pattern.title,
    patternType: pattern.type,
    similarTo: props.rootCause?.title
  }
  
  emit('filter-dashboard', filter)
  closeModal()
  
  $q.notify({
    type: 'positive',
    message: `Applied filter for similar pattern: ${pattern.title}`,
    timeout: 3000
  })
}

function exportSimilarPatterns() {
  if (!props.rootCause) return
  
  const analysis = `
Similar Pattern Analysis Report
==============================

Reference Pattern: ${props.rootCause.title}
Reference Type: ${props.rootCause.type}
Reference Confidence: ${Math.round(props.rootCause.confidence * 100)}%

Found ${similarPatterns.value.length} Similar Patterns:

${similarPatterns.value.map((pattern, index) => `
${index + 1}. ${pattern.title}
   Type: ${pattern.type}
   Similarity: ${Math.round(pattern.similarity * 100)}%
   Description: ${pattern.description}
   Timeframe: ${pattern.timeframe}
   Affected Users: ${pattern.affected_users}
   Error Count: ${pattern.error_count}
   
   Common Characteristics:
   ${pattern.common_characteristics.map(c => `   - ${c}`).join('\n')}
   
   Key Differences:
   ${pattern.differences.map(d => `   - ${d}`).join('\n')}
   
   ${pattern.detailed_analysis ? `Analysis: ${pattern.detailed_analysis}` : ''}
   
   ${pattern.recommended_actions ? `Recommended Actions:\n${pattern.recommended_actions.map(a => `   - ${a}`).join('\n')}` : ''}
`).join('\n---\n')}

Generated: ${new Date().toLocaleString()}
  `.trim()

  const blob = new Blob([analysis], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `similar-patterns-analysis-${Date.now()}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  $q.notify({
    type: 'positive',
    message: 'Similar patterns analysis exported',
    timeout: 2000
  })
}

function closeModal() {
  isOpen.value = false
  similarPatterns.value = []
}
</script>

<style scoped>
.reference-cause {
  background: linear-gradient(135deg, rgba(25, 118, 210, 0.05) 0%, rgba(25, 118, 210, 0.1) 100%);
  padding: 16px;
  border-radius: 8px;
}

.pattern-card {
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.pattern-card:hover {
  border-left-color: #1976d2;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.characteristics-list, .differences-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>