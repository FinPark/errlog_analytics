<template>
  <q-btn-dropdown
    color="secondary"
    icon="download"
    label="Export"
    dropdown-icon="expand_more"
  >
    <q-list>
      <q-item 
        clickable 
        v-close-popup 
        @click="exportAsCSV"
      >
        <q-item-section avatar>
          <q-icon name="table_chart" color="positive" />
        </q-item-section>
        <q-item-section>
          <q-item-label>Export as CSV</q-item-label>
          <q-item-label caption>Spreadsheet format</q-item-label>
        </q-item-section>
      </q-item>

      <q-item 
        clickable 
        v-close-popup 
        @click="exportAsJSON"
      >
        <q-item-section avatar>
          <q-icon name="data_object" color="info" />
        </q-item-section>
        <q-item-section>
          <q-item-label>Export as JSON</q-item-label>
          <q-item-label caption>Raw data format</q-item-label>
        </q-item-section>
      </q-item>

      <q-item 
        clickable 
        v-close-popup 
        @click="exportAsPDF"
      >
        <q-item-section avatar>
          <q-icon name="picture_as_pdf" color="negative" />
        </q-item-section>
        <q-item-section>
          <q-item-label>Export as PDF</q-item-label>
          <q-item-label caption>Report format</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-item 
        clickable 
        v-close-popup 
        @click="exportSummary"
      >
        <q-item-section avatar>
          <q-icon name="summarize" color="warning" />
        </q-item-section>
        <q-item-section>
          <q-item-label>Export Summary</q-item-label>
          <q-item-label caption>Statistics only</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar'

interface ExportData {
  errors: any[]
  summary: any
  filters?: any
}

const props = defineProps<{
  data: ExportData
  filename?: string
}>()

const $q = useQuasar()

function downloadFile(content: string, filename: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

function exportAsCSV() {
  try {
    const headers = ['ID', 'Timestamp', 'User', 'Error Type', 'Code', 'Severity', 'Filename']
    const csvContent = [
      headers.join(','),
      ...props.data.errors.map(error => [
        error.id,
        `"${error.timestamp}"`,
        `"${error.user}"`,
        `"${error.type}"`,
        error.code,
        `"${error.severity}"`,
        `"${error.filename || 'N/A'}"`
      ].join(','))
    ].join('\n')

    const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')
    const filename = props.filename || `error_log_export_${timestamp}.csv`
    
    downloadFile(csvContent, filename, 'text/csv')
    
    $q.notify({
      type: 'positive',
      message: `CSV export completed: ${filename}`,
      timeout: 3000
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to export CSV',
      timeout: 3000
    })
  }
}

function exportAsJSON() {
  try {
    const exportData = {
      exportInfo: {
        timestamp: new Date().toISOString(),
        totalErrors: props.data.errors.length,
        exportType: 'full'
      },
      summary: props.data.summary,
      filters: props.data.filters || null,
      errors: props.data.errors
    }

    const jsonContent = JSON.stringify(exportData, null, 2)
    const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')
    const filename = props.filename?.replace('.csv', '.json') || `error_log_export_${timestamp}.json`
    
    downloadFile(jsonContent, filename, 'application/json')
    
    $q.notify({
      type: 'positive',
      message: `JSON export completed: ${filename}`,
      timeout: 3000
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to export JSON',
      timeout: 3000
    })
  }
}

function exportAsPDF() {
  try {
    // Simple HTML-to-PDF export (basic implementation)
    const htmlContent = generatePDFContent()
    const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')
    const filename = props.filename?.replace('.csv', '.html') || `error_log_report_${timestamp}.html`
    
    downloadFile(htmlContent, filename, 'text/html')
    
    $q.notify({
      type: 'positive',
      message: `PDF Report (HTML) generated: ${filename}`,
      caption: 'Open in browser and print to PDF',
      timeout: 5000
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to generate PDF report',
      timeout: 3000
    })
  }
}

function exportSummary() {
  try {
    const summaryData = {
      exportInfo: {
        timestamp: new Date().toISOString(),
        exportType: 'summary'
      },
      statistics: props.data.summary,
      errorTypeCounts: getErrorTypeCounts(),
      userCounts: getUserCounts(),
      severityCounts: getSeverityCounts()
    }

    const jsonContent = JSON.stringify(summaryData, null, 2)
    const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')
    const filename = `error_log_summary_${timestamp}.json`
    
    downloadFile(jsonContent, filename, 'application/json')
    
    $q.notify({
      type: 'positive',
      message: `Summary export completed: ${filename}`,
      timeout: 3000
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Failed to export summary',
      timeout: 3000
    })
  }
}

function generatePDFContent(): string {
  const { summary, errors } = props.data
  const timestamp = new Date().toLocaleString()
  
  return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Error Log Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat { text-align: center; }
        .stat h3 { margin: 0; color: #1976d2; }
        .stat p { margin: 5px 0; font-size: 18px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .critical { color: #c10015; font-weight: bold; }
        .high { color: #ff9800; font-weight: bold; }
        .medium { color: #fbc02d; }
        .low { color: #4caf50; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Error Log Analysis Report</h1>
        <p>Generated on ${timestamp}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Summary Statistics</h2>
        <div class="stats">
            <div class="stat">
                <h3>Total Errors</h3>
                <p>${summary.totalErrors || 0}</p>
            </div>
            <div class="stat">
                <h3>Critical Errors</h3>
                <p>${summary.criticalErrors || 0}</p>
            </div>
            <div class="stat">
                <h3>Active Users</h3>
                <p>${summary.activeUsers || 0}</p>
            </div>
            <div class="stat">
                <h3>Files Analyzed</h3>
                <p>${summary.filesAnalyzed || 0}</p>
            </div>
        </div>
    </div>
    
    <h2>📋 Critical Errors (Top 10)</h2>
    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>User</th>
                <th>Error Type</th>
                <th>Code</th>
                <th>Severity</th>
            </tr>
        </thead>
        <tbody>
            ${errors.filter(e => e.severity === 'Critical').slice(0, 10).map(error => `
                <tr>
                    <td>${error.timestamp}</td>
                    <td>${error.user}</td>
                    <td>${error.type}</td>
                    <td>${error.code}</td>
                    <td class="critical">${error.severity}</td>
                </tr>
            `).join('')}
        </tbody>
    </table>
    
    <h2>📈 Recent Errors (Last 20)</h2>
    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>User</th>
                <th>Error Type</th>
                <th>Code</th>
                <th>Severity</th>
            </tr>
        </thead>
        <tbody>
            ${errors.slice(0, 20).map(error => `
                <tr>
                    <td>${error.timestamp}</td>
                    <td>${error.user}</td>
                    <td>${error.type}</td>
                    <td>${error.code}</td>
                    <td class="${error.severity.toLowerCase()}">${error.severity}</td>
                </tr>
            `).join('')}
        </tbody>
    </table>
</body>
</html>
  `.trim()
}

function getErrorTypeCounts() {
  const counts: Record<string, number> = {}
  props.data.errors.forEach(error => {
    counts[error.type] = (counts[error.type] || 0) + 1
  })
  return counts
}

function getUserCounts() {
  const counts: Record<string, number> = {}
  props.data.errors.forEach(error => {
    counts[error.user] = (counts[error.user] || 0) + 1
  })
  return counts
}

function getSeverityCounts() {
  const counts: Record<string, number> = {}
  props.data.errors.forEach(error => {
    counts[error.severity] = (counts[error.severity] || 0) + 1
  })
  return counts
}
</script>