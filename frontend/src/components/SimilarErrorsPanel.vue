<template>
  <q-card>
    <q-card-section>
      <div class="text-h6 q-mb-md">🔗 Similar Errors</div>
      
      <!-- Loading State -->
      <div v-if="loading" class="text-center q-pa-md">
        <q-spinner-dots size="30px" color="primary" />
        <div class="text-caption q-mt-sm">Finding similar errors...</div>
      </div>

      <!-- Similar Errors List -->
      <div v-else-if="similarErrors.length > 0">
        <div class="text-caption text-grey-7 q-mb-md">
          Found {{ similarErrors.length }} similar errors based on ML analysis
        </div>

        <q-list>
          <q-item
            v-for="(error, index) in similarErrors"
            :key="error.id"
            clickable
            @click="$emit('error-selected', error)"
            class="similar-error-item"
          >
            <q-item-section avatar>
              <q-circular-progress
                :value="error.similarity_percentage"
                size="40px"
                :thickness="0.2"
                color="primary"
                track-color="grey-3"
                class="q-ma-md"
              >
                <div class="text-caption">{{ error.similarity_percentage }}%</div>
              </q-circular-progress>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-weight-medium">
                {{ error.type }}
              </q-item-label>
              <q-item-label caption>
                {{ error.user }} • {{ error.timestamp }}
              </q-item-label>
              <q-item-label caption class="similarity-info">
                Similarity: {{ error.similarity_score.toFixed(3) }}
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
                <div class="text-caption text-grey-6 q-mt-xs">
                  #{{ error.id }}
                </div>
              </div>
            </q-item-section>
          </q-item>
        </q-list>

        <!-- Show More Button -->
        <div class="text-center q-mt-md" v-if="canLoadMore">
          <q-btn
            outline
            color="primary"
            label="Load More Similar"
            @click="loadMoreSimilar"
            :loading="loadingMore"
            size="sm"
          />
        </div>
      </div>

      <!-- No Similar Errors -->
      <div v-else class="text-center q-pa-md">
        <q-icon name="search_off" size="48px" color="grey-5" />
        <div class="text-subtitle1 q-mt-md">No similar errors found</div>
        <div class="text-caption text-grey-7">
          This error appears to be unique in the dataset
        </div>
      </div>

      <!-- ML Insights -->
      <div v-if="mlInsights.length > 0" class="q-mt-md q-pt-md" style="border-top: 1px solid #e0e0e0;">
        <div class="text-subtitle2 q-mb-sm">🤖 ML Insights</div>
        <div v-for="(insight, index) in mlInsights" :key="index" class="q-mb-xs">
          <q-chip
            outline
            color="secondary"
            icon="psychology"
            size="sm"
          >
            {{ insight }}
          </q-chip>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useQuasar } from 'quasar'
import { MLApiService, type SimilarError } from '@/services/ml-api'

interface Props {
  selectedError: any | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'error-selected': [error: any]
}>()

const $q = useQuasar()

// Data
const loading = ref(false)
const loadingMore = ref(false)
const similarErrors = ref<SimilarError[]>([])
const currentLimit = ref(5)
const canLoadMore = ref(true)
const mlInsights = ref<string[]>([])

// Methods
async function findSimilarErrors() {
  if (!props.selectedError || !props.selectedError.id) {
    similarErrors.value = []
    return
  }

  loading.value = true
  try {
    const errors = await MLApiService.getSimilarErrors(props.selectedError.id, currentLimit.value)
    similarErrors.value = errors
    
    // Generate ML insights based on similarity patterns
    generateMLInsights(errors)
    
    // Check if we can load more
    canLoadMore.value = errors.length === currentLimit.value
    
  } catch (error) {
    console.error('Error finding similar errors:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to find similar errors',
      timeout: 3000
    })
    similarErrors.value = []
  } finally {
    loading.value = false
  }
}

async function loadMoreSimilar() {
  if (!props.selectedError || !props.selectedError.id) return

  loadingMore.value = true
  currentLimit.value += 5

  try {
    const errors = await MLApiService.getSimilarErrors(props.selectedError.id, currentLimit.value)
    similarErrors.value = errors
    canLoadMore.value = errors.length === currentLimit.value
  } catch (error) {
    console.error('Error loading more similar errors:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load more similar errors',
      timeout: 3000
    })
  } finally {
    loadingMore.value = false
  }
}

function generateMLInsights(errors: SimilarError[]) {
  const insights = []

  if (errors.length === 0) {
    mlInsights.value = []
    return
  }

  // Analyze similarity scores
  const highSimilarity = errors.filter(e => e.similarity_percentage >= 80)
  const mediumSimilarity = errors.filter(e => e.similarity_percentage >= 50 && e.similarity_percentage < 80)

  if (highSimilarity.length > 0) {
    insights.push(`${highSimilarity.length} errors with >80% similarity - likely same root cause`)
  }

  if (mediumSimilarity.length > 0) {
    insights.push(`${mediumSimilarity.length} errors with moderate similarity - related issues`)
  }

  // Analyze user patterns
  const userCounts = new Map<string, number>()
  errors.forEach(error => {
    userCounts.set(error.user, (userCounts.get(error.user) || 0) + 1)
  })

  const dominantUser = Array.from(userCounts.entries()).reduce((a, b) => a[1] > b[1] ? a : b, ['', 0])
  if (dominantUser[1] > errors.length * 0.5) {
    insights.push(`User ${dominantUser[0]} experiences most similar errors - training opportunity`)
  }

  // Analyze severity patterns
  const severityCounts = new Map<string, number>()
  errors.forEach(error => {
    severityCounts.set(error.severity, (severityCounts.get(error.severity) || 0) + 1)
  })

  const criticalCount = severityCounts.get('Critical') || 0
  if (criticalCount > 0) {
    insights.push(`${criticalCount} similar critical errors - high priority investigation needed`)
  }

  // Time pattern insights
  if (errors.length >= 3) {
    insights.push(`Pattern affects multiple users/times - systemic issue likely`)
  }

  mlInsights.value = insights.slice(0, 3) // Top 3 insights
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

// Watch for selected error changes
watch(() => props.selectedError, () => {
  currentLimit.value = 5
  findSimilarErrors()
}, { immediate: true })
</script>

<style scoped>
.similar-error-item {
  border-radius: 8px;
  margin-bottom: 8px;
  transition: background-color 0.2s;
}

.similar-error-item:hover {
  background-color: rgba(25, 118, 210, 0.04);
}

.similarity-info {
  color: #1976d2;
  font-weight: 500;
}
</style>