<template>
  <q-card>
    <q-card-section>
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6">👥 User Risk Analysis</div>
          <div class="text-caption text-grey-7">
            ML-based risk assessment for all users
          </div>
        </div>
        <q-btn 
          outline 
          color="primary" 
          icon="refresh" 
          label="Refresh"
          @click="loadRiskData"
          :loading="loading"
          size="sm"
        />
      </div>

      <!-- Risk Distribution Summary -->
      <div class="row q-gutter-sm q-mb-md" v-if="riskData">
        <div class="col">
          <q-linear-progress 
            :value="riskData.risk_distribution.high_risk / riskData.total_users" 
            color="negative" 
            size="md"
          />
          <div class="text-caption q-mt-xs">
            🔴 High Risk: {{ riskData.risk_distribution.high_risk }}
          </div>
        </div>
        <div class="col">
          <q-linear-progress 
            :value="riskData.risk_distribution.medium_risk / riskData.total_users" 
            color="orange" 
            size="md"
          />
          <div class="text-caption q-mt-xs">
            🟡 Medium Risk: {{ riskData.risk_distribution.medium_risk }}
          </div>
        </div>
        <div class="col">
          <q-linear-progress 
            :value="riskData.risk_distribution.low_risk / riskData.total_users" 
            color="warning" 
            size="md"
          />
          <div class="text-caption q-mt-xs">
            🟠 Low Risk: {{ riskData.risk_distribution.low_risk }}
          </div>
        </div>
        <div class="col">
          <q-linear-progress 
            :value="riskData.risk_distribution.minimal_risk / riskData.total_users" 
            color="positive" 
            size="md"
          />
          <div class="text-caption q-mt-xs">
            🟢 Minimal Risk: {{ riskData.risk_distribution.minimal_risk }}
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center q-pa-md">
        <q-spinner-dots size="50px" color="primary" />
        <div class="text-subtitle1 q-mt-md">Analyzing user risk patterns...</div>
      </div>

      <!-- User Risk Heatmap -->
      <div v-else-if="riskData && riskData.heatmap_data.length > 0">
        <div class="text-subtitle1 q-mb-md">Risk Score Heatmap</div>
        
        <!-- Heatmap Grid -->
        <div class="risk-heatmap">
          <div 
            v-for="userData in riskData.heatmap_data" 
            :key="userData.user"
            class="risk-cell"
            :style="{ backgroundColor: userData.color }"
            @click="showUserDetails(userData)"
          >
            <div class="risk-cell-content">
              <div class="user-name">{{ userData.user }}</div>
              <div class="risk-score">{{ userData.risk_score }}/10</div>
              <div class="error-count">{{ userData.total_errors }} errors</div>
              <div class="critical-count" v-if="userData.critical_errors > 0">
                ⚠️ {{ userData.critical_errors }} critical
              </div>
            </div>
          </div>
        </div>

        <!-- Legend -->
        <div class="q-mt-md">
          <div class="text-caption text-grey-7 q-mb-xs">Risk Scale:</div>
          <div class="risk-legend">
            <div class="legend-item">
              <div class="legend-color" style="background-color: #f44336;"></div>
              <span>High (7.5-10)</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #ff9800;"></div>
              <span>Medium (5.0-7.5)</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #ffc107;"></div>
              <span>Low (2.5-5.0)</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #4caf50;"></div>
              <span>Minimal (0-2.5)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- No Data State -->
      <div v-else class="text-center q-pa-md">
        <q-icon name="person_off" size="48px" color="grey-5" />
        <div class="text-h6 q-mt-md">No user risk data available</div>
        <div class="text-caption text-grey-7">
          Upload error logs to see user risk analysis
        </div>
      </div>
    </q-card-section>

    <!-- User Details Modal -->
    <q-dialog v-model="showUserModal">
      <q-card style="min-width: 400px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">👤 {{ selectedUser?.user }} - Risk Analysis</div>
          <q-space />
          <q-btn icon="close" flat round dense @click="showUserModal = false" />
        </q-card-section>

        <q-card-section v-if="selectedUser">
          <!-- Risk Score Header -->
          <div class="text-center q-mb-md">
            <div 
              class="risk-score-large"
              :style="{ color: selectedUser.color }"
            >
              {{ selectedUser.risk_score }}/10
            </div>
            <div class="text-subtitle1">{{ selectedUser.category }}</div>
          </div>

          <!-- Statistics -->
          <q-list>
            <q-item>
              <q-item-section avatar>
                <q-icon name="error" color="negative" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Total Errors</q-item-label>
                <q-item-label caption>{{ selectedUser.total_errors }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item v-if="selectedUser.critical_errors > 0">
              <q-item-section avatar>
                <q-icon name="warning" color="orange" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Critical Errors</q-item-label>
                <q-item-label caption>{{ selectedUser.critical_errors }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>

          <!-- Insights -->
          <div class="q-mt-md">
            <div class="text-subtitle2 q-mb-sm">💡 AI Insights</div>
            <div v-for="(insight, index) in selectedUser.insights" :key="index" class="q-mb-sm">
              <q-chip 
                outline 
                color="primary" 
                icon="psychology"
                size="sm"
              >
                {{ insight }}
              </q-chip>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Close" @click="showUserModal = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { MLApiService, type UserRiskHeatmapData } from '@/services/ml-api'

const $q = useQuasar()

// Data
const loading = ref(false)
const riskData = ref<UserRiskHeatmapData | null>(null)
const showUserModal = ref(false)
const selectedUser = ref<any>(null)

// Methods
async function loadRiskData() {
  loading.value = true
  try {
    riskData.value = await MLApiService.getUserRiskHeatmap()
  } catch (error) {
    console.error('Error loading user risk data:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load user risk analysis',
      timeout: 3000
    })
  } finally {
    loading.value = false
  }
}

function showUserDetails(userData: any) {
  selectedUser.value = userData
  showUserModal.value = true
}

// Lifecycle
onMounted(() => {
  loadRiskData()
})
</script>

<style scoped>
.risk-heatmap {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.risk-cell {
  padding: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.risk-cell:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.risk-cell-content {
  text-align: center;
}

.user-name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 4px;
}

.risk-score {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.error-count {
  font-size: 12px;
  opacity: 0.9;
}

.critical-count {
  font-size: 11px;
  margin-top: 2px;
  opacity: 0.9;
}

.risk-legend {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.risk-score-large {
  font-size: 48px;
  font-weight: bold;
  line-height: 1;
}
</style>