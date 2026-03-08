#!/usr/bin/env node
/**
 * Thumbnail Download Script
 * 
 * Downloads thumbnail images from free image sources (Lorem Picsum)
 * based on object keywords for the autodrive-derived-nuscenes-filtered dataset.
 * 
 * Usage: node scripts/download-thumbnails.js
 */

import fs from 'fs'
import path from 'path'
import https from 'https'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Configuration
const THUMBNAILS_DIR = path.join(__dirname, '..', 'public', 'images', 'thumbnails')
const IMAGE_WIDTH = 400
const IMAGE_HEIGHT = 225

// Object scenarios with search keywords for image matching
const objectScenarios = [
  { id: 'bus-barrier', objects: ['bus', 'barrier'], keyword: 'bus-city-street' },
  { id: 'motorcycle-truck', objects: ['motorcycle', 'truck'], keyword: 'motorcycle-highway' },
  { id: 'motorcycle-barrier-cone', objects: ['motorcycle', 'barrier', 'traffic-cone'], keyword: 'road-construction' },
  { id: 'motorcycle-pedestrian', objects: ['motorcycle', 'pedestrian'], keyword: 'city-traffic' },
  { id: 'pedestrian-cone-cyclist', objects: ['pedestrian', 'traffic-cone', 'cyclist'], keyword: 'cyclist-city' },
  { id: 'car-motorcycle', objects: ['car', 'motorcycle'], keyword: 'car-motorcycle-traffic' },
  { id: 'cone-bus-motorcycle', objects: ['traffic-cone', 'bus', 'motorcycle'], keyword: 'bus-traffic' },
  { id: 'car-truck-barrier', objects: ['car', 'truck', 'barrier'], keyword: 'highway-traffic' },
  { id: 'pedestrian-car', objects: ['pedestrian', 'car'], keyword: 'pedestrian-crossing' },
  { id: 'cyclist-car-cone', objects: ['cyclist', 'car', 'traffic-cone'], keyword: 'bike-lane-city' },
  { id: 'truck-barrier', objects: ['truck', 'barrier'], keyword: 'truck-road' },
  { id: 'bus-pedestrian-cyclist', objects: ['bus', 'pedestrian', 'cyclist'], keyword: 'bus-stop-city' },
  { id: 'motorcycle-cone', objects: ['motorcycle', 'traffic-cone'], keyword: 'motorcycle-road' },
  { id: 'car-pedestrian-barrier', objects: ['car', 'pedestrian', 'barrier'], keyword: 'city-street' },
  { id: 'truck-cyclist', objects: ['truck', 'cyclist'], keyword: 'cyclist-urban' },
  { id: 'bus-car', objects: ['bus', 'car'], keyword: 'bus-car-traffic' },
  { id: 'motorcycle-cyclist-pedestrian', objects: ['motorcycle', 'cyclist', 'pedestrian'], keyword: 'urban-traffic' },
  { id: 'cone-barrier-car', objects: ['traffic-cone', 'barrier', 'car'], keyword: 'road-construction' },
  { id: 'truck-motorcycle-cone', objects: ['truck', 'motorcycle', 'traffic-cone'], keyword: 'traffic-road' },
  { id: 'pedestrian-cyclist-barrier', objects: ['pedestrian', 'cyclist', 'barrier'], keyword: 'bike-path' }
]

// Using Lorem Picsum for reliable placeholder images
function getPicsumUrl(seed, width, height) {
  return `https://picsum.photos/seed/${seed}/${width}/${height}.jpg`
}

// Download image from URL and save to file
function downloadImage(url, filepath) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 30000 }, (response) => {
      // Handle redirects
      if (response.statusCode === 302 || response.statusCode === 301) {
        downloadImage(response.headers.location, filepath)
          .then(resolve)
          .catch(reject)
        return
      }
      
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode}`))
        return
      }
      
      const fileStream = fs.createWriteStream(filepath)
      response.pipe(fileStream)
      
      fileStream.on('finish', () => {
        fileStream.close()
        resolve(filepath)
      })
      
      fileStream.on('error', (err) => {
        fs.unlink(filepath, () => {})
        reject(err)
      })
      
      response.on('error', (err) => {
        fs.unlink(filepath, () => {})
        reject(err)
      })
    }).on('error', (err) => {
      fs.unlink(filepath, () => {})
      reject(err)
    })
  })
}

// Main function to download all thumbnails
async function downloadAllThumbnails() {
  console.log('🚀 Starting thumbnail download...\n')
  
  // Ensure directory exists
  if (!fs.existsSync(THUMBNAILS_DIR)) {
    fs.mkdirSync(THUMBNAILS_DIR, { recursive: true })
    console.log(`✓ Created directory: ${THUMBNAILS_DIR}`)
  }
  
  const results = []
  
  for (let i = 0; i < objectScenarios.length; i++) {
    const scenario = objectScenarios[i]
    const filename = `${scenario.id}.jpg`
    const filepath = path.join(THUMBNAILS_DIR, filename)
    
    // Check if file already exists and has content
    try {
      const stats = fs.statSync(filepath)
      if (stats.size > 100) {
        console.log(`⏭️  [${i + 1}/${objectScenarios.length}] Skipping ${filename} (already exists, ${stats.size} bytes)`)
        results.push({ id: scenario.id, status: 'skipped', size: stats.size })
        continue
      }
    } catch {
      // File doesn't exist, proceed with download
    }
    
    // Use Lorem Picsum for consistent, reliable images
    const url = getPicsumUrl(scenario.id, IMAGE_WIDTH, IMAGE_HEIGHT)
    
    console.log(`⬇️  [${i + 1}/${objectScenarios.length}] Downloading ${filename}...`)
    
    try {
      await downloadImage(url, filepath)
      const stats = fs.statSync(filepath)
      console.log(`✅ Saved ${filename} (${stats.size} bytes)`)
      results.push({ id: scenario.id, status: 'success', size: stats.size })
    } catch (err) {
      console.error(`❌ Failed to download ${filename}: ${err.message}`)
      results.push({ id: scenario.id, status: 'error', error: err.message })
    }
    
    // Add a small delay to be nice to the server
    if (i < objectScenarios.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 300))
    }
  }
  
  console.log('\n📊 Download Summary:')
  console.log(`   Total: ${results.length}`)
  console.log(`   Success: ${results.filter(r => r.status === 'success').length}`)
  console.log(`   Skipped: ${results.filter(r => r.status === 'skipped').length}`)
  console.log(`   Failed: ${results.filter(r => r.status === 'error').length}`)
  
  // Generate mapping file for the frontend
  await generateMappingFile(results.filter(r => r.status !== 'error'))
  
  console.log('\n✅ Done!')
}

// Generate a mapping file that the frontend can use
async function generateMappingFile(successfulResults) {
  const mapping = {}
  
  for (const result of successfulResults) {
    const scenario = objectScenarios.find(s => s.id === result.id)
    if (scenario) {
      mapping[scenario.id] = {
        objects: scenario.objects,
        path: `/images/thumbnails/${result.id}.jpg`
      }
    }
  }
  
  const mappingPath = path.join(THUMBNAILS_DIR, 'mapping.json')
  fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2))
  
  console.log(`\n📝 Generated mapping file: ${mappingPath}`)
}

// Run the download
downloadAllThumbnails().catch(err => {
  console.error('❌ Fatal error:', err)
  process.exit(1)
})
