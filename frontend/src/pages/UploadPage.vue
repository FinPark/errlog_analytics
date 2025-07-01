<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md">
      <div class="text-h4">Upload Error Logs</div>
      <div class="text-subtitle1 text-grey-7">
        Upload your AMS error log files for analysis
      </div>
    </div>

    <!-- Log Type Selection -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6 q-mb-md">Select Log Type</div>
        <q-option-group
          v-model="selectedLogType"
          :options="logTypeOptions"
          color="primary"
          inline
        />
        <div class="text-caption text-grey-7 q-mt-sm">
          Choose the type of error logs you want to analyze
        </div>
      </q-card-section>
    </q-card>

    <!-- File Upload Area -->
    <q-card>
      <q-card-section>
        <div class="text-h6 q-mb-md">Upload Files</div>
        
        <!-- Drag & Drop Zone -->
        <div
          class="upload-zone q-pa-xl text-center"
          :class="{ 'upload-zone--dragover': isDragOver }"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="handleDrop"
        >
          <q-icon name="cloud_upload" size="64px" color="grey-5" />
          <div class="text-h6 q-mt-md">
            Drag & drop your log files here
          </div>
          <div class="text-subtitle2 text-grey-7 q-mb-md">
            or click to select files
          </div>
          
          <q-btn
            color="primary"
            icon="attach_file"
            label="Select Files"
            @click="triggerFileInput"
          />
          
          <input
            ref="fileInput"
            type="file"
            multiple
            accept=".log,.LOG"
            style="display: none"
            @change="handleFileSelect"
          />
        </div>

        <!-- File List -->
        <div v-if="uploadedFiles.length > 0" class="q-mt-md">
          <div class="row items-center justify-between q-mb-md">
            <div class="text-h6">Selected Files ({{ uploadedFiles.length }})</div>
            <q-btn
              color="primary"
              size="md"
              icon="upload"
              :label="isUploading ? 'Analyzing...' : 'Analyze Files'"
              :loading="isUploading"
              :disable="isUploading"
              @click="uploadFiles"
            />
          </div>
          
          <q-list bordered>
            <q-item
              v-for="(file, index) in uploadedFiles"
              :key="index"
              class="q-pa-md"
            >
              <q-item-section avatar>
                <q-icon
                  :name="getFileIcon(file.name)"
                  :color="getFileIconColor(file.name)"
                  size="md"
                />
              </q-item-section>
              
              <q-item-section>
                <q-item-label>{{ file.name }}</q-item-label>
                <q-item-label caption>
                  {{ formatFileSize(file.size) }} • {{ getDetectedType(file.name) }}
                </q-item-label>
              </q-item-section>
              
              <q-item-section side>
                <q-btn
                  flat
                  round
                  dense
                  icon="delete"
                  color="negative"
                  @click="removeFile(index)"
                />
              </q-item-section>
            </q-item>
          </q-list>
          
          <div v-if="isUploading" class="q-mt-sm text-center text-caption text-grey-7">
            Processing {{ uploadedFiles.length }} file(s)...
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Upload Progress -->
    <q-card v-if="isUploading || uploadComplete" class="q-mt-md">
      <q-card-section>
        <div class="text-h6 q-mb-md">
          <q-icon :name="uploadComplete ? 'check_circle' : 'upload'" 
                  :color="uploadComplete ? 'positive' : 'primary'" 
                  class="q-mr-sm" />
          {{ uploadComplete ? 'Analysis Complete' : 'Processing Files' }}
        </div>
        
        <div v-if="!uploadComplete">
          <q-linear-progress
            :value="uploadProgress"
            color="primary"
            size="md"
            class="q-mb-md"
            animation-speed="200"
          />
          <div class="text-center">
            {{ Math.round(uploadProgress * 100) }}% Complete
          </div>
          <div class="text-center text-caption text-grey-7 q-mt-sm">
            {{ uploadStatus }}
          </div>
        </div>
        
        <div v-else class="text-center">
          <q-icon name="check_circle" size="48px" color="positive" />
          <div class="text-h6 q-mt-md text-positive">Success!</div>
          <div class="text-subtitle1 q-mb-md">
            {{ uploadedFiles.length }} file(s) analyzed successfully
          </div>
          <div class="q-gutter-sm">
            <q-btn 
              color="primary" 
              label="View Results" 
              icon="dashboard"
              @click="$router.push('/dashboard')"
            />
            <q-btn 
              outline
              color="grey" 
              label="Analyze More Files" 
              icon="refresh"
              @click="resetUpload"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { uploadFiles as apiUploadFiles } from '@/services/api'

const router = useRouter()
const $q = useQuasar()

// Reactive state
const selectedLogType = ref('auto')
const uploadedFiles = ref<File[]>([])
const isDragOver = ref(false)
const isUploading = ref(false)
const uploadComplete = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref('')
const fileInput = ref<HTMLInputElement>()

// Log type options
const logTypeOptions = [
  { label: 'Auto-detect', value: 'auto' },
  { label: 'Visual Objects (E_*.LOG)', value: 'visual_objects' },
  { label: '.NET (EC_*.LOG)', value: 'dotnet' }
]

// File handling
function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files) {
    addFiles(Array.from(target.files))
  }
}

function handleDrop(event: DragEvent) {
  isDragOver.value = false
  if (event.dataTransfer?.files) {
    addFiles(Array.from(event.dataTransfer.files))
  }
}

function addFiles(files: File[]) {
  // Filter for .log files only
  const logFiles = files.filter(file => 
    file.name.toLowerCase().endsWith('.log')
  )
  
  if (logFiles.length === 0) {
    $q.notify({
      type: 'warning',
      message: 'Please select only .log files'
    })
    return
  }
  
  // Add files (avoid duplicates)
  logFiles.forEach(file => {
    if (!uploadedFiles.value.some(f => f.name === file.name)) {
      uploadedFiles.value.push(file)
    }
  })
  
  $q.notify({
    type: 'positive',
    message: `Added ${logFiles.length} file(s)`,
    timeout: 2000
  })
}

function removeFile(index: number) {
  uploadedFiles.value.splice(index, 1)
}

function getFileIcon(filename: string): string {
  if (filename.toUpperCase().startsWith('E_')) {
    return 'code'
  } else if (filename.toUpperCase().startsWith('EC_')) {
    return 'integration_instructions'
  }
  return 'description'
}

function getFileIconColor(filename: string): string {
  if (filename.toUpperCase().startsWith('E_')) {
    return 'blue'
  } else if (filename.toUpperCase().startsWith('EC_')) {
    return 'green'
  }
  return 'grey'
}

function getDetectedType(filename: string): string {
  if (filename.toUpperCase().startsWith('E_')) {
    return 'Visual Objects'
  } else if (filename.toUpperCase().startsWith('EC_')) {
    return '.NET'
  }
  return 'Unknown'
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Upload functionality
async function uploadFiles() {
  if (uploadedFiles.value.length === 0) {
    $q.notify({
      type: 'warning',
      message: 'Please select files to upload'
    })
    return
  }

  isUploading.value = true
  uploadComplete.value = false
  uploadProgress.value = 0
  
  const statusMessages = [
    'Uploading files...',
    'Validating file formats...',
    'Detecting log types...',
    'Parsing error entries...',
    'Analyzing timestamps...',
    'Processing error codes...',
    'Generating insights...',
    'Finalizing analysis...'
  ]

  try {
    // Realistic progress simulation with status messages
    let currentStep = 0
    uploadStatus.value = statusMessages[currentStep]
    
    const progressInterval = setInterval(() => {
      uploadProgress.value += 0.05
      
      // Update status message based on progress
      const progressPercent = uploadProgress.value * 100
      if (progressPercent > (currentStep + 1) * 12.5 && currentStep < statusMessages.length - 1) {
        currentStep++
        uploadStatus.value = statusMessages[currentStep]
      }
      
      if (uploadProgress.value >= 0.95) {
        clearInterval(progressInterval)
      }
    }, 200)

    // Actual API call
    console.log('Starting upload of', uploadedFiles.value.length, 'files')
    const result = await apiUploadFiles(uploadedFiles.value)
    console.log('Upload result:', result)
    
    clearInterval(progressInterval)
    uploadProgress.value = 1
    uploadStatus.value = 'Analysis complete!'
    
    // Show completion state
    setTimeout(() => {
      isUploading.value = false
      uploadComplete.value = true
      
      // Auto-redirect to dashboard after 2 seconds
      setTimeout(() => {
        console.log('Redirecting to dashboard...')
        router.push('/dashboard')
      }, 2000)
    }, 500)

    $q.notify({
      type: 'positive',
      message: 'Files analyzed successfully! Redirecting to dashboard...',
      timeout: 4000
    })

  } catch (error: any) {
    console.error('Upload failed:', error)
    isUploading.value = false
    uploadComplete.value = false
    
    // Extract detailed error information
    let errorMessage = 'Analysis failed'
    let errorDetails = ''
    
    if (error.response) {
      // Server responded with error
      errorMessage = `Server Error: ${error.response.status}`
      if (error.response.data) {
        if (typeof error.response.data === 'string') {
          errorDetails = error.response.data
        } else if (error.response.data.detail) {
          errorDetails = error.response.data.detail
        } else if (error.response.data.message) {
          errorDetails = error.response.data.message
        } else {
          errorDetails = JSON.stringify(error.response.data)
        }
      }
    } else if (error.request) {
      // Request made but no response
      errorMessage = 'Connection Error'
      errorDetails = 'Could not connect to backend. Please check if Docker containers are running.'
    } else {
      // Other errors
      errorMessage = 'Upload Error'
      errorDetails = error.message || 'Unknown error occurred'
    }
    
    $q.notify({
      type: 'negative',
      message: errorMessage,
      caption: errorDetails,
      timeout: 10000,
      actions: [
        { 
          label: 'Dismiss', 
          color: 'white',
          handler: () => { /* ... */ }
        }
      ]
    })
  }
}

// Reset upload state
function resetUpload() {
  uploadedFiles.value = []
  isUploading.value = false
  uploadComplete.value = false
  uploadProgress.value = 0
  uploadStatus.value = ''
  selectedLogType.value = 'auto'
}
</script>

<style scoped>
.upload-zone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-zone:hover,
.upload-zone--dragover {
  border-color: #1976d2;
  background-color: rgba(25, 118, 210, 0.05);
}
</style>