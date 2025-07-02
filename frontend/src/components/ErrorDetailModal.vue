<template>
  <q-dialog v-model="isOpen" persistent>
    <q-card style="min-width: 900px; max-width: 95vw;">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Error Details</div>
        <q-space />
        <q-btn 
          icon="close" 
          flat 
          round 
          dense 
          @click="closeModal" 
        />
      </q-card-section>

      <q-card-section v-if="error">
        <div class="row q-gutter-lg">
          <!-- Left Column: Error Details -->
          <div class="col-12 col-md-6">
            <!-- Error Header -->
            <div class="row q-gutter-md q-mb-md">
              <q-chip 
                :color="getSeverityColor(error.severity)" 
                text-color="white" 
                icon="warning"
              >
                {{ error.severity }}
              </q-chip>
              <q-chip 
                color="primary" 
                text-color="white" 
                icon="code"
              >
                Code {{ error.code }}
              </q-chip>
              <q-chip 
                color="secondary" 
                text-color="white" 
                icon="person"
              >
                {{ error.user }}
              </q-chip>
            </div>

            <!-- Error Information -->
            <q-list>
              <q-item>
                <q-item-section>
                  <q-item-label class="text-subtitle1 text-weight-medium">
                    Error Type
                  </q-item-label>
                  <q-item-label class="text-h6">
                    {{ error.type }}
                  </q-item-label>
                </q-item-section>
              </q-item>

              <q-separator />

              <q-item>
                <q-item-section>
                  <q-item-label class="text-subtitle1 text-weight-medium">
                    Timestamp
                  </q-item-label>
                  <q-item-label>
                    {{ error.timestamp }}
                  </q-item-label>
                </q-item-section>
              </q-item>

              <q-separator />

              <q-item>
                <q-item-section>
                  <q-item-label class="text-subtitle1 text-weight-medium">
                    Source File
                  </q-item-label>
                  <q-item-label>
                    {{ error.filename || 'Unknown' }}
                  </q-item-label>
                </q-item-section>
              </q-item>

              <q-separator />

              <q-item v-if="error.content">
                <q-item-section>
                  <q-item-label class="text-subtitle1 text-weight-medium">
                    Error Content
                  </q-item-label>
                  <q-item-label class="q-mt-sm">
                    <div class="error-content-container">
                      <pre class="error-content">{{ error.content }}</pre>
                      <q-btn 
                        v-if="error.content && error.content.length > 500"
                        flat
                        size="sm"
                        color="primary"
                        icon="unfold_more"
                        label="Show Full Content"
                        @click="showFullContent = !showFullContent"
                        class="q-mt-xs"
                      />
                    </div>
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>

            <!-- Original Log Entry -->
            <q-card flat bordered class="q-mt-md" v-if="error.raw_log_entry || error.content">
              <q-card-section>
                <div class="row items-center justify-between q-mb-sm">
                  <div class="text-subtitle1 text-weight-medium">
                    📄 Original Log Entry
                  </div>
                  <q-btn 
                    flat
                    round
                    dense
                    :icon="expandedLog ? 'fullscreen_exit' : 'fullscreen'"
                    @click="expandedLog = !expandedLog"
                    color="primary"
                  >
                    <q-tooltip>{{ expandedLog ? 'Collapse' : 'Expand' }}</q-tooltip>
                  </q-btn>
                </div>
                <div class="text-caption text-grey-7 q-mb-sm">
                  Raw log data from {{ error.filename }} ({{ getLogEntryLength() }} characters)
                </div>
                <pre 
                  :class="['log-entry', { 'log-entry-expanded': expandedLog }]"
                >{{ error.raw_log_entry || error.content }}</pre>
                <div class="row q-gutter-sm q-mt-sm">
                  <q-btn 
                    outline 
                    size="sm"
                    color="primary" 
                    icon="content_copy"
                    label="Copy Log"
                    @click="copyLogEntry"
                  />
                  <q-btn 
                    color="secondary" 
                    size="sm"
                    icon="open_in_new"
                    label="View Full File"
                    @click="openFullLogModal"
                    v-if="error.filename"
                  />
                  <q-btn 
                    outline
                    size="sm"
                    color="orange" 
                    icon="download"
                    label="Download Log"
                    @click="downloadLogEntry"
                  />
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- Right Column: Similar Errors -->
          <div class="col-12 col-md-6">
            <SimilarErrorsPanel 
              :selected-error="error"
              @error-selected="handleSimilarErrorSelected"
            />
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right" class="q-pa-md">
        <q-btn 
          flat 
          label="Copy Details" 
          color="primary" 
          icon="content_copy"
          @click="copyErrorDetails"
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

  <!-- Full Log Modal -->
  <q-dialog v-model="showFullLogModal" maximized>
    <q-card>
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">📄 Complete Log File: {{ error?.filename }}</div>
        <q-space />
        <q-btn 
          icon="close" 
          flat 
          round 
          dense 
          @click="showFullLogModal = false" 
        />
      </q-card-section>

      <q-card-section class="q-pt-none full-log-container">
        <div class="text-caption text-grey-7 q-mb-md">
          Full log content ({{ getLogEntryLength() }} characters)
        </div>
        <pre class="full-log-content">{{ error?.raw_log_entry || error?.content }}</pre>
      </q-card-section>

      <q-card-actions align="right" class="q-pa-md">
        <q-btn 
          outline
          label="Copy All" 
          color="primary" 
          icon="content_copy"
          @click="copyLogEntry"
        />
        <q-btn 
          outline
          label="Download" 
          color="secondary" 
          icon="download"
          @click="downloadLogEntry"
        />
        <q-btn 
          flat 
          label="Close" 
          color="grey" 
          @click="showFullLogModal = false"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'
import SimilarErrorsPanel from './SimilarErrorsPanel.vue'

interface ErrorDetail {
  id: number
  timestamp: string
  user: string
  type: string
  code: number
  severity: string
  content?: string
  filename?: string
}

const props = defineProps<{
  modelValue: boolean
  error: ErrorDetail | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'error-selected': [error: any]
}>()

const $q = useQuasar()

// Local state
const showFullContent = ref(false)
const expandedLog = ref(false)
const showFullLogModal = ref(false)

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

function getSeverityColor(severity: string): string {
  switch (severity?.toLowerCase()) {
    case 'critical': return 'negative'
    case 'high': return 'orange'
    case 'medium': return 'warning'
    case 'low': return 'positive'
    default: return 'grey'
  }
}

function closeModal() {
  isOpen.value = false
}

function copyErrorDetails() {
  if (!props.error) return
  
  const details = `
Error Details:
Type: ${props.error.type}
Code: ${props.error.code}
Severity: ${props.error.severity}
User: ${props.error.user}
Timestamp: ${props.error.timestamp}
File: ${props.error.filename || 'Unknown'}

Content:
${props.error.content || 'No additional content'}
  `.trim()

  navigator.clipboard.writeText(details).then(() => {
    $q.notify({
      type: 'positive',
      message: 'Error details copied to clipboard',
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

function handleSimilarErrorSelected(error: any) {
  // Close current modal and emit the new error selection
  isOpen.value = false
  emit('error-selected', error)
}

function copyLogEntry() {
  if (!props.error) return
  
  const logEntry = props.error.raw_log_entry || props.error.content || 'No log data available'
  
  navigator.clipboard.writeText(logEntry).then(() => {
    $q.notify({
      type: 'positive',
      message: 'Log entry copied to clipboard',
      timeout: 2000
    })
  }).catch(() => {
    $q.notify({
      type: 'negative',
      message: 'Failed to copy log entry',
      timeout: 2000
    })
  })
}

function getLogEntryLength(): string {
  const logEntry = props.error?.raw_log_entry || props.error?.content || ''
  return logEntry.length.toLocaleString()
}

function openFullLogModal() {
  showFullLogModal.value = true
}

function downloadLogEntry() {
  if (!props.error) return
  
  const logEntry = props.error.raw_log_entry || props.error.content || 'No log data available'
  const filename = props.error.filename || 'error-log'
  
  const blob = new Blob([logEntry], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename.replace(/\.[^/.]+$/, '')}-entry-${Date.now()}.log`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  $q.notify({
    type: 'positive',
    message: 'Log entry downloaded',
    timeout: 2000
  })
}
</script>

<style scoped>
.error-content {
  background-color: var(--q-color-grey-1);
  color: var(--q-color-on-surface);
  padding: 12px;
  border-radius: 4px;
  border: 1px solid var(--q-color-separator);
  font-family: 'Courier New', monospace;
  font-size: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
}

body.body--dark .error-content {
  background-color: var(--q-color-grey-9);
  color: var(--q-color-grey-3);
  border-color: var(--q-color-grey-7);
}

.log-entry {
  background-color: #2d3748;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #4a5568;
  font-family: 'Fira Code', 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
  font-size: 13px;
  line-height: 1.4;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 400px;
  overflow-y: auto;
  margin: 0;
  transition: max-height 0.3s ease;
}

.log-entry-expanded {
  max-height: 80vh;
}

body.body--light .log-entry {
  background-color: #f7fafc;
  color: #2d3748;
  border-color: #e2e8f0;
}

.log-entry::-webkit-scrollbar {
  width: 8px;
}

.log-entry::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.log-entry::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.log-entry::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.5);
}

.full-log-container {
  height: calc(100vh - 150px);
  padding: 16px;
}

.full-log-content {
  background-color: #1a202c;
  color: #e2e8f0;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #4a5568;
  font-family: 'Fira Code', 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  height: 100%;
  overflow: auto;
  margin: 0;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
}

body.body--light .full-log-content {
  background-color: #f8f9fa;
  color: #2d3748;
  border-color: #e2e8f0;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.1);
}

.full-log-content::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

.full-log-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 6px;
}

.full-log-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.4);
  border-radius: 6px;
}

.full-log-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.6);
}

.error-content-container {
  position: relative;
}
</style>