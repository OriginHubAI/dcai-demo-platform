# Autodrive Dataset Thumbnails

This directory contains thumbnail images for the `autodrive-derived-nuscenes-filtered` dataset Data Studio view.

## Overview

- **Total Images**: 20 thumbnails
- **Image Size**: 400x225 pixels (16:9 aspect ratio)
- **Format**: SVG (Scalable Vector Graphics)
- **Generation**: Programmatically generated with styled vector graphics

## Image Sources

Images are generated as SVG vector graphics using [`scripts/generate-autodrive-thumbnails.js`](../../../scripts/generate-autodrive-thumbnails.js). Each thumbnail features:

- Styled icons representing the object types (car, truck, bus, motorcycle, pedestrian, cyclist, traffic cone, barrier)
- Traffic scene backgrounds with road elements
- Color-coded objects matching the scenario type
- Object labels displayed on the thumbnail

## Object Scenarios

Each thumbnail corresponds to a specific combination of autonomous driving objects:

| Image | Objects | Description |
|-------|---------|-------------|
| `bus-barrier.svg` | bus, barrier | Bus stopped at intersection with construction barriers |
| `motorcycle-truck.svg` | motorcycle, truck | Motorcycle passing a large truck on highway |
| `motorcycle-barrier-cone.svg` | motorcycle, barrier, traffic-cone | Motorcycle navigating road work zone |
| `motorcycle-pedestrian.svg` | motorcycle, pedestrian | Motorcycle at crosswalk with pedestrians |
| `pedestrian-cone-cyclist.svg` | pedestrian, traffic-cone, cyclist | Cyclist and pedestrians near construction |
| `car-motorcycle.svg` | car, motorcycle | Car and motorcycle at traffic light |
| `cone-bus-motorcycle.svg` | traffic-cone, bus, motorcycle | Bus and motorcycle navigating traffic cones |
| `car-truck-barrier.svg` | car, truck, barrier | Car following truck on highway with barriers |
| `pedestrian-car.svg` | pedestrian, car | Pedestrians crossing, car waiting |
| `cyclist-car-cone.svg` | cyclist, car, traffic-cone | Cyclist in bike lane with road work cones |
| `truck-barrier.svg` | truck, barrier | Commercial truck in construction zone |
| `bus-pedestrian-cyclist.svg` | bus, pedestrian, cyclist | Bus stop with cyclists and pedestrians |
| `motorcycle-cone.svg` | motorcycle, traffic-cone | Motorcycle in temporary lane |
| `car-pedestrian-barrier.svg` | car, pedestrian, barrier | Car at pedestrian zone with barriers |
| `truck-cyclist.svg` | truck, cyclist | Cyclist sharing road with truck |
| `bus-car.svg` | bus, car | Bus in dedicated lane with cars |
| `motorcycle-cyclist-pedestrian.svg` | motorcycle, cyclist, pedestrian | Mixed urban traffic scene |
| `cone-barrier-car.svg` | traffic-cone, barrier, car | Cars in construction zone |
| `truck-motorcycle-cone.svg` | truck, motorcycle, traffic-cone | Truck and motorcycle in lane restriction |
| `pedestrian-cyclist-barrier.svg` | pedestrian, cyclist, barrier | Protected bike/pedestrian path |

## Regenerating Images

To regenerate the thumbnails, run the generation script from the project root:

```bash
node scripts/generate-autodrive-thumbnails.js
```

This will:
1. Generate fresh SVG thumbnails for all scenarios
2. Create an `index.html` preview file
3. Generate an updated `mapping.json` file

## Preview

Open `public/images/thumbnails/index.html` in a browser to see all thumbnails in a grid layout.

## Integration

The thumbnails are automatically used by:
- [`frontend/data/datasets.js`](../../../frontend/data/datasets.js) - Data generation logic
- [`frontend/components/datasets/DataStudio.vue`](../../../frontend/components/datasets/DataStudio.vue) - UI component

## Mapping File

The `mapping.json` file maps object combinations to their corresponding thumbnail paths for frontend consumption.
