#!/usr/bin/env node
/**
 * Generate Autodrive Thumbnails
 * 
 * Creates SVG-based thumbnails for autonomous driving scenarios.
 * These are styled representations of traffic scenes that better match
 * the described scenarios than random placeholder images.
 * 
 * Usage: node scripts/generate-autodrive-thumbnails.js
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const THUMBNAILS_DIR = path.join(__dirname, '..', 'public', 'images', 'thumbnails')
const IMAGE_WIDTH = 400
const IMAGE_HEIGHT = 225

// Traffic scene scenarios with styled SVG representations
const objectScenarios = [
  {
    id: 'bus-barrier',
    objects: ['bus', 'barrier'],
    description: 'Bus stopped at intersection with construction barriers on the roadside. Urban transit scene.',
    colors: { bg: '#4A5568', accent: '#ED8936', secondary: '#718096' }
  },
  {
    id: 'motorcycle-truck',
    objects: ['motorcycle', 'truck'],
    description: 'Motorcycle passing a large truck on highway. Clear visibility with moderate traffic flow.',
    colors: { bg: '#2D3748', accent: '#4299E1', secondary: '#A0AEC0' }
  },
  {
    id: 'motorcycle-barrier-cone',
    objects: ['motorcycle', 'barrier', 'traffic-cone'],
    description: 'Motorcycle navigating through road work zone with traffic cones and barriers.',
    colors: { bg: '#744210', accent: '#F6E05E', secondary: '#ED8936' }
  },
  {
    id: 'motorcycle-pedestrian',
    objects: ['motorcycle', 'pedestrian'],
    description: 'Motorcycle waiting at crosswalk with pedestrians crossing. Urban intersection scene.',
    colors: { bg: '#2C5282', accent: '#9AE6B4', secondary: '#F687B3' }
  },
  {
    id: 'pedestrian-cone-cyclist',
    objects: ['pedestrian', 'traffic-cone', 'cyclist'],
    description: 'Cyclist and pedestrians sharing path near construction cones. Shared urban space.',
    colors: { bg: '#285E61', accent: '#4FD1C5', secondary: '#ED8936' }
  },
  {
    id: 'car-motorcycle',
    objects: ['car', 'motorcycle'],
    description: 'Car and motorcycle side by side at traffic light. Downtown urban traffic scene.',
    colors: { bg: '#2D3748', accent: '#FC8181', secondary: '#63B3ED' }
  },
  {
    id: 'cone-bus-motorcycle',
    objects: ['traffic-cone', 'bus', 'motorcycle'],
    description: 'Bus and motorcycle navigating through temporary traffic cone lane markers.',
    colors: { bg: '#744210', accent: '#F6AD55', secondary: '#4A5568' }
  },
  {
    id: 'car-truck-barrier',
    objects: ['car', 'truck', 'barrier'],
    description: 'Car following truck on highway with concrete barriers. Heavy vehicle traffic scene.',
    colors: { bg: '#1A365D', accent: '#A0AEC0', secondary: '#718096' }
  },
  {
    id: 'pedestrian-car',
    objects: ['pedestrian', 'car'],
    description: 'Pedestrians crossing street while car waits at crosswalk. Urban intersection.',
    colors: { bg: '#2A4365', accent: '#F687B3', secondary: '#63B3ED' }
  },
  {
    id: 'cyclist-car-cone',
    objects: ['cyclist', 'car', 'traffic-cone'],
    description: 'Cyclist in bike lane with cars passing by. Road work cones marking construction area.',
    colors: { bg: '#2C5282', accent: '#68D391', secondary: '#ED8936' }
  },
  {
    id: 'truck-barrier',
    objects: ['truck', 'barrier'],
    description: 'Large commercial truck navigating through construction barriers. Industrial area.',
    colors: { bg: '#2D3748', accent: '#A0AEC0', secondary: '#4A5568' }
  },
  {
    id: 'bus-pedestrian-cyclist',
    objects: ['bus', 'pedestrian', 'cyclist'],
    description: 'Bus at bus stop with cyclists passing and pedestrians boarding. Transit hub scene.',
    colors: { bg: '#2B6CB0', accent: '#F6E05E', secondary: '#9AE6B4' }
  },
  {
    id: 'motorcycle-cone',
    objects: ['motorcycle', 'traffic-cone'],
    description: 'Motorcycle rider weaving through traffic cone marked temporary lanes.',
    colors: { bg: '#744210', accent: '#ED8936', secondary: '#F6AD55' }
  },
  {
    id: 'car-pedestrian-barrier',
    objects: ['car', 'pedestrian', 'barrier'],
    description: 'Car stopped at barrier-guarded pedestrian zone. Downtown shopping district.',
    colors: { bg: '#2D3748', accent: '#63B3ED', secondary: '#F687B3' }
  },
  {
    id: 'truck-cyclist',
    objects: ['truck', 'cyclist'],
    description: 'Cyclist sharing road with delivery truck. Urban delivery route scene.',
    colors: { bg: '#2C5282', accent: '#A0AEC0', secondary: '#68D391' }
  },
  {
    id: 'bus-car',
    objects: ['bus', 'car'],
    description: 'Bus in dedicated lane with cars in adjacent lanes. Public transit corridor.',
    colors: { bg: '#2B6CB0', accent: '#63B3ED', secondary: '#A0AEC0' }
  },
  {
    id: 'motorcycle-cyclist-pedestrian',
    objects: ['motorcycle', 'cyclist', 'pedestrian'],
    description: 'Mixed traffic with motorcycle, cyclist, and pedestrians. Shared urban street.',
    colors: { bg: '#4A5568', accent: '#F6AD55', secondary: '#68D391' }
  },
  {
    id: 'cone-barrier-car',
    objects: ['traffic-cone', 'barrier', 'car'],
    description: 'Cars navigating through construction zone with barriers and cones. Road work area.',
    colors: { bg: '#744210', accent: '#ED8936', secondary: '#63B3ED' }
  },
  {
    id: 'truck-motorcycle-cone',
    objects: ['truck', 'motorcycle', 'traffic-cone'],
    description: 'Truck and motorcycle on road marked with traffic cones. Lane restriction zone.',
    colors: { bg: '#2D3748', accent: '#F6AD55', secondary: '#A0AEC0' }
  },
  {
    id: 'pedestrian-cyclist-barrier',
    objects: ['pedestrian', 'cyclist', 'barrier'],
    description: 'Pedestrians and cyclists on separated path with barrier protection. Safe corridor.',
    colors: { bg: '#285E61', accent: '#68D391', secondary: '#4FD1C5' }
  }
]

// Icon SVGs for different object types
const icons = {
  car: `<rect x="30" y="70" width="60" height="35" rx="8" fill="currentColor"/><rect x="35" y="60" width="50" height="15" rx="5" fill="currentColor" opacity="0.8"/><circle cx="42" cy="105" r="8" fill="#1A202C"/><circle cx="78" cy="105" r="8" fill="#1A202C"/>`,
  truck: `<rect x="20" y="55" width="80" height="50" rx="4" fill="currentColor"/><rect x="25" y="60" width="70" height="30" fill="currentColor" opacity="0.7"/><circle cx="35" cy="105" r="8" fill="#1A202C"/><circle cx="85" cy="105" r="8" fill="#1A202C"/>`,
  bus: `<rect x="15" y="45" width="90" height="60" rx="6" fill="currentColor"/><rect x="20" y="50" width="80" height="25" rx="3" fill="currentColor" opacity="0.6"/><rect x="20" y="80" width="15" height="15" rx="2" fill="#1A202C" opacity="0.3"/><circle cx="35" cy="105" r="9" fill="#1A202C"/><circle cx="85" cy="105" r="9" fill="#1A202C"/>`,
  motorcycle: `<circle cx="40" cy="95" r="12" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="80" cy="95" r="12" fill="none" stroke="currentColor" stroke-width="6"/><path d="M40 95 L55 75 L65 75 L80 95" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><path d="M55 75 L50 55 L70 55" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>`,
  pedestrian: `<circle cx="60" cy="45" r="12" fill="currentColor"/><path d="M60 60 L60 100 M60 65 L45 85 M60 65 L75 85 M45 110 L60 100 L75 110" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>`,
  cyclist: `<circle cx="45" cy="90" r="10" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="85" cy="90" r="10" fill="none" stroke="currentColor" stroke-width="4"/><path d="M45 90 L60 70 L75 70 L85 90 M60 70 L55 50 L70 50" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><circle cx="60" cy="45" r="8" fill="currentColor"/>`,
  'traffic-cone': `<polygon points="60,25 45,95 75,95" fill="currentColor"/><rect x="47" y="55" width="26" height="12" fill="#1A202C" opacity="0.3"/><rect x="45" y="90" width="30" height="10" rx="2" fill="currentColor" opacity="0.7"/>`,
  barrier: `<rect x="20" y="60" width="80" height="40" rx="3" fill="currentColor" opacity="0.8"/><rect x="30" y="65" width="60" height="8" fill="#1A202C" opacity="0.2"/><rect x="30" y="87" width="60" height="8" fill="#1A202C" opacity="0.2"/><rect x="25" y="55" width="8" height="50" rx="2" fill="currentColor"/><rect x="67" y="55" width="8" height="50" rx="2" fill="currentColor" opacity="0.9"/>`
}

function generateSVG(scenario) {
  const { id, objects, description, colors } = scenario
  
  // Create object icons based on the objects in this scenario
  const objectIcons = objects.map((obj, i) => {
    const icon = icons[obj] || icons.car
    const x = 60 + (i % 3) * 120
    const y = 60 + Math.floor(i / 3) * 50
    const scale = objects.length > 2 ? 0.7 : 0.9
    const offsetX = objects.length === 1 ? 80 : objects.length === 2 ? 40 : 0
    
    return `
      <g transform="translate(${x + offsetX}, ${y}) scale(${scale})" style="color: ${i === 0 ? colors.accent : colors.secondary}">
        ${icon}
      </g>
    `
  }).join('')
  
  // Create object labels
  const objectLabels = objects.map((obj, i) => {
    const labels = {
      'car': 'CAR', 'truck': 'TRUCK', 'bus': 'BUS', 
      'motorcycle': 'MOTO', 'pedestrian': 'PED', 
      'cyclist': 'BIKE', 'traffic-cone': 'CONE', 'barrier': 'BARRIER'
    }
    return labels[obj] || obj.toUpperCase()
  }).join(' • ')
  
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${IMAGE_WIDTH}" height="${IMAGE_HEIGHT}" viewBox="0 0 ${IMAGE_WIDTH} ${IMAGE_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-${id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${colors.bg};stop-opacity:1" />
      <stop offset="100%" style="stop-color:${colors.bg};stop-opacity:0.7" />
    </linearGradient>
    <filter id="shadow-${id}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="${IMAGE_WIDTH}" height="${IMAGE_HEIGHT}" fill="url(#bg-${id})"/>
  
  <!-- Road/Scene indicator -->
  <rect x="0" y="160" width="${IMAGE_WIDTH}" height="65" fill="#1A202C" opacity="0.3"/>
  <line x1="0" y1="180" x2="${IMAGE_WIDTH}" y2="180" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="20,10" opacity="0.4"/>
  
  <!-- Object Icons -->
  ${objectIcons}
  
  <!-- Scene label background -->
  <rect x="10" y="10" width="${objectLabels.length * 9 + 20}" height="28" rx="4" fill="#1A202C" opacity="0.7"/>
  
  <!-- Object labels -->
  <text x="20" y="29" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" fill="white" letter-spacing="0.5">${objectLabels}</text>
  
  <!-- Bottom description hint -->
  <text x="${IMAGE_WIDTH - 10}" y="${IMAGE_HEIGHT - 10}" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="white" opacity="0.6" text-anchor="end">AutoDrive Scene</text>
</svg>`
}

// Convert SVG to PNG using canvas (Node.js compatible)
// For now, we'll save as SVG and provide a conversion option
function saveThumbnail(scenario) {
  const svg = generateSVG(scenario)
  const filepath = path.join(THUMBNAILS_DIR, `${scenario.id}.svg`)
  fs.writeFileSync(filepath, svg)
  return { id: scenario.id, filepath, size: svg.length }
}

// Generate HTML with embedded SVG thumbnails as a fallback
function generateHTMLThumbnails() {
  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Autodrive Thumbnails</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #1a202c; color: white; padding: 20px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 20px; }
    .thumbnail { background: #2d3748; border-radius: 8px; padding: 10px; }
    .thumbnail img { width: 400px; height: 225px; border-radius: 4px; display: block; }
    .thumbnail .info { margin-top: 8px; font-size: 12px; opacity: 0.8; }
    .thumbnail .objects { color: #63b3ed; font-weight: 600; }
  </style>
</head>
<body>
  <h1>Autodrive Dataset Thumbnails</h1>
  <div class="grid">
    ${objectScenarios.map(s => `
      <div class="thumbnail">
        <img src="${s.id}.svg" alt="${s.description}">
        <div class="info">
          <span class="objects">${s.objects.join(', ')}</span> - ${s.description.substring(0, 60)}...
        </div>
      </div>
    `).join('')}
  </div>
</body>
</html>`
  
  fs.writeFileSync(path.join(THUMBNAILS_DIR, 'index.html'), html)
}

// Main function
async function generateAllThumbnails() {
  console.log('🚀 Generating autodrive thumbnails...\n')
  
  // Ensure directory exists
  if (!fs.existsSync(THUMBNAILS_DIR)) {
    fs.mkdirSync(THUMBNAILS_DIR, { recursive: true })
    console.log(`✓ Created directory: ${THUMBNAILS_DIR}`)
  }
  
  const results = []
  
  for (let i = 0; i < objectScenarios.length; i++) {
    const scenario = objectScenarios[i]
    console.log(`🎨 [${i + 1}/${objectScenarios.length}] Generating ${scenario.id}...`)
    
    const result = saveThumbnail(scenario)
    results.push(result)
    console.log(`✅ Saved ${scenario.id}.svg (${result.size} bytes)`)
  }
  
  // Generate HTML preview
  generateHTMLThumbnails()
  console.log('\n📝 Generated index.html for preview')
  
  // Generate mapping file
  const mapping = {}
  for (const scenario of objectScenarios) {
    mapping[scenario.id] = {
      objects: scenario.objects,
      path: `/images/thumbnails/${scenario.id}.svg`,
      description: scenario.description
    }
  }
  
  const mappingPath = path.join(THUMBNAILS_DIR, 'mapping.json')
  fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2))
  console.log(`📝 Generated mapping.json`)
  
  console.log('\n📊 Summary:')
  console.log(`   Total: ${results.length} thumbnails generated`)
  console.log(`   Format: SVG (scalable vector graphics)`)
  console.log(`   Location: ${THUMBNAILS_DIR}`)
  console.log('\n✅ Done!')
  console.log('\n💡 Tip: Open public/images/thumbnails/index.html in browser to preview all thumbnails')
}

// Run
generateAllThumbnails().catch(err => {
  console.error('❌ Error:', err)
  process.exit(1)
})
