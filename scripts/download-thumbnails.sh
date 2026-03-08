#!/bin/bash

# Thumbnail Download Script
# Downloads thumbnail images from Lorem Picsum based on object keywords
# for the autodrive-derived-nuscenes-filtered dataset

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THUMBNAILS_DIR="$SCRIPT_DIR/../public/images/thumbnails"
WIDTH=400
HEIGHT=225

# Create directory if it doesn't exist
mkdir -p "$THUMBNAILS_DIR"

echo "🚀 Starting thumbnail download..."
echo ""

# Array of scenarios: "id|objects"
scenarios=(
  "bus-barrier|bus,barrier"
  "motorcycle-truck|motorcycle,truck"
  "motorcycle-barrier-cone|motorcycle,barrier,traffic-cone"
  "motorcycle-pedestrian|motorcycle,pedestrian"
  "pedestrian-cone-cyclist|pedestrian,traffic-cone,cyclist"
  "car-motorcycle|car,motorcycle"
  "cone-bus-motorcycle|traffic-cone,bus,motorcycle"
  "car-truck-barrier|car,truck,barrier"
  "pedestrian-car|pedestrian,car"
  "cyclist-car-cone|cyclist,car,traffic-cone"
  "truck-barrier|truck,barrier"
  "bus-pedestrian-cyclist|bus,pedestrian,cyclist"
  "motorcycle-cone|motorcycle,traffic-cone"
  "car-pedestrian-barrier|car,pedestrian,barrier"
  "truck-cyclist|truck,cyclist"
  "bus-car|bus,car"
  "motorcycle-cyclist-pedestrian|motorcycle,cyclist,pedestrian"
  "cone-barrier-car|traffic-cone,barrier,car"
  "truck-motorcycle-cone|truck,motorcycle,traffic-cone"
  "pedestrian-cyclist-barrier|pedestrian,cyclist,barrier"
)

total=${#scenarios[@]}
success=0
skipped=0
failed=0

for i in "${!scenarios[@]}"; do
  IFS='|' read -r id objects <<< "${scenarios[$i]}"
  filename="$THUMBNAILS_DIR/$id.jpg"
  
  # Check if file already exists and has content
  if [[ -f "$filename" && -s "$filename" ]]; then
    filesize=$(stat -f%z "$filename" 2>/dev/null || stat -c%s "$filename" 2>/dev/null || echo "0")
    echo "⏭️  [$((i+1))/$total] Skipping $id.jpg (already exists, $filesize bytes)"
    skipped=$((skipped + 1))
    continue
  fi
  
  echo "⬇️  [$((i+1))/$total] Downloading $id.jpg..."
  
  # Download using curl with redirect following
  if curl -sL -o "$filename" "https://picsum.photos/seed/$id/$WIDTH/$HEIGHT.jpg"; then
    if [[ -f "$filename" && -s "$filename" ]]; then
      filesize=$(stat -f%z "$filename" 2>/dev/null || stat -c%s "$filename" 2>/dev/null || echo "0")
      echo "✅ Saved $id.jpg ($filesize bytes)"
      success=$((success + 1))
    else
      echo "❌ Failed to download $id.jpg (empty file)"
      rm -f "$filename"
      failed=$((failed + 1))
    fi
  else
    echo "❌ Failed to download $id.jpg (curl error)"
    rm -f "$filename"
    failed=$((failed + 1))
  fi
  
  # Add a small delay to be nice to the server
  if [[ $i -lt $(($total - 1)) ]]; then
    sleep 0.3
  fi
done

echo ""
echo "📊 Download Summary:"
echo "   Total: $total"
echo "   Success: $success"
echo "   Skipped: $skipped"
echo "   Failed: $failed"

# Generate mapping.json
echo ""
echo "📝 Generating mapping file..."

# Build JSON manually to avoid dependency on jq
{
  echo "{"
  first=true
  for scenario in "${scenarios[@]}"; do
    IFS='|' read -r id objects <<< "$scenario"
    filename="$THUMBNAILS_DIR/$id.jpg"
    
    if [[ -f "$filename" && -s "$filename" ]]; then
      # Format objects as JSON array
      objects_json="[$(echo "$objects" | sed 's/[^,]*/"&"/g')]"
      
      if [[ "$first" == "true" ]]; then
        first=false
      else
        echo ","
      fi
      echo "  \"$id\": {"
      echo "    \"objects\": $objects_json,"
      echo "    \"path\": \"/images/thumbnails/$id.jpg\""
      echo -n "  }"
    fi
  done
  echo ""
  echo "}"
} > "$THUMBNAILS_DIR/mapping.json"

echo "✅ Generated mapping.json"
echo ""
echo "✅ Done!"
