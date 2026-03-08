# Autodrive Dataset Thumbnails

This directory contains thumbnail images for the `autodrive-derived-nuscenes-filtered` dataset Data Studio view.

## Overview

- **Total Images**: 20 thumbnails
- **Image Size**: 400x225 pixels (16:9 aspect ratio)
- **Format**: JPG
- **Total Size**: ~332KB

## Image Sources

Images are downloaded from [Lorem Picsum](https://picsum.photos/), a free placeholder image service. Each image is seeded with a unique identifier based on the object combination it represents.

## Object Scenarios

Each thumbnail corresponds to a specific combination of autonomous driving objects:

| Image | Objects | Description |
|-------|---------|-------------|
| `bus-barrier.jpg` | bus, barrier | Bus stopped at intersection with construction barriers |
| `motorcycle-truck.jpg` | motorcycle, truck | Motorcycle passing a large truck on highway |
| `motorcycle-barrier-cone.jpg` | motorcycle, barrier, traffic-cone | Motorcycle navigating road work zone |
| `motorcycle-pedestrian.jpg` | motorcycle, pedestrian | Motorcycle at crosswalk with pedestrians |
| `pedestrian-cone-cyclist.jpg` | pedestrian, traffic-cone, cyclist | Cyclist and pedestrians near construction cones |
| `car-motorcycle.jpg` | car, motorcycle | Car and motorcycle at traffic light |
| `cone-bus-motorcycle.jpg` | traffic-cone, bus, motorcycle | Bus and motorcycle navigating traffic cones |
| `car-truck-barrier.jpg` | car, truck, barrier | Car following truck on highway with barriers |
| `pedestrian-car.jpg` | pedestrian, car | Pedestrians crossing, car waiting |
| `cyclist-car-cone.jpg` | cyclist, car, traffic-cone | Cyclist in bike lane with road work cones |
| `truck-barrier.jpg` | truck, barrier | Commercial truck in construction zone |
| `bus-pedestrian-cyclist.jpg` | bus, pedestrian, cyclist | Bus stop with cyclists and pedestrians |
| `motorcycle-cone.jpg` | motorcycle, traffic-cone | Motorcycle in temporary lane |
| `car-pedestrian-barrier.jpg` | car, pedestrian, barrier | Car at pedestrian zone with barriers |
| `truck-cyclist.jpg` | truck, cyclist | Cyclist sharing road with truck |
| `bus-car.jpg` | bus, car | Bus in dedicated lane with cars |
| `motorcycle-cyclist-pedestrian.jpg` | motorcycle, cyclist, pedestrian | Mixed urban traffic |
| `cone-barrier-car.jpg` | traffic-cone, barrier, car | Cars in construction zone |
| `truck-motorcycle-cone.jpg` | truck, motorcycle, traffic-cone | Truck and motorcycle in lane restriction |
| `pedestrian-cyclist-barrier.jpg` | pedestrian, cyclist, barrier | Protected bike/pedestrian path |

## Regenerating Images

To regenerate the thumbnails, run the download script from the project root:

```bash
./scripts/download-thumbnails.sh
```

This will:
1. Download fresh images from Lorem Picsum
2. Skip existing images (delete them first to force re-download)
3. Generate an updated `mapping.json` file

## Integration

The thumbnails are automatically used by:
- [`frontend/data/datasets.js`](../../../frontend/data/datasets.js) - Data generation logic
- [`frontend/components/datasets/DataStudio.vue`](../../../frontend/components/datasets/DataStudio.vue) - UI component

## Mapping File

The `mapping.json` file maps object combinations to their corresponding thumbnail paths for frontend consumption.
