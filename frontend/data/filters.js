export const domainFilters = [
  { value: 'biology', label: 'Biology', count: 68 },
  { value: 'chemistry', label: 'Chemistry', count: 45 },
  { value: 'physics', label: 'Physics', count: 52 },
  { value: 'mathematics', label: 'Mathematics', count: 38 },
  { value: 'earth-science', label: 'Earth Science', count: 87 },
  { value: 'medicine', label: 'Medicine', count: 73 },
  { value: 'materials-science', label: 'Materials Science', count: 41 },
  { value: 'ecology', label: 'Ecology', count: 29 },
  { value: 'astronomy', label: 'Astronomy', count: 22 },
  { value: 'neuroscience', label: 'Neuroscience', count: 31 },
  { value: 'education', label: 'Education', count: 56 },
  { value: 'energy', label: 'Energy', count: 24 },
  { value: 'engineering', label: 'Engineering', count: 47 },
  { value: 'autonomous-driving', label: 'Autonomous Driving', count: 12 },
]

export const taskFilters = [
  { value: 'text-generation', label: 'Text Generation', count: 82 },
  { value: 'text-to-image', label: 'Text to Image', count: 45 },
  { value: 'feature-extraction', label: 'Feature Extraction', count: 67 },
  { value: 'fill-mask', label: 'Fill Mask', count: 38 },
  { value: 'text-classification', label: 'Text Classification', count: 54 },
  { value: 'summarization', label: 'Summarization', count: 29 },
  { value: 'translation', label: 'Translation', count: 33 },
  { value: 'question-answering', label: 'Question Answering', count: 41 },
  { value: 'automatic-speech-recognition', label: 'Speech Recognition', count: 26 },
  { value: 'image-classification', label: 'Image Classification', count: 48 },
  { value: 'image-to-text', label: 'Image to Text', count: 35 },
  { value: 'text-to-speech', label: 'Text to Speech', count: 22 },
  { value: 'text-to-audio', label: 'Text to Audio', count: 20 },
  { value: 'object-detection', label: 'Object Detection', count: 31 },
  { value: 'image-segmentation', label: 'Image Segmentation', count: 27 },
  { value: 'audio-classification', label: 'Audio Classification', count: 23 },
  { value: 'video-generation', label: 'Video Generation', count: 21 },
]

export const libraryFilters = [
  { value: 'transformers', label: 'Transformers', count: 95 },
  { value: 'pytorch', label: 'PyTorch', count: 78 },
  { value: 'diffusers', label: 'Diffusers', count: 42 },
  { value: 'tensorflow', label: 'TensorFlow', count: 36 },
  { value: 'jax', label: 'JAX', count: 28 },
  { value: 'onnx', label: 'ONNX', count: 25 },
  { value: 'safetensors', label: 'Safetensors', count: 63 },
  { value: 'sentence-transformers', label: 'Sentence Transformers', count: 31 },
]

export const languageFilters = [
  { value: 'en', label: 'English', count: 92 },
  { value: 'zh', label: 'Chinese', count: 54 },
  { value: 'multilingual', label: 'Multilingual', count: 47 },
  { value: 'fr', label: 'French', count: 33 },
  { value: 'de', label: 'German', count: 29 },
  { value: 'es', label: 'Spanish', count: 27 },
  { value: 'ja', label: 'Japanese', count: 38 },
  { value: 'ko', label: 'Korean', count: 24 },
]

export const licenseFilters = [
  { value: 'apache-2.0', label: 'Apache 2.0', count: 68 },
  { value: 'mit', label: 'MIT', count: 55 },
  { value: 'cc-by-4.0', label: 'CC BY 4.0', count: 43 },
  { value: 'cc-by-nc-4.0', label: 'CC BY-NC 4.0', count: 31 },
  { value: 'openrail', label: 'OpenRAIL', count: 26 },
  { value: 'llama3', label: 'Llama 3', count: 22 },
  { value: 'other', label: 'Other', count: 37 },
]

export const modalityFilters = [
  { value: 'text', label: 'Text', count: 85 },
  { value: 'image', label: 'Image', count: 62 },
  { value: 'audio', label: 'Audio', count: 34 },
  { value: 'video', label: 'Video', count: 21 },
]

export const spaceCategories = [
  { value: 'all', label: 'All' },
  { value: 'image-generation', label: 'Image Generation' },
  { value: 'video-generation', label: 'Video Generation' },
  { value: 'text-generation', label: 'Text Generation' },
  { value: 'audio', label: 'Audio' },
]

export const sortOptions = [
  { value: 'default', label: 'Default' },
  { value: 'trending', label: 'Trending' },
  { value: 'downloads', label: 'Most Downloads' },
  { value: 'likes', label: 'Most Likes' },
  { value: 'recent', label: 'Recently Updated' },
]

export const taskColorMap = {
  'text-generation': 'blue',
  'text-to-image': 'purple',
  'feature-extraction': 'teal',
  'fill-mask': 'green',
  'text-classification': 'orange',
  'summarization': 'indigo',
  'translation': 'pink',
  'question-answering': 'yellow',
  'automatic-speech-recognition': 'red',
  'image-classification': 'green',
  'image-to-text': 'purple',
  'text-to-speech': 'orange',
  'text-to-audio': 'pink',
  'object-detection': 'blue',
  'image-segmentation': 'teal',
  'audio-classification': 'red',
  'video-generation': 'indigo',
}

export const domainColorMap = {
  'biology': 'green',
  'chemistry': 'orange',
  'physics': 'blue',
  'mathematics': 'indigo',
  'earth-science': 'teal',
  'medicine': 'red',
  'materials-science': 'purple',
  'ecology': 'green',
  'astronomy': 'blue',
  'neuroscience': 'pink',
  'education': 'yellow',
  'energy': 'orange',
  'engineering': 'teal',
  'autonomous-driving': 'cyan',
}

// Dataset type filters
export const datasetTypeFilters = [
  { value: 'original', label: 'Original', count: 85 },
  { value: 'derived', label: 'Derived (Read-only)', count: 42 },
]

// Autodriving specific filters
export const timeRangeFilters = [
  { value: 'day', label: 'Daytime', count: 5200000 },
  { value: 'night', label: 'Nighttime', count: 1800000 },
  { value: 'dawn-dusk', label: 'Dawn/Dusk', count: 950000 },
  { value: 'all', label: 'All Conditions', count: 7950000 },
]

export const weatherFilters = [
  { value: 'clear', label: 'Clear', count: 4200000 },
  { value: 'rainy', label: 'Rainy', count: 1200000 },
  { value: 'snowy', label: 'Snowy', count: 580000 },
  { value: 'foggy', label: 'Foggy', count: 420000 },
  { value: 'overcast', label: 'Overcast', count: 1550000 },
]

export const sceneTypeFilters = [
  { value: 'highway', label: 'Highway', count: 2800000 },
  { value: 'urban', label: 'Urban', count: 3200000 },
  { value: 'suburban', label: 'Suburban', count: 1200000 },
  { value: 'rural', label: 'Rural', count: 750000 },
  { value: 'tunnel', label: 'Tunnel', count: 180000 },
  { value: 'parking', label: 'Parking', count: 420000 },
]

export const annotationTypeFilters = [
  { value: '3d-bbox', label: '3D Bounding Boxes', count: 5200000 },
  { value: '2d-bbox', label: '2D Bounding Boxes', count: 6800000 },
  { value: 'segmentation', label: 'Instance Segmentation', count: 3200000 },
  { value: 'trajectory', label: 'Trajectory', count: 1800000 },
  { value: 'lane', label: 'Lane Marking', count: 4200000 },
  { value: 'depth', label: 'Depth Map', count: 2100000 },
]

// Color maps for new filters
export const datasetTypeColorMap = {
  'original': 'green',
  'derived': 'blue',
}
