// Data Processing Task Pipeline Data

const pipelineData = {
  'task-001': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'ReasoningPipeline-pi...',
        description: 'This is a Dataset node',
        info: {
          Pipeline: 'ReasoningPipeline',
          'Data Samples': 10,
          ID: 'b6c87ccd65',
          Root: '/data/mzm/test_release/DataFlow-WebUI-v0.0.2/backend/data/dataflow_core/ex...',
          Hash: 'aa5ce875af51c46fcd774ce849518dd0'
        },
        fields: ['instruction', 'output', 'golden_answer', 'source'],
        initParams: {},
        runParams: {},
        logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'ReasoningQuestionFilter',
        initParams: {
          prompt_template: 'GeneralQuestionFilterPromp...',
          system_prompt: 'You are an expert in evaluating proble...',
          llm_serving: '11'
        },
        runParams: {
          input_key: 'instruction'
        },
        logs: [
          '[2026-02-02T15:15:16.511061] [1/5] Initializing operator: ReasoningQuestionFilter',
          '[2026-02-02T15:15:16.511117] - Initializing LLM serving: c4f66200d5e85944',
          '[2026-02-02T15:15:16.511121] - Loading prompt template: GeneralQuestionFilterPrompt',
          '[2026-02-02T15:15:16.511555] [1/5] ReasoningQuestionFilter initialized successfully',
          '[2026-02-02T15:15:16.511555] [1/5] Running operator: ReasoningQuestionFilter',
          '[2026-02-02T15:15:24.846240] Processed 8 samples',
          '[2026-02-02T15:15:33.332859] [1/5] ReasoningQuestionFilter completed successfully'
        ]
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'ReasoningQuestionGe...',
        initParams: {
          prompt_template: 'GeneralQuestionSynthesisPi...',
          num_prompts: 1,
          llm_serving: '11'
        },
        runParams: {
          input_key: 'instruction',
          output_synth_or_input_flag: 'Synth_or_Input'
        },
        logs: [
          '[2026-02-02T15:15:15.510498] [2/5] Initializing operator: ReasoningQuestionGenerator',
          '[2026-02-02T15:15:15.510562] - Initializing LLM serving: c4f66200d5e85944',
          '[2026-02-02T15:15:15.510867] - Loading prompt template: GeneralQuestionSynthesisPrompt',
          '[2026-02-02T15:15:15.511015] [2/5] ReasoningQuestionGenerator initialized successfully',
          '[2026-02-02T15:15:21.607027] [2/5] Running operator: ReasoningQuestionGenerator',
          'Processed 16 samples',
          '[2026-02-02T15:15:24.845007] [2/5] ReasoningQuestionGenerator completed successfully'
        ]
      },
      {
        id: 'node-4',
        type: 'generate',
        name: 'ReasoningAnswerGen...',
        initParams: {
          prompt_template: 'GeneralAnswerGeneratorPro...',
          llm_serving: '11'
        },
        runParams: {
          input_key: 'instruction',
          output_key: 'generated_cot'
        },
        logs: [
          '[2026-02-02T15:15:16.511061] [3/5] Initializing operator: ReasoningAnswerGenerator',
          '[2026-02-02T15:15:16.511117] - Initializing LLM serving: c4f66200d5e85944',
          '[2026-02-02T15:15:16.511121] - Loading prompt template: GeneralAnswerGeneratorPrompt',
          '[2026-02-02T15:15:16.511555] [3/5] ReasoningAnswerGenerator initialized successfully',
          '[2026-02-02T15:15:24.846240] [3/5] Running operator: ReasoningAnswerGenerator',
          'Processed 16 samples',
          '[2026-02-02T15:15:33.332859] [3/5] ReasoningAnswerGenerator completed successfully'
        ]
      },
      {
        id: 'node-5',
        type: 'filter',
        name: 'ReasoningAnswerMod...',
        initParams: {
          prompt_template: 'AnswerJudgePrompt',
          system_prompt: 'You are a helpful assistant specialized...',
          llm_serving: '11',
          keep_all_samples: true
        },
        runParams: {
          input_question_key: 'instruction',
          input_answer_key: 'generated_cot',
          input_reference_key: 'golden_answer'
        },
        logs: [
          '[2026-02-02T15:15:16.511591] [4/5] Initializing operator: ReasoningAnswerModJudgeFilter',
          '[2026-02-02T15:15:16.511650] - Initializing LLM serving: c4f66200d5e85944',
          '[2026-02-02T15:15:16.511655] - Loading prompt template: AnswerJudgePrompt',
          '[2026-02-02T15:15:16.512092] [4/5] ReasoningAnswerModJudgeFilter initialized successfully',
          '[2026-02-02T15:15:33.334090] [4/5] Running operator: ReasoningAnswerModJudgeFilter',
          'Processed 16 samples',
          '[2026-02-02T15:15:33.546448] [4/5] ReasoningAnswerModJudgeFilter completed successfully'
        ]
      }
    ]
  },
  'task-002': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'RNA-Sequence-Dataset',
        description: 'RNA sequence classification dataset',
        info: {
          Pipeline: 'RNAPipeline',
          'Data Samples': 5000,
          ID: 'rna-seq-001',
          Root: '/data/rna/sequences',
          Hash: 'abc123def456'
        },
        fields: ['sequence', 'label', 'length', 'gc_content'],
        initParams: {},
        runParams: {},
        logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'SequenceQualityFilter',
        initParams: {
          prompt_template: 'QualityFilterPrompt',
          system_prompt: 'Filter low quality sequences...',
          llm_serving: '8'
        },
        runParams: {
          input_key: 'sequence',
          min_length: 50
        },
        logs: [
          '[2026-02-02T10:15:16.511061] Initializing operator: SequenceQualityFilter',
          '[2026-02-02T10:15:16.511117] - Initializing LLM serving: c4f66200d5e85944',
          'Processed 4500 samples',
          'SequenceQualityFilter completed successfully'
        ]
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'SequenceFeatureGenerator',
        initParams: {
          prompt_template: 'FeatureGenPrompt',
          num_prompts: 3,
          llm_serving: '8'
        },
        runParams: {
          input_key: 'sequence',
          output_key: 'features'
        },
        logs: [
          '[2026-02-02T10:20:16.511061] Initializing operator: SequenceFeatureGenerator',
          'Generating sequence features...',
          'Processed 4500 samples',
          'SequenceFeatureGenerator completed successfully'
        ]
      }
    ]
  },
  'task-003': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'QC-DFT-Calculations',
        description: 'Quantum chemistry DFT calculation data',
        info: {
          Pipeline: 'QChemPipeline',
          'Data Samples': 250,
          ID: 'qc-dft-001',
          Root: '/data/qchem/dft',
          Hash: 'xyz789abc012'
        },
        fields: ['molecule', 'energy', 'forces', 'stress'],
        initParams: {},
        runParams: {},
        logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'ConvergenceFilter',
        initParams: {
          prompt_template: 'ConvergenceCheck',
          system_prompt: 'Check DFT convergence...',
          llm_serving: '12'
        },
        runParams: {
          input_key: 'energy',
          tolerance: 1e-5
        },
        logs: [
          '[2026-02-02T07:35:16.511061] Initializing operator: ConvergenceFilter',
          'Checking convergence criteria...',
          'Processed 230 samples',
          'ConvergenceFilter completed successfully'
        ]
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'EnergyNormalizer',
        initParams: {
          prompt_template: 'NormalizePrompt',
          num_prompts: 1,
          llm_serving: '12'
        },
        runParams: {
          input_key: 'energy',
          output_key: 'normalized_energy'
        },
        logs: [
          '[2026-02-02T07:40:16.511061] Initializing operator: EnergyNormalizer',
          'Normalizing energies...',
          'Processed 230 samples',
          'EnergyNormalizer completed successfully'
        ]
      }
    ]
  },
  'task-004': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Seismic-Waveform-Data',
        description: 'Seismic waveform event detection dataset',
        info: { Pipeline: 'SeismicPipeline', 'Data Samples': 12000, ID: 'seismic-001', Root: '/data/seismic/waveforms', Hash: 'seis789abc' },
        fields: ['waveform', 'timestamp', 'magnitude', 'station_id'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'NoiseReductionFilter',
        initParams: { prompt_template: 'NoiseFilter', system_prompt: 'Filter seismic noise...', llm_serving: '10' },
        runParams: { input_key: 'waveform', snr_threshold: 10 },
        logs: ['[2026-02-08T11:20:00] Initializing NoiseReductionFilter', 'Processed 9800 samples', 'NoiseReductionFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'EventDetector',
        initParams: { prompt_template: 'EventDetect', num_prompts: 2, llm_serving: '10' },
        runParams: { input_key: 'waveform', output_key: 'event_detected' },
        logs: ['[2026-02-08T11:25:00] Initializing EventDetector', 'Detected 342 seismic events', 'EventDetector completed']
      }
    ]
  },
  'task-005': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Astrophysics-Spectra',
        description: 'Astrophysics spectra redshift data',
        info: { Pipeline: 'AstroPipeline', 'Data Samples': 8500, ID: 'astro-001', Root: '/data/astro/spectra', Hash: 'astro456def' },
        fields: ['wavelength', 'flux', 'redshift', 'object_id'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'SpectralQualityFilter',
        initParams: { prompt_template: 'QualityCheck', system_prompt: 'Check spectral quality...', llm_serving: '9' },
        runParams: { input_key: 'flux', min_quality: 0.8 },
        logs: ['[2026-02-08T06:00:00] Initializing SpectralQualityFilter', 'Processed 7200 samples', 'Quality filter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'RedshiftLabeler',
        initParams: { prompt_template: 'RedshiftPrompt', num_prompts: 1, llm_serving: '9' },
        runParams: { input_key: 'wavelength', output_key: 'redshift_label' },
        logs: ['[2026-02-08T06:15:00] Initializing RedshiftLabeler', 'Labeled 7200 spectra', 'RedshiftLabeler completed']
      }
    ]
  },
  'task-006': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Drug-Molecule-Graphs',
        description: 'Drug molecule ADMET dataset',
        info: { Pipeline: 'DrugPipeline', 'Data Samples': 15000, ID: 'drug-001', Root: '/data/drug/molecules', Hash: 'drug123xyz' },
        fields: ['smiles', 'molecular_weight', 'logp', 'admet_props'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'DrugLikenessFilter',
        initParams: { prompt_template: 'LipinskiFilter', system_prompt: 'Apply Lipinski rules...', llm_serving: '11' },
        runParams: { input_key: 'smiles', rule: 'lipinski' },
        logs: ['[2026-02-07T09:10:00] Initializing DrugLikenessFilter', 'Filtered 13200 molecules', 'DrugLikenessFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'ADMETPredictor',
        initParams: { prompt_template: 'ADMETPrompt', num_prompts: 4, llm_serving: '11' },
        runParams: { input_key: 'smiles', output_key: 'admet_prediction' },
        logs: ['[2026-02-07T09:30:00] Initializing ADMETPredictor', 'Predicted ADMET for 13200 molecules', 'ADMETPredictor completed']
      }
    ]
  },
  'task-007': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Microscopy-Cell-Images',
        description: 'Cell segmentation image dataset',
        info: { Pipeline: 'CellPipeline', 'Data Samples': 8000, ID: 'cell-001', Root: '/data/cell/images', Hash: 'cell789abc' },
        fields: ['image', 'cell_type', 'resolution', 'stain'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'ImageQualityFilter',
        initParams: { prompt_template: 'ImageQuality', system_prompt: 'Filter blurry images...', llm_serving: '12' },
        runParams: { input_key: 'image', min_resolution: 512 },
        logs: ['[2026-02-06T20:00:00] Initializing ImageQualityFilter', 'Processed 7800 images', 'ImageQualityFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'CellSegmentation',
        initParams: { prompt_template: 'SegmentPrompt', num_prompts: 2, llm_serving: '12' },
        runParams: { input_key: 'image', output_key: 'segmentation_mask' },
        logs: ['[2026-02-06T22:00:00] Initializing CellSegmentation', 'Segmented 7800 images', 'CellSegmentation completed']
      }
    ]
  },
  'task-008': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Ocean-Climate-Sensors',
        description: 'Ocean climate sensor time series data',
        info: { Pipeline: 'OceanPipeline', 'Data Samples': 50000, ID: 'ocean-001', Root: '/data/ocean/sensors', Hash: 'ocean456def' },
        fields: ['timestamp', 'temperature', 'salinity', 'depth', 'location'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'SensorCalibrationFilter',
        initParams: { prompt_template: 'CalibrationFilter', system_prompt: 'Calibrate sensor readings...', llm_serving: '8' },
        runParams: { input_key: 'temperature', outlier_threshold: 3 },
        logs: ['[2026-02-07T11:00:00] Initializing SensorCalibrationFilter', 'Processed 48500 readings', 'CalibrationFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'DataCleaner',
        initParams: { prompt_template: 'CleanPrompt', num_prompts: 1, llm_serving: '8' },
        runParams: { input_key: 'salinity', output_key: 'cleaned_data' },
        logs: ['[2026-02-07T11:30:00] Initializing DataCleaner', 'Cleaned 48500 records', 'DataCleaner completed']
      }
    ]
  },
  'task-009': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Crystal-Structure-Data',
        description: 'Crystal structure feature dataset',
        info: { Pipeline: 'CrystalPipeline', 'Data Samples': 6000, ID: 'crystal-001', Root: '/data/crystal/structures', Hash: 'crystal123' },
        fields: ['structure', 'space_group', 'lattice_params', 'atomic_coords'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'StructureValidationFilter',
        initParams: { prompt_template: 'ValidateStructure', system_prompt: 'Validate crystal structures...', llm_serving: '10' },
        runParams: { input_key: 'structure', tolerance: 0.01 },
        logs: ['[2026-02-06T15:30:00] Initializing StructureValidationFilter', 'Validated 5800 structures', 'ValidationFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'FeatureExtractor',
        initParams: { prompt_template: 'FeatureExtraction', num_prompts: 3, llm_serving: '10' },
        runParams: { input_key: 'structure', output_key: 'crystal_features' },
        logs: ['[2026-02-06T17:00:00] Initializing FeatureExtractor', 'Extracted features for 5800 structures', 'FeatureExtractor completed']
      }
    ]
  },
  'task-010': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Genome-Variants',
        description: 'Genome variant annotation dataset',
        info: { Pipeline: 'GenomePipeline', 'Data Samples': 200000, ID: 'genome-001', Root: '/data/genome/variants', Hash: 'genome789abc' },
        fields: ['chromosome', 'position', 'ref', 'alt', 'quality'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'VariantQualityFilter',
        initParams: { prompt_template: 'VariantQuality', system_prompt: 'Filter low quality variants...', llm_serving: '9' },
        runParams: { input_key: 'quality', min_qual: 30 },
        logs: ['[2026-02-06T08:00:00] Initializing VariantQualityFilter', 'Filtered 185000 variants', 'QualityFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'VariantAnnotator',
        initParams: { prompt_template: 'AnnotateVariant', num_prompts: 2, llm_serving: '9' },
        runParams: { input_key: 'position', output_key: 'annotation' },
        logs: ['[2026-02-06T09:00:00] Initializing VariantAnnotator', 'Annotated 185000 variants', 'VariantAnnotator completed']
      }
    ]
  },
  'task-011': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'EEG-Signal-Data',
        description: 'Neuroscience EEG signal dataset',
        info: { Pipeline: 'EEGPipeline', 'Data Samples': 15000, ID: 'eeg-001', Root: '/data/eeg/signals', Hash: 'eeg456def' },
        fields: ['timestamp', 'channel', 'amplitude', 'frequency', 'subject_id'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'ArtifactRemovalFilter',
        initParams: { prompt_template: 'ArtifactRemoval', system_prompt: 'Remove EEG artifacts...', llm_serving: '11' },
        runParams: { input_key: 'amplitude', artifact_threshold: 100 },
        logs: ['[2026-02-07T13:00:00] Initializing ArtifactRemovalFilter', 'Processed 12000 samples', 'ArtifactRemovalFilter running...']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'SignalPreprocessor',
        initParams: { prompt_template: 'PreprocessSignal', num_prompts: 1, llm_serving: '11' },
        runParams: { input_key: 'amplitude', output_key: 'preprocessed_signal' },
        logs: ['[2026-02-07T13:30:00] Initializing SignalPreprocessor', 'Preprocessing signals...', 'Error: Processing timeout']
      }
    ]
  },
  'task-012': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'MD-Trajectory-Data',
        description: 'Molecular dynamics trajectory data',
        info: { Pipeline: 'MDPipeline', 'Data Samples': 10000, ID: 'md-001', Root: '/data/md/trajectories', Hash: 'md789abc' },
        fields: ['frame', 'coordinates', 'velocities', 'forces', 'time'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'TrajectoryParser',
        initParams: { prompt_template: 'ParseTrajectory', system_prompt: 'Parse MD trajectory...', llm_serving: '10' },
        runParams: { input_key: 'coordinates', timestep: 1 },
        logs: ['[2026-02-05T22:00:00] Initializing TrajectoryParser', 'Parsed 10000 frames', 'TrajectoryParser completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'TrajectoryAnalyzer',
        initParams: { prompt_template: 'AnalyzeTrajectory', num_prompts: 2, llm_serving: '10' },
        runParams: { input_key: 'coordinates', output_key: 'trajectory_analysis' },
        logs: ['[2026-02-06T00:00:00] Initializing TrajectoryAnalyzer', 'Analyzed 10000 frames', 'TrajectoryAnalyzer completed']
      }
    ]
  },
  'task-013': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Superconductor-DB',
        description: 'Superconductor Tc prediction dataset',
        info: { Pipeline: 'SuperconductorPipeline', 'Data Samples': 12000, ID: 'super-001', Root: '/data/superconductor/db', Hash: 'super123xyz' },
        fields: ['formula', 'tc', 'pressure', 'structure_type', 'ref'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'DataValidationFilter',
        initParams: { prompt_template: 'ValidateData', system_prompt: 'Validate superconductor data...', llm_serving: '9' },
        runParams: { input_key: 'tc', min_tc: 0 },
        logs: ['[2026-02-06T10:00:00] Initializing DataValidationFilter', 'Validated 11500 records', 'ValidationFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'TcPredictor',
        initParams: { prompt_template: 'PredictTc', num_prompts: 1, llm_serving: '9' },
        runParams: { input_key: 'formula', output_key: 'tc_prediction' },
        logs: ['[2026-02-06T10:30:00] Initializing TcPredictor', 'Predicted Tc for 11500 materials', 'TcPredictor completed']
      }
    ]
  },
  'task-014': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Satellite-Weather-Images',
        description: 'Satellite weather pattern images',
        info: { Pipeline: 'WeatherPipeline', 'Data Samples': 25000, ID: 'weather-001', Root: '/data/weather/satellite', Hash: 'weather456def' },
        fields: ['image', 'timestamp', 'region', 'cloud_cover', 'temperature'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'CloudCoverFilter',
        initParams: { prompt_template: 'FilterClouds', system_prompt: 'Filter by cloud coverage...', llm_serving: '12' },
        runParams: { input_key: 'cloud_cover', max_cover: 0.8 },
        logs: ['[2026-02-05T14:00:00] Initializing CloudCoverFilter', 'Filtered 22000 images', 'CloudCoverFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'WeatherClassifier',
        initParams: { prompt_template: 'ClassifyWeather', num_prompts: 3, llm_serving: '12' },
        runParams: { input_key: 'image', output_key: 'weather_pattern' },
        logs: ['[2026-02-05T16:00:00] Initializing WeatherClassifier', 'Classified 22000 images', 'WeatherClassifier completed']
      }
    ]
  },
  'task-015': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Biodiversity-Records',
        description: 'Ecology biodiversity records dataset',
        info: { Pipeline: 'BiodiversityPipeline', 'Data Samples': 80000, ID: 'bio-001', Root: '/data/biodiversity/records', Hash: 'bio789abc' },
        fields: ['species', 'location', 'date', 'observer', 'coordinates'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'DuplicateRecordFilter',
        initParams: { prompt_template: 'FindDuplicates', system_prompt: 'Find duplicate records...', llm_serving: '8' },
        runParams: { input_key: 'species', similarity: 0.95 },
        logs: ['[2026-02-08T12:30:00] Initializing DuplicateRecordFilter', 'Processing 80000 records...', 'Found 5000 duplicates']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'RecordDeduplicator',
        initParams: { prompt_template: 'Deduplicate', num_prompts: 1, llm_serving: '8' },
        runParams: { input_key: 'location', output_key: 'deduplicated_record' },
        logs: ['[2026-02-08T13:00:00] Initializing RecordDeduplicator', 'Deduplication in progress...']
      }
    ]
  },
  'task-016': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Iron-Steel-Papers',
        description: 'Metallurgy research papers dataset',
        info: { Pipeline: 'MetallurgyPipeline', 'Data Samples': 5000, ID: 'metal-001', Root: '/data/metallurgy/papers', Hash: 'metal123xyz' },
        fields: ['title', 'abstract', 'full_text', 'keywords', 'authors'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'LanguageFilter',
        initParams: { prompt_template: 'FilterLanguage', system_prompt: 'Filter non-English papers...', llm_serving: '9' },
        runParams: { input_key: 'full_text', language: 'en' },
        logs: ['[2026-02-07T15:00:00] Initializing LanguageFilter', 'Filtered 4800 papers', 'LanguageFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'NERExtractor',
        initParams: { prompt_template: 'ExtractNER', num_prompts: 2, llm_serving: '9' },
        runParams: { input_key: 'abstract', output_key: 'named_entities' },
        logs: ['[2026-02-07T15:30:00] Initializing NERExtractor', 'Extracted entities from 4800 papers', 'NERExtractor completed']
      }
    ]
  },
  'task-017': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Geoscience-Maps',
        description: 'Geoscience map segmentation dataset',
        info: { Pipeline: 'GeosciencePipeline', 'Data Samples': 3500, ID: 'geo-001', Root: '/data/geoscience/maps', Hash: 'geo456def' },
        fields: ['map_image', 'region', 'scale', 'legend', 'features'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'MapQualityFilter',
        initParams: { prompt_template: 'MapQuality', system_prompt: 'Check map quality...', llm_serving: '11' },
        runParams: { input_key: 'map_image', min_resolution: 1024 },
        logs: ['[2026-02-07T08:00:00] Initializing MapQualityFilter', 'Processed 3000 maps', 'MapQualityFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'SegmentationLabeler',
        initParams: { prompt_template: 'SegmentMap', num_prompts: 2, llm_serving: '11' },
        runParams: { input_key: 'map_image', output_key: 'segmentation' },
        logs: ['[2026-02-07T08:30:00] Initializing SegmentationLabeler', 'Labeling maps...', 'Error: Segmentation failed']
      }
    ]
  },
  'task-018': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Physics-Simulation-Data',
        description: 'Physics simulation validation dataset',
        info: { Pipeline: 'PhysicsPipeline', 'Data Samples': 20000, ID: 'physics-001', Root: '/data/physics/simulations', Hash: 'physics789abc' },
        fields: ['simulation_id', 'parameters', 'results', 'error', 'timestamp'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'ConvergenceCheckFilter',
        initParams: { prompt_template: 'CheckConvergence', system_prompt: 'Check simulation convergence...', llm_serving: '10' },
        runParams: { input_key: 'error', tolerance: 1e-6 },
        logs: ['[2026-02-06T16:00:00] Initializing ConvergenceCheckFilter', 'Checked 19500 simulations', 'ConvergenceCheck completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'DataValidator',
        initParams: { prompt_template: 'ValidateData', num_prompts: 1, llm_serving: '10' },
        runParams: { input_key: 'results', output_key: 'validation_result' },
        logs: ['[2026-02-06T18:00:00] Initializing DataValidator', 'Validated 19500 simulations', 'DataValidator completed']
      }
    ]
  },
  'task-019': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Clinical-Trials-Data',
        description: 'Clinical trials outcome dataset',
        info: { Pipeline: 'ClinicalPipeline', 'Data Samples': 18000, ID: 'clinical-001', Root: '/data/clinical/trials', Hash: 'clinical123xyz' },
        fields: ['trial_id', 'patient_id', 'outcome', 'drug', 'dosage'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'CompletenessFilter',
        initParams: { prompt_template: 'CheckCompleteness', system_prompt: 'Check data completeness...', llm_serving: '9' },
        runParams: { input_key: 'outcome', min_fields: 5 },
        logs: ['[2026-02-08T08:45:00] Initializing CompletenessFilter', 'Processing 18000 records...', 'Found 15000 complete records']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'OutcomeStructurer',
        initParams: { prompt_template: 'StructureOutcome', num_prompts: 2, llm_serving: '9' },
        runParams: { input_key: 'outcome', output_key: 'structured_outcome' },
        logs: ['[2026-02-08T09:15:00] Initializing OutcomeStructurer', 'Structuring outcomes...']
      }
    ]
  },
  'task-020': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Math-Olympiad-Problems',
        description: 'Math olympiad solutions dataset',
        info: { Pipeline: 'MathPipeline', 'Data Samples': 8000, ID: 'math-001', Root: '/data/math/olympiad', Hash: 'math456def' },
        fields: ['problem', 'solution', 'difficulty', 'topic', 'year'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'SolutionCompletenessFilter',
        initParams: { prompt_template: 'CheckSolution', system_prompt: 'Check solution completeness...', llm_serving: '8' },
        runParams: { input_key: 'solution', min_steps: 3 },
        logs: ['[2026-02-06T12:00:00] Initializing SolutionCompletenessFilter', 'Filtered 7800 problems', 'CompletenessFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'SolutionParser',
        initParams: { prompt_template: 'ParseSolution', num_prompts: 1, llm_serving: '8' },
        runParams: { input_key: 'solution', output_key: 'parsed_steps' },
        logs: ['[2026-02-06T12:30:00] Initializing SolutionParser', 'Parsed 7800 solutions', 'SolutionParser completed']
      }
    ]
  },
  'task-021': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Soil-Spectroscopy',
        description: 'Soil spectroscopy feature dataset',
        info: { Pipeline: 'SoilPipeline', 'Data Samples': 15000, ID: 'soil-001', Root: '/data/soil/spectroscopy', Hash: 'soil789abc' },
        fields: ['wavelength', 'reflectance', 'sample_id', 'location', 'depth'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'SpectralQualityFilter',
        initParams: { prompt_template: 'SpectralQuality', system_prompt: 'Check spectral quality...', llm_serving: '10' },
        runParams: { input_key: 'reflectance', snr_min: 20 },
        logs: ['[2026-02-05T09:00:00] Initializing SpectralQualityFilter', 'Filtered 14500 spectra', 'QualityFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'FeatureEngineer',
        initParams: { prompt_template: 'EngineerFeatures', num_prompts: 3, llm_serving: '10' },
        runParams: { input_key: 'wavelength', output_key: 'engineered_features' },
        logs: ['[2026-02-05T09:30:00] Initializing FeatureEngineer', 'Engineered features for 14500 samples', 'FeatureEngineer completed']
      }
    ]
  },
  'task-022': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Paleontology-Fossils',
        description: 'Paleontology fossil images dataset',
        info: { Pipeline: 'FossilPipeline', 'Data Samples': 12000, ID: 'fossil-001', Root: '/data/paleontology/fossils', Hash: 'fossil123xyz' },
        fields: ['image', 'fossil_type', 'era', 'location', 'specimen_id'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'ImageClarityFilter',
        initParams: { prompt_template: 'CheckClarity', system_prompt: 'Check image clarity...', llm_serving: '11' },
        runParams: { input_key: 'image', min_clarity: 0.7 },
        logs: ['[2026-02-08T13:00:00] Initializing ImageClarityFilter', 'Processing 12000 images...', 'Filtered 9500 clear images']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'FossilDetector',
        initParams: { prompt_template: 'DetectFossil', num_prompts: 2, llm_serving: '11' },
        runParams: { input_key: 'image', output_key: 'detection_result' },
        logs: ['[2026-02-08T13:30:00] Initializing FossilDetector', 'Detection training in progress...']
      }
    ]
  },
  'task-023': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Nuclear-Reactor-Logs',
        description: 'Nuclear reactor log anomaly dataset',
        info: { Pipeline: 'NuclearPipeline', 'Data Samples': 100000, ID: 'nuclear-001', Root: '/data/nuclear/logs', Hash: 'nuclear456def' },
        fields: ['timestamp', 'log_level', 'message', 'reactor_id', 'sensor_reading'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'LogFormatFilter',
        initParams: { prompt_template: 'ParseLogFormat', system_prompt: 'Parse log format...', llm_serving: '9' },
        runParams: { input_key: 'message', format: 'structured' },
        logs: ['[2026-02-06T18:00:00] Initializing LogFormatFilter', 'Parsed 98000 logs', 'LogFormatFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'AnomalyTagger',
        initParams: { prompt_template: 'TagAnomaly', num_prompts: 2, llm_serving: '9' },
        runParams: { input_key: 'message', output_key: 'anomaly_tag' },
        logs: ['[2026-02-06T19:00:00] Initializing AnomalyTagger', 'Tagged anomalies in 98000 logs', 'AnomalyTagger completed']
      }
    ]
  },
  'task-024': {
    nodes: [
      {
        id: 'node-1',
        type: 'dataset',
        name: 'Aerial-Imaging',
        description: 'Aerial imaging land use dataset',
        info: { Pipeline: 'AerialPipeline', 'Data Samples': 35000, ID: 'aerial-001', Root: '/data/aerial/images', Hash: 'aerial789abc' },
        fields: ['image', 'coordinates', 'resolution', 'capture_date', 'area_km2'],
        initParams: {}, runParams: {}, logs: []
      },
      {
        id: 'node-2',
        type: 'filter',
        name: 'CoverageFilter',
        initParams: { prompt_template: 'CheckCoverage', system_prompt: 'Check area coverage...', llm_serving: '12' },
        runParams: { input_key: 'area_km2', min_area: 1 },
        logs: ['[2026-02-05T16:00:00] Initializing CoverageFilter', 'Filtered 32000 images', 'CoverageFilter completed']
      },
      {
        id: 'node-3',
        type: 'generate',
        name: 'LandUseAnnotator',
        initParams: { prompt_template: 'AnnotateLandUse', num_prompts: 3, llm_serving: '12' },
        runParams: { input_key: 'image', output_key: 'land_use_label' },
        logs: ['[2026-02-05T18:00:00] Initializing LandUseAnnotator', 'Annotated 32000 images', 'LandUseAnnotator completed']
      }
    ]
  }
}

// Execution Results Data
const executionResults = {
  'task-001': {
    taskId: '3c40dce81a0d',
    timeAgo: '27s ago',
    sampleCounts: [
      { step: 'S1: ReasoningQue...', value: 8, color: '#f8b4b4' },
      { step: 'S2: ReasoningQue...', value: 16, color: '#fde68a' },
      { step: 'S3: ReasoningAns...', value: 16, color: '#bbf7d0' },
      { step: 'S4: ReasoningAns...', value: 16, color: '#bbf7d0' },
      { step: 'S5: ReasoningAns...', value: 16, color: '#bae6fd' },
    ],
    sampleData: `{"instruction": "A farmer has 12 sheep and 5 lambs. If he sells 3 sheep, how many animals remain?", "output": "The farmer originally has 12 sheep + 5 lambs = 17 animals. After selling 3 sheep, he has 12 - 3 = 9 sheep and still 5 lambs. Total animals remaining: 9 + 5 = 14.", "golden_answer": "14", "source": "math_word_problems"}
{"instruction": "Calculate the area of a circle with radius 5cm.", "output": "Using the formula A = πr², where r = 5cm. A = π × 5² = 25π ≈ 78.54 cm².", "golden_answer": "78.54 cm²", "source": "geometry_problems"}
{"instruction": "If a train travels at 80 km/h, how long does it take to travel 200 km?", "output": "Time = Distance / Speed = 200 km / 80 km/h = 2.5 hours or 2 hours 30 minutes.", "golden_answer": "2.5 hours", "source": "physics_problems"}`,
    currentStepLogs: [
      '[2026-02-02T15:15:16.511061] [3/5] Initializing operator: ReasoningAnswerGenerator',
      '[2026-02-02T15:15:16.511117] - Initializing LLM serving: c4f66200d5e85944',
      '[2026-02-02T15:15:16.511121] - Loading prompt template: GeneralAnswerGeneratorPrompt',
      '[2026-02-02T15:15:16.511555] [3/5] ReasoningAnswerGenerator initialized successfully',
      '[2026-02-02T15:15:24.846240] [3/5] Running operator: ReasoningAnswerGenerator',
      'Processed 16 samples',
      '[2026-02-02T15:15:33.332859] [3/5] ReasoningAnswerGenerator completed successfully'
    ],
    logs: [
      '[2026-02-02T15:15:15.220998] Starting pipeline execution: 3c40dce81a0d',
      '[2026-02-02T15:15:15.220998] Starting pipeline execution: 3c40dce81a0d',
      '[2026-02-02T15:15:15.221116] Step 1: Initializing storage...',
      '[2026-02-02T15:15:15.221119] Step 1: Initializing storage...',
      'Storage initialized with dataset: /data/mzm/test_release/DataFlow-WebUI-v0.0.2/backend/data/dataflow_core/example_data/ReasoningPipeline/pipeline_general.json',
      '[2026-02-02T15:15:15.221659] Storage initialized with dataset: /data/mzm/test_release/DataFlow-WebUI-v0.0.2/backend/data/dataflow_core/example_data/ReasoningPipeline/pipeline_general.json',
      '[2026-02-02T15:15:15.221707] Step 2: Initializing operators...',
      '[2026-02-02T15:15:15.221709] Step 2: Initializing operators...',
      '[2026-02-02T15:15:16.511061] [1/5] Initializing operator: ReasoningQuestionFilter',
      '[2026-02-02T15:15:16.511061] [1/5] ReasoningQuestionFilter initialized successfully',
      '[2026-02-02T15:15:16.511555] [1/5] Running operator: ReasoningQuestionFilter',
      'Processed 8 samples',
      '[2026-02-02T15:15:24.846240] [2/5] Initializing operator: ReasoningQuestionGenerator',
      'Processed 16 samples',
      '[2026-02-02T15:15:33.332859] [3/5] Running operator: ReasoningAnswerGenerator',
      'Processed 16 samples'
    ]
  },
  'task-002': {
    taskId: 'rna-seq-8f4d2a',
    timeAgo: '5m ago',
    sampleCounts: [
      { step: 'S1: QualityFilter', value: 4500, color: '#f8b4b4' },
      { step: 'S2: FeatureGen', value: 4500, color: '#bbf7d0' },
    ],
    sampleData: `{"sequence": "AUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCUAUGCU", "label": "mRNA", "length": 90, "gc_content": 0.33}
{"sequence": "GCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGC", "label": "rRNA", "length": 100, "gc_content": 1.0}
{"sequence": "UACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACGUACG", "label": "tRNA", "length": 95, "gc_content": 0.25}`,
    currentStepLogs: [
      '[2026-02-02T10:25:16.511061] Initializing operator: SequenceFeatureGenerator',
      '[2026-02-02T10:25:16.511117] - Initializing LLM serving: c4f66200d5e85944',
      'Generating features for RNA sequences...',
      'Processed 4500 samples',
      'SequenceFeatureGenerator completed successfully'
    ],
    logs: [
      '[2026-02-02T10:15:15.220998] Starting pipeline execution: rna-seq-8f4d2a',
      '[2026-02-02T10:15:15.221116] Step 1: Initializing storage...',
      'Storage initialized with RNA dataset',
      '[2026-02-02T10:15:16.511061] Step 2: Initializing operators...',
      '[2026-02-02T10:15:16.511555] Running operator: SequenceQualityFilter',
      'Processed 4500 samples (filtered from 5000)',
      '[2026-02-02T10:20:16.511061] Running operator: SequenceFeatureGenerator',
      'Feature generation complete'
    ]
  },
  'task-003': {
    taskId: 'qchem-dft-9e3b1c',
    timeAgo: '12m ago',
    sampleCounts: [
      { step: 'S1: Convergence', value: 230, color: '#fde68a' },
      { step: 'S2: Normalizer', value: 230, color: '#bae6fd' },
    ],
    sampleData: `{"molecule": "H2O", "energy": -76.3847, "forces": [[0.0, 0.0, 0.001], [0.0, -0.002, 0.0], [0.0, 0.002, -0.001]], "stress": [0.01, 0.01, 0.01, 0.0, 0.0, 0.0]}
{"molecule": "CH4", "energy": -40.2189, "forces": [[0.001, 0.0, 0.0], [-0.001, 0.001, 0.0], [0.0, -0.001, 0.001], [0.0, 0.0, -0.001], [0.0, 0.0, 0.0]], "stress": [0.02, 0.02, 0.02, 0.0, 0.0, 0.0]}
{"molecule": "CO2", "energy": -188.2431, "forces": [[0.0, 0.0, 0.0], [0.001, 0.0, 0.0], [-0.001, 0.0, 0.0]], "stress": [0.015, 0.015, 0.015, 0.0, 0.0, 0.0]}`,
    currentStepLogs: [
      '[2026-02-02T07:45:16.511061] Initializing operator: EnergyNormalizer',
      '[2026-02-02T07:45:16.511117] - Initializing LLM serving: c4f66200d5e85944',
      'Normalizing DFT energies...',
      'Processed 230 samples',
      'EnergyNormalizer completed successfully'
    ],
    logs: [
      '[2026-02-02T07:30:15.220998] Starting pipeline execution: qchem-dft-9e3b1c',
      '[2026-02-02T07:30:15.221116] Step 1: Initializing storage...',
      'Storage initialized with QChem dataset',
      '[2026-02-02T07:35:16.511061] Running operator: ConvergenceFilter',
      'Processed 230 samples (filtered from 250)',
      '[2026-02-02T07:40:16.511061] Running operator: EnergyNormalizer',
      'Energy normalization complete'
    ]
  },
  'task-004': {
    taskId: 'seismic-evt-7a2b9c',
    timeAgo: '8m ago',
    sampleCounts: [
      { step: 'S1: NoiseFilter', value: 9800, color: '#f8b4b4' },
      { step: 'S2: EventDetect', value: 342, color: '#bbf7d0' },
    ],
    sampleData: `{"waveform": [0.002, 0.003, 0.001, 0.004, 0.156, 0.892, 1.234, 0.756, 0.342, 0.123], "timestamp": "2026-02-08T11:20:15.123Z", "magnitude": 4.2, "station_id": "SEIS-001"}
{"waveform": [0.001, 0.002, 0.001, 0.003, 0.008, 0.015, 0.012, 0.009, 0.005, 0.003], "timestamp": "2026-02-08T11:22:30.456Z", "magnitude": 2.1, "station_id": "SEIS-003"}
{"waveform": [0.003, 0.005, 0.012, 0.089, 0.456, 1.892, 2.456, 1.234, 0.567, 0.234], "timestamp": "2026-02-08T11:25:45.789Z", "magnitude": 5.7, "station_id": "SEIS-002"}`,
    currentStepLogs: [
      '[2026-02-08T11:25:00] Initializing EventDetector',
      'Detecting seismic events...',
      'Found 342 seismic events',
      'EventDetector completed successfully'
    ],
    logs: [
      '[2026-02-08T11:20:00] Starting pipeline execution: seismic-evt-7a2b9c',
      'Storage initialized with seismic dataset',
      'Running operator: NoiseReductionFilter',
      'Processed 9800 samples (filtered from 12000)',
      'Running operator: EventDetector',
      'Event detection complete'
    ]
  },
  'task-005': {
    taskId: 'astro-spec-4f8d2e',
    timeAgo: '15m ago',
    sampleCounts: [
      { step: 'S1: QualityCheck', value: 7200, color: '#fde68a' },
      { step: 'S2: Redshift', value: 7200, color: '#bae6fd' },
    ],
    sampleData: `{"wavelength": [4000.5, 4001.0, 4001.5, 4002.0, 4862.7, 6564.6], "flux": [1.23, 1.25, 1.22, 1.24, 15.67, 23.45], "redshift": 0.0234, "object_id": "GAL-2026-001"}
{"wavelength": [4000.0, 4000.5, 4001.0, 5008.2, 6565.2], "flux": [0.89, 0.91, 0.88, 8.92, 18.34], "redshift": 0.1567, "object_id": "QSO-2026-042"}
{"wavelength": [4100.0, 4341.6, 4862.1, 6563.8], "flux": [3.45, 5.67, 7.89, 12.34], "redshift": 0.0089, "object_id": "STAR-2026-103"}`,
    currentStepLogs: [
      '[2026-02-08T06:15:00] Initializing RedshiftLabeler',
      'Calculating redshift values...',
      'Labeled 7200 spectra',
      'RedshiftLabeler completed'
    ],
    logs: [
      '[2026-02-08T06:00:00] Starting pipeline execution: astro-spec-4f8d2e',
      'Storage initialized with astrophysics spectra',
      'Running operator: SpectralQualityFilter',
      'Processed 7200 spectra (filtered from 8500)',
      'Running operator: RedshiftLabeler',
      'Redshift labeling complete'
    ]
  },
  'task-006': {
    taskId: 'drug-admet-9c3b1a',
    timeAgo: '1h ago',
    sampleCounts: [
      { step: 'S1: DrugFilter', value: 13200, color: '#f8b4b4' },
      { step: 'S2: ADMET', value: 13200, color: '#bbf7d0' },
    ],
    sampleData: `{"smiles": "CC(C)Cc1ccc(C(C)C(=O)O)cc1", "molecular_weight": 206.28, "logp": 3.5, "admet_props": {"solubility": 0.023, "absorption": 0.89, "cyp_inhibition": 0.12, "hERG": 0.34}}
{"smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "molecular_weight": 194.19, "logp": -0.07, "admet_props": {"solubility": 0.156, "absorption": 0.95, "cyp_inhibition": 0.08, "hERG": 0.21}}
{"smiles": "CC(=O)Oc1ccccc1C(=O)O", "molecular_weight": 180.16, "logp": 1.19, "admet_props": {"solubility": 0.089, "absorption": 0.92, "cyp_inhibition": 0.15, "hERG": 0.18}}`,
    currentStepLogs: [
      '[2026-02-07T09:30:00] Initializing ADMETPredictor',
      'Predicting ADMET properties...',
      'Predicted 13200 molecules',
      'ADMETPredictor completed'
    ],
    logs: [
      '[2026-02-07T09:10:00] Starting pipeline execution: drug-admet-9c3b1a',
      'Storage initialized with drug molecules',
      'Running operator: DrugLikenessFilter',
      'Filtered 13200 molecules (from 15000)',
      'Running operator: ADMETPredictor',
      'ADMET prediction complete'
    ]
  },
  'task-007': {
    taskId: 'cell-seg-2d7e5a',
    timeAgo: '2h ago',
    sampleCounts: [
      { step: 'S1: ImgQuality', value: 7800, color: '#fde68a' },
      { step: 'S2: Segment', value: 7800, color: '#bae6fd' },
    ],
    sampleData: `{"image": "microscopy/cell_001.png", "cell_type": "HeLa", "resolution": [1024, 1024], "stain": "DAPI", "segmentation_mask": [[0,0,1,1],[0,1,1,0],[1,1,0,0],[1,0,0,1]]}
{"image": "microscopy/cell_002.png", "cell_type": "MCF-7", "resolution": [1024, 1024], "stain": "Phalloidin", "segmentation_mask": [[1,1,0,0],[1,0,0,1],[0,0,1,1],[0,1,1,0]]}
{"image": "microscopy/cell_003.png", "cell_type": "A549", "resolution": [2048, 2048], "stain": "Hoechst", "segmentation_mask": [[0,1,1,1],[1,1,0,0],[1,0,0,1],[0,0,1,1]]}`,
    currentStepLogs: [
      '[2026-02-06T22:00:00] Initializing CellSegmentation',
      'Segmenting cell images...',
      'Segmented 7800 images',
      'CellSegmentation completed'
    ],
    logs: [
      '[2026-02-06T20:00:00] Starting pipeline execution: cell-seg-2d7e5a',
      'Storage initialized with microscopy images',
      'Running operator: ImageQualityFilter',
      'Processed 7800 images (from 8000)',
      'Running operator: CellSegmentation',
      'Cell segmentation complete'
    ]
  },
  'task-008': {
    taskId: 'ocean-clean-5b9f2c',
    timeAgo: '3h ago',
    sampleCounts: [
      { step: 'S1: Calibrate', value: 48500, color: '#f8b4b4' },
      { step: 'S2: Clean', value: 48500, color: '#bbf7d0' },
    ],
    sampleData: `{"timestamp": "2026-02-07T10:00:00Z", "temperature": 18.5, "salinity": 35.2, "depth": 100.0, "location": {"lat": 35.2, "lon": -123.4}}
{"timestamp": "2026-02-07T10:15:00Z", "temperature": 18.3, "salinity": 35.3, "depth": 150.0, "location": {"lat": 35.2, "lon": -123.4}}
{"timestamp": "2026-02-07T10:30:00Z", "temperature": 17.9, "salinity": 35.1, "depth": 200.0, "location": {"lat": 35.2, "lon": -123.4}}`,
    currentStepLogs: [
      '[2026-02-07T11:30:00] Initializing DataCleaner',
      'Cleaning sensor data...',
      'Cleaned 48500 records',
      'DataCleaner completed'
    ],
    logs: [
      '[2026-02-07T11:00:00] Starting pipeline execution: ocean-clean-5b9f2c',
      'Storage initialized with ocean sensor data',
      'Running operator: SensorCalibrationFilter',
      'Processed 48500 readings (from 50000)',
      'Running operator: DataCleaner',
      'Data cleaning complete'
    ]
  },
  'task-009': {
    taskId: 'crystal-feat-8e4c1b',
    timeAgo: '4h ago',
    sampleCounts: [
      { step: 'S1: Validate', value: 5800, color: '#fde68a' },
      { step: 'S2: Extract', value: 5800, color: '#bae6fd' },
    ],
    sampleData: `{"structure": "SiO2", "space_group": "P3_221", "lattice_params": {"a": 4.91, "b": 4.91, "c": 5.40, "alpha": 90, "beta": 90, "gamma": 120}, "atomic_coords": [["Si", 0.47, 0.0, 0.33], ["O", 0.41, 0.27, 0.12]]}
{"structure": "NaCl", "space_group": "Fm-3m", "lattice_params": {"a": 5.64, "b": 5.64, "c": 5.64, "alpha": 90, "beta": 90, "gamma": 90}, "atomic_coords": [["Na", 0.0, 0.0, 0.0], ["Cl", 0.5, 0.5, 0.5]]}
{"structure": "Fe2O3", "space_group": "R-3c", "lattice_params": {"a": 5.03, "b": 5.03, "c": 13.75, "alpha": 90, "beta": 90, "gamma": 120}, "atomic_coords": [["Fe", 0.0, 0.0, 0.35], ["O", 0.31, 0.0, 0.25]]}`,
    currentStepLogs: [
      '[2026-02-06T17:00:00] Initializing FeatureExtractor',
      'Extracting crystal features...',
      'Extracted features for 5800 structures',
      'FeatureExtractor completed'
    ],
    logs: [
      '[2026-02-06T15:30:00] Starting pipeline execution: crystal-feat-8e4c1b',
      'Storage initialized with crystal structures',
      'Running operator: StructureValidationFilter',
      'Validated 5800 structures (from 6000)',
      'Running operator: FeatureExtractor',
      'Feature extraction complete'
    ]
  },
  'task-010': {
    taskId: 'genome-var-3a7f9d',
    timeAgo: '5h ago',
    sampleCounts: [
      { step: 'S1: VarFilter', value: 185000, color: '#f8b4b4' },
      { step: 'S2: Annotate', value: 185000, color: '#bbf7d0' },
    ],
    sampleData: `{"chromosome": "chr1", "position": 1234567, "ref": "A", "alt": "G", "quality": 98.5, "annotation": "missense_variant", "gene": "BRCA1"}
{"chromosome": "chr7", "position": 8765432, "ref": "C", "alt": "T", "quality": 92.1, "annotation": "synonymous_variant", "gene": "EGFR"}
{"chromosome": "chr17", "position": 7654321, "ref": "G", "alt": "A", "quality": 99.9, "annotation": "stop_gained", "gene": "TP53"}`,
    currentStepLogs: [
      '[2026-02-06T09:00:00] Initializing VariantAnnotator',
      'Annotating variants...',
      'Annotated 185000 variants',
      'VariantAnnotator completed'
    ],
    logs: [
      '[2026-02-06T08:00:00] Starting pipeline execution: genome-var-3a7f9d',
      'Storage initialized with genome variants',
      'Running operator: VariantQualityFilter',
      'Filtered 185000 variants (from 200000)',
      'Running operator: VariantAnnotator',
      'Variant annotation complete'
    ]
  },
  'task-011': {
    taskId: 'eeg-preproc-6b2e8a',
    timeAgo: '6h ago',
    sampleCounts: [
      { step: 'S1: ArtifactRem', value: 12000, color: '#f8b4b4' },
      { step: 'S2: Preprocess', value: 12000, color: '#fde68a' },
    ],
    sampleData: `{"timestamp": "2026-02-07T13:00:00.000Z", "channel": "F3", "amplitude": 12.5, "frequency": 10.5, "subject_id": "S001", "preprocessed_signal": [0.12, 0.15, 0.11, 0.18, 0.22, 0.19, 0.14]}
{"timestamp": "2026-02-07T13:00:00.004Z", "channel": "C3", "amplitude": 8.3, "frequency": 12.2, "subject_id": "S001", "preprocessed_signal": [0.08, 0.09, 0.11, 0.10, 0.09, 0.08, 0.07]}
{"timestamp": "2026-02-07T13:00:00.008Z", "channel": "O1", "amplitude": 15.7, "frequency": 8.5, "subject_id": "S001", "preprocessed_signal": [0.18, 0.21, 0.25, 0.23, 0.19, 0.16, 0.14]}`,
    currentStepLogs: [
      '[2026-02-07T13:30:00] Initializing SignalPreprocessor',
      'Preprocessing EEG signals...',
      'Error: Processing timeout at sample 11500'
    ],
    logs: [
      '[2026-02-07T13:00:00] Starting pipeline execution: eeg-preproc-6b2e8a',
      'Storage initialized with EEG data',
      'Running operator: ArtifactRemovalFilter',
      'Processed 12000 samples (from 15000)',
      'Running operator: SignalPreprocessor',
      'Error: Step 2 failed - Processing timeout'
    ]
  },
  'task-012': {
    taskId: 'md-traj-9c5f1b',
    timeAgo: '7h ago',
    sampleCounts: [
      { step: 'S1: Parse', value: 10000, color: '#fde68a' },
      { step: 'S2: Analyze', value: 10000, color: '#bae6fd' },
    ],
    sampleData: `{"frame": 1, "coordinates": [[0.0, 0.0, 0.0], [0.96, 0.0, 0.0], [0.0, 0.96, 0.0]], "velocities": [[0.01, 0.02, -0.01], [-0.01, 0.01, 0.0], [0.0, -0.02, 0.01]], "forces": [[0.05, 0.03, -0.02], [-0.04, 0.02, 0.01], [0.01, -0.03, 0.02]], "time": 0.0}
{"frame": 2, "coordinates": [[0.001, 0.002, -0.001], [0.961, 0.001, 0.0], [-0.001, 0.959, 0.001]], "velocities": [[0.012, 0.018, -0.008], [-0.008, 0.012, 0.002], [0.002, -0.018, 0.012]], "forces": [[0.052, 0.028, -0.018], [-0.038, 0.025, 0.005], [0.012, -0.028, 0.018]], "time": 1.0}
{"frame": 3, "coordinates": [[0.003, 0.004, -0.002], [0.963, 0.002, 0.001], [-0.002, 0.957, 0.002]], "velocities": [[0.015, 0.015, -0.005], [-0.005, 0.015, 0.005], [0.005, -0.015, 0.015]], "forces": [[0.055, 0.025, -0.015], [-0.035, 0.028, 0.008], [0.015, -0.025, 0.015]], "time": 2.0}`,
    currentStepLogs: [
      '[2026-02-06T00:00:00] Initializing TrajectoryAnalyzer',
      'Analyzing trajectories...',
      'Analyzed 10000 frames',
      'TrajectoryAnalyzer completed'
    ],
    logs: [
      '[2026-02-05T22:00:00] Starting pipeline execution: md-traj-9c5f1b',
      'Storage initialized with MD trajectory',
      'Running operator: TrajectoryParser',
      'Parsed 10000 frames',
      'Running operator: TrajectoryAnalyzer',
      'Trajectory analysis complete'
    ]
  },
  'task-013': {
    taskId: 'super-tc-4d8e2a',
    timeAgo: '8h ago',
    sampleCounts: [
      { step: 'S1: Validate', value: 11500, color: '#f8b4b4' },
      { step: 'S2: Predict', value: 11500, color: '#bbf7d0' },
    ],
    sampleData: `{"formula": "HgBa2Ca2Cu3O8", "tc": 133.5, "pressure": 1.0, "structure_type": "cuprate", "ref": "Physica C 1993", "tc_prediction": 134.2}
{"formula": "YBa2Cu3O7", "tc": 92.0, "pressure": 1.0, "structure_type": "cuprate", "ref": "Z. Phys. B 1987", "tc_prediction": 91.5}
{"formula": "MgB2", "tc": 39.0, "pressure": 1.0, "structure_type": "intermetallic", "ref": "Nature 2001", "tc_prediction": 38.8}`,
    currentStepLogs: [
      '[2026-02-06T10:30:00] Initializing TcPredictor',
      'Predicting Tc values...',
      'Predicted Tc for 11500 materials',
      'TcPredictor completed'
    ],
    logs: [
      '[2026-02-06T10:00:00] Starting pipeline execution: super-tc-4d8e2a',
      'Storage initialized with superconductor data',
      'Running operator: DataValidationFilter',
      'Validated 11500 records (from 12000)',
      'Running operator: TcPredictor',
      'Tc prediction complete'
    ]
  },
  'task-014': {
    taskId: 'weather-cls-7f3b9c',
    timeAgo: '9h ago',
    sampleCounts: [
      { step: 'S1: CloudFilter', value: 22000, color: '#fde68a' },
      { step: 'S2: Classify', value: 22000, color: '#bae6fd' },
    ],
    sampleData: `{"image": "satellite/weather_20260205_1400.png", "timestamp": "2026-02-05T14:00:00Z", "region": "Pacific_North", "cloud_cover": 0.35, "temperature": 285.5, "weather_pattern": "partly_cloudy"}
{"image": "satellite/weather_20260205_1500.png", "timestamp": "2026-02-05T15:00:00Z", "region": "Pacific_North", "cloud_cover": 0.72, "temperature": 283.2, "weather_pattern": "cloudy"}
{"image": "satellite/weather_20260205_1600.png", "timestamp": "2026-02-05T16:00:00Z", "region": "Pacific_North", "cloud_cover": 0.18, "temperature": 288.7, "weather_pattern": "clear"}`,
    currentStepLogs: [
      '[2026-02-05T16:00:00] Initializing WeatherClassifier',
      'Classifying weather patterns...',
      'Classified 22000 images',
      'WeatherClassifier completed'
    ],
    logs: [
      '[2026-02-05T14:00:00] Starting pipeline execution: weather-cls-7f3b9c',
      'Storage initialized with satellite images',
      'Running operator: CloudCoverFilter',
      'Filtered 22000 images (from 25000)',
      'Running operator: WeatherClassifier',
      'Weather classification complete'
    ]
  },
  'task-015': {
    taskId: 'bio-dedup-2a5f8e',
    timeAgo: '10h ago',
    sampleCounts: [
      { step: 'S1: DupFilter', value: 75000, color: '#f8b4b4' },
      { step: 'S2: Deduplicate', value: 75000, color: '#bbf7d0' },
    ],
    sampleData: `{"species": "Panthera leo", "location": "Serengeti National Park", "date": "2026-02-01", "observer": "Dr. Smith", "coordinates": {"lat": -2.333, "lon": 34.833}, "deduplicated_record": true}
{"species": "Elephas africanus", "location": "Masai Mara", "date": "2026-02-03", "observer": "Jane Doe", "coordinates": {"lat": -1.5, "lon": 35.2}, "deduplicated_record": true}
{"species": "Giraffa camelopardalis", "location": "Amboseli", "date": "2026-02-05", "observer": "John Lee", "coordinates": {"lat": -2.65, "lon": 37.25}, "deduplicated_record": false}`,
    currentStepLogs: [
      '[2026-02-08T13:00:00] Initializing RecordDeduplicator',
      'Deduplicating records...',
      'Removed 5000 duplicates',
      'Processing in progress...'
    ],
    logs: [
      '[2026-02-08T12:30:00] Starting pipeline execution: bio-dedup-2a5f8e',
      'Storage initialized with biodiversity records',
      'Running operator: DuplicateRecordFilter',
      'Found 5000 duplicates in 80000 records',
      'Running operator: RecordDeduplicator'
    ]
  },
  'task-016': {
    taskId: 'metal-ner-5c9f2b',
    timeAgo: '11h ago',
    sampleCounts: [
      { step: 'S1: LangFilter', value: 4800, color: '#fde68a' },
      { step: 'S2: NER', value: 4800, color: '#bae6fd' },
    ],
    sampleData: `{"title": "Microstructure Evolution in Austenitic Stainless Steel during Annealing", "abstract": "The austenitic stainless steel 316L shows significant changes in grain structure when annealed at 1050°C.", "named_entities": {"materials": ["316L stainless steel"], "processes": ["annealing"], "temperatures": ["1050°C"], "properties": ["grain structure", "microstructure"]}}
{"title": "Effect of Carbon Content on Martensitic Transformation in High-Strength Steel", "abstract": "Carbon content above 0.8% wt inhibits martensitic transformation and promotes pearlite formation.", "named_entities": {"materials": ["high-strength steel"], "processes": ["martensitic transformation"], "properties": ["carbon content"], "values": ["0.8% wt"]}}
{"title": "Titanium Alloys for Aerospace Applications: A Review", "abstract": "Ti-6Al-4V remains the most widely used titanium alloy in aerospace due to its excellent strength-to-weight ratio.", "named_entities": {"materials": ["Ti-6Al-4V", "titanium alloy"], "applications": ["aerospace"], "properties": ["strength-to-weight ratio"]}}`,
    currentStepLogs: [
      '[2026-02-07T15:30:00] Initializing NERExtractor',
      'Extracting named entities...',
      'Extracted entities from 4800 papers',
      'NERExtractor completed'
    ],
    logs: [
      '[2026-02-07T15:00:00] Starting pipeline execution: metal-ner-5c9f2b',
      'Storage initialized with metallurgy papers',
      'Running operator: LanguageFilter',
      'Filtered 4800 papers (from 5000)',
      'Running operator: NERExtractor',
      'NER extraction complete'
    ]
  },
  'task-017': {
    taskId: 'geo-seg-8b4e1c',
    timeAgo: '12h ago',
    sampleCounts: [
      { step: 'S1: Quality', value: 3000, color: '#f8b4b4' },
      { step: 'S2: Segment', value: 3000, color: '#fde68a' },
    ],
    sampleData: `{"map_image": "geoscience/map_region_A_2025.png", "region": "Appalachian Basin", "scale": "1:24000", "legend": ["sandstone", "shale", "limestone", "granite"], "segmentation": {"sandstone": 0.35, "shale": 0.42, "limestone": 0.18, "granite": 0.05}}
{"map_image": "geoscience/map_region_B_2025.png", "region": "Permian Basin", "scale": "1:50000", "legend": ["dolomite", "chert", "gypsum", "halite"], "segmentation": {"dolomite": 0.28, "chert": 0.15, "gypsum": 0.35, "halite": 0.22}}
{"map_image": "geoscience/map_region_C_2025.png", "region": "Michigan Basin", "scale": "1:100000", "legend": ["salt", "anhydrite", "dolomite", "shale"], "segmentation": {"salt": 0.45, "anhydrite": 0.12, "dolomite": 0.25, "shale": 0.18}}`,
    currentStepLogs: [
      '[2026-02-07T08:30:00] Initializing SegmentationLabeler',
      'Segmenting geoscience maps...',
      'Error: Segmentation model failed to load'
    ],
    logs: [
      '[2026-02-07T08:00:00] Starting pipeline execution: geo-seg-8b4e1c',
      'Storage initialized with geoscience maps',
      'Running operator: MapQualityFilter',
      'Processed 3000 maps (from 3500)',
      'Running operator: SegmentationLabeler',
      'Error: Step 2 failed - Model loading error'
    ]
  },
  'task-018': {
    taskId: 'physics-val-3f7a9d',
    timeAgo: '13h ago',
    sampleCounts: [
      { step: 'S1: Converge', value: 19500, color: '#fde68a' },
      { step: 'S2: Validate', value: 19500, color: '#bae6fd' },
    ],
    sampleData: `{"simulation_id": "CFD-2026-001", "parameters": {"Reynolds": 10000, "Mach": 0.3, "Prandtl": 0.71}, "results": {"lift_coeff": 0.85, "drag_coeff": 0.042, "pressure_drop": 125.5}, "error": 1e-7, "timestamp": "2026-02-06T16:00:00Z", "validation_result": "passed"}
{"simulation_id": "CFD-2026-002", "parameters": {"Reynolds": 50000, "Mach": 0.5, "Prandtl": 0.71}, "results": {"lift_coeff": 0.92, "drag_coeff": 0.038, "pressure_drop": 203.7}, "error": 5e-8, "timestamp": "2026-02-06T16:30:00Z", "validation_result": "passed"}
{"simulation_id": "CFD-2026-003", "parameters": {"Reynolds": 200000, "Mach": 0.8, "Prandtl": 0.71}, "results": {"lift_coeff": 0.78, "drag_coeff": 0.055, "pressure_drop": 456.2}, "error": 8e-8, "timestamp": "2026-02-06T17:00:00Z", "validation_result": "passed"}`,
    currentStepLogs: [
      '[2026-02-06T18:00:00] Initializing DataValidator',
      'Validating simulation data...',
      'Validated 19500 simulations',
      'DataValidator completed'
    ],
    logs: [
      '[2026-02-06T16:00:00] Starting pipeline execution: physics-val-3f7a9d',
      'Storage initialized with physics simulations',
      'Running operator: ConvergenceCheckFilter',
      'Checked 19500 simulations (from 20000)',
      'Running operator: DataValidator',
      'Data validation complete'
    ]
  },
  'task-019': {
    taskId: 'clinical-struct-6e2b8a',
    timeAgo: '14h ago',
    sampleCounts: [
      { step: 'S1: Complete', value: 15000, color: '#f8b4b4' },
      { step: 'S2: Structure', value: 15000, color: '#bbf7d0' },
    ],
    sampleData: `{"trial_id": "NCT04567890", "patient_id": "PT-001", "outcome": "Treatment with 200mg showed 45% tumor reduction", "drug": "OncoBlock-200", "dosage": "200mg", "structured_outcome": {"drug": "OncoBlock-200", "dose_mg": 200, "response": "partial_response", "tumor_reduction_pct": 45}}
{"trial_id": "NCT04567891", "patient_id": "PT-002", "outcome": "Patient experienced stable disease after 3 months", "drug": "ImmunoGuard", "dosage": "50mg/m2", "structured_outcome": {"drug": "ImmunoGuard", "dose_mg_m2": 50, "response": "stable_disease", "duration_months": 3}}
{"trial_id": "NCT04567892", "patient_id": "PT-003", "outcome": "Complete remission achieved within 6 weeks", "drug": "ChemoX-75", "dosage": "75mg", "structured_outcome": {"drug": "ChemoX-75", "dose_mg": 75, "response": "complete_remission", "time_to_response_weeks": 6}}`,
    currentStepLogs: [
      '[2026-02-08T09:15:00] Initializing OutcomeStructurer',
      'Structuring trial outcomes...',
      'Processed 15000 records',
      'Structuring in progress...'
    ],
    logs: [
      '[2026-02-08T08:45:00] Starting pipeline execution: clinical-struct-6e2b8a',
      'Storage initialized with clinical trials',
      'Running operator: CompletenessFilter',
      'Found 15000 complete records (from 18000)',
      'Running operator: OutcomeStructurer'
    ]
  },
  'task-020': {
    taskId: 'math-parse-9a4f1c',
    timeAgo: '15h ago',
    sampleCounts: [
      { step: 'S1: Complete', value: 7800, color: '#fde68a' },
      { step: 'S2: Parse', value: 7800, color: '#bae6fd' },
    ],
    sampleData: `{"problem": "Find all positive integers n such that n^2 + 3n + 2 is divisible by 6.", "solution": "First factor: n^2 + 3n + 2 = (n+1)(n+2). This is always even since either n+1 or n+2 is even. For divisibility by 3, check n mod 3. When n ≡ 0 (mod 3), n+1 ≡ 1, n+2 ≡ 2. When n ≡ 1 (mod 3), n+1 ≡ 2, n+2 ≡ 0. When n ≡ 2 (mod 3), n+1 ≡ 0. So all n work except n ≡ 0 (mod 3).", "difficulty": "medium", "topic": "number_theory", "year": 2022, "parsed_steps": [{"step": 1, "action": "factor_polynomial", "result": "(n+1)(n+2)"}, {"step": 2, "action": "check_parity", "result": "always_even"}, {"step": 3, "action": "modulo_analysis", "result": "n_not_divisible_by_3"}]}
{"problem": "In triangle ABC, prove that a^2 + b^2 + c^2 ≥ 4√3·S, where S is the area.", "solution": "Using Heron's formula and AM-GM inequality. Let s = (a+b+c)/2. Then S = √[s(s-a)(s-b)(s-c)]. By AM-GM, (s-a)+(s-b)+(s-c) = s. Also a^2+b^2+c^2 ≥ 4√3·S with equality when a=b=c.", "difficulty": "hard", "topic": "geometry", "year": 2023, "parsed_steps": [{"step": 1, "action": "apply_heron_formula", "result": "S_in_terms_of_sides"}, {"step": 2, "action": "apply_am_gm", "result": "inequality_established"}, {"step": 3, "action": "equality_case", "result": "equilateral_triangle"}]}
{"problem": "Find the sum of all positive divisors of 72.", "solution": "Prime factorization: 72 = 2^3 × 3^2. Sum of divisors formula: σ(n) = (2^4-1)/(2-1) × (3^3-1)/(3-1) = 15 × 13 = 195.", "difficulty": "easy", "topic": "number_theory", "year": 2021, "parsed_steps": [{"step": 1, "action": "prime_factorization", "result": "2^3_×_3^2"}, {"step": 2, "action": "apply_divisor_formula", "result": "σ(72)_calculated"}, {"step": 3, "action": "final_computation", "result": "195"}]}`,
    currentStepLogs: [
      '[2026-02-06T12:30:00] Initializing SolutionParser',
      'Parsing math solutions...',
      'Parsed 7800 solutions',
      'SolutionParser completed'
    ],
    logs: [
      '[2026-02-06T12:00:00] Starting pipeline execution: math-parse-9a4f1c',
      'Storage initialized with math olympiad data',
      'Running operator: SolutionCompletenessFilter',
      'Filtered 7800 problems (from 8000)',
      'Running operator: SolutionParser',
      'Solution parsing complete'
    ]
  },
  'task-021': {
    taskId: 'soil-feat-5d8e2b',
    timeAgo: '16h ago',
    sampleCounts: [
      { step: 'S1: SpecFilter', value: 14500, color: '#f8b4b4' },
      { step: 'S2: Engineer', value: 14500, color: '#bbf7d0' },
    ],
    sampleData: `{"wavelength": [400, 450, 500, 550, 600, 650, 700, 750, 800, 850], "reflectance": [0.15, 0.18, 0.22, 0.28, 0.35, 0.42, 0.48, 0.52, 0.55, 0.58], "sample_id": "SOIL-2026-001", "location": {"lat": 40.7, "lon": -74.0}, "depth": 15, "engineered_features": {"ndvi": 0.67, "savi": 0.58, "clay_index": 0.23, "organic_matter": 3.2}}
{"wavelength": [400, 450, 500, 550, 600, 650, 700, 750, 800, 850], "reflectance": [0.12, 0.14, 0.17, 0.21, 0.26, 0.31, 0.36, 0.40, 0.43, 0.46], "sample_id": "SOIL-2026-002", "location": {"lat": 40.7, "lon": -74.1}, "depth": 30, "engineered_features": {"ndvi": 0.72, "savi": 0.65, "clay_index": 0.31, "organic_matter": 4.1}}
{"wavelength": [400, 450, 500, 550, 600, 650, 700, 750, 800, 850], "reflectance": [0.18, 0.22, 0.26, 0.32, 0.38, 0.45, 0.51, 0.56, 0.60, 0.63], "sample_id": "SOIL-2026-003", "location": {"lat": 40.8, "lon": -74.0}, "depth": 10, "engineered_features": {"ndvi": 0.62, "savi": 0.52, "clay_index": 0.18, "organic_matter": 2.8}}`,
    currentStepLogs: [
      '[2026-02-05T09:30:00] Initializing FeatureEngineer',
      'Engineering soil features...',
      'Engineered features for 14500 samples',
      'FeatureEngineer completed'
    ],
    logs: [
      '[2026-02-05T09:00:00] Starting pipeline execution: soil-feat-5d8e2b',
      'Storage initialized with soil spectroscopy',
      'Running operator: SpectralQualityFilter',
      'Filtered 14500 spectra (from 15000)',
      'Running operator: FeatureEngineer',
      'Feature engineering complete'
    ]
  },
  'task-022': {
    taskId: 'fossil-detect-7c3f9a',
    timeAgo: '17h ago',
    sampleCounts: [
      { step: 'S1: Clarity', value: 9500, color: '#fde68a' },
      { step: 'S2: Detect', value: 9500, color: '#bae6fd' },
    ],
    sampleData: `{"image": "fossils/trilobite_001.jpg", "fossil_type": "trilobite", "era": "Cambrian", "location": "Burgess Shale, Canada", "specimen_id": "FOS-2026-001", "detection_result": {"confidence": 0.94, "bbox": [120, 80, 340, 280], "species": "Olenoides serratus"}}
{"image": "fossils/ammonite_002.jpg", "fossil_type": "ammonite", "era": "Jurassic", "location": "Solnhofen, Germany", "specimen_id": "FOS-2026-002", "detection_result": {"confidence": 0.97, "bbox": [200, 150, 450, 400], "species": "Ammonites subradians"}}
{"image": "fossils/dinosaur_bone_003.jpg", "fossil_type": "vertebrate", "era": "Cretaceous", "location": "Hell Creek, USA", "specimen_id": "FOS-2026-003", "detection_result": {"confidence": 0.89, "bbox": [50, 100, 500, 350], "species": "Tyrannosaurus rex"}}`,
    currentStepLogs: [
      '[2026-02-08T13:30:00] Initializing FossilDetector',
      'Training fossil detection...',
      'Processing 9500 images',
      'Training in progress...'
    ],
    logs: [
      '[2026-02-08T13:00:00] Starting pipeline execution: fossil-detect-7c3f9a',
      'Storage initialized with fossil images',
      'Running operator: ImageClarityFilter',
      'Filtered 9500 clear images (from 12000)',
      'Running operator: FossilDetector'
    ]
  },
  'task-023': {
    taskId: 'nuclear-tag-4a8e1d',
    timeAgo: '18h ago',
    sampleCounts: [
      { step: 'S1: ParseLogs', value: 98000, color: '#fde68a' },
      { step: 'S2: TagAnomaly', value: 98000, color: '#bae6fd' },
    ],
    sampleData: `{"timestamp": "2026-02-06T18:15:23Z", "log_level": "WARNING", "message": "Coolant flow rate dropped to 245 m3/h (expected: 250-260)", "reactor_id": "PWR-001", "sensor_reading": 245.3, "anomaly_tag": "coolant_flow_degradation"}
{"timestamp": "2026-02-06T18:22:45Z", "log_level": "ERROR", "message": "Neutron flux sensor N-12 reading anomaly: 1.15×10^14 n/cm2/s (threshold: 1.0×10^14)", "reactor_id": "PWR-001", "sensor_reading": 1.15e14, "anomaly_tag": "neutron_flux_spike"}
{"timestamp": "2026-02-06T18:30:12Z", "log_level": "INFO", "message": "Control rod bank A adjusted: 5% insertion", "reactor_id": "PWR-001", "sensor_reading": 0.95, "anomaly_tag": "normal_operation"}`,
    currentStepLogs: [
      '[2026-02-06T19:00:00] Initializing AnomalyTagger',
      'Tagging anomalies...',
      'Tagged 98000 logs',
      'AnomalyTagger completed'
    ],
    logs: [
      '[2026-02-06T18:00:00] Starting pipeline execution: nuclear-tag-4a8e1d',
      'Storage initialized with reactor logs',
      'Running operator: LogFormatFilter',
      'Parsed 98000 logs (from 100000)',
      'Running operator: AnomalyTagger',
      'Anomaly tagging complete'
    ]
  },
  'task-024': {
    taskId: 'aerial-land-6f2b9e',
    timeAgo: '19h ago',
    sampleCounts: [
      { step: 'S1: Coverage', value: 32000, color: '#f8b4b4' },
      { step: 'S2: Annotate', value: 32000, color: '#bbf7d0' },
    ],
    sampleData: `{"image": "aerial/survey_001_tile_0_0.jpg", "coordinates": {"lat_min": 37.7749, "lat_max": 37.7849, "lon_min": -122.4194, "lon_max": -122.4094}, "resolution": 0.3, "capture_date": "2026-02-05", "area_km2": 1.12, "land_use_label": {"residential": 0.45, "commercial": 0.25, "vegetation": 0.20, "road": 0.10}}
{"image": "aerial/survey_001_tile_0_1.jpg", "coordinates": {"lat_min": 37.7749, "lat_max": 37.7849, "lon_min": -122.4094, "lon_max": -122.3994}, "resolution": 0.3, "capture_date": "2026-02-05", "area_km2": 1.12, "land_use_label": {"industrial": 0.40, "residential": 0.15, "vegetation": 0.30, "water": 0.15}}
{"image": "aerial/survey_001_tile_1_0.jpg", "coordinates": {"lat_min": 37.7649, "lat_max": 37.7749, "lon_min": -122.4194, "lon_max": -122.4094}, "resolution": 0.3, "capture_date": "2026-02-05", "area_km2": 1.12, "land_use_label": {"agricultural": 0.55, "vegetation": 0.30, "residential": 0.10, "road": 0.05}}`,
    currentStepLogs: [
      '[2026-02-05T18:00:00] Initializing LandUseAnnotator',
      'Annotating land use...',
      'Annotated 32000 images',
      'LandUseAnnotator completed'
    ],
    logs: [
      '[2026-02-05T16:00:00] Starting pipeline execution: aerial-land-6f2b9e',
      'Storage initialized with aerial images',
      'Running operator: CoverageFilter',
      'Filtered 32000 images (from 35000)',
      'Running operator: LandUseAnnotator',
      'Land use annotation complete'
    ]
  }
}

export function getDataProcessingPipeline(taskId) {
  return pipelineData[taskId]?.nodes || []
}

export function getExecutionResult(taskId) {
  return executionResults[taskId] || {
    taskId: 'unknown',
    timeAgo: '-',
    sampleCounts: [],
    currentStepLogs: [],
    logs: []
  }
}

export function getPipelineData(taskId) {
  return pipelineData[taskId]
}
