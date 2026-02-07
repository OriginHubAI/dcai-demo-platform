export const taskFilters = [
  { value: 'text-generation', label: 'Text Generation', count: 45000 },
  { value: 'text-to-image', label: 'Text to Image', count: 18000 },
  { value: 'feature-extraction', label: 'Feature Extraction', count: 12000 },
  { value: 'fill-mask', label: 'Fill Mask', count: 9500 },
  { value: 'text-classification', label: 'Text Classification', count: 8200 },
  { value: 'summarization', label: 'Summarization', count: 5400 },
  { value: 'translation', label: 'Translation', count: 4800 },
  { value: 'question-answering', label: 'Question Answering', count: 4200 },
  { value: 'automatic-speech-recognition', label: 'Speech Recognition', count: 3600 },
  { value: 'image-classification', label: 'Image Classification', count: 3100 },
  { value: 'image-to-text', label: 'Image to Text', count: 2800 },
  { value: 'text-to-speech', label: 'Text to Speech', count: 2200 },
  { value: 'text-to-audio', label: 'Text to Audio', count: 1500 },
  { value: 'object-detection', label: 'Object Detection', count: 1800 },
  { value: 'image-segmentation', label: 'Image Segmentation', count: 1200 },
  { value: 'audio-classification', label: 'Audio Classification', count: 900 },
  { value: 'video-generation', label: 'Video Generation', count: 600 },
]

export const libraryFilters = [
  { value: 'transformers', label: 'Transformers', count: 120000 },
  { value: 'pytorch', label: 'PyTorch', count: 95000 },
  { value: 'diffusers', label: 'Diffusers', count: 18000 },
  { value: 'tensorflow', label: 'TensorFlow', count: 15000 },
  { value: 'jax', label: 'JAX', count: 5200 },
  { value: 'onnx', label: 'ONNX', count: 4800 },
  { value: 'safetensors', label: 'Safetensors', count: 42000 },
  { value: 'sentence-transformers', label: 'Sentence Transformers', count: 3200 },
]

export const languageFilters = [
  { value: 'en', label: 'English', count: 85000 },
  { value: 'zh', label: 'Chinese', count: 12000 },
  { value: 'multilingual', label: 'Multilingual', count: 8500 },
  { value: 'fr', label: 'French', count: 4200 },
  { value: 'de', label: 'German', count: 3800 },
  { value: 'es', label: 'Spanish', count: 3500 },
  { value: 'ja', label: 'Japanese', count: 3100 },
  { value: 'ko', label: 'Korean', count: 2200 },
]

export const licenseFilters = [
  { value: 'apache-2.0', label: 'Apache 2.0', count: 35000 },
  { value: 'mit', label: 'MIT', count: 28000 },
  { value: 'cc-by-4.0', label: 'CC BY 4.0', count: 8500 },
  { value: 'cc-by-nc-4.0', label: 'CC BY-NC 4.0', count: 4200 },
  { value: 'openrail', label: 'OpenRAIL', count: 3800 },
  { value: 'llama3', label: 'Llama 3', count: 2100 },
  { value: 'other', label: 'Other', count: 15000 },
]

export const modalityFilters = [
  { value: 'text', label: 'Text', count: 45000 },
  { value: 'image', label: 'Image', count: 12000 },
  { value: 'audio', label: 'Audio', count: 5500 },
  { value: 'video', label: 'Video', count: 1200 },
]

export const spaceCategories = [
  { value: 'all', label: 'All' },
  { value: 'image-generation', label: 'Image Generation' },
  { value: 'video-generation', label: 'Video Generation' },
  { value: 'text-generation', label: 'Text Generation' },
  { value: 'audio', label: 'Audio' },
]

export const sortOptions = [
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
