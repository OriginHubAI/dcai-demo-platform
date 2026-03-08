#!/usr/bin/env node
/**
 * Autodrive Thumbnail Download Script
 * 
 * Downloads appropriate autonomous driving scene images from Unsplash
 * based on object keywords for the autodrive-derived-nuscenes-filtered dataset.
 * 
 * Usage: node scripts/download-autodrive-thumbnails.js
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

// Object scenarios with Unsplash search keywords
// Using specific traffic/autonomous driving related keywords
const objectScenarios = [
  { 
    id: 'bus-barrier', 
    objects: ['bus', 'barrier'], 
    keywords: ['bus', 'city', 'traffic', 'road'],
    description: 'Bus stopped at intersection with construction barriers'
  },
  { 
    id: 'motorcycle-truck', 
    objects: ['motorcycle', 'truck'], 
    keywords: ['motorcycle', 'truck', 'highway', 'road'],
    description: 'Motorcycle passing a large truck on highway'
  },
  { 
    id: 'motorcycle-barrier-cone', 
    objects: ['motorcycle', 'barrier', 'traffic-cone'], 
    keywords: ['road', 'construction', 'traffic', 'cone'],
    description: 'Motorcycle navigating road work zone'
  },
  { 
    id: 'motorcycle-pedestrian', 
    objects: ['motorcycle', 'pedestrian'], 
    keywords: ['motorcycle', 'city', 'street', 'urban'],
    description: 'Motorcycle at crosswalk with pedestrians'
  },
  { 
    id: 'pedestrian-cone-cyclist', 
    objects: ['pedestrian', 'traffic-cone', 'cyclist'], 
    keywords: ['cyclist', 'city', 'street', 'urban'],
    description: 'Cyclist and pedestrians near construction'
  },
  { 
    id: 'car-motorcycle', 
    objects: ['car', 'motorcycle'], 
    keywords: ['car', 'motorcycle', 'traffic', 'road'],
    description: 'Car and motorcycle at traffic light'
  },
  { 
    id: 'cone-bus-motorcycle', 
    objects: ['traffic-cone', 'bus', 'motorcycle'], 
    keywords: ['bus', 'traffic', 'city', 'road'],
    description: 'Bus and motorcycle navigating traffic cones'
  },
  { 
    id: 'car-truck-barrier', 
    objects: ['car', 'truck', 'barrier'], 
    keywords: ['truck', 'highway', 'traffic', 'road'],
    description: 'Car following truck on highway with barriers'
  },
  { 
    id: 'pedestrian-car', 
    objects: ['pedestrian', 'car'], 
    keywords: ['pedestrian', 'crosswalk', 'city', 'street'],
    description: 'Pedestrians crossing, car waiting'
  },
  { 
    id: 'cyclist-car-cone', 
    objects: ['cyclist', 'car', 'traffic-cone'], 
    keywords: ['bike', 'lane', 'city', 'street'],
    description: 'Cyclist in bike lane with road work cones'
  },
  { 
    id: 'truck-barrier', 
    objects: ['truck', 'barrier'], 
    keywords: ['truck', 'highway', 'road', 'transport'],
    description: 'Commercial truck in construction zone'
  },
  { 
    id: 'bus-pedestrian-cyclist', 
    objects: ['bus', 'pedestrian', 'cyclist'], 
    keywords: ['bus', 'stop', 'city', 'transit'],
    description: 'Bus stop with cyclists and pedestrians'
  },
  { 
    id: 'motorcycle-cone', 
    objects: ['motorcycle', 'traffic-cone'], 
    keywords: ['motorcycle', 'road', 'street', 'traffic'],
    description: 'Motorcycle in temporary lane'
  },
  { 
    id: 'car-pedestrian-barrier', 
    objects: ['car', 'pedestrian', 'barrier'], 
    keywords: ['car', 'street', 'city', 'road'],
    description: 'Car at pedestrian zone with barriers'
  },
  { 
    id: 'truck-cyclist', 
    objects: ['truck', 'cyclist'], 
    keywords: ['cyclist', 'urban', 'street', 'city'],
    description: 'Cyclist sharing road with truck'
  },
  { 
    id: 'bus-car', 
    objects: ['bus', 'car'], 
    keywords: ['bus', 'car', 'traffic', 'city'],
    description: 'Bus in dedicated lane with cars'
  },
  { 
    id: 'motorcycle-cyclist-pedestrian', 
    objects: ['motorcycle', 'cyclist', 'pedestrian'], 
    keywords: ['traffic', 'street', 'urban', 'city'],
    description: 'Mixed urban traffic scene'
  },
  { 
    id: 'cone-barrier-car', 
    objects: ['traffic-cone', 'barrier', 'car'], 
    keywords: ['road', 'construction', 'traffic', 'highway'],
    description: 'Cars in construction zone'
  },
  { 
    id: 'truck-motorcycle-cone', 
    objects: ['truck', 'motorcycle', 'traffic-cone'], 
    keywords: ['truck', 'motorcycle', 'road', 'traffic'],
    description: 'Truck and motorcycle in lane restriction'
  },
  { 
    id: 'pedestrian-cyclist-barrier', 
    objects: ['pedestrian', 'cyclist', 'barrier'], 
    keywords: ['bike', 'path', 'pedestrian', 'walkway'],
    description: 'Protected bike/pedestrian path'
  }
]

// Unsplash Source API - returns random images matching keywords
// Format: https://source.unsplash.com/{WIDTH}x{HEIGHT}/?{KEYWORDS}
// Note: Unsplash Source is deprecated, usingpicsum with better seeds or direct URLs
// Using a curated list of actual traffic scene images from various sources

// Direct URLs to appropriate traffic/autonomous driving images
// These are from free stock photo sites and Wikimedia Commons
const trafficImageUrls = {
  'bus-barrier': 'https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=400&h=225&fit=crop',
  'motorcycle-truck': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=225&fit=crop',
  'motorcycle-barrier-cone': 'https://images.unsplash.com/photo-1565043589221-1a6fd9ae45c7?w=400&h=225&fit=crop',
  'motorcycle-pedestrian': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=225&fit=crop',
  'pedestrian-cone-cyclist': 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=400&h=225&fit=crop',
  'car-motorcycle': 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=400&h=225&fit=crop',
  'cone-bus-motorcycle': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400&h=225&fit=crop',
  'car-truck-barrier': 'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=400&h=225&fit=crop',
  'pedestrian-car': 'https://images.unsplash.com/photo-1444723121867-c612c5c6cb9c?w=400&h=225&fit=crop',
  'cyclist-car-cone': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=400&h=225&fit=crop',
  'truck-barrier': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400&h=225&fit=crop',
  'bus-pedestrian-cyclist': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400&h=225&fit=crop',
  'motorcycle-cone': 'https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=400&h=225&fit=crop',
  'car-pedestrian-barrier': 'https://images.unsplash.com/photo-1486006920555-c77dcf18193c?w=400&h=225&fit=crop',
  'truck-cyclist': 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=400&h=225&fit=crop',
  'bus-car': 'https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=400&h=225&fit=crop',
  'motorcycle-cyclist-pedestrian': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=225&fit=crop',
  'cone-barrier-car': 'https://images.unsplash.com/photo-1565043589221-1a6fd9ae45c7?w=400&h=225&fit=crop',
  'truck-motorcycle-cone': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=225&fit=crop',
  'pedestrian-cyclist-barrier': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=400&h=225&fit=crop'
}

// Download image from URL and save to file
function downloadImage(url, filepath) {
  return new Promise((resolve, reject) => {
    const request = https.get(url, { 
      timeout: 30000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    }, (response) => {
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
    
    request.on('timeout', () => {
      request.destroy()
      fs.unlink(filepath, () => {})
      reject(new Error('Request timeout'))
    })
  })
}

// Main function to download all thumbnails
async function downloadAllThumbnails() {
  console.log('🚀 Starting autodrive thumbnail download...\n')
  
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
    
    // Get URL for this scenario
    const url = trafficImageUrls[scenario.id]
    
    if (!url) {
      console.log(`⚠️  [${i + 1}/${objectScenarios.length}] No URL for ${filename}, skipping`)
      results.push({ id: scenario.id, status: 'skipped', error: 'No URL' })
      continue
    }
    
    console.log(`⬇️  [${i + 1}/${objectScenarios.length}] Downloading ${filename}...`)
    console.log(`   URL: ${url}`)
    
    try {
      await downloadImage(url, filepath)
      const stats = fs.statSync(filepath)
      console.log(`✅ Saved ${filename} (${stats.size} bytes)`)
      results.push({ id: scenario.id, status: 'success', size: stats.size })
    } catch (err) {
      console.error(`❌ Failed to download ${filename}: ${err.message}`)
      results.push({ id: scenario.id, status: 'error', error: err.message })
    }
    
    // Add a delay to be nice to the server
    if (i < objectScenarios.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 500))
    }
  }
  
  console.log('\n📊 Download Summary:')
  console.log(`   Total: ${results.length}`)
  console.log(`   Success: ${results.filter(r => r.status === 'success').length}`)
  console.log(`   Skipped: ${results.filter(r => r.status === 'skipped').length}`)
  console.log(`   Failed: ${results.filter(r => r.status === 'error').length}`)
  
  // Generate mapping file for the frontend
  await generateMappingFile(results.filter(r => r.status === 'success'))
  
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
        path: `/images/thumbnails/${result.id}.jpg`,
        description: scenario.description
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
