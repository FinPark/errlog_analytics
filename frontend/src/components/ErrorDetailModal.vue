<template>
  <q-dialog v-model="isOpen" persistent>
    <q-card style="min-width: 700px; max-width: 90vw;">
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
                <pre class="error-content">{{ error.content }}</pre>
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
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
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'

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
}>()

const $q = useQuasar()

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
</style>