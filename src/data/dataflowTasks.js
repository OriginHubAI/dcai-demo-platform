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
