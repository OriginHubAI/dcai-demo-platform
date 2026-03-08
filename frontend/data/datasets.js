export const datasets = [
  // Science Datasets - Featured on First Page
  // Biology
  {
    id: 'rna-sequences',
    author: 'bioinfo-hub',
    name: 'RNA Sequences',
    task: 'text-classification',
    domain: 'biology',
    downloads: 2650000,
    likes: 3400,
    lastModified: '2025-03-12',
    rows: 12500000,
    size: '45GB',
    modality: 'text',
    language: 'en',
    license: 'mit',
    description: 'Curated RNA sequence data including mRNA, tRNA, and non-coding RNA with secondary structure annotations and functional classifications.'
  },
  {
    id: 'protein-structures-3d',
    author: 'alphafold-community',
    name: 'Protein Structures 3D',
    task: 'feature-extraction',
    domain: 'biology',
    downloads: 3900000,
    likes: 4200,
    lastModified: '2025-03-01',
    rows: 2300000,
    size: '320GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Three-dimensional protein structure predictions with amino acid sequences, folding annotations, and confidence scores from AlphaFold-derived pipelines.'
  },
  {
    id: 'genome-variants',
    author: 'broad-institute',
    name: 'Genome Variants',
    task: 'text-classification',
    domain: 'biology',
    downloads: 1850000,
    likes: 2400,
    lastModified: '2025-01-30',
    rows: 95000000,
    size: '500GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Human genome variant call data with SNPs, indels, and structural variants annotated with clinical significance and population frequencies.'
  },
  {
    id: 'microscopy-cell-images',
    author: 'cell-vision',
    name: 'Microscopy Cell Images',
    task: 'image-segmentation',
    domain: 'biology',
    downloads: 1430000,
    likes: 2100,
    lastModified: '2025-02-10',
    rows: 620000,
    size: '240GB',
    modality: 'image',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Fluorescence and electron microscopy images of cells with instance segmentation masks for nuclei, organelles, and membrane boundaries.'
  },
  // SFT/RL Datasets for AgentFlow
  {
    id: 'doc-dancer-sft-multimodal',
    author: 'agentflow-lab',
    name: 'DocDancer SFT Multimodal',
    task: 'question-answering',
    domain: 'computer-science',
    downloads: 380000,
    likes: 1150,
    lastModified: '2025-03-14',
    rows: 220000,
    size: '48GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Multimodal document QA dataset for DocDancer agent SFT. Features VLM-processed PDF documents with cross-page reasoning trajectories, doc_search and doc_read tool calls, and visually-grounded question-answer pairs with bounding box annotations.'
  },
  {
    id: 'rag-agent-sft-corpus',
    author: 'agentflow-lab',
    name: 'RAG Agent SFT Corpus',
    task: 'question-answering',
    domain: 'computer-science',
    downloads: 540000,
    likes: 1580,
    lastModified: '2025-03-12',
    rows: 280000,
    size: '12GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Supervised fine-tuning dataset for RAGAgent. Includes retrieval-augmented generation trajectories with FAISS-indexed knowledge base queries, multi-hop reasoning chains, and grounded QA pairs synthesized from Wikipedia and academic corpora.'
  },
  // Chemistry
  {
    id: 'chemistry-books',
    author: 'chem-nlp',
    name: 'Chemistry Books',
    task: 'text-generation',
    domain: 'chemistry',
    downloads: 1780000,
    likes: 2050,
    lastModified: '2025-01-25',
    rows: 190000,
    size: '8.5GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'A large-scale corpus of chemistry textbooks and reference materials spanning organic, inorganic, physical, and analytical chemistry.'
  },
  {
    id: 'quantum-chemistry-calcs',
    author: 'qchem-data',
    name: 'Quantum Chemistry Calcs',
    task: 'feature-extraction',
    domain: 'chemistry',
    downloads: 620000,
    likes: 980,
    lastModified: '2024-11-08',
    rows: 6700000,
    size: '55GB',
    modality: 'text',
    language: 'en',
    license: 'mit',
    description: 'Density functional theory calculation results for molecular systems including energies, forces, electron densities, and orbital coefficients.'
  },
  // Physics
  {
    id: 'physics-simulations',
    author: 'sci-compute',
    name: 'Physics Simulations',
    task: 'feature-extraction',
    domain: 'physics',
    downloads: 1020000,
    likes: 1750,
    lastModified: '2025-02-14',
    rows: 8900000,
    size: '150GB',
    modality: 'text',
    language: 'en',
    license: 'mit',
    description: 'Numerical simulation outputs for fluid dynamics, quantum mechanics, and thermodynamics problems with parameter configurations and convergence data.'
  },
  {
    id: 'superconductor-db',
    author: 'condensed-matter',
    name: 'Superconductor Database',
    task: 'feature-extraction',
    domain: 'physics',
    downloads: 420000,
    likes: 760,
    lastModified: '2025-02-01',
    rows: 165000,
    size: '2.8GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Comprehensive database of superconducting materials with critical temperature, crystal structure, chemical formula, and electronic band structure data.'
  },
  // Mathematics
  {
    id: 'math-olympiad-problems',
    author: 'deepmind',
    name: 'Math Olympiad Problems',
    task: 'question-answering',
    domain: 'mathematics',
    downloads: 4800000,
    likes: 3600,
    lastModified: '2025-03-15',
    rows: 125000,
    size: '280MB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'A curated collection of international math olympiad problems spanning algebra, geometry, number theory, and combinatorics with step-by-step solutions.'
  },
  {
    id: 'math-proofs-corpus',
    author: 'lean-community',
    name: 'Math Proofs Corpus',
    task: 'text-generation',
    domain: 'mathematics',
    downloads: 1680000,
    likes: 2600,
    lastModified: '2025-03-10',
    rows: 78000,
    size: '1.2GB',
    modality: 'text',
    language: 'en',
    license: 'mit',
    description: 'Formal and informal mathematical proofs spanning real analysis, abstract algebra, topology, and number theory with Lean 4 formalization annotations.'
  },
  // Earth Science
  {
    id: 'aerial-imaging',
    author: 'geo-vision',
    name: 'Aerial Imaging',
    task: 'image-classification',
    domain: 'earth-science',
    downloads: 2100000,
    likes: 3100,
    lastModified: '2025-02-05',
    rows: 850000,
    size: '180GB',
    modality: 'image',
    language: 'en',
    license: 'apache-2.0',
    description: 'High-resolution aerial and satellite imagery annotated for land use classification, urban planning, vegetation mapping, and environmental monitoring.'
  },
  {
    id: 'geoscience-maps',
    author: 'usgs-community',
    name: 'Geoscience Maps',
    task: 'image-segmentation',
    domain: 'earth-science',
    downloads: 680000,
    likes: 1120,
    lastModified: '2025-01-05',
    rows: 175000,
    size: '210GB',
    modality: 'image',
    language: 'en',
    license: 'cc-0',
    description: 'Geological survey maps with pixel-level annotations for rock types, fault lines, mineral deposits, and topographic features.'
  },
  {
    id: 'ocean-climate-sensors',
    author: 'noaa-research',
    name: 'Ocean Climate Sensors',
    task: 'feature-extraction',
    domain: 'earth-science',
    downloads: 530000,
    likes: 890,
    lastModified: '2025-03-05',
    rows: 56000000,
    size: '72GB',
    modality: 'text',
    language: 'en',
    license: 'cc-0',
    description: 'Time-series oceanographic sensor data including sea surface temperature, salinity, dissolved oxygen, and current velocity from global buoy networks.'
  },
  {
    id: 'seismic-waveforms',
    author: 'earthquake-lab',
    name: 'Seismic Waveforms',
    task: 'audio-classification',
    domain: 'earth-science',
    downloads: 390000,
    likes: 720,
    lastModified: '2024-12-15',
    rows: 2800000,
    size: '85GB',
    modality: 'audio',
    language: 'en',
    license: 'cc-0',
    description: 'Seismic waveform recordings from global seismograph stations classified by event type: earthquake, explosion, volcanic tremor, and noise.'
  },
  {
    id: 'satellite-weather',
    author: 'esa-climate',
    name: 'Satellite Weather',
    task: 'image-classification',
    domain: 'earth-science',
    downloads: 1150000,
    likes: 1560,
    lastModified: '2025-01-12',
    rows: 3200000,
    size: '400GB',
    modality: 'image',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Multi-spectral satellite imagery for weather pattern classification including cloud types, storm systems, and atmospheric phenomena.'
  },
  {
    id: 'paleontology-fossils',
    author: 'natural-history',
    name: 'Paleontology Fossils',
    task: 'object-detection',
    domain: 'earth-science',
    downloads: 280000,
    likes: 540,
    lastModified: '2025-02-08',
    rows: 95000,
    size: '48GB',
    modality: 'image',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'High-resolution fossil specimen images with bounding box annotations for taxonomic classification, geological era labeling, and morphological feature detection.'
  },
  // Medicine
  {
    id: 'clinical-trials-nlp',
    author: 'biomed-nlp',
    name: 'Clinical Trials NLP',
    task: 'text-classification',
    domain: 'medicine',
    downloads: 1560000,
    likes: 1930,
    lastModified: '2025-02-28',
    rows: 420000,
    size: '3.6GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Structured clinical trial records with outcome measures, intervention descriptions, eligibility criteria, and adverse event reports for biomedical NLP.'
  },
  {
    id: 'drug-molecule-graphs',
    author: 'pharma-ai',
    name: 'Drug Molecule Graphs',
    task: 'text-classification',
    domain: 'medicine',
    downloads: 2200000,
    likes: 2850,
    lastModified: '2025-02-22',
    rows: 1800000,
    size: '15GB',
    modality: 'text',
    language: 'en',
    license: 'apache-2.0',
    description: 'Molecular graph representations of drug compounds with SMILES notation, bioactivity labels, toxicity predictions, and ADMET property annotations.'
  },
  {
    id: 'medicine-textbooks',
    author: 'med-edu-ai',
    name: 'Medicine TextBooks',
    task: 'text-generation',
    domain: 'medicine',
    downloads: 890000,
    likes: 1680,
    lastModified: '2025-03-20',
    rows: 450000,
    size: '15GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'A comprehensive collection of medical textbooks covering internal medicine, surgery, pediatrics, and clinical guidelines for medical education and training.'
  },
  // Materials Science
  {
    id: 'iron-steel-papers',
    author: 'metallurgy-institute',
    name: 'Iron & Steel Papers',
    task: 'text-classification',
    domain: 'materials-science',
    downloads: 1350000,
    likes: 1820,
    lastModified: '2025-02-20',
    rows: 87500,
    size: '4.2GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Full-text research papers on iron and steel metallurgy covering alloy design, heat treatment, microstructure analysis, and mechanical properties.'
  },
  {
    id: 'polymer-patents',
    author: 'mat-sci-lab',
    name: 'Polymer Patents',
    task: 'text-classification',
    domain: 'materials-science',
    downloads: 920000,
    likes: 1450,
    lastModified: '2025-01-18',
    rows: 215000,
    size: '6.8GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-nc-4.0',
    description: 'A comprehensive dataset of polymer science patents including synthesis methods, material properties, and industrial applications from global patent offices.'
  },
  {
    id: 'materials-genome',
    author: 'nist-data',
    name: 'Materials Genome',
    task: 'feature-extraction',
    domain: 'materials-science',
    downloads: 740000,
    likes: 1280,
    lastModified: '2024-11-20',
    rows: 3200000,
    size: '28GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Materials properties database covering crystal structures, band gaps, elastic constants, and thermodynamic stability from the Materials Genome Initiative.'
  },
  // Ecology
  {
    id: 'ecology-biodiversity',
    author: 'gbif-community',
    name: 'Ecology Biodiversity',
    task: 'text-classification',
    domain: 'ecology',
    downloads: 480000,
    likes: 830,
    lastModified: '2025-02-18',
    rows: 28000000,
    size: '18GB',
    modality: 'text',
    language: 'multilingual',
    license: 'cc-by-4.0',
    description: 'Global biodiversity occurrence records with species taxonomy, geolocation, habitat classification, and conservation status annotations.'
  },
  {
    id: 'soil-spectroscopy',
    author: 'agri-science',
    name: 'Soil Spectroscopy',
    task: 'feature-extraction',
    domain: 'ecology',
    downloads: 310000,
    likes: 480,
    lastModified: '2024-12-20',
    rows: 780000,
    size: '12GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Near-infrared and mid-infrared soil spectral measurements with laboratory-analyzed properties including organic carbon, nitrogen, pH, and texture.'
  },
  // Astronomy
  {
    id: 'astrophysics-spectra',
    author: 'astro-data-lab',
    name: 'Astrophysics Spectra',
    task: 'feature-extraction',
    domain: 'astronomy',
    downloads: 870000,
    likes: 1680,
    lastModified: '2024-12-10',
    rows: 4500000,
    size: '95GB',
    modality: 'text',
    language: 'en',
    license: 'cc-0',
    description: 'Stellar and galactic spectral data from ground-based and space telescopes, annotated with redshift, chemical composition, and luminosity class.'
  },
  // Neuroscience
  {
    id: 'neuroscience-eeg',
    author: 'brain-data-lab',
    name: 'Neuroscience EEG',
    task: 'audio-classification',
    domain: 'neuroscience',
    downloads: 710000,
    likes: 1340,
    lastModified: '2025-01-22',
    rows: 1500000,
    size: '120GB',
    modality: 'audio',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Multi-channel EEG recordings with event-related potential annotations for cognitive neuroscience research including motor imagery and P300 paradigms.'
  },
  // Education (Science-related)
  {
    id: 'k12-science-textbooks',
    author: 'edu-research',
    name: 'K12 Science TextBooks',
    task: 'question-answering',
    domain: 'education',
    downloads: 3200000,
    likes: 2900,
    lastModified: '2025-03-08',
    rows: 340000,
    size: '12GB',
    modality: 'text',
    language: 'multilingual',
    license: 'cc-by-sa-4.0',
    description: 'Digitized K-12 science textbooks covering physics, chemistry, biology, and earth science with structured Q&A pairs and concept explanations.'
  },
  {
    id: 'scientific-figures',
    author: 'sci-doc-ai',
    name: 'Scientific Figures',
    task: 'image-to-text',
    domain: 'education',
    downloads: 960000,
    likes: 1580,
    lastModified: '2025-03-02',
    rows: 450000,
    size: '65GB',
    modality: 'image',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Charts, plots, diagrams, and illustrations extracted from scientific publications with structured captions and data table reconstructions.'
  },
  {
    id: 'arxiv-stem-papers',
    author: 'arxiv-community',
    name: 'ArXiv STEM Papers',
    task: 'text-generation',
    domain: 'education',
    downloads: 3500000,
    likes: 3800,
    lastModified: '2025-03-14',
    rows: 2400000,
    size: '85GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Full-text scientific papers from ArXiv across physics, mathematics, computer science, and quantitative biology with LaTeX source and metadata.'
  },
  {
    id: 'arxiv-papers-charts',
    author: 'arxiv-community',
    name: 'ArXiv Papers Charts',
    task: 'text-generation',
    domain: 'education',
    downloads: 1200000,
    likes: 2100,
    lastModified: '2025-03-22',
    rows: 850000,
    size: '42GB',
    modality: 'text',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Conversational dataset derived from ArXiv scientific papers with question-answer pairs, summaries, and explanations for academic discussions and chart understanding.'
  },
  {
    id: 'ds-agent-sft-analytics',
    author: 'agentflow-lab',
    name: 'DS Agent SFT Analytics',
    task: 'text-generation',
    domain: 'computer-science',
    downloads: 290000,
    likes: 920,
    lastModified: '2025-03-11',
    rows: 150000,
    size: '6.2GB',
    modality: 'text',
    language: 'en',
    license: 'mit',
    description: 'Data science agent SFT dataset with CSV analysis trajectories. Features ds_inspect_data, ds_read_csv, and ds_run_python tool executions, pandas/sklearn code generation with sandbox validation, and data science QA pairs with reasoning chains.'
  },
  {
    id: 'agent-sft-trajectories',
    author: 'agentflow-lab',
    name: 'Agent SFT Trajectories',
    task: 'text-generation',
    domain: 'computer-science',
    downloads: 890000,
    likes: 2450,
    lastModified: '2025-03-15',
    rows: 520000,
    size: '28GB',
    modality: 'text',
    language: 'en',
    license: 'apache-2.0',
    description: 'High-quality expert demonstration trajectories for agent supervised fine-tuning (SFT). Contains multi-modal exploration traces with Chain-of-Thought (CoT) reasoning and action sequences from DSAgent, DocDancer, RAGAgent, Text2SQL, and WebAgent environments.'
  },
  {
    id: 'agent-dpo-preferences',
    author: 'agentflow-lab',
    name: 'Agent DPO Preferences',
    task: 'text-classification',
    domain: 'computer-science',
    downloads: 650000,
    likes: 1820,
    lastModified: '2025-03-10',
    rows: 380000,
    size: '18GB',
    modality: 'text',
    language: 'en',
    license: 'apache-2.0',
    description: 'Direct Preference Optimization (DPO) dataset with paired positive/negative trajectories. Includes contrastive pairs of effective action paths versus redundant trial-and-error paths from sandbox environment exploration for agent alignment training.'
  },
  {
    id: 'agent-offline-rl-traces',
    author: 'agentflow-lab',
    name: 'Agent Offline RL Traces',
    task: 'feature-extraction',
    domain: 'computer-science',
    downloads: 720000,
    likes: 2100,
    lastModified: '2025-03-18',
    rows: 1200000,
    size: '65GB',
    modality: 'text',
    language: 'en',
    license: 'apache-2.0',
    description: 'Mixed positive-negative trajectory dataset for offline reinforcement learning. Contains evaluation traces with successful decisions, failed actions, self-correction reflections, and deadlock feedback from heterogeneous agent environments (GUI, RAG, SQL, Web).'
  },
  {
    id: 'web-agent-rl-trajectories',
    author: 'agentflow-lab',
    name: 'Web Agent RL Trajectories',
    task: 'feature-extraction',
    domain: 'computer-science',
    downloads: 480000,
    likes: 1420,
    lastModified: '2025-03-08',
    rows: 450000,
    size: '35GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-4.0',
    description: 'Deep research web agent trajectories for reinforcement learning. Features search-visit-browse action sequences with Serper/Google Search integration, webpage content extraction via Jina, and multi-step reasoning annotations for complex web QA tasks.'
  },
  {
    id: 'sql-agent-sft-dataset',
    author: 'agentflow-lab',
    name: 'SQL Agent SFT Dataset',
    task: 'text-generation',
    domain: 'computer-science',
    downloads: 420000,
    likes: 1280,
    lastModified: '2025-03-05',
    rows: 180000,
    size: '8.5GB',
    modality: 'text',
    language: 'en',
    license: 'mit',
    description: 'Text2SQL supervised fine-tuning dataset with schema exploration trajectories. Contains database introspection actions (list_databases, get_schema), SQL query generation with execution validation, and multi-hop query sequences from Chinook and Sakila databases.'
  },
  {
    id: 'gui-agent-rl-interactions',
    author: 'agentflow-lab',
    name: 'GUI Agent RL Interactions',
    task: 'feature-extraction',
    domain: 'computer-science',
    downloads: 310000,
    likes: 980,
    lastModified: '2025-03-16',
    rows: 560000,
    size: '120GB',
    modality: 'multimodal',
    language: 'en',
    license: 'apache-2.0',
    description: 'GUI and embodied agent interaction dataset for RL training. Includes screenshot sequences, DOM/UI element tree coordinates, action execution traces from Docker/VM sandbox environments, and reward signals based on interface state change rates.'
  },
  {
    id: 'agent-rl-reward-model-data',
    author: 'agentflow-lab',
    name: 'Agent RL Reward Model Data',
    task: 'text-classification',
    domain: 'computer-science',
    downloads: 260000,
    likes: 850,
    lastModified: '2025-03-20',
    rows: 680000,
    size: '22GB',
    modality: 'text',
    language: 'en',
    license: 'apache-2.0',
    description: 'Reward model training data for agent RL alignment. Contains trajectory rankings with human preference labels, task completion scores, tool call efficiency metrics, and step-by-step reward annotations for PPO/GRPO policy optimization.'
  },
  // Other Domains
  {
    id: 'nuclear-reactor-logs',
    author: 'energy-research',
    name: 'Nuclear Reactor Logs',
    task: 'text-classification',
    domain: 'energy',
    downloads: 340000,
    likes: 620,
    lastModified: '2024-10-30',
    rows: 9800000,
    size: '32GB',
    modality: 'text',
    language: 'en',
    license: 'other',
    description: 'Operational log data from nuclear reactor facilities including temperature readings, neutron flux measurements, coolant flow rates, and safety event records.'
  },
  {
    id: 'robotics-sensor-fusion',
    author: 'robo-science',
    name: 'Robotics Sensor Fusion',
    task: 'feature-extraction',
    domain: 'engineering',
    downloads: 850000,
    likes: 1420,
    lastModified: '2025-01-15',
    rows: 5600000,
    size: '200GB',
    modality: 'text',
    language: 'en',
    license: 'apache-2.0',
    description: 'Multi-modal sensor data from robotic platforms including LiDAR point clouds, IMU readings, force-torque measurements, and joint encoder states.'
  },
  // Autonomous Driving Datasets - Original
  {
    id: 'autodrive-raw-nuscenes',
    author: 'motional-labs',
    name: 'AutoDrive Raw - nuScenes',
    task: 'object-detection',
    domain: 'autonomous-driving',
    downloads: 2100000,
    likes: 4200,
    lastModified: '2025-03-15',
    rows: 1400000,
    size: '680GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-sa-4.0',
    description: 'Original raw autonomous driving dataset from nuScenes. Contains 1000 scenes of multimodal sensor data including 6 cameras, 1 LiDAR, 5 radar, GPS and IMU. Supports 3D object detection, tracking, and trajectory prediction tasks.',
    datasetType: 'original',
    derivedDatasets: ['autodrive-derived-nuscenes-filtered', 'autodrive-derived-nuscenes-labeled'],
    relatedTasks: [
      { id: 'task-nuscenes-filter', name: 'nuScenes Quality Filtering Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isOutput: true, startedAt: '2025-03-15T08:00:00Z', endedAt: '2025-03-15T14:30:00Z', duration: '6h 30m' },
      { id: 'task-nuscenes-label', name: 'nuScenes VLM Labeling Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isOutput: true, startedAt: '2025-03-14T10:00:00Z', endedAt: '2025-03-15T02:15:00Z', duration: '16h 15m' }
    ],
    metadata: {
      timeRange: { start: '2025-01-01', end: '2025-03-15', timezone: 'UTC' },
      spatial: {
        regions: ['boston', 'singapore'],
        coverage: 'urban and suburban areas',
        coordinates: { lat: [1.2, 42.4], lon: [103.8, 71.1] }
      },
      sensors: ['camera', 'lidar', 'radar', 'gps', 'imu'],
      conditions: ['day', 'night', 'rain', 'clear'],
      annotations: ['raw', 'unannotated']
    }
  },
  {
    id: 'autodrive-raw-kitti-360',
    author: 'kit-vision',
    name: 'AutoDrive Raw - KITTI-360',
    task: 'object-detection',
    domain: 'autonomous-driving',
    downloads: 1850000,
    likes: 3800,
    lastModified: '2025-02-28',
    rows: 980000,
    size: '520GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-sa-3.0',
    description: 'Original raw 360-degree autonomous driving dataset extending KITTI. Contains rich sensory data with 2 fisheye cameras, 2 perspective cameras, and 1 Velodyne LiDAR. Supports 360-degree perception and dense annotation tasks.',
    datasetType: 'original',
    derivedDatasets: ['autodrive-derived-kitti360-processed', 'autodrive-derived-kitti360-semantic'],
    relatedTasks: [
      { id: 'task-kitti360-process', name: 'KITTI-360 Enhancement Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isOutput: true, startedAt: '2025-03-08T14:00:00Z', endedAt: '2025-03-09T02:30:00Z', duration: '12h 30m' },
      { id: 'task-kitti360-semantic', name: 'KITTI-360 Semantic Segmentation Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isOutput: true, startedAt: '2025-03-06T08:00:00Z', endedAt: '2025-03-07T18:20:00Z', duration: '34h 20m' }
    ],
    metadata: {
      timeRange: { start: '2024-06-01', end: '2024-12-31', timezone: 'CET' },
      spatial: {
        regions: ['karlsruhe', 'germany'],
        coverage: 'urban, highway, and rural roads',
        coordinates: { lat: [49.0, 49.02], lon: [8.4, 8.42] }
      },
      sensors: ['camera', 'lidar', 'gps', 'imu'],
      conditions: ['day', 'clear', 'overcast'],
      annotations: ['raw', 'unannotated']
    }
  },
  {
    id: 'autodrive-raw-waymo-open',
    author: 'waymo-research',
    name: 'AutoDrive Raw - Waymo Open',
    task: 'object-detection',
    domain: 'autonomous-driving',
    downloads: 3200000,
    likes: 5800,
    lastModified: '2025-03-20',
    rows: 2300000,
    size: '1.2TB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-4.0',
    description: 'Original raw autonomous driving dataset from Waymo. High-resolution sensor data with 5 LiDARs and 5 cameras covering 360 degrees. Includes diverse geographic locations and weather conditions for robust perception research.',
    datasetType: 'original',
    derivedDatasets: ['autodrive-derived-waymo-motion', 'autodrive-derived-waymo-perception'],
    relatedTasks: [
      { id: 'task-waymo-motion', name: 'Waymo Motion Forecasting Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isOutput: true, startedAt: '2025-03-20T09:00:00Z', endedAt: '2025-03-21T08:45:00Z', duration: '23h 45m' },
      { id: 'task-waymo-perception', name: 'Waymo Perception Enhancement Pipeline', type: 'Data Processing', status: 'running', progress: 78, isOutput: true, startedAt: '2025-03-21T10:00:00Z', endedAt: null, duration: null }
    ],
    metadata: {
      timeRange: { start: '2024-01-01', end: '2025-03-20', timezone: 'America/Los_Angeles' },
      spatial: {
        regions: ['phoenix', 'san-francisco', 'mountain-view', 'los-angeles'],
        coverage: 'urban, suburban, highway',
        coordinates: { lat: [33.4, 37.8], lon: [112.0, 122.4] }
      },
      sensors: ['camera', 'lidar', 'radar'],
      conditions: ['day', 'night', 'dawn', 'dusk', 'rain', 'clear', 'overcast'],
      annotations: ['raw', 'unannotated']
    }
  },
  // Autonomous Driving Datasets - Derived (Read-only)
  {
    id: 'autodrive-derived-nuscenes-filtered',
    author: 'autodrive-ai',
    name: 'AutoDrive Derived - nuScenes Filtered',
    task: 'object-detection',
    domain: 'autonomous-driving',
    downloads: 890000,
    likes: 2100,
    lastModified: '2025-03-18',
    rows: 850000,
    size: '280GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-sa-4.0',
    description: 'Filtered and quality-enhanced version of nuScenes. High-quality scenes selected using DataFlow-MM pipeline with aesthetic filtering, deduplication, and quality scoring. Ready for training with clean annotations.',
    datasetType: 'derived',
    parentDataset: 'autodrive-raw-nuscenes',
    readonly: true,
    processingPipeline: 'nuscenes_quality_filter_pipeline',
    relatedTasks: [
      { id: 'task-nuscenes-filter', name: 'nuScenes Quality Filtering Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isInput: true, startedAt: '2025-03-15T08:00:00Z', endedAt: '2025-03-15T14:30:00Z', duration: '6h 30m' }
    ],
    metadata: {
      timeRange: { start: '2025-01-01', end: '2025-03-15', timezone: 'UTC' },
      spatial: {
        regions: ['boston', 'singapore'],
        coverage: 'filtered urban scenes',
        coordinates: { lat: [1.2, 42.4], lon: [103.8, 71.1] }
      },
      sensors: ['camera', 'lidar', 'radar'],
      conditions: ['day', 'night', 'clear', 'light-rain'],
      annotations: ['3d-bbox', 'tracking-id', 'velocity'],
      filterCriteria: {
        minQualityScore: 0.85,
        deduplication: true,
        blurRemoval: true
      }
    },
    semanticIndex: {
      objects: ['car', 'truck', 'bus', 'pedestrian', 'cyclist', 'motorcycle', 'traffic-cone', 'barrier'],
      scenes: ['intersection', 'highway-merge', 'parking-lot', 'residential', 'commercial'],
      actions: ['moving', 'stopped', 'turning', 'parked']
    }
  },
  {
    id: 'autodrive-derived-nuscenes-labeled',
    author: 'autodrive-ai',
    name: 'AutoDrive Derived - nuScenes Labeled',
    task: 'image-segmentation',
    domain: 'autonomous-driving',
    downloads: 760000,
    likes: 1850,
    lastModified: '2025-03-16',
    rows: 620000,
    size: '340GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-sa-4.0',
    description: 'VLM-enhanced labeled version of nuScenes with semantic segmentation masks and natural language descriptions. Generated using Qwen2.5-VL for detailed scene understanding and caption generation.',
    datasetType: 'derived',
    parentDataset: 'autodrive-raw-nuscenes',
    readonly: true,
    processingPipeline: 'nuscenes_vlm_labeling_pipeline',
    relatedTasks: [
      { id: 'task-nuscenes-label', name: 'nuScenes VLM Labeling Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isInput: true, startedAt: '2025-03-14T10:00:00Z', endedAt: '2025-03-15T02:15:00Z', duration: '16h 15m' }
    ],
    metadata: {
      timeRange: { start: '2025-01-01', end: '2025-03-15', timezone: 'UTC' },
      spatial: {
        regions: ['boston', 'singapore'],
        coverage: 'urban annotated scenes',
        coordinates: { lat: [1.2, 42.4], lon: [103.8, 71.1] }
      },
      sensors: ['camera', 'lidar'],
      conditions: ['day', 'clear', 'overcast'],
      annotations: ['semantic-seg', 'instance-seg', 'caption', 'qa-pairs'],
      vlmModel: 'Qwen2.5-VL-3B-Instruct'
    },
    semanticIndex: {
      objects: ['vehicle', 'person', 'road', 'sidewalk', 'building', 'vegetation', 'traffic-sign', 'traffic-light'],
      attributes: ['color', 'size', 'orientation', 'occlusion-level'],
      relationships: ['in-front-of', 'behind', 'next-to', 'on-road', 'crossing']
    }
  },
  {
    id: 'autodrive-derived-kitti360-processed',
    author: 'autodrive-ai',
    name: 'AutoDrive Derived - KITTI-360 Processed',
    task: 'object-detection',
    domain: 'autonomous-driving',
    downloads: 650000,
    likes: 1580,
    lastModified: '2025-03-10',
    rows: 720000,
    size: '210GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-sa-3.0',
    description: 'Processed KITTI-360 with enhanced annotations and 360-degree consistency checks. Includes refined 3D bounding boxes and improved temporal tracking across all camera views.',
    datasetType: 'derived',
    parentDataset: 'autodrive-raw-kitti-360',
    readonly: true,
    processingPipeline: 'kitti360_enhancement_pipeline',
    relatedTasks: [
      { id: 'task-kitti360-process', name: 'KITTI-360 Enhancement Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isInput: true, startedAt: '2025-03-08T14:00:00Z', endedAt: '2025-03-09T02:30:00Z', duration: '12h 30m' }
    ],
    metadata: {
      timeRange: { start: '2024-06-01', end: '2024-12-31', timezone: 'CET' },
      spatial: {
        regions: ['karlsruhe'],
        coverage: 'processed urban scenes',
        coordinates: { lat: [49.0, 49.02], lon: [8.4, 8.42] }
      },
      sensors: ['camera', 'lidar'],
      conditions: ['day', 'clear'],
      annotations: ['3d-bbox', 'tracking-id', '360-aligned']
    },
    semanticIndex: {
      objects: ['car', 'van', 'truck', 'pedestrian', 'cyclist', 'tram'],
      scenes: ['city-street', 'highway', 'country-road'],
      temporal: ['static', 'moving', 'parked']
    }
  },
  {
    id: 'autodrive-derived-kitti360-semantic',
    author: 'autodrive-ai',
    name: 'AutoDrive Derived - KITTI-360 Semantic',
    task: 'image-segmentation',
    domain: 'autonomous-driving',
    downloads: 540000,
    likes: 1320,
    lastModified: '2025-03-08',
    rows: 680000,
    size: '185GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-sa-3.0',
    description: 'Dense semantic segmentation dataset derived from KITTI-360. Pixel-level annotations for 64 semantic classes using automated labeling with human-in-the-loop validation.',
    datasetType: 'derived',
    parentDataset: 'autodrive-raw-kitti-360',
    readonly: true,
    processingPipeline: 'kitti360_semantic_pipeline',
    relatedTasks: [
      { id: 'task-kitti360-semantic', name: 'KITTI-360 Semantic Segmentation Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isInput: true, startedAt: '2025-03-06T08:00:00Z', endedAt: '2025-03-07T18:20:00Z', duration: '34h 20m' }
    ],
    metadata: {
      timeRange: { start: '2024-06-01', end: '2024-12-31', timezone: 'CET' },
      spatial: {
        regions: ['karlsruhe'],
        coverage: 'semantically annotated areas',
        coordinates: { lat: [49.0, 49.02], lon: [8.4, 8.42] }
      },
      sensors: ['camera'],
      conditions: ['day', 'clear'],
      annotations: ['semantic-seg', 'panoptic-seg'],
      classes: 64
    },
    semanticIndex: {
      stuff: ['road', 'sidewalk', 'building', 'wall', 'fence', 'pole', 'traffic-light', 'traffic-sign', 'vegetation', 'terrain', 'sky'],
      things: ['person', 'rider', 'car', 'truck', 'bus', 'train', 'motorcycle', 'bicycle', 'caravan', 'trailer'],
      parts: ['license-plate', 'wheel', 'headlight', 'door']
    }
  },
  {
    id: 'autodrive-derived-waymo-motion',
    author: 'autodrive-ai',
    name: 'AutoDrive Derived - Waymo Motion',
    task: 'feature-extraction',
    domain: 'autonomous-driving',
    downloads: 1200000,
    likes: 2850,
    lastModified: '2025-03-22',
    rows: 1450000,
    size: '480GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-4.0',
    description: 'Motion prediction dataset derived from Waymo Open. 9-second trajectory futures for all agents with map information. Optimized for motion forecasting and behavior prediction models.',
    datasetType: 'derived',
    parentDataset: 'autodrive-raw-waymo-open',
    readonly: true,
    processingPipeline: 'waymo_motion_forecasting_pipeline',
    relatedTasks: [
      { id: 'task-waymo-motion', name: 'Waymo Motion Forecasting Pipeline', type: 'Data Processing', status: 'completed', progress: 100, isInput: true, startedAt: '2025-03-20T09:00:00Z', endedAt: '2025-03-21T08:45:00Z', duration: '23h 45m' }
    ],
    metadata: {
      timeRange: { start: '2024-01-01', end: '2025-03-20', timezone: 'America/Los_Angeles' },
      spatial: {
        regions: ['phoenix', 'san-francisco', 'mountain-view', 'los-angeles'],
        coverage: 'motion-rich scenarios',
        coordinates: { lat: [33.4, 37.8], lon: [112.0, 122.4] }
      },
      sensors: ['lidar', 'camera'],
      conditions: ['all-conditions'],
      annotations: ['trajectory', 'intent', 'interaction-graph'],
      predictionHorizon: '9s'
    },
    semanticIndex: {
      agentTypes: ['vehicle', 'pedestrian', 'cyclist'],
      behaviors: ['stationary', 'straight', 'turn-left', 'turn-right', 'u-turn', 'lane-change'],
      scenarios: ['intersection', 'merging', 'roundabout', 'parking-lot', 'highway'],
      interactions: ['leader-follower', 'merging', 'crossing', 'yielding']
    }
  },
  {
    id: 'autodrive-derived-waymo-perception',
    author: 'autodrive-ai',
    name: 'AutoDrive Derived - Waymo Perception',
    task: 'object-detection',
    domain: 'autonomous-driving',
    downloads: 980000,
    likes: 2400,
    lastModified: '2025-03-21',
    rows: 1680000,
    size: '620GB',
    modality: 'multimodal',
    language: 'en',
    license: 'cc-by-nc-4.0',
    description: 'High-quality perception dataset derived from Waymo Open. Multi-frame temporal consistency and camera-LiDAR fusion annotations. Optimized for 3D detection and tracking tasks.',
    datasetType: 'derived',
    parentDataset: 'autodrive-raw-waymo-open',
    readonly: true,
    processingPipeline: 'waymo_perception_enhancement_pipeline',
    relatedTasks: [
      { id: 'task-waymo-perception', name: 'Waymo Perception Enhancement Pipeline', type: 'Data Processing', status: 'running', progress: 78, isInput: true, startedAt: '2025-03-21T10:00:00Z', endedAt: null, duration: null }
    ],
    metadata: {
      timeRange: { start: '2024-01-01', end: '2025-03-20', timezone: 'America/Los_Angeles' },
      spatial: {
        regions: ['phoenix', 'san-francisco', 'mountain-view', 'los-angeles'],
        coverage: 'diverse perception scenarios',
        coordinates: { lat: [33.4, 37.8], lon: [112.0, 122.4] }
      },
      sensors: ['camera', 'lidar'],
      conditions: ['day', 'night', 'rain', 'clear', 'overcast'],
      annotations: ['3d-bbox', 'tracking-id', 'velocity', 'acceleration'],
      temporalWindow: '5-frames'
    },
    semanticIndex: {
      objects: ['vehicle', 'pedestrian', 'cyclist', 'sign', 'traffic-light'],
      difficulty: ['easy', 'medium', 'hard'],
      occlusion: ['none', 'partial', 'heavy'],
      distance: ['0-30m', '30-50m', '50m+']
    }
  },
]

export function getDatasetById(id) {
  return datasets.find(d => d.id === id)
}

// Generate mock autonomous driving data for DataStudio
export function generateAutodrivingData(datasetId) {
  const regions = ['boston', 'singapore']
  const objects = ['car', 'truck', 'bus', 'pedestrian', 'cyclist', 'motorcycle', 'traffic-cone', 'barrier']
  const scenes = ['intersection', 'highway-merge', 'parking-lot', 'residential', 'commercial']
  const weather = ['clear', 'light-rain', 'overcast', 'night']
  const actions = ['moving', 'stopped', 'turning', 'parked']
  
  const descriptions = [
    'Urban intersection with multiple vehicles and pedestrians crossing. Traffic light is green.',
    'Highway merge scenario with a truck entering from the ramp. Clear visibility conditions.',
    'Residential street with parked cars on both sides. Cyclist moving in the bike lane.',
    'Commercial area with heavy pedestrian traffic. Multiple traffic cones indicating road work.',
    'Night scene at a well-lit intersection. Vehicle stopped at red light, pedestrians waiting.',
    'Parking lot with vehicles maneuvering into spots. Barriers marking construction zone.',
    'Highway segment with moderate traffic. Bus in the HOV lane, cars in regular lanes.',
    'Downtown area with mixed traffic including motorcycles and bicycles. Traffic signals active.',
    'Suburban intersection with school zone signage. Pedestrians on sidewalks, vehicles stopped.',
    'Industrial area with trucks entering and exiting. Wide lanes, clear road markings.'
  ]
  
  // Generate 50 sample records
  return Array.from({ length: 50 }, (_, i) => {
    const region = regions[Math.floor(Math.random() * regions.length)]
    const baseLat = region === 'boston' ? 42.36 : 1.35
    const baseLon = region === 'boston' ? -71.05 : 103.87
    
    // Generate random semantic vector (384 dimensions, normalized)
    const vector = Array.from({ length: 384 }, () => (Math.random() - 0.5) * 2)
    const norm = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0))
    const normalizedVector = vector.map(v => v / norm)
    
    // Select random objects for this scene
    const numObjects = 2 + Math.floor(Math.random() * 4)
    const sceneObjects = []
    for (let j = 0; j < numObjects; j++) {
      const obj = objects[Math.floor(Math.random() * objects.length)]
      if (!sceneObjects.includes(obj)) sceneObjects.push(obj)
    }
    
    // Generate timestamp within the dataset time range
    const startDate = new Date('2025-01-01')
    const endDate = new Date('2025-03-15')
    const timestamp = new Date(startDate.getTime() + Math.random() * (endDate.getTime() - startDate.getTime()))
    
    return {
      id: `sample-${String(i + 1).padStart(6, '0')}`,
      timestamp: timestamp.toISOString(),
      location: {
        region: region,
        lat: baseLat + (Math.random() - 0.5) * 0.1,
        lon: baseLon + (Math.random() - 0.5) * 0.1
      },
      description: descriptions[Math.floor(Math.random() * descriptions.length)],
      imageUrl: `https://picsum.photos/seed/${datasetId}-${i}/400/225`,
      semantic: {
        objects: sceneObjects,
        attributes: [
          weather[Math.floor(Math.random() * weather.length)],
          scenes[Math.floor(Math.random() * scenes.length)],
          actions[Math.floor(Math.random() * actions.length)]
        ],
        vector: normalizedVector
      },
      metadata: {
        camera: 'front_center',
        resolution: '1600x900',
        weather: weather[Math.floor(Math.random() * weather.length)],
        scene: scenes[Math.floor(Math.random() * scenes.length)]
      }
    }
  })
}
