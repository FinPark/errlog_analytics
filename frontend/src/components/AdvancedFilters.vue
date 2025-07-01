<template>
  <q-card class="q-mb-md">
    <q-card-section>
      <div class="row items-center justify-between q-mb-md">
        <div class="text-h6">🔍 Advanced Filters</div>
        <q-btn 
          flat 
          dense 
          :icon="showFilters ? 'expand_less' : 'expand_more'"
          @click="showFilters = !showFilters"
        />
      </div>

      <q-slide-transition>
        <div v-show="showFilters">
          <div class="row q-gutter-md">
            <!-- Search Input -->
            <div class="col-12 col-md-4">
              <q-input
                v-model="localFilters.search"
                label="Search in error content"
                placeholder="Type to search..."
                outlined
                clearable
                debounce="300"
                @update:model-value="updateFilters"
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>

            <!-- User Filter -->
            <div class="col-12 col-md-2">
              <q-select
                v-model="localFilters.users"
                :options="userOptions"
                label="Users"
                outlined
                multiple
                clearable
                use-chips
                @update:model-value="updateFilters"
              >
                <template v-slot:prepend>
                  <q-icon name="person" />
                </template>
              </q-select>
            </div>

            <!-- Severity Filter -->
            <div class="col-12 col-md-2">
              <q-select
                v-model="localFilters.severities"
                :options="severityOptions"
                label="Severity"
                outlined
                multiple
                clearable
                use-chips
                @update:model-value="updateFilters"
              >
                <template v-slot:prepend>
                  <q-icon name="warning" />
                </template>
              </q-select>
            </div>

            <!-- Error Type Filter -->
            <div class="col-12 col-md-4">
              <q-select
                v-model="localFilters.errorTypes"
                :options="errorTypeOptions"
                label="Error Types"
                outlined
                multiple
                clearable
                use-chips
                @update:model-value="updateFilters"
              >
                <template v-slot:prepend>
                  <q-icon name="error" />
                </template>
              </q-select>
            </div>
          </div>

          <!-- Date Range Filter -->
          <div class="row q-gutter-md q-mt-md">
            <div class="col-12 col-md-3">
              <q-input
                v-model="localFilters.dateFrom"
                label="From Date"
                outlined
                type="date"
                @update:model-value="updateFilters"
              >
                <template v-slot:prepend>
                  <q-icon name="event" />
                </template>
              </q-input>
            </div>

            <div class="col-12 col-md-3">
              <q-input
                v-model="localFilters.dateTo"
                label="To Date"
                outlined
                type="date"
                @update:model-value="updateFilters"
              >
                <template v-slot:prepend>
                  <q-icon name="event" />
                </template>
              </q-input>
            </div>

            <!-- Quick Date Filters -->
            <div class="col-12 col-md-6">
              <div class="text-caption q-mb-sm">Quick filters:</div>
              <q-btn-group flat>
                <q-btn 
                  flat 
                  size="sm" 
                  label="Today" 
                  @click="setQuickDateFilter('today')"
                />
                <q-btn 
                  flat 
                  size="sm" 
                  label="Last 7 days" 
                  @click="setQuickDateFilter('week')"
                />
                <q-btn 
                  flat 
                  size="sm" 
                  label="Last 30 days" 
                  @click="setQuickDateFilter('month')"
                />
                <q-btn 
                  flat 
                  size="sm" 
                  label="Clear" 
                  @click="clearDateFilters"
                />
              </q-btn-group>
            </div>
          </div>

          <!-- Filter Actions -->
          <div class="row justify-end q-mt-md">
            <q-btn 
              flat 
              color="grey" 
              label="Reset All" 
              @click="resetFilters"
            />
            <q-btn 
              color="primary" 
              label="Apply Filters" 
              class="q-ml-sm"
              @click="applyFilters"
            />
          </div>

          <!-- Active Filters Summary -->
          <div v-if="hasActiveFilters" class="q-mt-md">
            <div class="text-caption text-grey-7 q-mb-sm">Active filters:</div>
            <div class="q-gutter-xs">
              <q-chip 
                v-if="localFilters.search"
                removable 
                @remove="localFilters.search = ''; updateFilters()"
                color="primary" 
                text-color="white"
                size="sm"
              >
                Search: "{{ localFilters.search }}"
              </q-chip>
              
              <q-chip 
                v-for="user in localFilters.users"
                :key="user"
                removable 
                @remove="removeFromArray(localFilters.users, user); updateFilters()"
                color="info" 
                text-color="white"
                size="sm"
              >
                User: {{ user }}
              </q-chip>
              
              <q-chip 
                v-for="severity in localFilters.severities"
                :key="severity"
                removable 
                @remove="removeFromArray(localFilters.severities, severity); updateFilters()"
                :color="getSeverityColor(severity)" 
                text-color="white"
                size="sm"
              >
                {{ severity }}
              </q-chip>
              
              <q-chip 
                v-for="errorType in localFilters.errorTypes"
                :key="errorType"
                removable 
                @remove="removeFromArray(localFilters.errorTypes, errorType); updateFilters()"
                color="secondary" 
                text-color="white"
                size="sm"
              >
                {{ errorType }}
              </q-chip>
              
              <q-chip 
                v-if="localFilters.dateFrom || localFilters.dateTo"
                removable 
                @remove="clearDateFilters"
                color="warning" 
                text-color="white"
                size="sm"
              >
                {{ formatDateRange() }}
              </q-chip>
            </div>
          </div>
        </div>
      </q-slide-transition>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

interface FilterOptions {
  search: string
  users: string[]
  severities: string[]
  errorTypes: string[]
  dateFrom: string
  dateTo: string
}

const props = defineProps<{
  errors: any[]
  modelValue: FilterOptions
}>()

const emit = defineEmits<{
  'update:modelValue': [value: FilterOptions]
  'filter': [filteredErrors: any[]]
}>()

const showFilters = ref(false)

const localFilters = ref<FilterOptions>({
  search: '',
  users: [],
  severities: [],
  errorTypes: [],
  dateFrom: '',
  dateTo: ''
})

// Options for dropdowns
const userOptions = computed(() => 
  [...new Set(props.errors.map(e => e.user))].sort()
)

const severityOptions = computed(() => 
  [...new Set(props.errors.map(e => e.severity))].sort()
)

const errorTypeOptions = computed(() => 
  [...new Set(props.errors.map(e => e.type))].sort()
)

const hasActiveFilters = computed(() => 
  localFilters.value.search ||
  localFilters.value.users.length > 0 ||
  localFilters.value.severities.length > 0 ||
  localFilters.value.errorTypes.length > 0 ||
  localFilters.value.dateFrom ||
  localFilters.value.dateTo
)

// Watch for prop changes
watch(() => props.modelValue, (newVal) => {
  localFilters.value = { ...newVal }
}, { immediate: true })

function updateFilters() {
  emit('update:modelValue', { ...localFilters.value })
  applyFilters()
}

function applyFilters() {
  let filtered = [...props.errors]

  // Text search
  if (localFilters.value.search) {
    const searchTerm = localFilters.value.search.toLowerCase()
    filtered = filtered.filter(error => 
      error.type.toLowerCase().includes(searchTerm) ||
      error.user.toLowerCase().includes(searchTerm) ||
      (error.content && error.content.toLowerCase().includes(searchTerm)) ||
      (error.filename && error.filename.toLowerCase().includes(searchTerm))
    )
  }

  // User filter
  if (localFilters.value.users.length > 0) {
    filtered = filtered.filter(error => 
      localFilters.value.users.includes(error.user)
    )
  }

  // Severity filter
  if (localFilters.value.severities.length > 0) {
    filtered = filtered.filter(error => 
      localFilters.value.severities.includes(error.severity)
    )
  }

  // Error type filter
  if (localFilters.value.errorTypes.length > 0) {
    filtered = filtered.filter(error => 
      localFilters.value.errorTypes.includes(error.type)
    )
  }

  // Date range filter
  if (localFilters.value.dateFrom || localFilters.value.dateTo) {
    filtered = filtered.filter(error => {
      const errorDate = parseErrorDate(error.timestamp)
      if (!errorDate) return true

      const fromDate = localFilters.value.dateFrom ? new Date(localFilters.value.dateFrom) : null
      const toDate = localFilters.value.dateTo ? new Date(localFilters.value.dateTo) : null

      if (fromDate && errorDate < fromDate) return false
      if (toDate && errorDate > toDate) return false

      return true
    })
  }

  emit('filter', filtered)
}

function parseErrorDate(timestamp: string): Date | null {
  try {
    // Parse DD.MM.YYYY HH:MM:SS format
    const parts = timestamp.split(' ')
    if (parts.length !== 2) return null
    
    const [datePart] = parts
    const [day, month, year] = datePart.split('.')
    
    return new Date(parseInt(year), parseInt(month) - 1, parseInt(day))
  } catch {
    return null
  }
}

function setQuickDateFilter(period: string) {
  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]

  switch (period) {
    case 'today':
      localFilters.value.dateFrom = todayStr
      localFilters.value.dateTo = todayStr
      break
    case 'week':
      const weekAgo = new Date(today)
      weekAgo.setDate(today.getDate() - 7)
      localFilters.value.dateFrom = weekAgo.toISOString().split('T')[0]
      localFilters.value.dateTo = todayStr
      break
    case 'month':
      const monthAgo = new Date(today)
      monthAgo.setDate(today.getDate() - 30)
      localFilters.value.dateFrom = monthAgo.toISOString().split('T')[0]
      localFilters.value.dateTo = todayStr
      break
  }
  updateFilters()
}

function clearDateFilters() {
  localFilters.value.dateFrom = ''
  localFilters.value.dateTo = ''
  updateFilters()
}

function resetFilters() {
  localFilters.value = {
    search: '',
    users: [],
    severities: [],
    errorTypes: [],
    dateFrom: '',
    dateTo: ''
  }
  updateFilters()
}

function removeFromArray(array: string[], item: string) {
  const index = array.indexOf(item)
  if (index > -1) {
    array.splice(index, 1)
  }
}

function getSeverityColor(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'critical': return 'negative'
    case 'high': return 'orange'
    case 'medium': return 'warning'
    case 'low': return 'positive'
    default: return 'grey'
  }
}

function formatDateRange(): string {
  if (localFilters.value.dateFrom && localFilters.value.dateTo) {
    return `${localFilters.value.dateFrom} - ${localFilters.value.dateTo}`
  } else if (localFilters.value.dateFrom) {
    return `From ${localFilters.value.dateFrom}`
  } else if (localFilters.value.dateTo) {
    return `Until ${localFilters.value.dateTo}`
  }
  return 'Date range'
}

onMounted(() => {
  // Apply initial filters
  applyFilters()
})
</script>