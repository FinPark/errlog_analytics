<template>
  <q-page class="flex flex-center">
    <div class="text-center">
      <div class="text-h2 text-primary q-mb-md">
        <q-icon name="analytics" size="100px" />
      </div>
      <div class="text-h3 q-mb-md">Error Log Analytics</div>
      <div class="text-h6 text-grey-7 q-mb-xl">
        Advanced analysis of AMS error logs (Visual Objects & .NET)
      </div>
      
      <div class="row q-gutter-md justify-center">
        <q-card class="q-pa-md" style="min-width: 250px">
          <q-card-section class="text-center">
            <q-icon name="upload" size="48px" color="primary" />
            <div class="text-h6 q-mt-md">Upload Logs</div>
            <div class="text-caption text-grey-7">
              Upload multiple log files for analysis
            </div>
          </q-card-section>
          <q-card-actions align="center">
            <q-btn
              color="primary"
              to="/upload"
              label="Start Upload"
              icon="upload"
            />
          </q-card-actions>
        </q-card>
        
        <q-card class="q-pa-md" style="min-width: 250px">
          <q-card-section class="text-center">
            <q-icon name="dashboard" size="48px" color="secondary" />
            <div class="text-h6 q-mt-md">Dashboard</div>
            <div class="text-caption text-grey-7">
              View analytics and visualizations
            </div>
          </q-card-section>
          <q-card-actions align="center">
            <q-btn
              color="secondary"
              to="/dashboard"
              label="View Dashboard"
              icon="dashboard"
            />
          </q-card-actions>
        </q-card>
      </div>
      
      <!-- Features Overview -->
      <div class="q-mt-xl">
        <div class="text-h5 q-mb-md">Features</div>
        <div class="row q-gutter-md justify-center">
          <q-chip icon="code" color="positive" text-color="white">
            Dual Format Support
          </q-chip>
          <q-chip icon="timeline" color="info" text-color="white">
            Timeline Analysis
          </q-chip>
          <q-chip icon="warning" color="orange" text-color="white">
            Critical Error Detection
          </q-chip>
          <q-chip icon="person" color="purple" text-color="white">
            User Activity Analysis
          </q-chip>
          <q-chip icon="bar_chart" color="teal" text-color="white">
            Interactive Charts
          </q-chip>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// Home page component
</script>